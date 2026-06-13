# ty: ignore[possibly-unresolved-reference]
from asyncutils import cli as L, constants as D, context as F, exceptions as E, time_since_boot as T, version as V
from asyncutils._internal import patch as P, running_console as R
from asyncutils._internal.submodules import __dict__ as d
if (a := d.pop('__all_submodules', None)) is None: raise type('InitializationError', (BaseException,), {})('asyncutils: cannot reload internal initialization module')
_u, _f, _s, s, t, U, A = (_d := {}).update, ('',), 'asyncutils.', {}, '_all', (S := list(a)).extend, []
class Module:
    __slots__ = '__all__', '_n', '_s'; del (dunders := dir(L))[-1]
    def __new__(cls, name, /, _d=_d, _a=frozenset(a), _=s):
        if name in _a: return _[name]
        try: return getattr(_[_d[name]], name)
        except (AttributeError, KeyError): raise AttributeError(f"module 'asyncutils' has no attribute {name!r}") from None
    def __reduce__(self): return type(self), (self._n,)
    def __getattr__(self, n, /, u='__', _=F.all_contextual_consts): # cover: off
        if n == '_s': super().__setattr__(n, s := (_.union if self._n == 'context' else frozenset)(self.__all__)); return s
        if n[:2] == u == n[-2:] or n in self._s: return getattr(self.load(), n)
        raise AttributeError(f"module 'asyncutils.{self._n}' has no attribute {n!r}") from None
    def __setattr__(self, n, v, /):
        if n in self.__slots__: raise AttributeError('immutable attribute', name=n, obj=self)
        setattr(self.load(), n, v)
    def __delattr__(self, n, /):
        if n in self.__slots__: raise AttributeError('cannot delete attribute', name=n, obj=self)
        delattr(self.load(), n) # cover: on
    def __repr__(self, _=_s): return f"<module '{_}{self._n}' (not loaded)>"
    def __init_subclass__(cls, /, **_): raise TypeError('cannot subclass the type of asyncutils submodule objects')
    def load(self, _s=s, _m=__import__('sys').modules, _g=R.getc, _f=_f, _n=_s, _a='retrieved loaded submodule: %s', _b='now loading: %s', _c='found cached submodule: %s'):
        if (t := type(self)) is not __class__: return self # ty: ignore[unresolved-reference]
        if type(m := _s.get(n := self._n)) is not t: l(_a, n); return m
        if (m := _m.get(_n := _n+n)) is None: l(_b, n); m = __import__(_n, fromlist=_f)
        else: l(_c, n)
        if d := getattr(_g(), 'locals', None): d[n] = m
        _s[n] = m; return m
    def __dir__(self): return (*self.dunders, *self.__all__)
    P.patch_classmethod_signatures((__new__, _ := 'name, /')); P.patch_method_signatures((load, ''), (__repr__, ''), (__getattr__, _)); del _
f, b, _a, n = object.__new__, object.__setattr__, *Module.__slots__[:2]
for _k in a: U(_v := d[_k+t]); _u(dict.fromkeys(_v, _k)); s[_k] = a = f(Module); b(a, n, _k); b(a, _a, _v)
def l(*a, _=A.append): _(a)
for _k, _v in (('version', V), ('exceptions', E), ('context', F), ('constants', D), ('cli', L)): l('preloading: %s', _k); s[_k] = _v
l('all submodules initialized in %.2f milliseconds', T())
U(('console_preloaded_submodules', 'preloaded_submodules', 'submodules_map', 'time_since_boot'))
del P, R, E, V, F, L, D, T, U, d, f, t, n, _d, _k, _v, _f, _s, _u, _a, b
