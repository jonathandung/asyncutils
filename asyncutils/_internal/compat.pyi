import sys as s, typing as t
from functools import partial
__all__ = 'LifoQueue', 'Placeholder', 'PriorityQueue', 'Queue', 'QueueEmpty', 'QueueFull', 'QueueShutDown', 'apargs', 'partial'
if s.version_info >= (3, 14): from functools import Placeholder # type: ignore[attr-defined]
else: Placeholder: t.Final[object] # type: ignore[no-redef,misc]
if s.version_info >= (3, 13): from asyncio.queues import Queue, QueueEmpty, QueueFull, QueueShutDown, LifoQueue, PriorityQueue # type: ignore[attr-defined]
else: from .py312 import * # type: ignore[assignment] # noqa: F403
apargs: dict[str, t.Any]