"""
🧪 تمرین NumPy – 01

یک آرایه‌ی 1بعدی از اعداد 0 تا 20 بساز و فقط اعداد زوج را استخراج کن.
"""

import numpy as np


def even_1d_array(start: int = 0, stop: int = 21, step: int = 1):
    my_array = np.arange(start, stop, step)
    return my_array[my_array % 2 == 0]
