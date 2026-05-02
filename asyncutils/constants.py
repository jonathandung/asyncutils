from asyncutils._internal import patch as P
from asyncutils._internal.helpers import fullname
from asyncutils._internal.submodules import constants_all as __all__
RECIP_E, EXECUTORS_FROZENSET = 0.36787944117144233, frozenset(POSSIBLE_EXECUTORS := ('thread', 'process', 'interpreter', 'loky', 'loky_noreuse', 'dask', 'ipython', 'elib_flux_cluster', 'elib_flux_job', 'elib_slurm_cluster', 'elib_slurm_job', 'elib_single_node', 'pebble_thread', 'pebble_process'))
class sentinel_base:
    _can_instantiate = False; __slots__ = '__mod', '__name'
    def __new__(cls, name=None, _=__import__('keyword').iskeyword, g=__import__('sys')._getframemodulename):
        cls._assert_can_instantiate()
        if name is None: return super().__new__(cls)
        if _(name) or not all(p.isidentifier() and not _(p) for p in name.split('.', 1)): raise ValueError('invalid name')
        if (m := g(1)) is not None: name = f'{m}.{name}'
        if (o := (c := cls._cache).get(name)) is None:
            (o := super().__new__(cls)).__name, o.__mod = name, m
            with cls._lock: c[name] = o
        return o
    @property
    def name(self): return self.__name
    @property
    def module(self): return self.__mod
    @classmethod
    def _assert_can_instantiate(cls):
        if not cls._can_instantiate: raise TypeError(f'cannot instantiate {fullname(cls)!r}')
    def __repr__(self): return f'<{fullname(self)} {self.__name!r} at {id(self):#x}>'
    def __str__(self): return getattr(self, '_sentinel_base__name', '<unbound>')+(' <private>'*self.is_private)
    def __set_name__(self, owner, name, /, _='NOTE: The following is considered bad practice:\nclass {0}:\n{1} = {2}({3!r})\n...\ninstead, consider:\nclass {0}:\n{1} = {2}()\n'.format):
        N = f'{fullname(owner)}.{name}'.replace('<locals>.', '').replace('<lambda>.', '')
        with self._lock:
            if (n := getattr(self, '__name', None)) is None:
                if not self.is_(self._cache.setdefault(N, self)): raise NameError(f'{fullname(self)} name collision', name=N)
                self.__name = N
            elif n == N and self._cache.get(N) is self:
                if b := self.bound_to: __import__('sys').stderr.write(_(b.rpartition('.')[-1], self.back, fullname(self), N))
                else: raise NameError(f'cannot bind named unbound {fullname(self)} to class {fullname(owner)!r}', name=N)
            else: raise NameError(f'cannot bind named {fullname(self)} to class {fullname(owner)!r}', name=N)
    def __reduce__(self):
        try: return type(self), (self.__name,)
        except AttributeError: raise TypeError(f'cannot pickle unbound instance of {fullname(self)}') from None
    def __init_subclass__(cls, lock_impl=__import__('_thread').allocate_lock):
        if getattr(cls, '__slots__', True): raise TypeError('sentinel classes should have empty __slots__')
        cls._cache, cls._lock, cls._can_instantiate = {}, lock_impl(), True
    @property
    def is_private(self): return (self.back or '').startswith('_')
    @property
    def bound_to(self): return getattr(self, '_sentinel_base__name', '').rpartition('.')[0] or None
    @property
    def back(self): return getattr(self, '_sentinel_base__name', '').rpartition('.')[2] or None
    def is_(self, o, /): return self is o
    P.patch_classmethod_signatures((__new__, 'name=None'), (__init_subclass__, 'lock_impl={}')); P.patch_method_signatures((__set_name__, 'owner, name, /'))
class _sentinel(sentinel_base):
    __slots__ = ()
    def __init_subclass__(cls): raise TypeError('cannot subclass the type of asyncutils-internal sentinels')
    def __reduce__(self): return self.name
_NO_DEFAULT, RAISE, SYNC_AWAIT = map(_sentinel, ('_NO_DEFAULT', 'RAISE', 'SYNC_AWAIT'))
CLOSED, HALF_OPEN, OPEN = range(3)
_sentinel._can_instantiate = False
del _sentinel, P