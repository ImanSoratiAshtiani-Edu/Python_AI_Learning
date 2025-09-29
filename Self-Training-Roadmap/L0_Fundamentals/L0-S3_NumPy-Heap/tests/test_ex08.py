from l0_s3_1.ex08 import ex08


def test_ex08_basic():
    arr, a, r, f = ex08()
    # a must be 4x5 with a[0,0] mutated to 99
    assert a.shape == (4, 5)
    assert a[0, 0] == 99
    # ravel result should reflect the mutation (view)
    assert r[0] == 99
    # flatten result should be independent (copy)
    assert f[0] == 0


def test_ex08_identity_and_lengths():
    arr, a, r, f = ex08()
    # r shares memory with a (usually True in this construction)
    assert r.base is a or r.base is not None
    # lengths should match total elements
    assert r.size == a.size == 20
    assert f.size == 20
