from functools import partial
from itertools import accumulate, islice, repeat
from operator import add

from hypothesis import given, strategies as st

from whyfp.util import repeat_fn


@given(st.integers())
def test_repeat_func(initial: int):
    to_add = 5
    expected = accumulate(repeat(to_add), func=add, initial=initial)
    series = repeat_fn(partial(add, to_add), initial)
    assert all(x == y for x, y in islice(zip(series, expected, strict=True), 100))
