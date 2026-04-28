# mypy: disable-error-code="assignment,attr-defined"
'''Compatibility shims for older Python versions.'''
import sys as s, typing as t
from functools import partial
__all__ = 'LifoQueue', 'Placeholder', 'PriorityQueue', 'Queue', 'QueueEmpty', 'QueueFull', 'QueueShutDown', 'heapify', 'heappop', 'heappush', 'heappushpop', 'heapreplace', 'pargs', 'partial'
if s.version_info >= (3, 14): from functools import Placeholder; pargs: dict[str, t.Any]; from heapq import heapify_max as heapify, heappop_max as heappop, heappush_max as heappush, heappushpop_max as heappushpop, heapreplace_max as heapreplace
else: from .py313 import *
if s.version_info >= (3, 13): from asyncio.queues import *
else: from .py312 import *