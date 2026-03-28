__all__ = 'apargs', 'partial', 'Placeholder', 'Queue', 'QueueEmpty', 'QueueFull', 'QueueShutDown', 'LifoQueue'
import sys
if sys.version_info >= (3, 14):
    apargs = {'suggest_on_error': True, 'color': __import__('os').getenv('PYTHON_BASIC_REPL') != '1'}
    from _functools import partial, Placeholder # type: ignore[import-not-found]
else: from .py313 import * # noqa: F403
if sys.version_info >= (3, 13): from asyncio.queues import Queue, QueueEmpty, QueueFull, QueueShutDown, LifoQueue
else: from .py312 import * # noqa: F403