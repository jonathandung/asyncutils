if __name__ != '__main__': raise ImportError('cannot import asyncutils.__main__')
import sys as S
if not (g := globals()).get(k := '__package__'):
    if S.version_info < (3, 15): g[k] = 'asyncutils'
    S.path.insert(0, S.path[0][:-11]); a, b = map(S.intern, ('_frozen_importlib', 'ModuleSpec'))
    if s := g.get('__spec__'):
        for g in type(s).__mro__:
            if g.__module__ == a and g.__qualname__ == b == g.__name__: s.name = 'asyncutils.__main__'; break
    del a, b, s
S._xoptions['asyncutils_run_as_main'] = True
del k, S
from ._internal import initialize
from . import base, console
with base.event_loop.from_flags(0) as g: raise SystemExit(console.AsyncUtilsConsole(g).run(suppress_asyncio_warnings=True, suppress_unawaited_coroutine_warnings=True))