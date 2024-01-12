#!/usr/bin/env python3
"""
100-safely_fist_element.py
"""
from typing import Sequence, Any, Union, Optional


def safe_first_element(lst: Sequence[Any]) -> Optional[Any]:
    """
    Augment the following code with the correct duck-typed annotations.
    """
    if lst:
        return lst[0]
    else:
        return None
