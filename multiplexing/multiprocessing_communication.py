###使用Queue完成进程间通信的办法：
#1.queue.Queue只适用于线程间通信，多进程通信用multiprocessing.queues，但这个queues.Queue()不能用于pool。
#2.进程池（pool）用multiprocessing的Manager实例化的Queue(queue=Manager().Queue(maxsiaze))进行通信。
#3.共享全局变量通信只适用于多线程，不适用于多进程,因为多进程中资源是独立的不是共享的
###使用pipe完成进程间通信的办法：
#1.from multiprocessing import Pipe Pipe只能用于两个进程的通信
###使用Manager内部的数据结构（list, dict,...）进行进程间内存共享，共享进程从而共享内存：
#1.Manager是进程安全的可以不带锁
#2.子进程必须带join
###使用multiprocessingi的Array，Value，是直接共享内存：
#1.需要使用锁
#2.用法跟manager的一样
#3.子进程可以不用join
'''参考链接:
1. https://www.cnblogs.com/gengyi/p/8661235.html
2.http://www.cnblogs.com/liuhailong-py-way/p/5680588.html
'''

# #使用Queue进程间通信
# import time
# from multiprocessing import Process,Queue,Manager
#
#
# def consumer(queue):
#     time.sleep(2)
#     data = queue.get()
#     print(data)
#
#
# def producer(queue):
#     queue.put('a')
#     time.sleep(2)
# if __name__=='__main__':
#     queue = Manager().Queue(10)
#     progress1 = Process(target=producer,args=(queue,))
#     progress2 = Process(target=consumer,args=(queue,))
#     progress1.start()
#     progress2.start()
#     # progress1.join()
#     # progress2.join()

#
# #使用Pipe进程间通信：
# import time
# from multiprocessing import Pipe,Process
#
# def consumer(pipe):
#     print(pipe.recv())
#
# def producer(pipe):
#     pipe.send('dfeafa')
#
#
#
#
# if __name__ =='__main__':
#     sender, reciver = Pipe()
#     sender1 = Process(target=producer, args=(sender,))
#     reciver1 = Process(target=consumer, args=(reciver,))
#     sender1.start()
#     reciver1.start()

#使用Manager内部数据结构实现共享进程从而共享数据,由于Manager内部带锁（进程安全的),多进程时可以不用lock：
import time
from multiprocessing import Manager,Process,Value

# def producer(co_dict, key, value):
def producer(a):

    a[0] += 1
    time.sleep(2)

# def consumer(co_dict, key, value):
def consumer(a):
    time.sleep(2)
    a[0] +=2
    print(a)

if __name__ == '__main__':
    codict=Manager().dict()
    #a = Manager().Value('i',5)  #Array(self, typecode, sequence)Value(self, typecode, value): Array，Value是c语言的，内部的数据类型必须统一
    a = Manager().Array('i',[1,2,3])
    # P1 = Process(target=producer,args=(codict,'P1','2'))
    # P2 = Process(target=consumer,args=(codict,'P1','3'))
    # P1 = Process(target=producer,args=(a.value,))#.Value创建的是一个对象，不能直接加减，要用.value访问值
    # P2 = Process(target=consumer,args=(a.value,))
    P2 = Process(target=consumer,args=(a,))#.Array
    P1 = Process(target=producer,args=(a,))
    P1.daemon(False)
    P2.daemon(False)


    P1.start()
    P2.start()
    # P1.join()
    # P2.join()#不用join会报错
#原因：
# Array,Value等是在主进程创建的
#子进程是修改主进程：a[0] +1
# 主进程和子进程都在执行，主进程里有个字典，子进程要修改这个字典。
# 进程和进程之间要通信的话，需要创建连接的。相当于两边都写上一个socket，进程之间通过连接进行操作。也就是说Manager内部还是通过进程间通信实现数据共享
# 主进程执行到底部，说明执行完了，会把它里面的连接断开了。
# 主进程把连接断开了，子进程就连接不上主进程。所以要使用join
# 如果在底部写停10秒，主进程就停止下来，并没有执行完。主进程没有执行完，连接还没有断开，那子进程就可以连接它了


#使用Value,Array，这两个是直接在内核区预留的内存共享区分配区域给Array和Value，所以不存在通信的过程，但如果不用join可能存在子进程还没修改完，主进程就访问了。
# from multiprocessing import Process,Array,Value
#
# def add_test(v):
#     for i in range(len(v)):
#         v[i] = i
#         print(v[i])
#
# if __name__=='__main__':
#     array = Array('i',2) #Array(typecode_or_type, size_or_initializer, lock=True),注意只能规定array的长度
#     P1 = Process(target=add_test,args=(array,))
#     P1.start()
#     P1.join() #
#     for i in array: #遍历得出结果
#         print(i)
