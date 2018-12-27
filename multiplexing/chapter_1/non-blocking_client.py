import select
import socket
from urllib.parse import urlparse

# 非阻塞io，setblocking（False），但是send recv都会因为设为非阻塞后，connect没完成而报错，所以需要while True + try except 完成收发过程
# 需要记住的是阻塞io并不会消耗cpu，而非阻塞io会因为循环的问询而消耗可能消耗大量的cpu
# 非阻塞虽然不会耗时等待，但会不断调用cpu去问询，这个问询的过程出现在与server通信的每一个阶段
# 所以单纯的把socket设置为非组塞，并不会提升socket通信的效率，还需要结合io复用


def get_url(url):
    url = urlparse(url)
    host = url.netloc
    path = url.path

    if path == '':
        path = '/'

    return host, path


url = input('please input the url:\n')
(host, path) = get_url(url)
client = socket.socket()
client.setblocking(False)  # True 阻塞并不消耗cpu

# 由于把client设置为non-blocking，connect的时候，server并不会立马连接，
# client端并不会一直等待server的连接，而是会继续将执行，所以我们捕捉pass
try:
    client.connect((host, 80))

except BlockingIOError:
    pass

# 由于connect直接pass，到send的时候可能并没有建立连接，会抛出OSError，我们应该继续循环，等待直到server端返回建立连接的包

while True:
    try:
        client.send(
            'GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n'.format(path, host).encode('utf8'))
        break
    except OSError:
        pass
data = ''
# 由于是非阻塞的套接字，可能执行recv的时候并没有收到数据，会报错，我们就需要不断循环，完成收的任务
while True:
    try:
        d = client.recv(1024).decode('utf8')
        if d:
            data += d
        else:
            break
    except BlockingIOError:
        pass

html_data = data
print(html_data.split('\r\n\r\n')[1])


# get_url('http://www.baidu.com')
