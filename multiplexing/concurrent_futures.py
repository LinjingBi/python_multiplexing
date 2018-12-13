from concurrent.futures import ThreadPoolExecutor, as_completed,wait, FIRST_COMPLETED


#线程池，为什么要用线程池
#主线程可以获取某一个线程的状态或者某一个任务的状态，以及返回值
#当一个线程完成的时候，我们主线程能立即知道
#futurs可以让多线程和多进程编码接口一致

import time

def get_html(times):
    time.sleep(times)
    print('got html {} success'.format(times))
    return times

executor = ThreadPoolExecutor(max_workers=2)
# if __name__ == '__main__':
#     #通过submit函数提交到线程池，submit是立即返回一个future对象
#     task1 = executor.submit(get_html,3)
#     task2 = executor.submit(get_html,2)
#
#     # print(task1.done()) #判断某一任务是否完成
#     time.sleep(3.1)
#     print(task1.done())
#     print(task1.result())  #返回任务的返回值
#     print(task2.cancel())  #一旦任务成功进入线程池（size<maximumsize），就不可能被cancel，没进入可以cancel

#成组的获取成功任务的返回
#方法一，利用as_completed(tasks)，返回值为future对象，不是最终结果，返回顺序为执行完成顺序
intervel = [3,2,4]
tasks = [executor.submit(get_html, times) for times in intervel ]
# for future in as_completed(tasks):
#     data = future.result()
#     print('get {} result'.format(data))

wait(tasks, return_when=FIRST_COMPLETED)
print('done')
#方法二，利用线程池（executor）的map功能直接映射，输出（future）为线程的返回值，并且返回的顺序为map的顺序
# for future in executor.map(get_html,intervel):
#     print(future)



