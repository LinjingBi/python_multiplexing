import socket
import threading
from selectors import DefaultSelector,EVENT_READ,EVENT_WRITE

selector = DefaultSelector()

class Server:
    def __init__(self):
        self.client = None
        self.server = None
        self.client_list = []
        self.msg = {}
    def server_side(self):
        self.server = socket.socket()
        self.server.setblocking(False)
        self.server.bind(('0.0.0.0',8000))
        self.server.listen()
        # try:
        #     client,addr = self.server.accept()
        # except BlockingIOError:
        #     pass
        selector.register(self.server,EVENT_READ,self.accept)

    def accept(self,key):
        #selector.unregister(key.fd)
        client,addr = key.fileobj.accept()
        client.setblocking(0)
        self.client_list.append(client)
        #if len(self.client_list)==3:
        selector.register(client,EVENT_READ,self.connected)

    def connected(self,key):
        selector.unregister(key.fd)
        msg = key.fileobj.recv(1024).decode('utf8')
        if msg:
            print(msg)
            self.msg[key.fileobj]=msg

            selector.register(key.fileobj,EVENT_WRITE,self.broadcoast)

    def broadcoast(self,key):
        selector.unregister(key.fd)
        for user in self.client_list:
            if user != key.fileobj:
                user.send(self.msg[key.fileobj].encode('utf8'))
        # reply = input('Reply:')
        # key.fileobj.send('Server:{}'.format(reply).encode('utf8'))
        selector.register(key.fileobj,EVENT_READ,self.connected)



def loop():
    while True:
        ready = selector.select()
        for key,mask in ready:
            call_back = key.data
            call_back(key)


if __name__ == '__main__':
    server = Server()
    server.server_side()
    loop()