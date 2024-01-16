#!/usr/bin/env python3
"""
2-measure_runtime.py
"""
import asyncio
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
    measure_runtime should measure the total runtime,
    and return it.
    """
    s_time = asyncio.get_event_loop().time()

    await asyncio.gather(
        async_comprehension(),
        async_comprehension(),
        async_comprehension(),
        async_comprehension()
    )

    e_time = asyncio.get_event_loop().time()

    return e_time - s_time
