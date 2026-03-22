if __name__ != '__main__': raise ImportError('cannot import asyncutils.__main__')
import sys as S
if not (g := globals()).get(k := '__package__'):
    if S.version_info < (3, 15): g[k] = 'asyncutils'
    S.path.insert(0, S.path[0][:-11]); a, b = map(S.intern, ('_frozen_importlib', 'ModuleSpec'))
    if s := g.get('__spec__'):
        for g in type(s).__mro__:
            if g.__module__ == a and g.__qualname__ == b == g.__name__: s.name = 'asyncutils.__main__'; break
    del a, b, s
del g, k, S
from .cli import run
raise SystemExit(run())