# test_numpy_array.py
import numpy as np


def test_array_generation():
    rng = np.random.default_rng(2)
    arr = rng.integers(0, 10, size=(2, 5))

    # Expected output deterministico con seed = 2
    expected = np.array([[8, 2, 1, 2, 4], [8, 4, 0, 3, 6]])

    # Confronto
    assert np.array_equal(arr, expected), f"Output diverso: {arr}"
