from collections.abc import Iterable
import math

from hypothesis import given, strategies as st
from more_itertools import iequals, take

from whyfp.sqrt import next_sqrt_approx, relative_sqrt, sqrt_approxs, within_sqrt


@given(
    st.floats(allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, exclude_min=True, allow_infinity=False, allow_nan=False),
)
def test_next_sqrt_approx(num: float, prev_approx: float):
    next_approx = next_sqrt_approx(num, prev_approx)
    expected = (prev_approx + num / prev_approx) / 2
    assert math.isclose(next_approx, expected)


@given(
    st.floats(min_value=0, exclude_min=True, allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, exclude_min=True, allow_infinity=False, allow_nan=False),
)
def test_sqrt_approxs(num: float, initial: float):
    def func(num: float, initial: float) -> Iterable[float]:
        while True:
            yield initial
            initial = next_sqrt_approx(num, initial)

    expected = func(num, initial)
    assert iequals(take(10, sqrt_approxs(num, initial)), take(10, expected))


@given(
    st.floats(min_value=0, exclude_min=True, max_value=1e6),
    st.floats(min_value=1e-8, max_value=2.0),
)
def test_within_sqrt(num: float, tol: float):
    expected = math.sqrt(num)
    assert math.isclose(within_sqrt(num, tol, initial=num), expected, abs_tol=tol, rel_tol=0)


@given(
    st.floats(min_value=0, exclude_min=True, allow_infinity=False, allow_nan=False),
    st.floats(min_value=1e-8, max_value=1e-1),
)
def test_relative_sqrt(num: float, tol: float):
    expected = math.sqrt(num)
    assert math.isclose(relative_sqrt(num, tol, initial=num), expected, abs_tol=0, rel_tol=tol)
