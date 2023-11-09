"""Newton-Raphson square root finding algorithm for nonnegative real numbers."""
from collections.abc import Iterable
from functools import partial

from whyfp.util import repeat_fn


def relative_sqrt(num: float, eps: float, initial: float) -> float:
    """Return first Newton-Raphson square root estimate of ``num`` within ratio ``eps``."""
    pass


def within_sqrt(num: float, eps: float, initial: float) -> float:
    """Return first Newton-Raphson square root estimate of ``num`` within tolerance ``eps``."""
    pass


def sqrt_approxs(num: float, initial: float) -> Iterable[float]:
    """Return Newton-Raphson square root approximations of ``num`` following ``initial`` estimate."""
    return repeat_fn(partial(next_sqrt_approx, num=num), initial)


def next_sqrt_approx(num: float, prev: float) -> float:
    """Return Newton-Raphson square root approximation following ``prev``."""
    return (prev + num / prev) / 2
