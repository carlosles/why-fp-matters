from collections.abc import Callable
import math
import statistics

from hypothesis import given, strategies as st
import pytest

from whyfp.integration import easy_integrate, integrate, pi_approxs, within_integrate
from whyfp.util import fastest, second, within


@given(
    st.tuples(
        st.floats(min_value=-100, max_value=100),
        st.floats(min_value=-100, max_value=100),
    ).filter(lambda pair: pair[1] >= pair[0]),
)
@pytest.mark.parametrize('func', [lambda x: 2.5 * x**2, math.exp, math.sin])
def test_easy_integrate(func: Callable[[float], float], bounds: tuple[float, float]):
    a, b = bounds
    expected = statistics.mean(map(func, [a, b])) * (b - a)
    assert math.isclose(easy_integrate(func, a, b), expected)


@pytest.mark.parametrize(
    ('func', 'a', 'b', 'expected'),
    [
        (lambda _: 5, -3, 7, 5 * 10),  # rectangle
        (lambda x: 5 - x, 0, 5, 5 * 5 / 2),  # triangle
        (lambda x: math.sqrt(1 - x**2), -1, 1, math.pi / 2),  # semicircle
        (lambda x: x**2, 0, 1, 1 / 3),
        (math.sqrt, 0, 1, 2 / 3),
        (math.sin, 0, math.pi, 2),
        (lambda x: 1 / (1 + x**2), 0, 1, math.pi / 4),
    ],
)
def test_integrate(func: Callable[[float], float], a: float, b: float, expected: float):
    integrals = integrate(func, a, b)
    prev_error = math.inf
    for _ in range(10):
        error = abs(next(integrals) - expected)
        assert error <= prev_error
        prev_error = error
    assert math.isclose(next(integrals), expected, abs_tol=1e-4)


def test_pi_approxs():
    pi = second(pi_approxs())
    assert math.isclose(pi, math.pi, abs_tol=1e-5)


@pytest.mark.parametrize('bounds', [(0, 1), (0, 15), (-2, 2), (-10, -3.5)])
@pytest.mark.parametrize('tol', [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8])
@pytest.mark.parametrize('func', [lambda x: (2.5 * x**2 - x) / math.sqrt(1 + abs(x))])
def test_within_integrate(func: Callable[[float], float], tol: float, bounds: tuple[float, float]):
    a, b = bounds
    integrals = fastest(integrate(func, a, b))
    assert within_integrate(func, a, b, tol) == next(within(integrals, tol))
