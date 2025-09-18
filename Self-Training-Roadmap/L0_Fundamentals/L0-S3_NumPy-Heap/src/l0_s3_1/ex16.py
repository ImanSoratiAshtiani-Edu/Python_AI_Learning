import numpy as np


def ex16():
    arr_c = np.arange(10, 22, dtype=np.int32).reshape(3, 4, order="C")
    arr_f = np.arange(10, 22).reshape(3, 4, order="F")
    # print(arr_c.strides)   # C-order array is interpretes row-wisely
    # print(arr_f.strides)   # F-order array is interpretes column-wisely
    return arr_c, arr_c.strides, arr_f, arr_f.strides
