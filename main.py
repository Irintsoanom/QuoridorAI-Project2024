import socket
import json
import threading
import time
import random


serverAddress = ('127.0.0.1', 3000)
localAddress, userPort = '0.0.0.0', 35042
pos = None
adv = None
enemyPos = None

jokeList = ['Prends ça!', "Mdrrrr, même pas mal", 'Croûte', 'Bim bam boum', 'Wesh alors', 'Par la barbe de Merlin', 'Saperlipopette', 'Bisous, je m anvole']
myUsername = "Nomena"

connectMsg = {
    "request": "subscribe",
   "port": userPort,
   "name": myUsername,
   "matricules": ["22366"]
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
                    a = recv_json(client)
                    print(a)
                    if 'request' in a:
                        if a['request'] == "ping":
                            client.sendall(bytes(statusJson, encoding='utf-8'))
                            print('Connection still going...')
                        elif a['request'] == "play":
                            play(a, client)
                    else:
                        print('No request from the server')
            except socket.timeout:
                pass

def play(request, client):
    lives = request['lives']
    errors = request['errors']
    state = request['state']

    #State
    players = state['players']
    current = state['current']
    board = state['board']

    if players.index(myUsername) == 0:
        blockers = state['blockers'][0]
    else:
        blockers = state['blockers'][1]
    current = state['current']

    if current == 0:
        adv = 1
    else:
        adv = 0

    print(adv)
    pos = getPos(board, current)
    enemyPos = getPos(board, adv)
    print(f'Position : {pos} - Enemy : {enemyPos}')
    print(errors)

    if current == 0:
        newPos = [pos[0] + 2, pos[1]]
        move =   {
            "type": "pawn",
            "position": [newPos] 
        }
    else:
        newPos = [pos[0] - 2, pos[1]]
        move =   {
            "type": "pawn",
            "position": [newPos] 
        }
    response = {
        "response": "move",
        "move": move,
        "message": random.choice(jokeList)
    }
    res = json.dumps(response)
    client.sendall(bytes(res, encoding='utf-8'))

def getPos(board, current):
    for i,lst in enumerate(board):
        for j,player in enumerate(lst):
            if player == current:
                return (i, j)
    return (None, None)

if __name__=='__main__':
    thread = threading.Thread(target=statusCheck, daemon=True).start()
    connect()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('Bye')





