from .. import config
from .log import debug as _l
from .submodules import __dict__ as d
from . import patch as P, running_console as R
import sys
if (a := d.pop('__all_submodules', None)) is None: raise ImportError('cannot reload initialization script')
g, _a, _u, _f, _s, d, s = lambda: a, frozenset(a), (_d := {}).update, ('',), 'asyncutils.', iter(d.items()), {}
for _k, _v in d:
    if _k[0] != '_': break
for _k, _v in d: _u(dict.fromkeys(_v, _k[:-4]))
class module(metaclass=type('', (type,), {'__repr__': lambda _, /: f'<function __getattr__ at {id(_):#x}>'})):
    __slots__ = '_name'
    def __new__(cls, name, /, _d=_d, _a=_a, _s=s, _p=config.__package__):
        if name in _a: return _s[name]
        if name == '__git_version__':
            try: return __import__('subprocess').check_output(('git', 'rev-parse', 'HEAD'), text=True).strip()
            except: raise RuntimeError('failed to get git commit hash') from None
        try: return getattr(_s[_d[name]], name)
        except AttributeError, KeyError: raise AttributeError(f'module {_p!r} has no attribute {name!r}') from None
    def __reduce__(self): return type(self), (self._name,)
    def __getattr__(self, name, /): return getattr(self.load(), name)
    def __repr__(self, _s=_s): return f"<module '{_s}{self._name}' (not loaded)>"
    def load(self, _s=s, _m=sys.modules, _g=R._get_, _f=_f, _l=_l, _n=_s):
        if not isinstance(m := _s.get(n := self._name), type(self)): return m
        if (m := _m.get(_n := _n+n)) is None: _l(f'now loading: {n}'); m = __import__(_n, fromlist=_f)
        if l := getattr(_g(), 'locals', None): l[n] = m
        _s[n] = m; return m
    P.patch_classmethod_signatures((__new__, 'name, /')); P.patch_method_signatures((load, ''))
if config.loaded_all:
    for _ in a: s[_] = __import__(_s+_, fromlist=_f)
    globals().update(s); R._request_write_load_all_()
else:
    f = object.__new__
    for _ in a: r._name, s[_] = _, (r := f(module))
    s['config'] = config; del f, r
a += ('submodules_map',)
_l('all submodules initialized')
_l('now loading: config')
del sys, config, P, R, _l, _d, _k, _v, _a, _f, _s, _u, d, _