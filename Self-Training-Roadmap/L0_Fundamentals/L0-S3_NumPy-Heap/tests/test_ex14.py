import numpy as np

from l0_s3_1.ex14 import ex14


def test_ex14_boolean_indexing():
    a, gt10, even = ex14()
    # reconstructed matrix with order='F'
    exp_a = np.array([[5, 8, 11], [6, 9, 12], [7, 10, 13]])
    assert np.array_equal(a, exp_a)
    # elements > 10 encountered in row-major order -> [11,12,13]
    assert np.array_equal(gt10, np.array([11, 12, 13]))
    # even elements in row-major order: 8,6,12,10
    assert np.array_equal(even, np.array([8, 6, 12, 10]))
