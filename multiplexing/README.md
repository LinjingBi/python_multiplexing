# chapter 1 socket网络通信
- 用阻塞io实现的socket server端和client端
- 用非阻塞io实现的client端
- 用select+callback+eventloop实现的socket通信
- 基于select+callback+eventloop实现的多人聊天室的server端和client端
- 用select+协程+eventpool实现socket通信
# chapter 2 线程和进程
- 多线程编程的库threading，以及创建线程（python_thread.py）
- 多线程编程的Lock，condition，semaphore，queue(thread_lock.py, thread_queue.py, thread_cond.py, thread_sem.py)
- 多线程编程的ThreadingPoolExecuter (threadpool_concurrent_futures.py)
- 多进程的创建(multiprocessing_pool.py)
- linux中的进程(multiprocess_fork_inlinux.py)
- 多进程间的通信(multiprocessing_communication.py)
- 多进程多线程比较(progress_thread_compare.py)
# chapter 3 协程
- 介绍python生成器(coroutine_yield_test.py)
- 介绍yield from(coroutine_yield_from.py, yield_from_inside.py)
- 从生成器到协程的过渡(from_yield_to_asyncio.py)
- python中的协程asyncio模块(asyncio.md, asyncio_first_class.py)
- 协程嵌套的原理(coroutine_inside.py)
- 协程中的Lock，condition，queue(ayncio_lock.py)
- 在协程中实现多线程(thread_in_asyncio.py)