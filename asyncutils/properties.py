from asyncutils import sync_await
from asyncutils._internal.compat import Placeholder, partial
from asyncutils._internal.helpers import fullname, get_loop_and_set, subscriptable
from asyncutils._internal.submodules import properties_all as __all__
from asyncio.locks import Lock
from weakref import WeakKeyDictionary
@subscriptable
class AsyncProperty:
    __slots__ = '__cls', '__deleted', '__doc', '__hide', '__loop', '__name', '__strict', 'fdel', 'fget', 'fset'
    def __new__(cls, fget=None, fset=None, fdel=None, *, doc=None, strict=True, hide=False):
        if fget is None: return partial(cls, Placeholder, fset, fdel, doc=doc, strict=strict)
        (_ := object.__new__(cls)).fget, _.fset, _.fdel, _.__doc, _.__deleted, _.__loop, _.__strict, _.__hide = fget, fset, fdel, getattr(fget, '__doc__', None) if doc is None else doc, set(), get_loop_and_set(), strict, hide; return _
    def __get__(self, obj, _=None, /): self._raise_for_unbound(); return self._check_hidden(self)if obj is None else self._get_helper(f'asyncutils.properties.AsyncProperty: unreadable attribute: {self.__name}') if (f := self.fget) is None else self._get_helper('asyncutils.properties.AsyncProperty: cannot get deleted attribute') if obj in self.__deleted else self._helper(f, obj)
    def __set__(self, obj, val, /):
        self._raise_for_unbound()
        if obj is None: return self._check_hidden()
        if (f := self.fset) is None: return self._set_helper('asyncutils.properties.AsyncProperty: immutable attribute', val)
        if obj in self.__deleted: return self._set_helper('asyncutils.properties.AsyncProperty: cannot set deleted attribute', val)
        if self._helper(f, obj, val, c='set') is not None: raise TypeError('asyncutils.properties.AsyncProperty: setter must return None')
    def __delete__(self, obj, /):
        self._raise_for_unbound()
        if obj is None: return self._check_hidden()
        if (f := self.fdel) is None:
            if self.__strict: raise AttributeError('asyncutils.properties.AsyncProperty: undeletable attribute', name=self.__name)
            return self.__deleted.add(obj)
        if self._helper(f, obj, c='delete') is not None: raise TypeError('asyncutils.properties.AsyncProperty: deleter must return None')
    def __set_name__(self, typ, name, /): self.__name, self.__cls = name, typ
    def __repr__(self): return f'{fullname(self)}({self.fget!r}, {self.fset!r}, {self.fdel!r}, doc={self.__doc!r}, strict={self.__strict})'
    def _check_hidden(self, res=None):
        if self.__hide: raise AttributeError(name=self.__name, obj=self.__cls)
        return res
    def _raise_for_unbound(self):
        if not all(hasattr(self, _) for _ in ('_AsyncProperty__name', '_AsyncProperty__cls')): raise TypeError(f'{self!r} is not bound to a class')
    def _get_helper(self, msg):
        if self.__strict or self.__hide: raise AttributeError(msg, name=self.__name)
        return self
    def _helper(self, f, *a, c='get'):
        try: return sync_await(f(*a), loop=self.__loop)
        except BaseException as e: raise AttributeError(f'failed to {c} attribute {self.__name}') from e
    def _set_helper(self, msg, val):
        if self.__strict: raise AttributeError(msg, name=self.__name)
        setattr(self.__cls, self.__name, val)
    def getter(self, fget, /): return type(self)(fget, self.fset, self.fdel, doc=self.__doc, strict=self.__strict)
    def setter(self, fset, /): return type(self)(self.fget, fset, self.fdel, doc=self.__doc, strict=self.__strict)
    def deleter(self, fdel, /): return type(self)(self.fget, self.fset, fdel, doc=self.__doc, strict=self.__strict)
    def __getattr__(self, n, /):
        if (f := self.fget) is None: raise AttributeError(name=n, obj=self)
        return getattr(f, n)
    @property
    def __doc__(self): return self.__doc
    @property
    def __name__(self): return self.__name
class AsyncLockProperty(AsyncProperty):
    __slots__ = '__cache', '__lock_getter'
    @staticmethod
    def _new_lock(_, *, lock_impl=Lock): return lock_impl()
    def __new__(cls, *a, lock_getter=None, **k):
        if type(_ := super().__new__(cls, *a, **k)) is cls: _.__lock_getter, _.__cache = lock_getter or _._new_lock, WeakKeyDictionary()
        return _
    def __repr__(self): return f'{super().__repr__()[:-1]}, lock_getter={self.__lock_getter!r})'
    def _helper(self, f, *a, **k):
        async def _():
            async with self.get_lock(a[0]): return await f(*a)
        return super()._helper(_, **k)
    def get_lock(self, obj):
        if (r := (c := self.__cache).get(obj)) is None: c[obj] = r = self.__lock_getter(obj)
        return r
    @property
    def __doc__(self): return self._AsyncProperty__doc
    @property
    def __name__(self): return self._AsyncProperty__name
class coercedmethod: # noqa: N801
    __slots__ = '__f', '__n', '__o'
    def __init_subclass__(cls, /, **_): raise TypeError('cannot subclass asyncutils.properties.coercedmethod')
    def __init__(self, f, /): self.__f = f
    def __set_name__(self, typ, name, /): self.__o, self.__n = typ, name
    def __getattr__(self, n, /): return getattr(self.__f, n)
    def __get__(self, obj, typ=None, /):
        if obj is None: raise AttributeError(f'class {fullname(typ)} has no attribute {self.__n!r}', name=self.__n) if typ is self.__o else RuntimeError('incorrectly bound asyncutils.properties.coercedmethod')
        if not (typ is None or isinstance(obj, typ)): raise TypeError('asyncutils.properties.coercedmethod: __get__ called incorrectly')
        return lambda *a, **k: self.__f(obj, *a, **k)