from l0_s3_1.ex08 import ex08


def ex09():
    a = ex08()[0].reshape(4, -1, order="F")
    a_r = a.ravel(order="F")
    print(a)
    print(a_r)
    return a, a_r


ex09()
