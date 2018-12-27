import threading
import time
# 通过Semphore的信号量来控制同一时间的活跃线程数，.acquire(),sem.value -1; .release(), sem.value +1
# 内部通过condition， wait， noytify实现不同线程间的唤醒

class Consumer(threading.Thread):
    def __init__(self, url, sem):
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
            # print(self.sem._value)
            self.sem.acquire()
            # print(i)
            csm = Consumer(
                url='http://www.baidu.com/{}'.format(i),
                sem=self.sem)
            csm.start()

# threading.Semaphore(3)传入的value,是同时间在运行的最大线程数
sem = threading.Semaphore(3)
# producer已经继承threading.Thread，本身就是一个线程类，可以直接被实例化后开始
p = Producer('url', sem)
p.start()
