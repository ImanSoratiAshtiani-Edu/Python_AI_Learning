from l0_s3_1.ex11 import ex11


def ex12():
    arr = ex11()[0]
    std_a = arr.std()
    max_0 = arr.max(axis=0)
    max_index_a = arr.argmax()

    # print(arr)
    # print(std_a)
    # print(max_0)
    # print(max_index_a)
    return arr, std_a, max_0, max_index_a
