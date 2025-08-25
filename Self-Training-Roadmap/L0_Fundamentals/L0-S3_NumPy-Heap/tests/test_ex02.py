from __future__ import annotations

import numpy as np

from l0_s3_1.ex02 import my_2d_array


def test_my_2d_array() -> None:
    a, el_2_3, col_1, reversed_3th_row = my_2d_array()

    # چک کن ماتریس درست ساخته شده باشه
    expected_a = np.arange(1, 10).reshape(3, 3)
    assert np.array_equal(a, expected_a)

    # چک کن عنصر سطر دوم، ستون سوم درست باشه
    assert el_2_3 == 6

    # چک کن ستون اول درست باشه
    assert np.array_equal(col_1, np.array([1, 4, 7]))

    # چک کن سطر سوم معکوس درست باشه
    assert np.array_equal(reversed_3th_row, np.array([9, 8, 7]))
