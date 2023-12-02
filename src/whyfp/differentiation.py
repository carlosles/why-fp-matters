"""Algorithm for numerical differentiation of real-valued functions."""
from collections.abc import Callable, Iterable
from functools import partial
from operator import mul

from more_itertools import first

from whyfp.util import fastest, improve, repeat_fn, within

__all__ = ['within_diff', 'within_diff_4', 'differentiate', 'easy_diff']


def within_diff(func: Callable[[float], float], x: float, tol: float, h0: float) -> float:
    """Return derivative of `func` at `x` within absolute tolerance `tol` using the fastest scheme."""
    return first(within(fastest(differentiate(func, x, h0)), tol))


def within_diff_4(func: Callable[[float], float], x: float, tol: float, h0: float) -> float:
    """Return derivative of `func` at `x` within absolute tolerance `tol` using 4th-order scheme."""
    return first(within(improve(improve(improve(differentiate(func, x, h0)))), tol))


def differentiate(func: Callable[[float], float], x: float, h0: float) -> Iterable[float]:
    """Yield estimates for derivative of `func` at `x` using progressively smaller `h0`."""
    halve = partial(mul, 0.5)
    return map(partial(easy_diff, func, x), repeat_fn(halve, h0))


def easy_diff(func: Callable[[float], float], x: float, h: float) -> float:
    """Return the straight line slope of function `func` between points  `x` and `x+h`."""
    return (func(x + h) - func(x)) / h
