import threading
import time


class Consumer(threading.Thread):
    def __init__(self,url,sem):
        super().__init__()
        self.url = url
        self.sem = sem
    def run(self):
        time.sleep(2)
        print('working on url:{}'.format(self.url))
        self.sem.release()



class Producer(threading.Thread):
    def __init__(self, name, sem):
        super().__init__(name=name)
        self.sem = sem

    def run(self):

        for i in range(10):
            #print(self.sem._value)
            self.sem.acquire()
            #print(i)
            csm = Consumer(url='http://www.baidu.com/{}'.format(i),sem=self.sem)
            csm.start()

sem = threading.Semaphore(3)
p = Producer('url',sem)
p.start()
 