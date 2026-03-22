from .. import config as C, exceptions as E, version as V
from .log import debug as l
from .submodules import __dict__ as d
from . import patch as P, running_console as R
if (a := d.pop('__all_submodules', None)) is None: raise ImportError('asyncutils: cannot reload initialization script')
_a, _u, _f, _s, _i, s, t = frozenset(a), (_d := {}).update, ('',), 'asyncutils.', iter(d.items()), {}, '_all'
for _k, _v in _i:
    if _k[0] != '_': break
for _k, _v in _i: _u(dict.fromkeys(_v, _k.removesuffix(t)))
class module(metaclass=type('', (type,), {'__repr__': lambda _, /: f'<function __getattr__ at {id(_):#x}>'})):
    __slots__ = '_name', '_fs'
    def __new__(cls, name, /, _d=_d, _a=_a, _s=s, _=_f):
        if name in _a: return _s[name]
        if name == '__git_version__':
            if (r := getattr(cls, '_git_ver', None)) is None:
                try: cls._git_ver = r = (__import__('importlib.resources', fromlist=_).files('asyncutils')/'GIT_VERSION').read_text()
                except: raise RuntimeError('failed to get git commit hash') from None
            return r
        try: return getattr(_s[_d[name]], name)
        except AttributeError, KeyError: raise AttributeError(f"module 'asyncutils' has no attribute {name!r}") from None
    def __reduce__(self): return type(self), (self._name,)
    def __getattr__(self, name, /):
        if (s := self._fs) is None: self._fs = s = frozenset(self.__dir__())
        if name in s: return getattr(self.load(), name)
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
else:
    f = object.__new__
    for _ in a: r._name, r._fs, s[_] = _, None, (r := f(module))
    s.update(config=C, exceptions=E, version=V); del f, r
a += ('submodules_map',)
l('all submodules initialized')
l('now loading: config')
del C, P, R, E, V, l, d, t, _d, _k, _v, _a, _f, _s, _u, _i, _