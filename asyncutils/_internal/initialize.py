from asyncutils import cli as L, config as C, constants as D, context as F, exceptions as E, time_since_boot as T, version as V
from asyncutils._internal import patch as P, running_console as R
from asyncutils._internal.log import debug as l
from asyncutils._internal.submodules import __dict__ as d
if (a := d.pop('__all_submodules', None)) is None: raise type('InitializationError', (BaseException,), {})('asyncutils: cannot reload internal initialization module')
_a, _u, _f, _s, _i, s, t = frozenset(a), (_d := {}).update, ('',), 'asyncutils.', iter(d.items()), {}, '_all'
for _k, _v in _i:
    if _k[0] != '_': break
try:
    while True: _u(dict.fromkeys(_v, _k.removesuffix(t))); _k, _v = next(_i)
except StopIteration: ...
class Module:
    __slots__ = '_fs', '_name'
    def __new__(cls, name, /, _d=_d, _a=_a, _=s):
        if name in _a: return _[name]
        try: return getattr(_[_d[name]], name)
        except (AttributeError, KeyError): raise AttributeError(f"module 'asyncutils' has no attribute {name!r}") from None
    def __reduce__(self): return type(self), (self._name,)
    def __getattr__(self, name, /, _=F.all_contextual_consts, f=frozenset()):
        if name == '_fs': self._fs = s = (_ if name == 'context' else f).union(self.__dir__()); return s
        if name in self._fs: return getattr(self.load(), name)
        raise AttributeError(f"module 'asyncutils.{self._name}' has no attribute {name!r}") from None
    def __repr__(self, _s=_s): return f"<module '{_s}{self._name}' (not loaded)>"
    def __init_subclass__(cls, /, **_): raise TypeError('cannot subclass the type of asyncutils submodule objects')
    def load(self, _s=s, _m=__import__('sys').modules, _g=R.get, _f=_f, _l=l, _n=_s):
        if (t := type(self)) is not __class__: return self
        if type(m := _s.get(n := self._name)) is not t: return m
        if (m := _m.get(_n := _n+n)) is None: _l(f'now loading: {n}'); (m := __import__(_n, fromlist=_f)).__dir__ = self.__dir__
        if l := getattr(_g(), 'locals', None): l[n] = m
        _s[n] = m; return m
    __all__ = property(__dir__ := lambda self, d=d, t=t: d[self._name+t]); P.patch_classmethod_signatures((__new__, 'name, /')); P.patch_method_signatures((load, ''), (__dir__, ''))
f = object.__new__
for _ in a: r._name, s[_] = _, (r := f(Module))
l('all submodules initialized in %.2f milliseconds', T())
for _ in (f := ('cli', 'config', 'constants', 'context', 'exceptions', 'version')): l('preloading: %s', _)
for _k, _v in zip(f, (L, C, D, F, E, V)): s[_k], _v.__dir__ = _v, s[_k].__dir__ # type: ignore[attr-defined]
if C.loaded_all:
    f = Module.load
    for _ in s.values(): f(_)
    l('all submodules loaded in %.2f milliseconds', T())
a.extend(('console_preloaded_submodules', 'preloaded_submodules', 'submodules_map', 'time_since_boot'))
del C, P, R, E, V, F, L, T, l, d, f, r, t, _d, _k, _v, _a, _f, _s, _u, _i, _