import socket
import json


def send_data(host, port, data):
    with socket.socket() as sk_client:
        sk_client.connect((host, port))
        sk_client.send(bytes(json.dumps(data), 'utf8'))
        response = sk_client.recv(1024)
        print(str(response, "utf-8"))


while True:
    send_data('172.16.100.13',9999, {'cmd': 'ls -l'})
    input("------>")
