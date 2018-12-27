import socket


client = socket.socket()
client.connect(('localhost',8000))

while True:
    client.send('he'.encode('utf8'))
    print(client.recv(1024).decode('utf8'))