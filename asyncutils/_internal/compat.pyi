import sys as s, typing as t
from functools import partial
__all__ = 'apargs', 'partial', 'Placeholder', 'Queue', 'QueueEmpty', 'QueueFull', 'QueueShutDown', 'LifoQueue'
if s.version_info >= (3, 14): from functools import Placeholder
else: Placeholder: t.Final[object] # type: ignore[no-redef,misc]
if s.version_info >= (3, 13): from asyncio.queues import Queue, QueueEmpty, QueueFull, QueueShutDown, LifoQueue
else: from .py312 import * # type: ignore[assignment] # noqa: F403
apargs: dict[str, t.Any]