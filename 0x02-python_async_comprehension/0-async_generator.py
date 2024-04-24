#!/usr/bin/env python3
'''Asynchronous generator'''

import asyncio
import random
import typing


async def async_generator() -> None: # type: ignore
    '''Asynchronous generator that yields a random number'''
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
