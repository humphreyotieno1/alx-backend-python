#!/usr/bin/env python3
'''Define function to sum mixed list'''
from typing import List, Union


def sum_mixed_list(mxd_list: List[Union[int, float]]) -> float:
    '''Sum all elements in mxd_list'''
    return sum(mxd_list)
