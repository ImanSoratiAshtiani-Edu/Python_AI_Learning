from __future__ import annotations

import numpy as np

from l0_s3_1.ex03 import random_arrays_ops


def test_random_arrays_ops() -> None:
    a, b, sum_ab, sub_ab, mul_ab = random_arrays_ops(size=3, seed=42)

    # مقادیر ثابت با seed=42
    expected_a = np.array([0.37454012, 0.95071431, 0.73199394])
    expected_b = np.array([0.59865848, 0.15601864, 0.15599452])

    assert np.allclose(a, expected_a)
    assert np.allclose(b, expected_b)
    assert np.allclose(sum_ab, expected_a + expected_b)
    assert np.allclose(sub_ab, expected_a - expected_b)
    assert np.allclose(mul_ab, expected_a * expected_b)
