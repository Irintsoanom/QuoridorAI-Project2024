import socket
import json
import threading
import time
import random
import math
from game import Game


serverAddress = ('127.0.0.1', 3000)
localAddress, userPort = '0.0.0.0', 35042
pos = None
adv = None
enemyPos = None

myUsername = "Joueur principal"

connectMsg = {
    "request": "subscribe",
   "port": userPort,
   "name": myUsername,
   "matricules": ["1"]
}
status = {
    "response": "pong"
}

data = json.dumps(connectMsg)
statusJson = json.dumps(status)

def connect():
    with socket.socket() as s:
        s.connect(serverAddress)
        s.sendall(bytes(data,encoding='utf8'))
        response = s.recv(2048).decode()
    print(response)

def recv_json(socket: socket.socket):
    finished = False 
    msg = b''
    obj = None
    while not finished:
        msg += socket.recv(2048)
        try:
            obj = json.loads(msg.decode('utf8'))
            finished = True
        except json.JSONDecodeError:
            pass
        except UnicodeDecodeError:
            pass
    return obj

game = Game()

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
                    msg = recv_json(client)
                    if 'request' in msg:
                        if msg['request'] == "ping":
                            client.sendall(bytes(statusJson, encoding='utf8'))
                            print('Connection still going...')
                        elif msg['request'] == "play":
                            print('Game starting')
                            game.setState(msg)
                            play = game.play()
                            client.sendall(bytes(play, encoding="utf8"))
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