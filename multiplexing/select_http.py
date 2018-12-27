# asyncio没有提供http协议的接口，aiohttp有
import asyncio
import time
from urllib.parse import urlparse


async def get_html(link):
    url = urlparse(link)
    host = url.netloc
    path = url.path
    # 协程的办法就是把原理耗时阻塞的位置也就是注册的位置，全部yield from出去

    # 用协程的方式完成了socket.connect,以及register EVENT_WRITE
    reader, writer = await asyncio.open_connection(host, 80)
    # 完成了unregister，然后socket.send，并且register
    # EVENT_READ，说明下一步是要从recv也就是现在的reader读收到的回复
    writer.write(
        'GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n'.format(path, host).encode('utf8'))
    all_lines = []
    async for raw_line in reader:  # 用异步的方式导出reader内部recv的东西
        line = raw_line.decode('utf8')
        all_lines.append(line)
    html = '\n'.join(all_lines)
    print(html)
    return html


async def main():
    tasks = []
    for i in range(20):
        url = 'http://shop.projectsedu.com/goods/{}/'.format(i)
        tasks.append(asyncio.ensure_future(get_html(url)))
    # asyncio.as_completed()是一个异步的方式，所以必须配合await，返回的是task对象的result
    for task in asyncio.as_completed(tasks):
        result = await task
        print(result)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    Tasks = []
    start = time.time()
    # for i in range(20):  # 构造20个预备协程
    #     url = 'http://shop.projectsedu.com/goods/{}/'.format(i)
    #     Tasks.append(get_html(url))
    # loop.run_until_complete(asyncio.wait(Tasks))  # 为他们统一创建task对象，开始执行

    # #不想在函数内部打印
    for i in range(20):  # 构造20个预备协程
        url = 'http://shop.projectsedu.com/goods/{}/'.format(i)
        Tasks.append(loop.create_task(get_html(url)))
    loop.run_until_complete(asyncio.wait(Tasks))
    for item in Tasks:
        print(item.result())

    # 达到as_complete()的效果，完成就打印
    # 需要重新构造一个异步的main（）,上方代码除了第一句全部注释
    # 开启一个异步程序的时候全部用loop.run_until_complete(func())/loop.run_forever(func())
    # loop.run_until_complete(main())

    print('running time: {}'.format(time.time() - start))
