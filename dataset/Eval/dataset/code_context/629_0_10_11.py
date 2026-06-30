# -*- coding: utf-8 -*-
from functools import lru_cache, wraps
from typing import Callable, TypeVar

T = TypeVar("T")


def use_once(func: Callable[..., T]) -> Callable[..., T]:
    @lru_cache(maxsize=1)

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
