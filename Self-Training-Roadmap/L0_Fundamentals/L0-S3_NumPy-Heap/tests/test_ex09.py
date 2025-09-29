import numpy as np

from l0_s3_1.ex09 import ex09


def test_ex09_f_order_ravel_prefix_matches_first_column():
    a, a_r = ex09()
    # In F-order, linearization is column-major: first 4 items equal first column of a
    assert np.array_equal(a_r[: a.shape[0]], a[:, 0])


def test_ex09_length_and_dtype():
    a, a_r = ex09()
    assert a_r.size == a.size
    assert a_r.dtype == a.dtype
