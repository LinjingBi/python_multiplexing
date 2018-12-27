#1.epoll并不是一定比selelct好
#在高并发并且连接活跃度不是很高的情况下，epoll比select好（社交网络）
#在连接数目少，同时连接很活跃的情况下，select比epoll好（游戏）

import socket
from urllib.parse import urlparse
#1.DefaultSelector会根据平台选择epoll（linux）或者select（windows）
#2.DefaultSelector会提供io复用及注册机制
from selectors import DefaultSelector,EVENT_READ,EVENT_WRITE

selector=DefaultSelector()
Stop = False


class Fetcher:
    def __init__(self):
        self.url = None
        self.host = None
        self.path = None
        self.client = None
        self.urls = []
        self.worker = None
        self.data = ''

    def get_url(self, *url):
        self.urls = list(url)
        for url in self.urls:
            self.worker=url
            self.url = urlparse(url)
            self.host = self.url.netloc
            path = self.url.path
            if not path:
                path = '/'
            self.path = path
            self.connecting()

    def connected(self, key):
        if key.fileobj is self.client:
            print('9999999\n')
        else:
            print(type(key.fileobj))
        selector.unregister(key.fd)
        self.client.send('GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n'.format(self.path,self.host).encode('utf8'))
        selector.register(self.client.fileno(),EVENT_READ,self.readable)

    def readable(self, key):
        d = self.client.recv(1024).decode('utf8')
        if d:
            self.data += d
        else:
            #print(self.data)
            selector.unregister(key.fd)
            self.client.close()
            self.urls.remove(self.worker)
            if not self.urls:
                global Stop
                Stop = True

    def connecting(self):
        self.client = socket.socket()
        print(self.client)
        self.client.setblocking(False)
        try:
            self.client.connect((self.host, 80))
        except BlockingIOError:
            pass

        selector.register(self.client, EVENT_WRITE, self.connected)


def loop():
    while not Stop:
        ready = selector.select()

        for key, event in ready:
            call_back = key.data
            call_back(key)


if __name__ == "__main__":
    geturl = Fetcher()
    urls = 'http://www.baidu.com'
    geturl.get_url(urls)
    loop()



