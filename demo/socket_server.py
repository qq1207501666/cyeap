import socket
import socketserver
import json


def send_data(host, port, data):
    with socket.socket() as sk_client:
        sk_client.connect((host, port))
        sk_client.send(bytes(json.dumps(data), 'utf8'))
        response = sk_client.recv(1024)
        print(str(response, "utf-8"))


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    """
    继承BaseRequestHandler类,重写handle()方法
    """
    def handle(self):
        try:
            result = self.request.recv(1024)
            data = str(result, 'utf-8')
            result = json.loads(data)
            print(result)
            print(type(result))
        except ConnectionResetError as error:
            print('ConnectionResetError: 客户端断开了连接')

# 运行socket服务
if __name__ == "__main__":
    HOST, PORT = "172.16.100.13", 9999
    server = socketserver.ThreadingTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server.serve_forever()


