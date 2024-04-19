#!/usr/bin/env python3
'''Complex types - functions'''
from typing import Sequence, Any, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    '''Return first element of a sequence or None if empty'''
    if lst:
        return lst[0]
    else:
        return None
