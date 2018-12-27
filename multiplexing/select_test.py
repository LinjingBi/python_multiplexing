import select
import socket
from urllib.parse import urlparse

#非阻塞io，setblocking（False），但是send recv都会因为设为非阻塞后，connect没完成而报错，所以需要while True + try except 完成收发过程
#需要记住的是阻塞io并不会消耗cpu，而非阻塞io会因为循环的问询而消耗可能消耗大量的cpu
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
client.setblocking(False) #True 阻塞并不消耗cpu
try:
        client.connect((host,80))

except BlockingIOError:
        pass
    # except OSError:
    #     pass
while True:
    try:
        client.send('GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n'.format(path,host).encode('utf8'))
        break
    except OSError:
        pass
data = ''
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




