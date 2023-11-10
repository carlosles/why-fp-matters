from functools import partial
from itertools import accumulate, compress, islice, repeat
from operator import add, truediv

from hypothesis import given, strategies as st
from more_itertools import difference, iequals

from whyfp.util import relative, repeat_fn, within


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
