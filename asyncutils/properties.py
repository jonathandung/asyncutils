from asyncutils._internal.compat import Placeholder, partial
from asyncutils._internal.helpers import fullname, subscriptable
from asyncutils._internal.submodules import properties_all as __all__
from _collections import deque
from weakref import WeakKeyDictionary as W
import asyncutils as A, abc
class D(W):
    def __init__(self, d=None, /): super().__init__(); self.cs, self.dv = bool, d
    def __set_name__(self, o, n, /, _=frozenset(('__doc__', '__module__', '__name__'))):
        self.cs = o
        if n not in _: raise TypeError
    def __get__(self, o, t=None, /):
        if not (t is None or issubclass(t, self.cs)): raise TypeError
        return self.dv if o is None else self.get(o)
    __set__, __delete__ = W.__setitem__, W.__delitem__
@subscriptable
class AsyncPropertyBase(A.LoopBoundMixin, metaclass=type('AsyncPropertyMeta', (abc.ABCMeta,), {'__prepare__': classmethod(lambda c, n, b, _=D, /, **k: (p := c.__base__.__prepare__(n, b, **k)).update(__doc__=_(), __module__=_('asyncutils.properties'), __name__=_(n), __slots__=()) or p)})):
    __slots__ = '__cls', '__deleted', '__hide', '__lock', '__queue', '__strict', '__weakref__', 'fdel', 'fget', 'fset'
    def __new__(cls, fget=None, fset=None, fdel=None, *, doc=None, strict=True, hide=False):
        if fget is None: return partial(cls, Placeholder, fset, fdel, doc=doc, strict=strict)
        (_ := object.__new__(cls)).fget, _.fset, _.fdel, _.__doc__, _.__module__, _.__deleted, _.__strict, _.__hide, _.__queue, _.__lock = fget, fset, fdel, getattr(fget, '__doc__', None) if doc is None else doc, getattr(fget, '__module__', None), set(), strict, hide, deque(), cls._lock_factory(); return _
    def __get__(self, o, _=None, /):
        if o is None: self._check_hidden(); return self
        self._raise_for_unbound()
        if self.fget is None: return self._get_helper('asyncutils.properties.AsyncProperty: unreadable attribute')
        if o in self.__deleted: return self._get_helper('asyncutils.properties.AsyncProperty: cannot get deleted attribute')
        return self._get(o)
    def __set__(self, o, v, /):
        if o is None: return self._check_hidden()
        self._raise_for_unbound()
        if (f := self.fset) is None: return self._set_helper('asyncutils.properties.AsyncProperty: immutable attribute', v)
        if o in self.__deleted: return self._set_helper('asyncutils.properties.AsyncProperty: cannot set deleted attribute', v)
        self.__queue.append(self._helper(f, 'set', o, v))
    def __delete__(self, o, /):
        if o is None: return self._check_hidden()
        self._raise_for_unbound()
        if (f := self.fdel) is None:
            if self.__strict: raise AttributeError('asyncutils.properties.AsyncProperty: undeletable attribute', name=self.__name__)
            return self.__deleted.add(o)
        self.__queue.append(self._helper(f, 'delete', o))
    def __set_name__(self, /, *_): self.__cls, self.__name__ = _
    def __repr__(self): return f'{fullname(self)}({self.fget!r}, {self.fset!r}, {self.fdel!r}, doc={self.__doc__!r}, strict={self.__strict})'
    def _check_hidden(self):
        if self.__hide: raise AttributeError(name=self.__name__, obj=self.__cls)
    def _raise_for_unbound(self):
        if not hasattr(self, '_AsyncPropertyBase__cls'): raise TypeError(f'{self!r} is not bound to a class')
    def _get_helper(self, m):
        if self.__strict or self.__hide: raise AttributeError(m, name=self.__name__)
        return self
    @abc.abstractmethod
    def _inner_helper(self, x, /): raise NotImplementedError
    async def _get(self, o, /):
        p = (q := self.__queue).popleft
        async with self.__lock:
            while q:
                if await p() is not None and self.__strict: raise TypeError('setter or deleter returned non-None value')
        return await self.fget(o)
    def _helper(self, f, c, *a):
        try: return self._inner_helper(f(*a))
        except A.CRITICAL: raise A.Critical
        except BaseException as e: raise AttributeError(f'failed to {c} attribute {self.__name__}') from e
    def _set_helper(self, m, v):
        if self.__strict: raise AttributeError(m, name=self.__name__)
        setattr(self.__cls, self.__name__, v)
    def getter(self, f, /): return type(self)(f, self.fset, self.fdel, doc=self.__doc__, strict=self.__strict)
    def setter(self, f, /): return type(self)(self.fget, f, self.fdel, doc=self.__doc__, strict=self.__strict)
    def deleter(self, f, /): return type(self)(self.fget, self.fset, f, doc=self.__doc__, strict=self.__strict)
    def __getattr__(self, n, /):
        if (f := self.fget) is None: raise AttributeError(name=n, obj=self)
        return getattr(f, n)
    def __init_subclass__(cls, /, *, lock_factory, **_):
        if not isinstance(cls.__dict__.get('__slots__'), tuple): raise TypeError('subclass of asyncutils.properties.AsyncProperty must define tuple __slots__')
        cls._lock_factory = lock_factory; super().__init_subclass__(**_)
class LazyAsyncProperty(AsyncPropertyBase, lock_factory=__import__('asyncio').Lock): _inner_helper = staticmethod(A.wrap_in_coro)
class ConcurrentAsyncProperty(AsyncPropertyBase, lock_factory=staticmethod(lambda _=A.anullcontext, /: _)): _inner_helper = A.LoopBoundMixin.make
class coercedmethod: # noqa: N801
    __slots__ = '__f', '__n', '__o'
    def __init_subclass__(cls, /, **_): raise TypeError('cannot subclass asyncutils.properties.coercedmethod')
    def __init__(self, f, /): self.__f = f
    def __set_name__(self, /, *_): self.__o, self.__n = _
    def __getattr__(self, n, /): return getattr(self.__f, n)
    def __get__(self, o, t=None, /):
        if o is None: raise AttributeError(f'class {fullname(t)} has no attribute {self.__n!r}', name=self.__n) if t is self.__o else RuntimeError('incorrectly bound asyncutils.properties.coercedmethod')
        if not (t is None or isinstance(o, t)): raise TypeError('asyncutils.properties.coercedmethod: __get__ called incorrectly')
        return lambda *a, **k: self.__f(o, *a, **k)
del abc, W, D
