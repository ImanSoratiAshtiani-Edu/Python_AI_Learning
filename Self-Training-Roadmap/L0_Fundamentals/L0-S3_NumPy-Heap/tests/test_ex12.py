import numpy as np

from l0_s3_1.ex11 import ex11
from l0_s3_1.ex12 import ex12


def test_ex12_std_max_and_argmax():
    arr_ex11 = ex11()[0]
    arr, std_a, max_0, max_index_a = ex12()
    # shape and equality with ex11 base array
    assert arr.shape == (3, 4)
    assert np.array_equal(arr, arr_ex11)
    # population std of 0..11
    # var = 11.916666..., std ~ 3.45205252953466
    assert np.isclose(std_a, 3.4520525295346629, rtol=1e-12, atol=1e-12)
    # column-wise max
    assert np.array_equal(max_0, np.array([8, 9, 10, 11]))
    # flat index of global max (11) in C-order
    assert max_index_a == 11
