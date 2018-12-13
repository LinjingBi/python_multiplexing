from concurrent.futures import ThreadPoolExecutor, as_completed
from concurrent.futures import ProcessPoolExecutor
import time


#多进程编程
#耗CPU的操作用多进程编程，对于io操作来说，使用多线程编程，进程切换代价高于线程


#1.耗CPU操作，二者时间比较：多线程是5.03s 多进程3.58s
def fib(n):
    if n<=2:
        return 1
    return fib(n-1)+fib(n-2)
# if __name__ =='__main__': #在windows下，进程池（ProcessPoolExecutor）必须运行在if name==main，linux不用。线程池都不用
#     start=time.time()
#     executor = ProcessPoolExecutor(3)
#     tasks=[executor.submit(fib, n) for n in range(25,35)]
#     for future in as_completed(tasks):
#         print(future.result())
#     print('running time is:{}'.format(time.time()-start))

#io操作，二者时间比较：多进程2.22s 多线程2.00s
def random_sleep(n):
    time.sleep(n)
    return n
if __name__ =='__main__': #在windows下，进程池（ProcessPoolExecutor）必须运行在if name==main，linux不用。线程池都不用
    start=time.time()
    executor = ThreadPoolExecutor(3)
    tasks=[executor.submit(random_sleep, n) for n in range(1,3)]
    for future in as_completed(tasks):
        print(future.result())
    print('running time is:{}'.format(time.time()-start))
