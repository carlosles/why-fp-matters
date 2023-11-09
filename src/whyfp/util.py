"""Utilities shared between various modules."""
from collections.abc import Callable, Iterable
from typing import Any


def repeat_fn(func: Callable[[Any], Any], value: Any) -> Iterable[Any]:
    """Repeat function application recursively and indefinitely."""
    yield value
    yield from repeat_fn(func, func(value))
