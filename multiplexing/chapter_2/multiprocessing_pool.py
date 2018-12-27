import multiprocessing
import time

def geturl(n):
    time.sleep(n)
    print('url {} processing'.format(n))
    return n

if __name__=='__main__':
    #1.通过multiprocessing.Process创造进程
    #multiprocessing has the same API as threading.
    # process1 = multiprocessing.Process(target=geturl, args=(2,))
    # process1.start()
    # print(process1.pid)#因为是进程，所以有PID可以查看
    # process1.join()
    # print(99)
    #2.通过multiprocessing.Pool进程池创建管理进程
    pool= multiprocessing.Pool(multiprocessing.cpu_count())
    result = pool.apply_async(geturl, args=(2,)) #立即返回一个进程对象，并未代表已经开始执行（考虑进程池的大小）
    #join：要求主进程等待所有任务完成
    pool.close() #先保证pool内的活动都完成，close强制完成
    pool.join() #再join
    print(result.get()) #获取进程的返回值

# #通过迭代产生多个线程
#     intervel = [1,5,3]
#     # for result in pool.map(geturl,intervel):
#     #     print(result)
#     '''
#     url 1 processing
#     url 3 processing
#     url 5 processing
#     1
#     5
#     3
#     '''
#     # for result in pool.imap(geturl,intervel):
#     #     print(result)
#     '''
#     url 1 processing
#     1
#     url 3 processing
#     url 5 processing
#     5
#     3
#     '''
#     for result in pool.imap_unordered(geturl,intervel):
#         print(result)
#     '''
#     url 1 processing
#     1
#     url 3 processing
#     3
#     url 5 processing
#     5
#     '''
#     # tasks=[pool.apply_async(geturl,n) for n in intervel]