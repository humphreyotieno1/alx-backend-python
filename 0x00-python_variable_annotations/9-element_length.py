#!/usr/bin/env python3
'''Annotating function'''
from typing import List, Tuple, Iterable, Sequence


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    '''Returns a list of tuples containing elements and their lengths'''
    return [(i, len(i)) for i in lst]
