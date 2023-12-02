from collections.abc import Callable
import math
import statistics

from hypothesis import given, strategies as st
import pytest

from whyfp.integration import easy_integrate, pi_approxs
from whyfp.util import second


@given(
    st.tuples(
        st.floats(min_value=-100, max_value=100),
        st.floats(min_value=-100, max_value=100),
    ).filter(lambda pair: pair[1] > pair[0]),
)
@pytest.mark.parametrize('func', [lambda x: 2.5 * x**2, math.exp, math.sin])
def test_easy_integrate(func: Callable[[float], float], xs: tuple[float, float]):
    a, b = xs
    expected = statistics.mean(map(func, [a, b])) * (b - a)
    assert math.isclose(easy_integrate(func, a, b), expected)


def test_integrate():
    pass


def test_pi_approxs():
    pi = second(pi_approxs())
    assert math.isclose(pi, math.pi, abs_tol=1e-5)


def test_within_integrate():
    pass
