import numpy as np

from l0_s3_1.ex11 import ex11


def test_ex11_shapes_and_values():
    a, sum_a, sum_a_0, sum_a_1, mean_a_1 = ex11()
    assert a.shape == (3, 4)
    # total sum of 0..11
    assert sum_a == 66
    # column sums and row sums
    assert np.array_equal(sum_a_0, np.array([12, 15, 18, 21]))
    assert np.array_equal(sum_a_1, np.array([6, 22, 38]))
    # row means
    assert np.allclose(mean_a_1, np.array([1.5, 5.5, 9.5]))
