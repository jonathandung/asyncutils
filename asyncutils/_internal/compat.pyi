'''Compatibility shims for older Python versions.'''
from .types import SupportsRichComparison
import sys as s
from typing import Any
from functools import partial
__all__ = 'D', 'LifoQueue', 'Placeholder', 'PriorityQueue', 'Queue', 'QueueEmpty', 'QueueFull', 'QueueShutDown', 'heapify', 'heappop', 'heappush', 'heappushpop', 'heapreplace', 'j', 'partial'
D: dict[str, Any]
j: dict[str, Any]
if s.version_info >= (3, 14):
    from functools import Placeholder
    def heapify[C: SupportsRichComparison](heap: list[C], /) -> None: ...
    def heappop[C: SupportsRichComparison](heap: list[C], /) -> C: ...
    def heappush[C: SupportsRichComparison](heap: list[C], item: C, /) -> None: ...
    def heappushpop[C: SupportsRichComparison](heap: list[C], item: C, /) -> C: ...
    def heapreplace[C: SupportsRichComparison](heap: list[C], item: C, /) -> C: ...
else: from .py313 import *
if s.version_info >= (3, 13): from asyncio.queues import *
else: from .py312 import *