#!/usr/bin/env python3
if __name__ != '__main__': raise ImportError('cannot import asyncutils.__main__')
if not (g := globals()).get(k := '__package__'):
    import sys as S; n = 'asyncutils'
    if S.version_info < (3, 15): g[k] = n
    (p := S.path).insert(0, p[0].removesuffix(n)); a, b = map(S.intern, ('_frozen_importlib', 'ModuleSpec'))
    if s := g.get('__spec__'):
        for g in type(s).__mro__:
            if g.__module__ == a and g.__qualname__ == b == g.__name__: s.name = 'asyncutils.__main__'; break
    del a, b, p, s, S
del g, k
from .cli import run # noqa: E402
raise SystemExit(run())