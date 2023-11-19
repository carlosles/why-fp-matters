from collections.abc import Iterator
from functools import partial
from itertools import accumulate, compress, islice, repeat, tee
import math
from operator import add, truediv

from hypothesis import given, strategies as st
from more_itertools import difference, iequals
import pytest

from whyfp.differentiation import differentiate
from whyfp.sqrt import sqrt_approxs
from whyfp.util import elim_error, fastest, improve, order, relative, repeat_fn, second, within


@given(st.integers())
def test_repeat_func(initial: int):
    to_add = 5
    expected = accumulate(repeat(to_add), func=add, initial=initial)
    series = repeat_fn(partial(add, to_add), initial)
    assert all(x == y for x, y in islice(zip(series, expected, strict=True), 100))


@given(st.lists(st.floats()), st.floats(min_value=0))
def test_within(values: list[float], tolerance: float):
    is_within = (ii > 0 and abs(d) <= tolerance for ii, d in enumerate(difference(values)))
    expected = compress(values, is_within)
    assert iequals(within(iter(values), tolerance), expected)


@given(st.lists(st.floats(min_value=0.1, max_value=1000, exclude_min=True)), st.floats(min_value=0))
def test_relative(values: list[float], tol: float):
    is_within = (ii > 0 and abs(1 / d - 1) <= tol for ii, d in enumerate(difference(values, truediv)))
    expected = compress(values, is_within)
    assert iequals(relative(iter(values), tol), expected)


@given(st.lists(st.integers(), min_size=2))
def test_second(values: list[float]):
    _, x, *_ = values
    assert second(iter(values)) == x


@given(st.lists(st.floats(allow_infinity=False, allow_nan=False)), st.integers(min_value=1, max_value=5))
def test_elim_error(values: list[float], n: int):
    pairs = zip(values[:-1], values[1:], strict=True)
    for x, (a, b) in zip(elim_error(n, values), pairs, strict=True):
        expected = (b * 2**n - a) / (2**n - 1)
        assert math.isclose(x, expected)


@pytest.mark.parametrize(
    ('values', 'expected'),
    [([1, 2, 2.5, 2.75, 2.875], 1), ([1, 5, 6, 6.25, 6.3125], 2)],
)
def test_order(values: list[float], expected: int):
    assert order(values) == expected


@pytest.mark.parametrize(
    ('values', 'expected'),
    [
        ([1, 2, 2.5, 2.75, 2.875], [3.0] * 4),
        ([1, 5, 6, 6.25, 6.3125], [6.3333333333333] * 4),
    ],
)
def test_improve(values: list[float], expected: list[float]):
    assert all(math.isclose(x, y) for x, y in zip(improve(values), expected, strict=True))


@pytest.mark.parametrize(
    'values', [sqrt_approxs(35.0, 35.0), differentiate(lambda x: 5 + x**2 - x**3 / 10, x=0, h0=25.0)]
)
def test_fastest(values: Iterator[float]):
    values, values_copy = tee(values)
    fastest_values = iter(fastest(values_copy))
    for _ in range(10):
        assert second(values) == next(fastest_values)
        values = improve(values)
