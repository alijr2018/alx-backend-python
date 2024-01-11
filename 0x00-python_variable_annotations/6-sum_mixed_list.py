#!/usr/bin/env python3
"""
6-sum_mixed_list.py
"""

from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """
    Write a type-annotated function sum_mixed_list which,
    takes a list mxd_lst of integers and floats and,
    returns their sum as a float.
    """
    return sum(mxd_lst)
