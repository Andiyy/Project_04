# import time
# from multiprocessing import Process, Manager
#
#
# class Test:
#     def foo(self, data):
#         data.value += 1
#         print(1)
#         time.sleep(3)
#         print(2)
#
#     def start(self):
#         manager = Manager()
#         self.x = manager.Value('i', 1)
#         self.y = manager.Value('i', 0)
#         manager.Array('f', )
#
#         a = Process(target=self.foo, args=(self.x,))
#         b = Process(target=self.foo, args=(self.y,))
#
#         print('Before waiting: ')
#         print('x = {0}'.format(self.x.value))
#         print('y = {0}'.format(self.y.value))
#
#         a.start()
#         b.start()
#
#         test = True
#         while test:
#             if a.is_alive() or b.is_alive():
#                 time.sleep(1)
#             else:
#                 test = False
#
#         print('After waiting: ')
#         print('x = {0}'.format(self.x.value))
#         print('y = {0}'.format(self.y.value))
#
#
# if __name__ == "__main__":
#     a = Test()
#     a.start()

from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Value, Array
from ctypes import Structure, c_double

class Point(Structure):
    _fields_ = [('x', c_double), ('y', c_double)]

def modify(n, x, s, A):
    n.value **= 2
    x.value **= 2
    s.value = s.value.upper()


if __name__ == '__main__':
    lock = Lock()

    n = Value('i', 7)
    x = Value(c_double, 1.0/3.0, lock=False)
    s = Array('c', b'hello world', lock=lock)
    A = Array(range(10))

    p = Process(target=modify, args=(n, x, s, A))
    p.start()
    p.join()

    print(n.value)
    print(x.value)
    print(s.value)
    print(A)
