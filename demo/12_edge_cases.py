"""Edge cases: tiny functions, decorators, lambdas, one-liners."""

def double(x):
    return x * 2


def triple(x):
    return x * 3


def noop():
    pass


def empty():
    pass


adder = lambda a, b: a + b
multiplier = lambda a, b: a * b
