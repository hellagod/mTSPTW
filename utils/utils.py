import time
from random import randint

def timing(fun, *arg, **kwargs):
    s = time.time()
    res = fun(*arg, **kwargs)
    f = time.time()
    return f-s, res

def generate_pair(a, b):
    while True:
        number = randint(a, b)
        yield number
        yield number


def create_test_data(n, m):
    gen = generate_pair(1, 50)
    delta = randint(1, 35)
    data = {
        'n': n,
        'm': m,
        'costs': {(i, j): randint(1, 100) for i in range(n + 1) for j in range(n + 1) if i != j},
        'times': [[randint(1, 100) if i != j else 0 for j in range(n + 1)] for i in range(n + 1)],
    }
    data['time_windows'] = [None,
                            *[(data['times'][0][i + 1] + next(gen), data['times'][0][i + 1] + next(gen) + delta)
                              for i in range(n)]]
    data['big_M'] = sum(map(sum, data['time_windows'][1:]))
    return data
