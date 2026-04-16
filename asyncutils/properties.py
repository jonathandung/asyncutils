from ._internal.compat import Placeholder, partial
from ._internal.helpers import fullname, subscriptable
from ._internal.submodules import properties_all as __all__
from asyncio.events import new_event_loop
from asyncio.locks import Lock
from atexit import register
from weakref import finalize
@subscriptable
class AsyncProperty:
    __slots__ = '__doc__', '_cls', '_deleted', '_finalize', '_loop', '_name', '_strict', 'fdel', 'fget', 'fset'
    def __new__(cls, fget=None, *a, **k): return partial(cls, Placeholder, *a, **k) if fget is None else super().__new__(cls)
    def __init__(self, fget=None, fset=None, fdel=None, *, doc=None, strict=True, loop=None): super().__init__(); self.fget, self.fset, self.fdel, self.__doc__, self._deleted, self._loop, self._finalize, self._strict = fget, fset, fdel, doc or getattr(fget, '__doc__', None), set(), (l := loop or new_event_loop()), register(l.close) if loop is None else l.stop, strict
    def __get__(self, obj, _=None, /):
        self._raise_for_unbound()
        if (f := self.fget) is None: return self._get_helper(f'unreadable attribute: {self._name}')
        if obj is None: return self
        if obj in self._deleted: return self._get_helper('cannot get deleted attribute')
        return self._helper(f, obj)
    def __set__(self, obj, val, /):
        self._raise_for_unbound()
        if (f := self.fset) is None: return self._set_helper('immutable attribute', val)
        if obj in self._deleted: return self._set_helper('cannot set deleted attribute', val)
        self._helper(f, obj, val, c='set')
    def __delete__(self, obj, /):
        self._raise_for_unbound()
        if (f := self.fdel) is None:
            if self._strict: raise AttributeError('undeletable attribute')
            return self._deleted.add(obj)
        self._helper(f, obj, c='delete')
    def __set_name__(self, typ, name, /): self._name, self._cls = name, typ
    def __repr__(self): return f'{type(self).__name__}({self.fget!r}, {self.fset!r}, {self.fdel!r}, doc={self.__doc__!r}, strict={self._strict}, loop={self._loop!r})'
    def _raise_for_unbound(self):
        if not all(hasattr(self, _) for _ in ('__name__', '_cls')): raise TypeError(f'instance of {type(self)._name} is not bound to a class')
    def _get_helper(self, msg):
        if self._strict: raise AttributeError(msg, name=self._name)
        return self
    def _helper(self, f, *a, c='get'):
        try: return self._loop.run_until_complete(f(*a))
        except BaseException as e: raise AttributeError(f'failed to {c} attribute {self._name}') from e
    def _set_helper(self, msg, val):
        if self._strict: raise AttributeError(msg, name=self._name)
        type.__setattr__(self._cls, self._name, val)
    def getter(self, fget, /): return type(self)(fget, self.fset, self.fdel, doc=self.__doc__, strict=self._strict, loop=self._loop)
    def setter(self, fset, /): return type(self)(self.fget, fset, self.fdel, doc=self.__doc__, strict=self._strict, loop=self._loop)
    def deleter(self, fdel, /): return type(self)(self.fget, self.fset, fdel, doc=self.__doc__, strict=self._strict, loop=self._loop)
class AsyncLockProperty(AsyncProperty):
    __slots__ = '_cache', '_lock_getter'
    @staticmethod
    def _new_lock(_, *, lock_impl=Lock): return lock_impl()
    def __init__(self, *a, lock_getter=None, **k): super().__init__(*a, **k); self._lock_getter, self._cache = lock_getter or self._new_lock, {}
    def __repr__(self): return f'{super().__repr__()[:-1]}, lock_getter={self._lock_getter!r})'
    def _helper(self, f, *a, c='get'):
        async def _():
            async with self.get_lock(a[0]): await f(*a)
        return super()._helper(_, c=c)
    def get_lock(self, obj):
        if (r := (c := self._cache).get(i := id(obj))) is None: c[i] = r = self._lock_getter(obj)
        try: finalize(obj, c.pop, i, None) # noqa: SIM105
        except TypeError: ...
        return r
class coercedmethod: # noqa: N801
    __slots__ = '__f', '__name', '__owner'
    def __init_subclass__(cls, /, **_): raise TypeError('cannot subclass coercedmethod')
    def __init__(self, f, /): self.__f = f
    def __set_name__(self, typ, name, /): self.__owner, self.__name = typ, name
    def __getattr__(self, n, /): return getattr(self.__f, n)
    def __get__(self, obj, typ=None, /):
        if obj is None: raise AttributeError(f'class {fullname(typ)} has no attribute {self.__name!r}') if typ is self.__owner else RuntimeError('incorrectly bound coercedmethod')
        if not (typ is None or isinstance(obj, typ)): raise TypeError('coercedmethod.__get__ called incorrectly')
        return lambda *a, **k: self.__f(obj, *a, **k)