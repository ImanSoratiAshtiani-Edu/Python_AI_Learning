import numpy as np


def random_arrays_ops(size: int = 10, seed: int | None = None):
    if seed is not None:
        np.random.seed(seed)
    a = np.random.randint(size)
    b = np.random.randint(size)

    sub_ab = a - b
    sum_ab = a + b
    mul_ab = a * b

    return a, b, sub_ab, sum_ab, mul_ab
