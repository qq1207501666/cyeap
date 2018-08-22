import pika
import json


def send_json(routing_key, dict_obj, exchange='cyeap', type='direct'):
    # 创建链接
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.16.120.13'))
    # 建立隧道
    channel = connection.channel()
    # 声明一个交换机
    channel.exchange_declare(exchange=exchange, exchange_type='direct')
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=bytes(json.dumps(dict_obj), 'utf8'))
    # 关闭连接
    connection.close()


cmd = {"cmd": "restart_tomcat",
       "args": {"opt": "hahahahahha",
                "tomcat_path": "黑恶hi额警方ii多少分打扫hi额", }
       }
# send_json("172.16.120.37", cmd)
