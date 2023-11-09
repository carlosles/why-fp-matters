import math

from hypothesis import given, strategies as st

from whyfp.sqrt import next_sqrt_approx


@given(
    st.floats(allow_infinity=False, allow_nan=False),
    st.floats(min_value=0, exclude_min=True, allow_infinity=False, allow_nan=False),
)
def test_next_sqrt_approx(num: float, prev_approx: float):
    next_approx = next_sqrt_approx(num, prev_approx)
    expected = (prev_approx + num / prev_approx) / 2
    assert math.isclose(next_approx, expected)
