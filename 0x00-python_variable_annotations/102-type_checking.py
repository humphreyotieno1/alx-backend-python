#!/usr/bin/env python3
'''Type checking'''
from typing import Tuple, List


def zoom_array(lst: Tuple[int, ...], factor: int = 2) -> Tuple[int, ...]:
    '''Type checking'''
    zoomed_in: Tuple[int, ...] = tuple(
        item for item in lst
        for _ in range(factor)
    )
    return zoomed_in


array: Tuple[int, int, int] = (12, 72, 91)

zoom_2x: Tuple[int, ...] = zoom_array(array)

zoom_3x: Tuple[int, ...] = zoom_array(array, 3)
