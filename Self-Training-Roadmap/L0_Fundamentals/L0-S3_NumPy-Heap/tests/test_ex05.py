from __future__ import annotations

import numpy as np

from l0_s3_1.ex05 import ex05


def test_ex05() -> None:
    a, col3, row4_reversed, submatrix, fancy, odd_numbers = ex05()

    # تست ماتریس اصلی
    expected = np.arange(1, 26).reshape(5, 5)
    assert np.array_equal(a, expected)

    # تست ستون سوم
    assert np.array_equal(col3, np.array([3, 8, 13, 18, 23]))

    # تست سطر چهارم معکوس
    assert np.array_equal(row4_reversed, np.array([20, 19, 18, 17, 16]))

    # تست زیربخش 3×3 بالا-چپ
    expected_sub = np.array([[1, 2, 3], [6, 7, 8], [11, 12, 13]])
    assert np.array_equal(submatrix, expected_sub)

    # تست Fancy indexing
    assert np.array_equal(fancy, np.array([5, 10, 15, 20, 25]))

    # تست Boolean indexing (اعداد فرد)
    expected_odds = np.arange(1, 26, 2)
    assert np.array_equal(odd_numbers, expected_odds)
