import numpy as np


def ex08():
    arr = np.arange(20)
    a = arr.reshape(4, -1)
    a_r = a.ravel()
    a_f = a.flatten()
    a[0, 0] = 99
    # print(a_f)
    # print(a_r)
    return arr, a, a_r, a_f
