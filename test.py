from array import array
import numpy as np


def t_1():
    a_a = array('i')
    for i in range(1000):
        a_a.append(i)


def t_2():
    a_a = np.empty(0)
    for i in range(1):
        a_a = np.append(a_a, i)


t_1()
t_2()
