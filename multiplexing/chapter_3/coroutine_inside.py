# #run_until_complete()和run_forever()区别
# import asyncio
# loop = asyncio.get_event_loop()
# loop.run_until_complete(future=)     #会在指定的future运行完后，执行loop.stop()
# loop.run_forever()                   #会一直运行


# 如何终止loop: 如果键入ctrl+c，loop终止

import asyncio
import time


async def get_html(t):
    print('sleeping...')
    await asyncio.sleep(t)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    task_list = [get_html(1), get_html(3), get_html(2)]
    loop.run_forever()
    all_task = asyncio.Task.all_tasks()

    try:
        loop.run_forever()
    except KeyboardInterrupt as e:
        for task in all_task:
            print('cancel task')
            print(task.cancel())  # cancel成功True
        loop.stop()  # 只是暂停
        loop.run_forever()  # stop后立马要run_forever,不然报错
    finally:
        loop.close()  # 彻底关闭

# 子协程嵌套原理：python3.6 chain
# coroutines：https://docs.python.org/3.6/library/asyncio-task.html#example-chain-coroutines

# 嵌套原理跟yield from 一致：
# 1.构造一个Eventloop 2.为每一个协程创捷Task对象 3.loop.run_forever(task), 启动协程A，协程A通过await启动协程B，一层一层嵌套，
# 4.如果有await asyncio.sleep(),就会停止继续嵌套 5.从所在嵌套协程，直接返回Task 6.Task再返回Eventloop，等待sleep时间过去
# 6.sleep过去，从Eventloop直接返回暂停的嵌套协程，
# 7.从最深层的嵌套一层一层往前返回值，一路raise StopIteration(return_value),直到经过Task，最终返回Eventloop
