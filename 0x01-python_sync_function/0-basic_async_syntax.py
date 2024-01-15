#!/usr/bin/env python3
"""
0-basic_async_syntax.py
"""
import random
import asyncio


async def wait_random(max_delay: int = 10) -> float:
    """
    Write an asynchronous coroutine that take in an int.
    """
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
