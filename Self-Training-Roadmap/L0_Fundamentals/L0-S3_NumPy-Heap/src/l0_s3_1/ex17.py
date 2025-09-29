import math
from typing import List, Tuple

import numpy as np


def ex17_array_prep() -> (
    Tuple[Tuple[int, np.ndarray, np.ndarray], Tuple[int, List[float], List[float]]]
):
    arr4x5 = np.arange(20, dtype=np.int32).reshape(4, -1, order="C")
    print("Array:\n", arr4x5)
    method = ex17_methodBased(arr4x5)
    loop = ex17_loopBased(arr4x5)
    return method, loop


def ex17_methodBased(arr4x5: np.ndarray) -> Tuple[int, np.ndarray, np.ndarray]:
    total_sum: int = int(arr4x5.sum())
    columns_mean: np.ndarray = arr4x5.mean(axis=0)
    rows_std: np.ndarray = arr4x5.std(axis=1)  # ddof=0 (population std) مثل پیش‌فرض NumPy
    return total_sum, columns_mean, rows_std


def ex17_loopBased(arr4x5: np.ndarray) -> Tuple[int, List[float], List[float]]:
    rows, cols = arr4x5.shape
    total: int = 0
    columns_sum: List[float] = [0.0] * cols
    rows_mean: List[float] = [0.0] * rows
    rows_std: List[float] = [0.0] * rows

    # جمع کل + جمع هر ستون + میانگین هر ردیف
    for r in range(rows):
        row_sum = 0
        for c in range(cols):
            val = int(arr4x5[r, c])
            total += val
            columns_sum[c] += val
            row_sum += val
        rows_mean[r] = row_sum / cols

    columns_mean: List[float] = [s / rows for s in columns_sum]

    # انحراف معیار هر ردیف (population std: ddof=0)
    for r in range(rows):
        mean_r = rows_mean[r]
        var = 0.0
        for c in range(cols):
            diff = float(arr4x5[r, c]) - mean_r
            var += diff * diff
        var /= cols
        rows_std[r] = math.sqrt(var)

    return total, columns_mean, rows_std


# --- quick verification ---
method, loop = ex17_array_prep()
print("\n--- Method-based ---")
print("Total sum:", method[0])
print("Columns mean:", method[1])
print("Rows std:", method[2])

print("\n--- Loop-based ---")
print("Total sum:", loop[0])
print("Columns mean:", loop[1])
print("Rows std:", loop[2])

# تطبیق نتیجه‌ها
assert method[0] == loop[0]
assert np.allclose(method[1], loop[1])
assert np.allclose(method[2], loop[2])
print("\n✅ Loop-based matches NumPy method-based results.")
