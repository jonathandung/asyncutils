# type: ignore
'''Compatibility shims for older Python versions.'''
import sys as s, typing as t
from functools import partial
__all__ = 'LifoQueue', 'Placeholder', 'PriorityQueue', 'Queue', 'QueueEmpty', 'QueueFull', 'QueueShutDown', 'pargs', 'partial'
if s.version_info >= (3, 14): from functools import Placeholder
else: Placeholder: t.Final[object]
if s.version_info >= (3, 13): from asyncio.queues import Queue, QueueEmpty, QueueFull, QueueShutDown, LifoQueue, PriorityQueue
else: from .py312 import * # noqa: F403
pargs: dict[str, t.Any]