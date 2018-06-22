import socket
import json


def send_json(host, port, json_data):
    """
    发送json数据
    :param host: IPv4地址
    :param port: 端口
    :param json_data: json数据
    :return: 发送是否成功
    """
    with socket.socket() as sk_client:
        sk_client.connect((host, port))  # 连接
        sk_client.send(bytes(json.dumps(json_data), 'utf8'))
        rep = []
        while True:
            data = str(sk_client.recv(10240), "utf-8")
            if not data:
                break
            rep.append(data)
        return "".join(rep)
