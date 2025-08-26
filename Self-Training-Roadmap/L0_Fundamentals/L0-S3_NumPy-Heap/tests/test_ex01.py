from __future__ import annotations

import numpy as np

from l0_s3_1.ex01 import even_1d_array


def test_even_1d_array() -> None:
    out = even_1d_array()
    assert isinstance(out, np.ndarray)
    assert out.tolist() == [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

    # تست با پارامترهای متفاوت
    out2 = even_1d_array(5, 15)
    assert out2.tolist() == [6, 8, 10, 12, 14]
