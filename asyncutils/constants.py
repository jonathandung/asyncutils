from ._internal import patch as P
RECIP_E = 0.3678794411714423
class sentinel_base:
    _can_instantiate, __slots__ = False, ('__name',)
    def __new__(cls, name=None, _=__import__('keyword').iskeyword):
        cls._assert_can_instantiate()
        if name is None: return super().__new__(cls)
        if _(name) or not all(p.isidentifier() and not _(p) for p in name.split('.', 1)): raise ValueError('invalid name')
        if (o := (c := cls._cache).get(name)) is None:
            (o := super().__new__(cls)).__name = name
            with cls._lock: c[name] = o
        return o
    @property
    def name(self): return self.__name
    @classmethod
    def _assert_can_instantiate(cls):
        if not cls._can_instantiate: raise TypeError(f'cannot instantiate {cls.__qualname__!r}') from None
    def __repr__(self): return f'<{type(self).__qualname__} {self.__name!r} at {id(self):#x}>'
    def __str__(self): return getattr(self, 'name', '<unbound>')+(' <private>' if self.is_private else '')
    def __set_name__(self, owner, name, /):
        if getattr(self, '__name', None) is None: self._assert_can_instantiate(); self.__name = n = f'{owner.__qualname__}.{name}'; self._cache[n] = self
        else: raise NameError(f'cannot bind named {type(self).__qualname__} to class')
    def __reduce__(self):
        try: return type(self), (self.__name,)
        except AttributeError: raise TypeError(f'cannot pickle unbound instance of {type(self).__qualname__}') from None
    def __init_subclass__(cls, lock_impl=__import__('_thread').allocate_lock):
        if getattr(cls, '__slots__', True): raise TypeError('slots should be empty for sentinel classes')
        cls._cache, cls._lock, cls._can_instantiate = {}, lock_impl(), True
    @property
    def is_private(self): return getattr(self, '__name', '').split('.', 1)[-1].startswith('_')
    @property
    def bound_to(self):
        if len(l := getattr(self, '__name', '').split('.', 1)) == 2: return l[0]
    P.patch_classmethod_signatures((__new__, 'name=None'), (__init_subclass__, 'lock_impl={}'))
class _sentinel(sentinel_base):
    __slots__ = ()
    def __init_subclass__(cls): raise TypeError('cannot subclass _sentinel')
    def __reduce__(self): return f'asyncutils.config.{self.name}'
_NO_DEFAULT, RAISE, SYNC_AWAIT = map(_sentinel, ('_NO_DEFAULT', 'RAISE', 'SYNC_AWAIT'))
_sentinel._can_instantiate = False