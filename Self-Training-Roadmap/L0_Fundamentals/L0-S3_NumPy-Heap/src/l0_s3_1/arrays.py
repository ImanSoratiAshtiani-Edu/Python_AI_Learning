from __future__ import annotations

import numpy as np
import numpy.typing as npt


def even_numbers(n: int) -> npt.NDArray[np.int_]:
    """اعداد زوج 0..n-1 را به صورت آرایه NumPy برمی‌گرداند."""
    a: npt.NDArray[np.int_] = np.arange(n, dtype=np.int_)
    return a[a % 2 == 0]
