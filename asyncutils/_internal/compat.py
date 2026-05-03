__all__ = 'LifoQueue', 'Placeholder', 'PriorityQueue', 'Queue', 'QueueEmpty', 'QueueFull', 'QueueShutDown', 'heapify', 'heappop', 'heappush', 'heappushpop', 'heapreplace', 'pargs', 'partial'
if (V := __import__('sys').version_info) >= (3, 14): g = __import__('os').environ.get; pargs = {'suggest_on_error': True, 'color': g('NO_COLOR') != '1' and g('TERM') != 'dumb'}; from _functools import Placeholder, partial; from _heapq import heapify_max as heapify, heappop_max as heappop, heappush_max as heappush, heappushpop_max as heappushpop, heapreplace_max as heapreplace; del g # type: ignore[import-not-found]
else: from asyncutils._internal.py313 import *
if V >= (3, 13): from asyncio.queues import *
else: from asyncutils._internal.py312 import *
del V