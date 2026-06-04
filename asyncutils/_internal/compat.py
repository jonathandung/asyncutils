import sys as S, collections as C
__all__ = 'D', 'LifoQueue', 'Placeholder', 'PriorityQueue', 'Queue', 'QueueEmpty', 'QueueFull', 'QueueShutDown', 'f', 'heapify', 'heappop', 'heappush', 'heappushpop', 'heapreplace', 'j', 'p', 'partial', 's'
c, V, b = not (g := (E := __import__('os').environ).get)('NO_COLOR'), S.version_info, bool(g('PYTHON_BASIC_REPL')) if (r := not (F := S.flags).ignore_environment) else None
if d := g('TERM') == 'dumb':
    if g('FORCE_COLOR'): __import__('_warnings').warn('possibly undesired conflict in environment variables: non-empty FORCE_COLOR overrides TERM=dumb', RuntimeWarning)
    else: c = False
    if r and not b and V >= (3, 13): E['PYTHON_BASIC_REPL'] = '1'
    (s := S.stdout).write('\x1b[?2004l'); s.flush(); del s
x = {'sort_dicts': False, 'underscore_numbers': True, 'width': 88}
if V < (3, 15): y = ()
else: x.update(indent=4, expand=True); y = frozendict(),
if V < (3, 14): j = {}; from asyncutils._internal.py313 import *
else: j = {'suggest_on_error': not d, 'color': c}; from _functools import Placeholder, partial; from heapq import heapify_max as heapify, heappop_max as heappop, heappush_max as heappush, heappushpop_max as heappushpop, heapreplace_max as heapreplace
if V < (3, 13): from asyncutils._internal.py312 import *; d = True
else: from asyncio.queues import *
D = {'basic_repl': d or (r and b), 'quiet': F.quiet}
p = __import__('pprint').PrettyPrinter(**x) # ty: ignore[invalid-argument-type]
t = [o for e in ({}, C.OrderedDict(), *y) for o in (e, e.keys(), e.values(), e.items())]
t += ([], (), b'', bytearray(), '', range(0), range(1<<31), __import__('array').array('b'), C.deque(), C.defaultdict(), C.Counter(), type.__dict__, (lambda: S._getframe().f_locals)(), C.ChainMap(), __import__('itertools').repeat(None), set(), frozenset()) # ty: ignore[unsupported-operator]
(u := (s := list(map(type, t))).extend)(type(iter(_)) for _ in t)
del t[-4:]
u(type(reversed(_)) for _ in t)
s = frozenset(s)
try: f = S._getframemodulename
except AttributeError:
    if (u := getattr(S, '_getframe', None)) is None: raise
    def f(depth=0, _=u): return _(depth).f_globals.get('__name__')
del V, E, F, g, c, S, r, d, b, t, u, C, x, y
