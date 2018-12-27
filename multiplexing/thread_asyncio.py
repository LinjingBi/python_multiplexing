# 通过同步阻塞多线程的方式获取html
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
import socket
from urllib.parse import urlparse


def get_html(link):
    '''

    :param link:
    :return:页面的html
    '''
    url = urlparse(link)
    host = url.netloc
    path = url.path
    client = socket.socket()
    client.connect((host, 80))

    client.send(
        'GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n'.format(path, host).encode('utf8'))
    html = b''
    while True:
        data = client.recv(1024)
        if data:
            html += data
        else:
            break
    print(html)


if __name__ == '__main__':
    # '''
    # 如何在异步代码中运行多线程: 先把线程放入线程池，再用run_in_executor,这样异步就不会被阻塞而变成顺序执行，会变成多线程执行。
    # '''
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor(3)
    Tasks = []
    start = time.time()
    for i in range(20):
        url = 'http://shop.projectsedu.com/goods/{}/'.format(i)
        # 把线程放到线程池executor.submit(func, *args)，然后打包成concurrent.futures.Future对象
        task = loop.run_in_executor(executor, get_html, url)
        Tasks.append(task)
    # 数组用asyncio.wait（）
    loop.run_until_complete(asyncio.wait(Tasks))
    print('running time: {}'.format(time.time() - start))
