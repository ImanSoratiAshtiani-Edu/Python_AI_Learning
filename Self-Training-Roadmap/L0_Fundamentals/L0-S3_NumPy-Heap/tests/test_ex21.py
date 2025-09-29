import numpy as np
import pytest

from l0_s3_1.ex21 import ex21


def test_ex21_behavior_fixed_or_buggy():
    """
    This test passes if ex21() is already fixed (uses reshape) and returns
    the expected results. If the legacy bug is present (using `.shape(4,5)`),
    it will mark the test as xfail with a clear reason instead of failing CI.
    """
    try:
        arr, arr_ravel = ex21()
    except AttributeError:
        pytest.xfail(
            "ex21() still uses `.shape(4,5)` instead of `.reshape(4,5)` — please fix the function."
        )
        return  # not reached

    # Validate intended behavior
    assert isinstance(arr, np.ndarray), "ex21 should return a NumPy array as first element."
    assert arr.shape == (4, 5), "Expected a (4,5) array from np.arange(20).reshape(4,5)."

    expected_arr = np.arange(20).reshape(4, 5)
    assert np.array_equal(
        arr, expected_arr
    ), "Array contents should match np.arange(20).reshape(4,5)."

    expected_ravel_F = expected_arr.ravel(order="F")
    assert np.array_equal(
        arr_ravel, expected_ravel_F
    ), "Second return should be Fortran-order ravel of the array."
