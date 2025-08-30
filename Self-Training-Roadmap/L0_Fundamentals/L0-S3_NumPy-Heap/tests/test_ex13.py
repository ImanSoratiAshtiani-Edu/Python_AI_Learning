import numpy as np

from l0_s3_1.ex13 import ex13


def test_ex13_slicing_and_views():
    a, r1, c2, sub = ex13()
    assert a.shape == (4, 5)
    # expected arrays
    exp_a = np.array(
        [[10, 11, 12, 13, 14], [15, 16, 17, 18, 19], [20, 21, 22, 23, 24], [25, 26, 27, 28, 29]]
    )
    exp_r1 = np.array([15, 16, 17, 18, 19])
    exp_c2 = np.array([12, 17, 22, 27])
    exp_sub = np.array([[17, 18, 19], [22, 23, 24], [27, 28, 29]])
    assert np.array_equal(a, exp_a)
    assert np.array_equal(r1, exp_r1)
    assert np.array_equal(c2, exp_c2)
    assert np.array_equal(sub, exp_sub)
