"""Algorithm for numerical differentiation of real-valued functions."""
from collections.abc import Callable, Iterable
from functools import partial
from itertools import starmap
from operator import add, mul

from more_itertools import first

from whyfp.util import fastest, improve, within


def within_integrate(func: Callable[[float], float], a: float, b: float, tol: float) -> float:
    """Return integral of `func` between [`a`, `b`] with tolerance `tol` using the fastest scheme."""
    return first(within(fastest(integrate(func, a, b)), tol))


def pi_approxs() -> Iterable[float]:
    """Yield sequence of approximations for number π (pi) using eighth-order scheme.

    Note: the second approximation is already correct to five decimal places.
    """

    def pi_over_4(x: float) -> float:
        return 1 / (1 + x**2)

    return map(partial(mul, 4), improve(integrate(pi_over_4, 0, 1)))


def integrate(func: Callable[[float], float], a: float, b: float) -> Iterable[float]:
    """Yield progressively better estimates for the integral of `func` between `a` and `b`."""

    def integ(f: Callable[[float], float], a: float, b: float, fa: float, fb: float) -> Iterable[float]:
        yield (fa + fb) * (b - a) / 2
        mid = (a + b) / 2
        fmid = f(mid)
        half1 = integ(f, a, mid, fa, fmid)
        half2 = integ(f, mid, b, fmid, fb)
        yield from starmap(add, zip(half1, half2, strict=True))

    return integ(func, a, b, func(a), func(b))


def easy_integrate(func: Callable[[float], float], a: float, b: float) -> float:
    """Return the straight line slope of function `func` between points  `x` and `x+h`."""
    pass
