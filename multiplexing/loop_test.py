# 事件循环+回调（在协程环境下，用驱动生成器）+epoll，IO多路复用
# asyncio是python用于解决异步io的一整套方案
# tornado,gevent,twisted(scrapy, django channels)
# tornado实现了动态web服务器，而django+flask只是提供了web框架
# 组合：tornado+nginx


# 使用asyncio
import asyncio
import time
from functools import partial




async def get_html(url):
    print('task start')
    # 因为asyncio.sleep相当于需要切换执行的函数，所以一定要有await，类似于yield from。等待await后面的东西执行完成
    await asyncio.sleep(2)

    # '''错误用法
    # await time.sleep(2) #首先，timesleep是一个阻塞的方法不要用在协程里面。会报错，因为timesleep没有返回值，而await需要一个awaitable的对象。
    # time.sleep(2)       # 虽然不会报错，但是协程会被阻塞在这个函数，如果事件循环里有很多函数的话，整个程序就会变成顺序执行，而不是非阻塞。
    # '''

    return 'bobby'

# async def test():
#     await asyncio.sleep(1)
#     print(6666)

# if __name__ == '__main__':
#     start = time.time()
#     loop = asyncio.get_event_loop()     #返回协程中的事件循环，如果没有，初始化一个，协程必须配合事件循环使用
#     tast = [get_html(get_html('http://www.baidu.com')) for i in range(10)]
#     # loop.run_until_complete(get_html('http://www.baidu.com'))  #相当于join，等事件循环里的函数跑完了再执行下面的代码
#     # loop.run_until_complete(test())
#
#
#     loop.run_until_complete(asyncio.wait(tast))
#     print('running time is {}'.format(time.time()-start))


# 获取协程的返回值

def callback(url, future):  # 作为协程完毕的callback功能函数，有一个默认参数future，该参数一定要放在第一位
    print('html 获取完毕')


async def test():
    print(9)
    await asyncio.sleep(1)

# if __name__ == '__main__':
#     start = time.time()
#     loop = asyncio.get_event_loop()  # 返回协程中的事件循环，如果没有，初始化一个，协程必须配合事件循环使用
#     #tast = [get_html('http://www.baidu.com') for i in range(10)]
#     # loop.run_until_complete(get_html('http://www.baidu.com'))  #相当于join，等事件循环里的函数跑完了再执行下面的代码
#     # loop.run_until_complete(test())
#     # 如果协程是以数组的形式传入的，用asyncio.wait
#     #get_future = asyncio.wait(tast)
#     #查看协程返回值需要先将协程生成一个future对象，方法有两个asyncio.ensure_future（），loop.create_task（）
#     # get_future = asyncio.ensure_future(get_html('http://www.baidu.com'))
#     get_future = loop.create_task(get_html('http://www.baidu.com')) #相当于把协程注册到loop当中，第一个方法最终也会调用此方法
#     #get_future.add_done_callback(callback)  # 协程完毕后调用的通知函数，注意输入的是函数名称，要放在run_until_complete前面
#     get_future.add_done_callback(partial(callback, 'http://www.baidu.com')) #如果callback函数有其他传入参数，用partial包装
#     loop.run_until_complete(get_future)
#     print(get_future.result())
#
#     print('running time is {}'.format(time.time() - start))


# 区别asyncio.gather和async.wait

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # tasks = [get_html('http://www.baidu.com') for i in range(10)]
    # tasks = asyncio.wait(tasks)    #只能放一组
    test = test()
    # 如果不用下面的run_until..将会导致主程序执行完，而协程们还未被唤醒并完成
    tasks1 = [get_html('http://www.baidu.com') for i in range(2)]
    tasks2 = [get_html('http://www.baidu.com') for i in range(2)]
    # loop.run_until_complete(asyncio.gather(*tasks1,*tasks2))
    # #两种方式用gather分组运行
    task1 = asyncio.gather(*tasks1)
    task2 = asyncio.gather(*tasks2)

    # task2.cancel()              #取消
    loop.run_until_complete(asyncio.gather(task1, task2, test))
    # loop.run_until_complete(tasks)


