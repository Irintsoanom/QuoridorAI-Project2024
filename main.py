import socket
import json
import threading


serverAddress = ('127.0.0.1', 3000)
localAddress, userPort = '0.0.0.0', 7001

connectMsg = {
    "request": "subscribe",
   "port": userPort,
   "name": "Nomena",
   "matricules": ["22336"]
}

statusRequest = {
    "request": "ping"
}

status = {
    "response": "pong"
}

data = json.dumps(connectMsg)
statusJson = json.dumps(status)

def connect():
    with socket.socket() as s:
        s.connect(serverAddress)
        s.sendall(bytes(data,encoding='utf-8'))
        response = s.recv(2048).decode()
    print(response)

def statusCheck():
    with socket.socket() as s:
        s.bind(localAddress, userPort)
        s.listen()
        s.settimeout(1)
        while True:
            try:
                client, address = s.accept()
                with client:
                    check = client.recv(2048).decode(encoding='utf-8')
                    a = json.dumps(check)
                    b = json.dumps(statusRequest)
                    if a == b:
                        s.connect(serverAddress)
                        s.sendall(bytes(statusJson, encoding='utf-8'))
            except socket.timeout:
                print('Time out : Try again')

thread = threading.Thread(target=statusCheck, daemon=True).start()

if __name__=='__main__':
    connect()




