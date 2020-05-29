from multiprocessing import Process, Queue, Value
import numpy as np
import time


class Test12:
    steps = 10
    b = np.zeros(steps)

    def run(self):
        q_1 = Queue()
        q_2 = Queue()

        p_1 = Process(target=self.f, args=(q_1,))
        p_2 = Process(target=self.f_2, args=(q_2,))

        p_1.start()
        p_2.start()

        a = q_1.get()  # prints "[42, None, 'hello']"
        b = q_2.get()  # prints "[42, None, 'hello']"
        p_1.join()
        p_2.join()

        print(a)
        print(b)

    def f(self, q):
        a = np.zeros(self.steps)

        for i in range(self.steps):
            a[i] = i
            self.b[i] = i

        q.put(a)
        time.sleep(2)
        print(2)

    def f_2(self, q):
        a = np.zeros(self.steps)

        for i in range(self.steps):
            a[i] = i

        q.put(a)

        print(1)


if __name__ == '__main__':
    a = Test12()
    a.run()




# from multiprocessing import Process, Pipe
# import time
#
#
# def f(conn):
#     conn.send([42, None, 'hello'])
#
#     time.sleep(2)
#     print(2)
#     conn.close()
#
#
# if __name__ == '__main__':
#     parent_conn, child_conn = Pipe()
#     p = Process(target=f, args=(child_conn,))
#     p.start()
#     print(parent_conn.recv())   # prints "[42, None, 'hello']"
#     p.join()
#     print(1)

# from multiprocessing import Process, Value, Array
#
# def f(n, a):
#     n.value = 3.1415927
#     for i in range(len(a)):
#         a[i] = -a[i]
#
# if __name__ == '__main__':
#     num = Value('d', 0.0)
#     arr = Array('i', range(10))
#
#     p = Process(target=f, args=(num, arr))
#     p.start()
#     p.join()
#
#     print(num.value)
#     print(arr[:])
