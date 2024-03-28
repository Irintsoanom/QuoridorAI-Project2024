import socket
import json


serverAddress = ('0.0.0.0', 5000)

connectMsg = {
    "request": "subscribe",
   "port": 8888,
   "name": "Nomena",
   "matricules": ["22336"]
}

data = json.dumps(connectMsg)

def connect():
    with socket.socket() as s:
        s.connect(serverAddress)
        s.sendall(bytes(data,encoding='utf-8'))
        response = s.recv(2048).decode()
    print(response)

if __name__=='__name__':
    connect()




