from collections.abc import Callable
import math

from hypothesis import given, strategies as st
import pytest

from whyfp.differentiation import differentiate, easy_diff, within_diff, within_diff_4
from whyfp.util import fastest, improve, within


@pytest.mark.parametrize(
    ('func', 'x', 'h', 'expected'),
    [
        (lambda x: x, 0, -0.5, 1),
        (lambda x: -3.5 * x, 0, 0.01, -3.5),
        (lambda x: 0.9 * x, 0, 50, 0.9),
        (lambda x: x**2, 0, 4, 16 / 4),
        (lambda x: x**2, 3, 4, (49 - 9) / 4),
    ],
)
def test_easy_diff(func: Callable[[float], float], x: float, h: float, expected: float):
    assert math.isclose(easy_diff(func, x, h), expected)


@given(
    st.floats(min_value=-20, max_value=20),
    st.floats(min_value=-2, max_value=2).filter(lambda x: abs(x) > 1e-6),
)
@pytest.mark.parametrize('func', [lambda x: 2.5 * x**2, math.exp, math.sin])
def test_differentiate(func: Callable[[float], float], x: float, h0: float):
    derivatives = differentiate(func, x, h0)
    h = h0
    for _ in range(10):
        assert easy_diff(func, x, h) == next(derivatives)
        h /= 2


@given(
    st.floats(min_value=-20, max_value=20),
    st.floats(min_value=1e-4, max_value=1e-1),
    st.floats(min_value=-2, max_value=2).filter(lambda x: abs(x) > 1e-2),
)
@pytest.mark.parametrize('func', [lambda x: (2.5 * x**2 - x) / math.sqrt(1 + abs(x)), math.sin])
def test_within_diff_4(func: Callable[[float], float], x: float, tol: float, h0: float):
    derivatives = improve(improve(improve(differentiate(func, x, h0))))
    assert within_diff_4(func, x, tol, h0) == next(within(derivatives, tol))


@given(
    st.floats(min_value=-20, max_value=20),
    st.floats(min_value=1e-4, max_value=1e-1),
    st.floats(min_value=-2, max_value=2).filter(lambda x: abs(x) > 1e-2),
)
@pytest.mark.parametrize('func', [lambda x: (2.5 * x**2 - x) / math.sqrt(1 + abs(x)), math.cos])
def test_within_diff(func: Callable[[float], float], x: float, tol: float, h0: float):
    derivatives = fastest(differentiate(func, x, h0))
    assert within_diff(func, x, tol, h0) == next(within(derivatives, tol))
