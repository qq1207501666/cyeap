import pika
import uuid
import time
import json
import logging

logger = logging.getLogger('django')  # 获取日志对象
MQ_HOST = '172.16.120.13'  # Rabbit MQ 服务
EXCHANGE = "cyeap_direct"


class RpcClient(object):
    """
    RPC调用类
    """

    def __init__(self):
        self.response = None
        self.corr_id = None
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=MQ_HOST))  # 连接 rabbit mq
        self.channel = self.connection.channel()  # 连接到通道
        self.channel.exchange_declare(exchange=EXCHANGE, exchange_type='direct')  # 声明一个交换机
        result = self.channel.queue_declare(exclusive=True)  # 定义一个排他队列,用作回调队列
        self.callback_queue = result.method.queue  # 获取队列名称
        self.channel.queue_bind(exchange=EXCHANGE, queue=self.callback_queue)  # 将交换机和队列绑定
        self.channel.basic_consume(self.on_response,  # 只要一收到消息就调用on_response
                                   no_ack=True,
                                   queue=self.callback_queue)  # 接收这个队列的消息

    def on_response(self, channel, method, props, body):  # 必须四个参数
        # 如果收到的ID和本机生成的相同,则返回的结果就是我想要的指令返回的结果,验证请求响应的一致性
        if self.corr_id == props.correlation_id:
            self.response = body  # 响应的消息

    def call(self, ip, dict_obj):
        self.response = None  # 初始化响应消息,如果不初始化一下,则可能会保留上次的响应消息
        self.corr_id = str(uuid.uuid4())  # 验证请求响应的一致性的随机唯一字符串
        result = self.channel.queue_declare(queue=ip)  # 声明一个队列
        queue_name = result.method.queue
        self.channel.queue_bind(exchange=EXCHANGE, queue=queue_name, routing_key=ip)  # 将交换机和队列绑定
        self.channel.basic_publish(
            exchange=EXCHANGE,
            routing_key=ip,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,  # 让服务端命令结果返回到callback_queue
                correlation_id=self.corr_id,
            ),
            body=bytes(json.dumps(dict_obj), 'utf8')
        )
        start_time = time.time()
        while self.response is None:  # 当没有数据，就一直循环
            # 启动后，on_response函数接到消息，self.response 值就不为空了
            self.connection.process_data_events()  # 非阻塞版的start_consuming()
            print("No message...")
            time.sleep(1)
            use_time = int(time.time() - start_time)
            if use_time > 15:  # 15秒超时设置
                print("Overtime!")
                break
        # 收到消息就调用on_response
        return self.response


def send_json(ip, dict_obj):
    """
    发送消息
    :param ip:
    :param dict_obj:
    :param exchange:
    :return:
    """
    conn = pika.BlockingConnection(pika.ConnectionParameters(host=MQ_HOST))  # 连接 rabbit mq
    channel = conn.channel()
    channel.exchange_declare(exchange=EXCHANGE, exchange_type='direct')  # 声明一个交换机
    result = channel.queue_declare(queue=ip)  # 声明一个队列
    queue_name = result.method.queue
    channel.queue_bind(exchange=EXCHANGE, queue=queue_name, routing_key=ip)  # 将交换机和队列绑定
    channel.basic_publish(exchange=EXCHANGE, routing_key=ip, body=bytes(json.dumps(dict_obj), 'utf8'))  # 发送json消息


def call(ip, dict_obj):
    """
    发送消息
    :param ip:
    :param dict_obj:
    :param exchange:
    :return:
    """
    rpc = RpcClient()
    result = rpc.call(ip, dict_obj)
    if result:
        return str(result, 'utf-8')
    return ""
