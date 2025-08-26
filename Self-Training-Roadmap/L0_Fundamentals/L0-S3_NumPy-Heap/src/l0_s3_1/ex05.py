import numpy as np


def ex05():
    arr = np.arange(1, 26).reshape(5, 5)
    a_r_3 = arr[:, 2]  # a[2,:]
    a_r_4_reversed = arr[3, ::-1]
    a_3_3_up_left = arr[:3, :3]
    # Fancy indexing
    a_c_last = arr[:, -1]
    # Boolean indexing
    arr_odd = arr[arr % 2 == 1]
    return arr, a_r_3, a_r_4_reversed, a_3_3_up_left, a_c_last, arr_odd
