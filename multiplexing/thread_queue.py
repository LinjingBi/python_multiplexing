import threading
import time
import queue



# #线程中利用消息队列Queue实现线程通信
#
# detail_url_list=queue.Queue(maxsize=10)
#
#
# class GetDetailHtml(threading.Thread):
#     def __init__(self, name, *args):
#         super().__init__(name=name,args=args)
#
#     def run(self):
#          while not detail_url_list.empty():
#          #while True:
#                 url = detail_url_list.get(block=True)
#                 detail_url_list.task_done()
#                 print('正在解析{}'.format(url),self._name)
#                 #time.sleep(2)
#                 print('html解析完毕')
#
#
# class GetDetailUrl(threading.Thread):
#     def __init__(self,name,*args):
#         super().__init__(name=name,args=args)
#
#     def run(self):
#                 print('解析{}'.format(self._name))
#                 #time.sleep(2)
#                 detail_url_list.put(self._args,block=True)
#                 print('{}解析完毕'.format(self._name), -start + time.time())
#
#
# start=time.time()
# for i in range(12):
#     GetUrl = GetDetailUrl('url{}'.format(i),'http://www.baidu.com/{}'.format(i))
#     GetUrl.start()
# # GetUrl.join()
#
# for i in range(2):
#     html = GetDetailHtml('html{}'.format(i))
#     html.start()
#     #html.join()
#
#
# detail_url_list.join()
#
# print(time.time()-start)


###用condition写生产者-消费者模式

#1.
#当库存小于十个的时候，生产者要努力生产，大于等于10个的时候，生产者可以休息
#当库存等于1时，消费者要等待，等到生产者生产了大于等于1个时，才能开始消费

stock = 0
cnd = threading.Condition()


class Producer(threading.Thread):

    def __init__(self,name):
        super().__init__(name=name)

    def run(self):
        global stock
        while True:
            with cnd:
                if stock < 10:
                    stock += 1
                    print('现在库存不足（10-），{}刚刚生产了1个产品，库存为{}'.format(self._name, stock))
                    # cnd.notify_all()
                    cnd.notify()
                else:
                    print('库存充足（10+），可以休息一会儿了')
                    cnd.wait()
                time.sleep(2)
                #cnd.release()


class Consumer(threading.Thread):

    def __init__(self,name):
        super().__init__(name=name)

    def run(self):
        global stock
        while True:
            with cnd:
                if stock > 1:
                    # cnd.notify_all()
                    cnd.notify()
                    stock -= 1
                    print('我是消费者{}，我消费1个产品，现在库存为{}'.format(self._name, stock))
                else:
                    print('只剩一个产品了，消费者{}等待中'.format(self._name))
                    cnd.wait()
                time.sleep(2)
                #cnd.release()

if __name__ == '__main__':
    for i in range(2):
        prd = Producer('P{}'.format(i))
        prd.start()
    for i in range(10):
        csm = Consumer('C{}'.format(i))
        csm.start()
