__all__ = 'LifoQueue', 'Placeholder', 'PriorityQueue', 'Queue', 'QueueEmpty', 'QueueFull', 'QueueShutDown', 'apargs', 'partial'
from sys import version_info as V
if V >= (3, 14):
    apargs = {'suggest_on_error': True, 'color': __import__('os').getenv('PYTHON_BASIC_REPL') != '1'}
    from _functools import Placeholder, partial  # type: ignore[import-not-found]
else: from .py313 import * # noqa: F403
if V >= (3, 13): from asyncio.queues import LifoQueue, PriorityQueue, Queue, QueueEmpty, QueueFull, QueueShutDown
else: from .py312 import * # noqa: F403
del V