import threading
import time

#1. 通过实例化Thread建立多线程

def get_url(url):
    time.sleep(4)
    print('get url finished')

def get_html(url):
    time.sleep(2)
    print('get html finished')




# def main():
thread1 = threading.Thread(target=get_url, args=(1,))
thread2 = threading.Thread(target=get_html, args=(1,))
#thread1.setDaemon(False) #为True时，主线程执行完毕子线程也被迫关闭
start_time = time.time()


thread1.start()
print('thread1 start')
thread2.start()
print('thread2 start')

# thread2.join() #join用法：阻塞主线程直到join（）的线程运行完毕，但是其他子线程不受影响
# thread1.join()
# main是主进程 thread1，thread2是子线程 前面没有join（）时，主线程与子线程并行。两个子线程都用join时，总时间为子线程运行时间最大值，这也说明子线程都是并行。
print('running time is {}'.format(time.time() - start_time))


#2. 通过继承Threading来实现多线程
# class GetDetailHtml(threading.Thread):
#     def __init__(self, name, *args):
#         super().__init__(name=name, args=args)
#     def run(self):
#         print(self._args)
#         time.sleep(2)
#         print('{}finished'.format(self._name))
# thread1 = GetDetailHtml('get1',12,3,2)
# thread1.start()
# #thread1.join()
# print(9)