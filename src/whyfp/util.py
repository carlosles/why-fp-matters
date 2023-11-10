"""Utilities shared between various modules."""
from collections.abc import Callable, Iterable
from itertools import pairwise
from typing import Any


def repeat_fn(func: Callable[[Any], Any], value: Any) -> Iterable[Any]:
    """Repeat function application recursively and indefinitely."""
    yield value
    yield from repeat_fn(func, func(value))


def within(values: Iterable[float], tol: float) -> Iterable[float]:
    """Yield values that differ by no more than tolerance ``tol`` between successive values."""
    return (y for x, y in pairwise(values) if abs(x - y) <= tol)


def relative(values: Iterable[float], tol: float) -> Iterable[float]:
    """Yield values that differ by no more than relative tolerance ``tol`` between successive values."""
    return (y for x, y in pairwise(values) if abs(x / y - 1) <= tol)
