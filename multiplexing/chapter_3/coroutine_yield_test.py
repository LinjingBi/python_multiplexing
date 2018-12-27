# ！！！为什么需要协程！！！
# 1. 回调模式编码复杂度高
# 2. 同步编程的并发性不高
# 3. 多线程编程需要线程间同步，用到lock
# 协程需要做到什么
# 1. 采用同步的方法去编写异步代码
# 2. 使用单线程去切换任务：
# 1. 同步模式下线程是由操作系统切换的，单线程切换意味着由程序员自己去调度任务
# 2. 不需要锁，并发性高，如果单线程内切换函数，性能远高于线程切换，并发性更好


def gen_func(a):
    yield a
    # print(88)
    html = yield  # 0. 要等函数一步一步（用next）yiled到赋值语句的前一个，才能执行1.
    # 1.首先，需要一个gen.send（None）或者next（gen），让生成器输出yield右手边的值
    # 2.然后，gen.send(value_for_html),给html赋值，
    # 3.并且函数会运行到执行完赋值后的下一个yield为止，也就是说print(gen.send(value_for_html))打印的是下一个yield的值
    print(html)  # 2.bobby
    yield 3
    yield 4
    yield 5
    # yield 6


if __name__ == '__main__':
    # gen_func（12）并不会执行，因为生成器只有实列化后，通过对实例进行next操作才会开始执行，这一点不同于普通函数传入参数就会开始执行。
    gen = gen_func(12)
    print(next(gen))  # 0. 12
    print(gen.send(None))  # 1.None
    html = 'bobby'
    print(gen.send(html))  # 3.3
    # 当yield左边没有=表明在等待send值，只有一个单纯的yield时，调用send（任意数字/内容）效果都等同于next
    # gen.close() #关闭生成器, 关闭后，下一句在执行next会在主程序中报错，在生成器中试图try except 也会报错，不要尝试try这样的话主程序还可以正常运行
    #             #close后，再调用next产生的错误继承自BaseException，并不是普通的Exception
    try:
        # throw会在上一步已经执行完的yield报错（yield 3），可以用try
        # pass掉，主程序继续执行，但是生成器已经close，就算后面有yield，也会抛SI
        gen.throw(Exception('download error'))
    except Exception as e:
        pass
    #gen.throw(Exception, 'download error')
    try:
        print(next(gen))
    except StopIteration as e:
        print(e.value)
