#!/usr/bin/env python3
"""
101-safely_get_value.py
"""
from typing import TypeVar, Mapping, Any, Union, Optional

T = TypeVar('T')


def safely_get_value(
    dct: Mapping,
    key: Any,
    default: Optional[T] = None
) -> Union[Any, T]:
    """
    Given the parameters and the return values,
    add type annotations to the function.
    """
    if key in dct[key]:
        return dct[key]
    else:
        return default
