from asyncio import Lock,Queue

#在异步程序里，也会有Lock和Queue，但是内部的机制和同步不一样，不再涉及阻塞模式的锁和continue，而是通过yield from实现子协程暂停
#具体代码可以见源码

lock = Lock()
#由于协程本来就是单线程，所以声明一个全局变量做消息队列也可以，但是Queue可以设置最大长度，所以有大小限制的时候可以用Q
queue = Queue(maxsize=2)



#下面简单列出Lock和Queue的语法
async def lock_test():

    # 由于是异步锁，with前要加上async
    # 当第一个尝试acquire时，会立马获得锁，后面再来的会被yield from暂停，直到锁被release并且从等待队列出来的是该函数，该函数才会被唤醒
    async with lock:

    # queue的put get都是异步方法所以都要加上await
    # put需要暂停的是当queue.full()时，还想进行put的函数，它会创建一个future对象，
    # 然后yield from future，被暂停，直到被get导致queue非满，再继续运行。
    # 继续运行时，会首先把自己从put的等待队列中pop出来，最后一步是从get的等待队列中pop一个，因为这时queue已经非空，可以继续get
    await queue.put(1)

    # get需要暂停的是当queue.is_empty时还想进行get的函数。步骤跟get差不多
    await queue.get()
