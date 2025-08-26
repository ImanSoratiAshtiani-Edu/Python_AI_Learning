# src/l0_s3_1/ex06.py
import numpy as np


def ex06():
    # 1) reshape
    a = np.arange(16).reshape(4, 4)

    # 2) ravel (view) و بررسی اتصال داده
    r = np.ravel(a)
    a[0, 0] = 16
    ravel_reflects = a[0, 0] == r[0]  # باید True باشد

    # 3) hstack / vstack روی دو آرایه 2×2
    rng = np.random.default_rng(0)  # RNG جدید و تکرارپذیر
    b = rng.integers(0, 6, size=(2, 2))
    c = rng.integers(0, 6, size=(2, 2))
    v_stacked = np.vstack((b, c))
    h_stacked = np.hstack((b, c))

    # 4) vsplit روی ماتریس 6×6
    d = rng.integers(0, 10, size=(6, 6))
    v_splits = np.vsplit(d, 3)  # tuple/لیست از سه زیرماتریس 2×6

    # همه را برگردان تا تست‌پذیر باشند
    return a, r, ravel_reflects, b, c, v_stacked, h_stacked, d, v_splits
