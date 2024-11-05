from random import randint


def generate_pair(a,b):
    while True:
        number = randint(a,b)
        yield number
        yield number
