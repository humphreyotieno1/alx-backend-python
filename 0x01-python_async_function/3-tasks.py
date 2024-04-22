#!/usr/bin/env python3
'''Return asyncio.Task object'''

import asyncio
from random import uniform

wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    '''Return asyncio.Task object'''
    return asyncio.create_task(wait_random(max_delay))
