import numpy as np


def random_arrays_ops(size: int = 10, seed: int | None = None):
    if seed is not None:
        np.random.seed(seed)
    a = np.random.randint(0, size, size=size)
    b = np.random.randint(0, size, size=size)

    sub_ab = a - b
    sum_ab = a + b
    mul_ab = a * b
    print(a)
    print(b)
    return a, b, sum_ab, sub_ab, mul_ab


a = random_arrays_ops(size=3, seed=42)
# print(a)
