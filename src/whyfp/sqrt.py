"""Newton-Raphson square root finding algorithm for nonnegative real numbers."""
from collections.abc import Iterable
from functools import partial

from more_itertools import first

from whyfp.util import relative, repeat_fn, within


def relative_sqrt(num: float, tol: float, initial: float) -> float:
    """Return first Newton-Raphson square root estimate of ``num`` within relative tolerance ``tol``."""
    return first(relative(sqrt_approxs(num, initial), tol))


def within_sqrt(num: float, tol: float, initial: float) -> float:
    """Return first Newton-Raphson square root estimate of ``num`` within absolute tolerance ``tol``."""
    return first(within(sqrt_approxs(num, initial), tol))


def sqrt_approxs(num: float, initial: float) -> Iterable[float]:
    """Return Newton-Raphson square root approximations of ``num`` following ``initial`` estimate."""
    return repeat_fn(partial(next_sqrt_approx, num), initial)


def next_sqrt_approx(num: float, prev: float) -> float:
    """Return Newton-Raphson square root approximation following ``prev``."""
    return (prev + num / prev) / 2
