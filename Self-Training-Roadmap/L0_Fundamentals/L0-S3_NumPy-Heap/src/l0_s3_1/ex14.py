import numpy as np


def ex14():
    a_3_3 = np.arange(5, 14).reshape(3, 3, order="F")
    mask_gt10 = a_3_3 > 10
    mask_even = a_3_3 % 2 == 0
    a_gt10 = a_3_3[mask_gt10]
    a_even = a_3_3[mask_even]
    return a_3_3, a_gt10, a_even
