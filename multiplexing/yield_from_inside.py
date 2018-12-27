#pep380

#1. 用法：RESULT = yield from EXPR
#符号说明
'''
_i: 子生成器，同时也是一个迭代器
_y: 子生成器产生的值
_r： yield from 表达式最终的值
_s：调用方通过send()发送的值
_e: 异常对象
'''
###yield_from内部解析（简明版）

_i = iter(EXPR) #EXPR是一个可迭代对象，_i是子生成器

try:
    _y = next(_i) #预激子生成器，把产出的第一个值存在_y（也就是子生成器中第一个yield右手边的内容）
except StopIteration as _e:
    _r = _e.value  #如果子生成器抛出StopIteration到委托生成器，那么就将异常对象的value传递给表达式的最终生成值（因为报SI意味着子生成器已经结束，所以返回值也就是最终值）
else:
    while 1: #如果预激完毕后子生成器没有报错，也就是说try一切正常，会执行else，试图继续yield子生成器的值
        _s = yield _y #委托生成器会在yield _y(预激结果）后被卡住（也就是说主函数里的预激委托生成器的语句，至此，在委托生成器内部完成了对子生成器的预激以及预激可能产生的SI错误的捕捉处理，现在，卡住并等待主函数send值以继续）
                      #此处说明委托生成器是需要主函数一直用send传入值控制，才会一步一步执行，不能是next，因为yield左边有=，这表明主函数中最好全部用send控制委托生成器而不是next
        try:
            _y = _i.send(_s) #这一步表示主函数已经send值到委托生成器内部，委托生成器恢复执行到try，并尝试给子生成器转发_s。如果顺利执行，那么子生成器将会从上次等待send值的断点处继续执行，直到执行完遇到的第一个yield，并把yield右手边的值赋值给_y
                            #有时候子生成器内部对应的yield可能并不需要send转发的值，但如果有值也不会报错，这时的send（_s)效果等同于next（_i）
        except StopIteration as _e:
            _r = _e.value    #意味着收到值继续执行直到子生成器结束（遇到return）都没有再遇到yield就会报SI，那么此时SI的返回值就代表了子生成器的最终值_r。
            break            #子生成器结束，委托生成器也可以结束了。
        #如果这里没有SI，委托生成将重复上诉步骤，直到子生成器结束。
RESULT = _r    #最后返回子生成器最终值给RESULT，完成本次协作。
                                                 ###一个猜想###
#有一个很有意思的现象，yield from内部构造只处理了子生成器的各种异常，但是其实委托生成器自己也是一个生成器，
# 也就说明如果它的执行不是通过yield自然停止，而是被它所在的函数或代码段中断，它自己也会抛出SI，而这里处理的都是子生成器的报错，
#所以我们会将它放到它所在的函数的while 1 循环内部，这样委托生成器就不会因为子生成器结束，造成它执行完RESULT = _r后由于所在函数的代码结束（而不是遇到下一个yield）而报SI，这个SI不会有返回值。
#有了这个外部的while 1，委托生成器在子生成器结束后应该会再次返回它的第一行代码执行直到遇到第一个yield并永远停止。
                                               ####分割行###

##完整版,多了对子生成器其他异常的处理，异常种类见下：
'''
1. 子生成器可能只是一个迭代器，并不是一个作为协程的生成器，所以它不支持.throw和.close方法
2. 如果子生成器支持.throw()和.send()方法，但是在子生成器内部，这两个办法都会抛出异常
3. 调用方让子生成器自己抛出异常
4. 当调用方使用next()或者.send(None)时，都要在子生成器上调用next()函数，当调用方使用.send()发送非None值时，才调用子生成器的.send()方法
'''
_i = iter(EXPR)
try:
    _y = next(_i)
except StopIteration as _e:
    _r = _e.value
else:           #相比简明版，完整版多了委托生成器对子生成器预激后进行循环处理时子生成器所报各种异常的处理
    while 1:
        try:
            _s = yield _y
        except GeneratorExit as _e:           #可能执行被键盘输入ctrl+c中断
            try:
                _m = _i.close                 #尝试找子生成器的关闭方法
            except AssertionError:
                pass                         #对应1.，可能只是一个迭代器，没有close方法
            else:
                _m()                         #没抛异常，执行close()关闭子生成器
            raise _e                         #不管有没有close(),委托生成器都会抛出这个GE异常
        except BaseException as _e:
            _x = sys.exc_info()              #收集异常信息
            try:
                _m = _i.throw                #尝试获取子生成器抛出BE类异常的方法
            except AttributeError:
                raise _e                     #对应1.， 直接抛出，无法使用throw
            else:
                try:
                    _y = _m(_x)              #使用throw方法，在当前执行到的yield处抛出异常
                except StopIteration as _e:  #可能已经没有yield，程序结束
                    _r = _e.value
                    break
        else:
            try:
                if _s:
                    _y = _i.send(_s)
                else:
                    _y = next(_i)             #对应4.，send值为none时，子生成器一律调用next
            except StopIteration as _e:
                _r = _e.value

RESULT = _r

                                                ###总结###
'''
1. 子生成器产生的值都是直接传给调用方的：调用方通过.send()发送的值都是直接传递给子生成器的；如果发送的是None会调用next()，不然，还是子生成器的.send()
2. 子生成器(EXPR)退出的时候，最后的return EXPR会触发一个StopIteration(EXPR)异常
3. yield from表达式的值，是子生成器终止时，传递给StopIteration异常的第一个参数
4. 如果调用的时候出现StopIteration异常,委托生成器会恢复运行，同时其他异常向上冒泡
5. 传入委托生成器里的异常里，除了GeneratorExit之外，其他所有的异常都会传递给子生成器的.throw()方法；如果调用.throw()的时候出现了StopIteration，那么恢复委托生成器的运行，其他异常全部向上冒泡
6. 如果在委托生成器上调用close()或传入GeneratorExit异常，会调用子生成器的.close()方法，没有的话就不会有调用。如果在调用.close()出现异常，那么就向上冒泡，否则的话委托生成器就会抛出GeneratorExit异常
'''

