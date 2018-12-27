#yiled from解析：
# iterable_object = [['set',1,2],['list',3,4],['dict',5,6],['generator',7,8],]
#
#
# def yield_from_equivalent(iter_obj):
#     for obj in iter_obj:
#         for value in obj:
#             yield value
#
#
# def yield_from(iter_obj):
#     for obj in iter_obj:
#         yield from obj
#
#
# for item in yield_from_equivalent(iterable_object):
#     print(item)
#
# for item in yield_from(iterable_object):
#     print(item)


#yield from 实例，近似协程，用同步编程的方式实现异步编程
def sum_data():
    x = yield
    sale = sum(x)
    return sale, x

def middle(key):
    global record
    while True:     #不用while True， main（）里面就要用try。因为yield from 内部构造就有一个yield还有return，
                    # 如果没有while True，从sum的return过来就直接到了yield from的return然后赋值然后结束mi函数，由于不是因为遇到yield结束而是因为mi函数执行结束而结束，就会报StopIteration的错。
                    #用了while True之后，就算sum过来，执行完yieldfrom然后在执行完赋值语句之后，也会因为有一个while True而继续走到yield from的内部执行，直到遇到内部的yield，
                    # 然后停止，此时cpu应该不会阻塞在此，反而会继续回到上一次的断点，也就是main的for循环，从此开启了新一轮的for循环，mi又被新的middle函数覆盖，导致上次的mid就永远卡在了这里，未完成，等待垃圾回收。
        record[key] = yield from sum_data()

def main():
    #通过月销量，计算各种口味土豆泥总销量，并按格式打印
    global record
    record = {'麻辣土豆泥':(34,54,76,150),
              '奶香土豆泥':(43,76,100,200,300),
              '榴莲土豆泥':(0,0,0,0,0,0)
    }
    for key, value in record.items():
        mi = middle(key)
        mi.send(None)
        mi.send(value)
        # try:
        #     mi.send(value)
        # except StopIteration:
        #     pass
main()
print(record)







