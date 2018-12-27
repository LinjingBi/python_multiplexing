import socket
from urllib.parse import urlparse


client = socket.socket()
client.connect(('localhost',8000))

while True:
    client.send('hello'.encode('utf8'))
    print(client.recv(1024).decode('utf8'))