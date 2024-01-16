#!/usr/bin/env python3
"""
0-async_generator.py
"""
import asyncio
import random
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    """
    Write a coroutine called async_generator,
    that takes no arguments.
    """
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
