import numpy as np


def ex10():
    arr = np.arange(12)
    a = arr.reshape(2, 3, 2)
    a_reshaped1 = a.reshape(-1)
    a_reshaped2 = a_reshaped1.reshape(3, -1)
    a[0, 0, 0] = 99
    # print(a)
    # print(a_reshaped1)
    # print(a_reshaped2)
    return a, a_reshaped1, a_reshaped2
