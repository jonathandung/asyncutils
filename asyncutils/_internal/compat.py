import sys as S
__all__ = 'D', 'LifoQueue', 'Placeholder', 'PriorityQueue', 'Queue', 'QueueEmpty', 'QueueFull', 'QueueShutDown', 'heapify', 'heappop', 'heappush', 'heappushpop', 'heapreplace', 'j', 'p', 'partial'
c, V, b = not (g := (E := __import__('os').environ).get)('NO_COLOR'), (S.hexversion-0xf0)>>16, bool(g('PYTHON_BASIC_REPL')) if (r := not (F := S.flags).ignore_environment) else None
if d := g('TERM') == 'dumb':
    if g('FORCE_COLOR'): __import__('_warnings').warn('possibly undesired conflict in environment variables: non-empty FORCE_COLOR overrides TERM=dumb', RuntimeWarning)
    else: c = False
    if r and not b and V >= 0x30d: E['PYTHON_BASIC_REPL'] = '1'
    (s := S.stdout).write('\x1b[?2004l'); s.flush(); del s
if V >= 0x30e: j = {'suggest_on_error': not d, 'color': c}; from _functools import Placeholder, partial; from _heapq import heapify_max as heapify, heappop_max as heappop, heappush_max as heappush, heappushpop_max as heappushpop, heapreplace_max as heapreplace
else: j = {}; from asyncutils._internal.py313 import *
if V >= 0x30d: from asyncio.queues import *
else: from asyncutils._internal.py312 import *; d = True
D = {'basic_repl': d or (r and b), 'quiet': F.quiet}
p = __import__('pprint').PrettyPrinter(sort_dicts=False, underscore_numbers=True, **({'indent': 4, 'expand': True} if V >= 0x30f else {})) # ty: ignore[invalid-argument-type]
del V, E, F, g, c, S, r, d, b