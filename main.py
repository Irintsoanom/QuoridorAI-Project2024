import socket
import json


serverAddress = ('0.0.0.0', 5000)

connectMsg = {
    "request": "subscribe",
   "port": 8888,
   "name": "fun_name_for_the_client",
   "matricules": ["22336"]
}

data = json.dumps(connectMsg)

# def connect():
#     with socket.socket() as s:
#         s.bind(serverAddress)
#         s.listen()
#         s.settimeout(0.5)
#         while True:
#             try:
#                 client, clientAddress = s.accept()

