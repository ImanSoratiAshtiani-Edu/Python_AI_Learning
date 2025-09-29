import numpy as np

from l0_s3_1.ex16 import ex16


def test_ex16_shapes_and_orders():
    arr_c, strides_c, arr_f, strides_f = ex16()

    # basic shapes
    assert arr_c.shape == (3, 4)
    assert arr_f.shape == (3, 4)

    # memory order checks
    assert not np.isfortran(arr_c), "arr_c should be C-order"
    assert np.isfortran(arr_f), "arr_f should be Fortran-order"

    # content checks
    assert np.array_equal(arr_c, np.arange(10, 22, dtype=np.int32).reshape(3, 4, order="C"))
    assert np.array_equal(arr_f, np.arange(10, 22).reshape(3, 4, order="F"))

    # stride checks computed dynamically from dtype.itemsize
    item_c = arr_c.dtype.itemsize
    item_f = arr_f.dtype.itemsize

    expected_c = (4 * item_c, 1 * item_c)  # (cols*item, item)
    expected_f = (1 * item_f, 3 * item_f)  # (item, rows*item)

    assert strides_c == expected_c, f"C-order strides should be {expected_c}, got {strides_c}"
    assert strides_f == expected_f, f"F-order strides should be {expected_f}, got {strides_f}"
