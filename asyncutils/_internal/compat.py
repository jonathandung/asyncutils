import sys as S
__all__ = 'LifoQueue', 'Placeholder', 'PriorityQueue', 'Queue', 'QueueEmpty', 'QueueFull', 'QueueShutDown', 'dumbterm', 'heapify', 'heappop', 'heappush', 'heappushpop', 'heapreplace', 'pargs', 'partial', 'respenv'
respenv, c, V = not S.flags.ignore_environment, (g := (E := __import__('os').environ).get)('NO_COLOR') != '1', (S.hexversion-0xf0)>>16
if dumbterm := g('TERM') == 'dumb':
    if g('FORCE_COLOR') == '1': __import__('warnings').warn('FORCE_COLOR=1 overrides TERM=dumb')
    else: c = False
    if respenv and V >= 0x30d: E['PYTHON_BASIC_REPL'] = '1'
    print(end='\x1b[?2004l', flush=True) # noqa: T201
if V >= 0x30e: pargs = {'suggest_on_error': not dumbterm, 'color': c}; from _functools import Placeholder, partial; from _heapq import heapify_max as heapify, heappop_max as heappop, heappush_max as heappush, heappushpop_max as heappushpop, heapreplace_max as heapreplace # type: ignore[import-not-found]
else: from asyncutils._internal.py313 import *
if V >= 0x30d: from asyncio.queues import *
else: from asyncutils._internal.py312 import *
del V, E, g, c, S