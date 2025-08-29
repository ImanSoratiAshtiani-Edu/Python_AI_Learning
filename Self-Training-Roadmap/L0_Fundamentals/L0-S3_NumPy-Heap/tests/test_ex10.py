from l0_s3_1.ex10 import ex10


def test_ex10_views_reflect_mutation():
    a, y, z = ex10()
    # After setting a[0,0,0] = 99 inside ex10,
    # both reshaped views should reflect the change at their corresponding positions
    assert y[0] == 99
    assert z[0, 0] == 99


def test_ex10_shapes_and_sizes():
    a, y, z = ex10()
    assert a.shape == (2, 3, 2)
    assert y.shape == (12,)
    assert z.shape == (3, 4)
    # sizes must be equal
    assert a.size == y.size == z.size == 12
