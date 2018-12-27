# def downloader(url): #子生成器 在没有async的情况下，没有yield就不是生成器，所以下一个例子的死循环就不会构成。
#     #yield '12'
#     return 'bobby'
#
# def uploader(url):  #委托生成器
#     global html
#     while True:
#         html = yield from downloader(url)
#         print(html)
#     #return 8
#
# if __name__ == '__main__':
#     up = uploader('http://www.baidu.com')
#     up.send(None)
#     # try:
#     #     print(up.send(None))
#     # except StopIteration as e:
#     #     print(e.value)


####一个造成死循环的有趣的例子

# async def downloader(url): #子生成器，有async，await 就没有 yield yield from
#     #yield '12'
#     return 'bobby'  #由于没有yield 直接return，导致子生成器在预激阶段就已经结束，所有的流程就回到了委托生成器，
#                     #而委托生成器，有一个while 1 循环，就会再次预激子生成器，再次返回，如此反复陷入死循环
#
# async def uploader(url):  #委托生成器
#     global html
#     while 1:
#         html = await downloader(url)
#         print(html)
#     #return 8
#
# if __name__ == '__main__':
#     up = uploader('http://www.baidu.com')
#     #next(up)
#     up.send(None) #会死循环打印html


#async-await真正的展示
###python为了将语义变得更加明确，就引入了async和await关键词用于定义原生的协程，将协程的定义过程与生成器分辨开
###！！有async，await 就没有 yield yield from！！


async def downloader(url):
    return 'bobby'

# 不使用async，如何让普通生成器变成awaitable对象（包含__await__()方法）,只能作为参考，就这段代码而言，跟async不等效，因为downloader没有return，html也就没被赋值
# import types
#
# @types.coroutine
# def downloader(url):
#     yield 'bobby'


async def uploader(url):
    html = await downloader(url) #注意await后面的对象的类一定要包含__await__()
    return html

if __name__ == '__main__':
    up = uploader('http://www.baidu.com')
    up.send(None)    #不能用next（up），next无法完成预激
    # try:            #用try消除异常，并打印uploader返回值
    #     up.send(None)
    # except StopIteration as e:
    #     print(e.value)