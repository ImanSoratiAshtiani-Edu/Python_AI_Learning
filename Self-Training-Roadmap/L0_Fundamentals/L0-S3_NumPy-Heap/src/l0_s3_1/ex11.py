import numpy as np


def ex11():
    a_3_4 = np.arange(12).reshape(3, 4, order="C")
    sum_a = a_3_4.sum()
    sum_a_0 = a_3_4.sum(axis=0)
    sum_a_1 = a_3_4.sum(axis=1)
    mean_a_1 = a_3_4.mean(axis=1)
    return a_3_4, sum_a, sum_a_0, sum_a_1, mean_a_1
