from __future__ import annotations

import numpy as np

from l0_s3_1.ex04 import ex04


def test_ex04() -> None:
    arr, arr2, arr3, arr4, arr5, shape, size, ndim, dtype, itemsize = ex04()

    # تست ماتریس ۴×۴ پر از ۹
    expected_arr = np.full((4, 4), 9, dtype=np.int64)
    assert np.array_equal(arr, expected_arr)

    # تست linspace (۲۰ مقدار بین ۰ تا ۱، بدون شامل شدن ۱)
    expected_arr2 = np.linspace(0, 1, 20, endpoint=False)
    assert np.allclose(arr2, expected_arr2)

    # تست dtype و astype
    assert arr3.dtype == np.int64
    assert arr4.dtype == np.float64
    assert np.allclose(arr4, arr3.astype(np.float64))

    # تست آرایه ۳×۵ رندوم با seed=42
    np.random.seed(42)
    expected_arr5 = np.random.randint(0, 10, size=(3, 5))
    assert np.array_equal(arr5, expected_arr5)

    # تست ویژگی‌های آرایه
    assert shape == (3, 5)
    assert size == 15
    assert ndim == 2
    assert dtype == np.int64
    assert itemsize == arr5.itemsize
