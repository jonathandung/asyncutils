'''Various compatibility shims for older Python versions.'''
from .types import SupportsRichComparison
import sys as m
from _collections_abc import Iterable
from pprint import PrettyPrinter
from typing import Any, Final
from functools import partial
__all__ = 'D', 'LifoQueue', 'Placeholder', 'PriorityQueue', 'Queue', 'QueueEmpty', 'QueueFull', 'QueueShutDown', 'heapify', 'heappop', 'heappush', 'heappushpop', 'heapreplace', 'j', 'p', 'partial', 's'
D: Final[dict[str, Any]]
j: Final[dict[str, Any]]
p: Final[PrettyPrinter]
if m.version_info >= (3, 14):
    from functools import Placeholder
    def heapify[C: SupportsRichComparison](heap: list[C], /) -> None: ...
    def heappop[C: SupportsRichComparison](heap: list[C], /) -> C: ...
    def heappush[C: SupportsRichComparison](heap: list[C], item: C, /) -> None: ...
    def heappushpop[C: SupportsRichComparison](heap: list[C], item: C, /) -> C: ...
    def heapreplace[C: SupportsRichComparison](heap: list[C], item: C, /) -> C: ...
else: from .py313 import *
if m.version_info >= (3, 13): from asyncio.queues import *
else: from .py312 import *
s: Final[frozenset[type[Iterable]]]