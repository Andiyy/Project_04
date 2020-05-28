import time
from multiprocessing import Process, Manager


class Test:
    def foo(self, data):
        data.value += 1
        print(1)
        time.sleep(3)
        print(2)

    def start(self):
        manager = Manager()
        x = manager.Value('i', 1)
        y = manager.Value('i', 0)

        a = Process(target=self.foo, args=(x,))
        b = Process(target=self.foo, args=(y,))

        print('Before waiting: ')
        print('x = {0}'.format(x.value))
        print('y = {0}'.format(y.value))

        a.start()
        b.start()

        test = True
        while test:
            if a.is_alive() or b.is_alive():
                time.sleep(1)
            else:
                test = False

        print('After waiting: ')
        print('x = {0}'.format(x.value))
        print('y = {0}'.format(y.value))


if __name__ == "__main__":
    a = Test()
    a.start()

