# tests/test_ex06.py
from __future__ import annotations

import numpy as np

from l0_s3_1.ex06 import ex06


def test_ex06() -> None:
    a, r, ravel_reflects, b, c, v_stacked, h_stacked, d, v_splits = ex06()

    # 1) reshape درست است
    assert a.shape == (4, 4)

    expected = np.arange(16).reshape(4, 4)
    expected[0, 0] = 16
    np.testing.assert_array_equal(a, expected)
    # چون یک خانه را به 16 تغییر دادیم:
    assert a[0, 0] == 16

    # 2) ravel یک view است → باید تغییر را منعکس کند
    assert ravel_reflects
    assert r[0] == 16

    # 3) ابعاد و منطق vstack/hstack
    assert b.shape == (2, 2) and c.shape == (2, 2)
    np.testing.assert_array_equal(v_stacked[:2], b)
    np.testing.assert_array_equal(v_stacked[2:], c)
    np.testing.assert_array_equal(h_stacked[:, :2], b)
    np.testing.assert_array_equal(h_stacked[:, 2:], c)

    # 4) vsplit سه قطعهٔ 2×6 می‌دهد و با d سازگار است
    assert len(v_splits) == 3
    assert all(x.shape == (2, 6) for x in v_splits)
    np.testing.assert_array_equal(np.vstack(v_splits), d)
