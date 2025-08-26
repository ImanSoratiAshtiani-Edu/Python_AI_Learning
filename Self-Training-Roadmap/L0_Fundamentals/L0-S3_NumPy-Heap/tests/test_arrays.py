from __future__ import annotations

import numpy as np

from l0_s3_1.arrays import even_numbers


def test_even_numbers() -> None:
    out = even_numbers(10)
    assert isinstance(out, np.ndarray)
    assert out.tolist() == [0, 2, 4, 6, 8]
