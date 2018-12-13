import os
import time
#fork 只能用于linux/unix !!!!
pid = os.fork()
print('jiji')

if pid == 0:
    print('子进程{}，父进程{}'.format(os.getpid(),os.getppid()))
else:
    print('我是父进程{}'.format(pid))
time.sleep(2)

'''
root@tokyo:/socket_python# python3 multiprocess_test.py 
jiji
father12508
jiji
son12508father12507
'''
#说明父进程先是通过fork创建了一个pid不为0的子进程，然后父进程继续运行，子进程获得了pid=os.fork()以下的所有资源，并开始运行。
# 父进程会先结束，由于在父进程中pid是赋值了的不为零，所以执行else并打印。对于子进程，由于继承的资源并没有pid赋值语句，执行if并打印。
#sleep(2)用于在父进程print完毕后被挂起两秒不会立即结束，这样子进程的打印结果会跟父进程在同一个结果框里，否则，子进程的打印结果会是如下：
'''
root@tokyo:/socket_python# python3 multiprocess_test.py 
jiji
son12500
jiji
root@tokyo:/socket_python# son12500father1

'''
