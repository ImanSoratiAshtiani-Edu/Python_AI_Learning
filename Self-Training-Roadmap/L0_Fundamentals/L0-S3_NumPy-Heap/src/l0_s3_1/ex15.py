import numpy as np


def ex15():
    a_4_4 = np.arange(1, 17).reshape(4, 4, order="C")
    a_fancy = a_4_4[[0, 1, 2, 3], [0, 2, 3, 1]]
    a_r_0 = a_4_4[0]
    a_r_3 = a_4_4[-1]
    return a_4_4, a_fancy, a_r_0, a_r_3
