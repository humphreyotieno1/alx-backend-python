#!/usr/bin/env python3
'''Return the number of tasks in the list'''

import asyncio
from typing import List

task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    '''Return the number of tasks in the list'''
    delays = []
    tasks = []

    for _ in range(n):
        task = task_wait_random(max_delay)
        tasks.append(task)

    for task in tasks:
        await task
        delays.append(task.result())

    return sorted(delays)
