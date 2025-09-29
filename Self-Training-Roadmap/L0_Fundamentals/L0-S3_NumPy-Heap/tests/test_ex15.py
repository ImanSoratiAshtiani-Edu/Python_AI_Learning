import numpy as np

from l0_s3_1.ex15 import ex15


def test_ex15_fancy_and_rows():
    A, fancy, r0, r3 = ex15()
    exp_A = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])
    assert np.array_equal(A, exp_A)
    # selected items: (0,0)=1, (1,2)=7, (2,3)=12, (3,1)=14
    assert np.array_equal(fancy, np.array([1, 7, 12, 14]))
    assert np.array_equal(r0, np.array([1, 2, 3, 4]))
    assert np.array_equal(r3, np.array([13, 14, 15, 16]))
