import socket
from urllib.parse import urlparse


def get_url(url):
    url = urlparse(url)
    host = url.netloc
    path = url.path
    if path == '':
        path = '/'
    return host, path


client = socket.socket()
url = input('url:\n')
host, path = get_url(url)
client.connect((host,80))

client.sendall('GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n'.format(path, host).encode('utf8'))

data=''

while True:
    d = client.recv(1024).decode('utf8')
    if d:
        data += d
    else:
        break

data = data.split('\r\n\r\n')

print(data[1])
client.close()




# while True:
#     text = input('client:')
#     client.sendall(text.encode('utf-8'))
#     receive = client.recv(1024)
#     print(receive.decode('utf-8'))
#     if receive.decode('utf-8') == 'serverclosed':
#         client.close()
#         break
#     # client.close()