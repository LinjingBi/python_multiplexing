import socket
import time
from selectors import DefaultSelector,EVENT_READ,EVENT_WRITE

selector = DefaultSelector()


class Client:
    def __init__(self):
        self.client = None
        self.name = None


    def client_side(self,name):
        self.client = socket.socket()
        #print(client.fileno())
        self.name = name
        self.client.setblocking(False)
        try:
            self.client.connect(('localhost',8000))
        except BlockingIOError:
            pass

        selector.register(self.client.fileno(),EVENT_WRITE,self.connected)
        #selector.register(self.client.fileno(),EVENT_READ,self.connected)

    def connected(self,key):
        selector.unregister(key.fd)
        start=time.time()
        while time.time()-start<2:
            print(8)
            reply = input('C3:')
            self.client.send('{}:{}'.format(self.name,reply).encode('utf8'))
        selector.register(self.client.fileno(),EVENT_READ,self.readable)

    def readable(self,key):
        data = self.client.recv(1024).decode('utf8')
        print('{}'.format(data))
        selector.unregister(key.fd)
        selector.register(key.fileobj, EVENT_WRITE,self.connected)


def loop():
    while True:
        ready = selector.select()
        for key,mask in ready:
            call_back = key.data
            call_back(key)




if __name__ == "__main__":
    client = Client()
    name = 'C{}'.format(3)
    client.client_side(name=name)
    loop()









