import socket
import json
import threading
import time
import random


serverAddress = ('172.17.10.59', 3000)
localAddress, userPort = '0.0.0.0', 35000
pos = None

jokeList = ['Prends ça!', "Mdrrrr, même pas mal", 'Croûte', 'Bim bam boum']
myUsername = "Test"

connectMsg = {
    "request": "subscribe",
   "port": userPort,
   "name": myUsername,
   "matricules": ["226"]
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
                            print('Connection still going...')
                        elif a['request'] == "play":
                            play(a, client)
                    else:
                        print('No request from the server')
            except socket.timeout:
                pass

def recv_json(socket: socket.socket):
    finished = False 
    msg = b''
    obj = None
    while not finished:
        msg += socket.recv(2048)
        try:
            obj = json.load(msg.decode('utf-8'))
        except json.JSONDecodeError:
            pass
        except UnicodeDecodeError:
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

    pos = getPos(board, current)
    print(pos)

    if current == 0:
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





