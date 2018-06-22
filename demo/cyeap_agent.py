import socketserver
import json
import subprocess


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    """
    继承BaseRequestHandler类,重写handle()方法
    """

    def handle(self):
        try:
            result = self.request.recv(1024)
            data = str(result, 'utf-8')
            result = json.loads(data)
            if isinstance(result, dict):
                cmd = result.get("cmd")
                if cmd:
                    output = subprocess.check_output(cmd, shell=True)
                    self.request.sendall(output)
            else:
                self.request.sendall("Not Support", "utf-8")
        except ConnectionResetError as error:
            print('ConnectionResetError: 客户端断开了连接')


# 运行socket服务
if __name__ == "__main__":
    host = "172.16.120.14"  # 获取本机IP
    port = 9999  # 端口
    print(host, port)
    server = socketserver.ThreadingTCPServer((host, port), ThreadedTCPRequestHandler)
    server.serve_forever()
