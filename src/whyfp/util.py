"""Utilities shared between various modules."""
from collections.abc import Callable, Iterable
from itertools import islice, pairwise
import math
from typing import TypeVar, cast

from more_itertools import nth

T = TypeVar('T')


def repeat_fn(func: Callable[[T], T], value: T) -> Iterable[T]:
    """Repeat function application recursively and indefinitely."""
    yield value
    yield from repeat_fn(func, func(value))


def within(values: Iterable[float], tol: float) -> Iterable[float]:
    """Yield values that differ by no more than tolerance ``tol`` between successive values."""
    return (y for x, y in pairwise(values) if abs(x - y) <= tol)


def relative(values: Iterable[float], tol: float) -> Iterable[float]:
    """Yield values that differ by no more than relative tolerance ``tol`` between successive values."""
    return (y for x, y in pairwise(values) if abs(x / y - 1) <= tol)


def fastest(values: Iterable[float]) -> Iterable[float]:
    """Yield sequence of approximations computed using a progressively higher order scheme."""
    return map(second, repeat_fn(improve, values))


def improve(values: Iterable[float]) -> Iterable[float]:
    """Yield improved sequence of approximations."""
    return elim_error(order(values), values)


def order(values: Iterable[float]) -> int:
    """Return estimate of power exponent that characterizes sequence of approximations."""
    a, b, c = islice(values, 3)
    try:
        rate = (a - c) / (b - c) - 1
        return round(math.log2(rate))
    except (ZeroDivisionError, ValueError):
        return 1


def elim_error(n: int, values: Iterable[float]) -> Iterable[float]:
    """Yield values with error terms eliminated from the sequence of successive approximations."""
    return ((b * 2**n - a) / (2**n - 1) for a, b in pairwise(values))


def second(values: Iterable[T]) -> T:
    """Return second item from sequence of values."""
    return cast(T, nth(values, 1))
