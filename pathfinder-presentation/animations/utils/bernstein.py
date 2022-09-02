from typing import Callable


def factorial(n: int) -> int:
    return 1 if n <= 1 else n * factorial(n - 1)


def binomial_coefficient(n: int, k: int) -> int:
    if k < 0 or k > n:  # "outside" Pascal's triangle
        return 0
    else:
        return int(factorial(n) / (factorial(k) * factorial(n - k)))


def get_bernstein(n: int, i: int) -> Callable[[float], int]:
    return lambda t: binomial_coefficient(n, i) * (t ** i) * (1 - t) ** (n - i)


def get_bernstein_derivative(n: int, i: int) -> Callable[[float], int]:
    return lambda t: n * (get_bernstein(n - 1, i - 1)(t) - get_bernstein(n - 1, i)(t))
