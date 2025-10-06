import random

def generate_numeric_list(size=10, lower_bound=-100, upper_bound=100):
    return [random.randint(lower_bound, upper_bound) for _ in range(size)]


def max_min_v1(numeric_list):
    if not numeric_list:
        return None, None

    max_value = numeric_list[0]
    min_value = numeric_list[0]

    for num in numeric_list:
        if num > max_value:
            max_value = num
        if num < min_value:
            min_value = num

    return max_value, min_value

def max_min_v2(numeric_list):
    max_value= None
    min_value = None

    for num in numeric_list:
        if max_value is None or num > max_value:
            max_value = num
        if min_value is None or num < min_value:
            min_value = num

    return max_value, min_value

def ex01():
    if __name__=="__main__":
        numeric_list = generate_numeric_list()
        print("Generated List:", numeric_list)

        max_v1, min_v1 = max_min_v1(numeric_list)
        print("Version 1 - Max:", max_v1, "Min:", min_v1)

        max_v2, min_v2 = max_min_v2(numeric_list)
        print("Version 2 - Max:", max_v2, "Min:", min_v2)

ex01()

import timeit, sys
numeric_list = generate_numeric_list(-100, 100, 10)
print(f"max_min_v1: {timeit.timeit('max_min_v1(numeric_list)', globals=globals(), number=1):.9f}")
print(f"max_min_v2: {timeit.timeit('max_min_v2(numeric_list)', globals=globals(), number=1):.9f}")
print(f"size of the list: {sys.getsizeof(numeric_list)} bytes")
