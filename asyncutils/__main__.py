if __name__ != '__main__': raise ImportError('cannot import asyncutils.__main__')
import sys as S
S.path.insert(0, S.path[0][:-11]); a, b = map(S.intern, ('_frozen_importlib', 'ModuleSpec'))
if s := globals().get('__spec__'):
    for S in type(s).__mro__:
        if S.__module__ == a and S.__qualname__ == b == S.__name__: s.name = 'asyncutils.__main__'; break
del a, b, s, S
from .cli import run
raise SystemExit(run())