import collections as C, sys as S
__all__ = 'D', 'Placeholder', 'heapify', 'heappop', 'heappush', 'heappushpop', 'heapreplace', 'j', 'partial', 's'
c, V, b = not (g := (E := __import__('os').environ).get)('NO_COLOR'), S.version_info, bool(g('PYTHON_BASIC_REPL')) if (r := not (F := S.flags).ignore_environment) else None
if d := g('TERM') == 'dumb':
    if g('FORCE_COLOR'): __import__('_warnings').warn('possibly undesired conflict in environment variables: non-empty FORCE_COLOR overrides TERM=dumb', RuntimeWarning)
    else: c = False
    if r and not b and V >= (3, 13): E['PYTHON_BASIC_REPL'] = '1'
    (s := S.stdout).write('\x1b[?2004l'); s.flush(); del s
y = () if V < (3, 15) else (frozendict(),) # noqa: F821
if V < (3, 14): j = {}; from asyncutils._internal.py313 import * # noqa: F403
else: j = {'suggest_on_error': not d, 'color': c}; from _functools import Placeholder, partial; from heapq import heapify_max as heapify, heappop_max as heappop, heappush_max as heappush, heappushpop_max as heappushpop, heapreplace_max as heapreplace
if V < (3, 13): import asyncutils._internal.py312 as V; d = True
D = {'basic_repl': d or (r and b), 'quiet': F.quiet}
t = [[], (), b'', bytearray(), '', range(0), range(1<<31), __import__('array').array('b'), C.deque(), C.defaultdict(), C.Counter(), type.__dict__, (lambda _=S._getframe: _().f_locals)()] # noqa: PLC3002
t += (o for e in ({}, C.OrderedDict(), *y) for o in (e, e.keys(), e.values(), e.items()))
(u := (s := set(map(type, t))).update)(type(reversed(_)) for _ in t)
t += (C.ChainMap(), __import__('itertools').repeat(None), set(), frozenset())
u(type(iter(_)) for _ in t)
s = frozenset(s)
del V, E, F, g, c, S, r, d, b, t, u, C, y
