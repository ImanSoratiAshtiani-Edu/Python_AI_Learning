import numpy as np


def ex13():
    a_4_5 = np.arange(10, 30).reshape(4, 5, order="C")
    a_r_1 = a_4_5[1]
    a_c_2 = a_4_5[:, 2]
    # a_sub = a_4_5[[1,1,1,2,2,2,3,3,3], [2,3,4,2,3,4,2,3,4,]]
    a_sub = a_4_5[1:4, 2:5]
    #   print(a_4_5)
    #   print(a_sub)
    return a_4_5, a_r_1, a_c_2, a_sub
