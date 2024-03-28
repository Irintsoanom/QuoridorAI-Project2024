import socket
import json
import threading
import time


serverAddress = ('127.0.0.1', 3000)
localAddress, userPort = '0.0.0.0', 7001

connectMsg = {
    "request": "subscribe",
   "port": userPort,
   "name": "Nomena",
   "matricules": ["22336"]
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
    print('Listen on port', userPort)
    with socket.socket() as s:
        s.bind((localAddress, userPort))
        s.listen()
        s.settimeout(1)
        while True:
            try:
                client, address = s.accept()
                with client:
                    check = client.recv(2048).decode(encoding='utf-8')
                    a = json.loads(check)
                    print(a)
                    if 'request' in a:
                        if a['request'] == "ping":
                            client.sendall(bytes(statusJson, encoding='utf-8'))
                        elif a['request'] == "play":
                            print("Can't play")
                    else:
                        print('No request from the server')
            except socket.timeout:
                pass

if __name__=='__main__':
    thread = threading.Thread(target=statusCheck, daemon=True).start()
    connect()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('Bye')





