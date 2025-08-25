import numpy as np


def ex04():
    # arr = np.ones((4,4),dtype=np.int32)*np.array( [9])
    arr = np.full(
        (
            4,
            4,
        ),
        9,
        dtype=np.int64,
    )
    arr2 = np.linspace(0, 1, 20, endpoint=False)
    arr3 = np.array([1, 2, 3, 4], dtype=np.int64)

    arr4 = arr3.astype(np.float64)
    np.random.seed(42)
    arr5 = np.random.randint(0, 10, size=(3, 5), dtype=np.int64)

    return arr, arr2, arr3, arr4, arr5, arr5.shape, arr5.size, arr5.ndim, arr5.dtype, arr5.itemsize


print(*ex04(), sep="\n")
# print("\n".join(map(str, ex04())))
