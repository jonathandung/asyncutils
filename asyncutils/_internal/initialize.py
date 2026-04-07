from .. import config as C, constants as D, exceptions as E, version as V, time_since_boot as T
from .log import debug as l
from .submodules import __dict__ as d
from . import patch as P, running_console as R
if (a := d.pop('__all_submodules', None)) is None: raise ImportError('asyncutils: cannot reload internal initialization module')
_a, _u, _f, _s, _i, s, t = frozenset(a), (_d := {}).update, ('',), 'asyncutils.', iter(d.items()), {}, '_all'
for _k, _v in _i:
    if _k[0] != '_': break
try:
    while True: _u(dict.fromkeys(_v, _k.removesuffix(t))); _k, _v = next(_i)
except StopIteration: ...
class module(metaclass=type('', (type,), {'__repr__': lambda _, /: f'<function __getattr__ at {id(_):#x}>'})):
    __slots__ = '_name', '_fs'
    def __new__(cls, name, /, _d=_d, _a=_a, _s=s):
        if name in _a: return _s[name]
        try: return getattr(_s[_d[name]], name)
        except (AttributeError, KeyError): raise AttributeError(f"module 'asyncutils' has no attribute {name!r}") from None
    def __reduce__(self): return type(self), (self._name,)
    def __getattr__(self, name, /):
        if name == '_fs': self._fs = s = frozenset(self.__dir__()); return s
        if name in self._fs: return getattr(self.load(), name)
        raise AttributeError(f"module 'asyncutils.{self._name}' has no attribute {name!r}") from None
    def __repr__(self, _s=_s): return f"<module '{_s}{self._name}' (not loaded)>"
    def __init_subclass__(cls, /, **_): raise TypeError('cannot subclass module')
    def load(self, _s=s, _m=__import__('sys').modules, _g=R._get_, _f=_f, _l=l, _n=_s):
        if not isinstance(m := _s.get(n := self._name), type(self)): return m
        if (m := _m.get(_n := _n+n)) is None: _l(f'now loading: {n}'); m = __import__(_n, fromlist=_f)
        if l := getattr(_g(), 'locals', None): l[n] = m
        _s[n] = m; return m
    __all__ = property(__dir__ := lambda self, d=d, t=t: d[self._name+t]); P.patch_classmethod_signatures((__new__, 'name, /')); P.patch_method_signatures((load, ''))
if C.loaded_all:
    for _ in a: s[_] = __import__(_s+_, fromlist=_f)
    globals().update(s); R._request_write_load_all_()
    l(f'all submodules loaded in {T():.1f} milliseconds')
else:
    f = object.__new__
    for _ in a: r._name, s[_] = _, (r := f(module))
    s.update(zip(f := ('config', 'constants', 'exceptions', 'version'), (C, D, E, V))); l(f'all submodules initialized in {T():.1f} milliseconds')
    for _ in f: l(f'now loading: {_}')
    del f, r
a.extend(('submodules_map', 'preloaded_submodules', 'time_since_boot'))
del C, P, R, E, V, l, d, t, _d, _k, _v, _a, _f, _s, _u, _i, _