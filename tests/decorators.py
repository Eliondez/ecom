import functools
import time
import numpy as np
from random import random


def timer(func):
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        runtime = time.perf_counter() - start
        print(f"{func.__name__} took {runtime:.4f} secs")
        return result
    return _wrapper


@timer
def complex_calculation1():
    res = [random() for i in range(1000 * 100 * 100)]
    res = sum(res)
    return res


@timer
def complex_calculation2():
    res = np.random.rand(1000 * 100 * 100)
    res = res.sum()
    return res


print(complex_calculation1())
print(complex_calculation2())
