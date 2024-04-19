#!/usr/bin/env python3
'''Typevar annotation - functions'''
from typing import TypeVar, Union, Any, Mapping


T = TypeVar('T')


def safely_get_value(dct: Mapping[Any, T], key: Any, default: Union[T, None] = None) -> Union[T, Any]:
    '''Return value of a key in a dictionary or default'''
    if key in dct:
        return dct[key]
    else:
        return default
