import numpy as np

# Importing the module runs a quick self-check inside ex17.py.
# That's okay for now; tests below exercise the core functions.
from l0_s3_1.ex17 import ex17_array_prep, ex17_methodBased


def test_ex17_method_vs_numpy():
    arr = np.arange(20, dtype=np.int32).reshape(4, 5, order="C")
    total, col_mean, row_std = ex17_methodBased(arr)

    assert total == int(arr.sum())
    assert np.allclose(col_mean, arr.mean(axis=0))
    assert np.allclose(row_std, arr.std(axis=1))  # ddof=0


def test_ex17_loop_matches_method():
    method, loop = ex17_array_prep()

    # unpack
    total_m, col_m, row_m = method
    total_l, col_l, row_l = loop

    assert total_m == total_l
    assert np.allclose(col_m, col_l)
    assert np.allclose(row_m, row_l)
