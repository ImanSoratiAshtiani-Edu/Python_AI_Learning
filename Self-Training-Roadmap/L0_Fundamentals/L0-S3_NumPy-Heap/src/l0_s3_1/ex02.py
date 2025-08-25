import numpy as np


def my_2d_array():
    a = np.arange(1, 10).reshape(3, 3)
    el_2_3 = a[1, 2]
    col_1 = a[:, 0]
    reversed_3th_row = a[2, ::-1]
    return a, el_2_3, col_1, reversed_3th_row
