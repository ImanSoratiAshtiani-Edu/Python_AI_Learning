import numpy as np


def ex21():
    arr = np.arange(20).reshape(4, 5)
    arr_ravel = arr.ravel(order="F")
    return arr, arr_ravel
