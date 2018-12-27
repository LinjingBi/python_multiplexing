import threading

cond = threading.Condition()

# 通过在一个线程中用wait获得锁，另一个线程中notify释放锁，来完成不同线程之间交互唤醒，也就是本例中的两个线程之间你来我往的对话


class TianMao(threading.Thread):
    def __init__(self, cond):
        super().__init__(name='TianMao')
        self.cond = cond

    def run(self):
        with self.cond:
            print(1)
            self.cond.notify()  # 只能在获取了cond这个底层锁的情况下运行，而不是获取了wait的上层锁

            self.cond.wait()
            print(3)
            self.cond.notify()


class XiaoAi(threading.Thread):
    global cond

    def __init__(self):
        super().__init__(name='XiaoAi')
        #self.cond = cond

    def run(self):
        cond.acquire()
        # cond.wait()
        print(2)
        cond.notify()

        cond.wait()
        print(4)
        cond.release()


if __name__ == '__main__':
    TM = TianMao(cond)
    #TM2 = TianMao(cond)
    XA = XiaoAi()

    TM.start()
    XA.start()

    # TM2.start()
