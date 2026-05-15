import sys as S
__all__ = 'D', 'LifoQueue', 'Placeholder', 'PriorityQueue', 'Queue', 'QueueEmpty', 'QueueFull', 'QueueShutDown', 'heapify', 'heappop', 'heappush', 'heappushpop', 'heapreplace', 'j', 'partial'
c, V, b = (g := (E := __import__('os').environ).get)('NO_COLOR') != '1', (S.hexversion-0xf0)>>16, None if (r := (F := S.flags).ignore_environment) else g('PYTHON_BASIC_REPL') == '1'
if d := g('TERM') == 'dumb':
    if g('FORCE_COLOR') == '1': __import__('_warnings').warn('possibly undesired conflict in environment variables: FORCE_COLOR=1 overrides TERM=dumb', RuntimeWarning)
    else: c = False
    if r and not b and V >= 0x30d: E['PYTHON_BASIC_REPL'] = '1'
    (s := S.stdout).write('\x1b[?2004l'); s.flush(); del s
if V >= 0x30e: j = {'suggest_on_error': not d, 'color': c}; from _functools import Placeholder, partial; from _heapq import heapify_max as heapify, heappop_max as heappop, heappush_max as heappush, heappushpop_max as heappushpop, heapreplace_max as heapreplace
else: j = {}; from asyncutils._internal.py313 import *
if V >= 0x30d: from asyncio.queues import *
else: from asyncutils._internal.py312 import *; d = True
D = {'basic_repl': d or (r and b), 'quiet': F.quiet}
del V, E, F, g, c, S, r, d, b