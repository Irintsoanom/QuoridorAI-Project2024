import socket
import json
import threading
import time
import random


serverAddress = ('127.0.0.1', 3000)
localAddress, userPort = '0.0.0.0', 7042

jokeList = ['Prends ça!', "Mdrrrr, même pas mal", 'Croûte']
myUsername = "Nomena"

connectMsg = {
    "request": "subscribe",
   "port": userPort,
   "name": myUsername,
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
                            getState(a)
                            play(a, client)
                    else:
                        print('No request from the server')
            except socket.timeout:
                pass

def getState(request):
    lives = request['lives']
    errors = request['errors']
    state = request['state']
    players = state['players']
    current = state['current']

    if players.index(myUsername) == 0:
        blockers = state['blockers'][0]
    else:
        blockers = state['blockers'][1]
    
    print(f'Je suis {myUsername} et je suis actuellement le joueur num {current}, il me reste {lives} vies et {blockers} murs')

      
def play(msg, client):
    state = msg['state']['current']
    if state == 0:
        move =   {
            "type": "pawn",
            "position": [[0,3]] 
        }
    else:
        move =   {
            "type": "pawn",
            "position": [[4, 16]] 
        }
    response = {
        "response": "move",
        "move": move,
        "message": random.choice(jokeList)
    }
    res = json.dumps(response)
    client.sendall(bytes(res, encoding='utf-8'))



if __name__=='__main__':
    thread = threading.Thread(target=statusCheck, daemon=True).start()
    connect()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('Bye')





