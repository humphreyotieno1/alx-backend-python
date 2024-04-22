#!/usr/bin/env python3
'''Coroutine that spawns an asynchronous coroutine'''

import asyncio
from typing import List
from random import randint
from time import sleep


wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    '''Asynchronous coroutine that spawns wait_random n times with max_delay'''
    delays = []
    tasks = []

    for _ in range(n):
        delay = randint(0, max_delay)
        task = asyncio.create_task(wait_random(delay))
        tasks.append(task)

    for task in tasks:
        await task
        delays.append(task.result())

    return sorted(delays)
