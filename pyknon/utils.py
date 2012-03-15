import itertools


def flatten(iterable):
    return list(itertools.chain.from_iterable(iterable))


def fibonacci(n):
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)
        a, b = b, a + b
    return result


# http://blog.yjl.im/2011/01/generating-pascals-triangle-using.html
def pascals_triangle(n):
    x = [1]
    yield x
    for i in range(n - 1):
        x = [sum(i) for i in zip([0] + x, x + [0])]
        yield x
