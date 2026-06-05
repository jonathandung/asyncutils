from asyncutils._internal.compat import Placeholder, partial
from asyncutils._internal.helpers import LoopMixinBase, subscriptable
from asyncutils._internal.submodules import properties_all as __all__
from _collections import deque
from weakref import WeakKeyDictionary as W
import asyncutils as A, abc
n = 'None'
class D(W):
    def __init__(self, d, /): super().__init__(); self.c, self.v = bool, d
    def __set_name__(self, o, n, /, _=frozenset(('__doc__', '__module__', '__name__'))):
        if n not in _: raise TypeError
        self.c = o
    def __get__(self, o, t=None, /):
        if not (t is None or issubclass(t, self.c)): raise TypeError
        return self.v if o is None else self.get(o)
    def __str__(self, _=n, /): return _ if (v := self.v) is None else v
    def __repr__(self, _=n, /): return _ if (v := self.v) is None else repr(v)
    __set__, __delete__ = W.__setitem__, W.__delitem__
@subscriptable
class AsyncPropertyBase(LoopMixinBase, metaclass=type('AsyncPropertyMeta', (abc.ABCMeta,), {'__prepare__': classmethod(lambda c, n, b, _=D, /, **k: (p := c.__base__.__prepare__(n, b, **k)).update(__doc__=_(None), __name__=_(n)) or p), '__new__': lambda m, n, b, d, _=D, /, **k: d.__setitem__('__module__', _('asyncutils.properties')) or m.__base__.__new__(m, n, b, d, **k)})):
    __slots__ = '__cls', '__deleted', '__hide', '__lock', '__queue', '__strict', '__weakref__', 'fdel', 'fget', 'fset'
    def __new__(cls, fget=None, *a, **k): # ty: ignore[invalid-assignment]
        if fget is None: return partial(cls, Placeholder, *a, **k) if a else partial(cls, **k)
        (_ := object.__new__(cls))._setup(fget, *a, **k); return _
    _repr_helper = staticmethod(repr)
    def _setup(self, f, /, fset=None, fdel=None, *, _='<unknown>', doc=None, strict=True, hide=False): self.fget, self.fset, self.fdel, self.__doc__, self.__module__, self.__deleted, self.__strict, self.__hide, self.__queue, self.__lock = f, fset, fdel, getattr(f, '__doc__', None) if doc is None else doc, getattr(f, '__module__', _), set(), strict, hide, deque(), self._lock_factory()
    def __get__(self, o, _=None, /):
        if o is None: self.__check_hidden(); return self
        self.__check_unbound()
        if self.fget is None: return self.__get_helper('asyncutils.properties.AsyncPropertyBase: unreadable attribute')
        if o in self.__deleted: return self.__get_helper('asyncutils.properties.AsyncPropertyBase: cannot get deleted attribute')
        return self.__get(o)
    def __set__(self, o, v, /):
        if o is None: return self.__check_hidden()
        self.__check_unbound()
        if (f := self.fset) is None: return self.__set_helper('asyncutils.properties.AsyncPropertyBase: immutable attribute', v)
        if o in self.__deleted: return self.__set_helper('asyncutils.properties.AsyncPropertyBase: cannot set deleted attribute', v)
        self.__queue.append(self.__helper(f, 'set', o, v))
    def __delete__(self, o, /):
        if o is None: return self.__check_hidden()
        self.__check_unbound()
        if (f := self.fdel) is None:
            if self.__strict: raise AttributeError('asyncutils.properties.AsyncPropertyBase: undeletable attribute', name=self.__name__)
            return self.__deleted.add(o)
        self.__queue.append(self.__helper(f, 'delete', o))
    def __set_name__(self, /, *_): self.__cls, self.__name__ = _
    def __repr__(self): return f'asyncutils.properties.{type(self).__name__}({", ".join(map(self._repr_helper, (self.fget, self.fset, self.fdel)))}, doc={self.__doc__!r}, strict={self.__strict}, hide={self.__hide})'
    def __reduce__(self):
        if self.__hide: raise TypeError('asyncutils.properties.AsyncPropertyBase: cannot pickle hidden property')
        return f'{self.__cls.__name__}.{self.__name__}'
    def __check_hidden(self):
        if self.__hide: raise AttributeError(name=self.__name__, obj=self.__cls)
    def __check_unbound(self):
        if not hasattr(self, '_AsyncPropertyBase__cls'): raise TypeError(f'{self!r} is not bound to a class')
    def __get_helper(self, m, /):
        if self.__strict or self.__hide: raise AttributeError(m, name=self.__name__)
        return self
    @abc.abstractmethod
    def _wrap_aw(self, _, /): raise NotImplementedError
    async def __get(self, o, /):
        p = (q := self.__queue).popleft
        async with self.__lock:
            while q:
                if await p() is not None and self.__strict: raise TypeError('setter or deleter returned non-None value')
        return await self.fget(o)
    def __helper(self, f, c, /, *a):
        try: return self._wrap_aw(f(*a))
        except A.CRITICAL: raise A.Critical
        except BaseException as e: raise AttributeError(f'failed to {c} attribute {self.__name__}') from e
    def __set_helper(self, m, v, /):
        if self.__strict: raise AttributeError(m, name=self.__name__)
        setattr(self.__cls, self.__name__, v)
    def getter(self, f, /): return type(self)(f, self.fset, self.fdel, doc=self.__doc__, strict=self.__strict, hide=self.__hide)
    def setter(self, f, /): return type(self)(self.fget, f, self.fdel, doc=self.__doc__, strict=self.__strict, hide=self.__hide)
    def deleter(self, f, /): return type(self)(self.fget, self.fset, f, doc=self.__doc__, strict=self.__strict, hide=self.__hide)
    def __getattr__(self, n, /):
        if (f := self.fget) is None: raise AttributeError(name=n, obj=self)
        return getattr(f, n)
    def __init_subclass__(cls, /, *, lock_factory=None, **_):
        if not isinstance(cls.__dict__.get('__slots__'), tuple): raise TypeError('subclass of asyncutils.properties.AsyncPropertyBase must define tuple __slots__')
        if lock_factory is not None: cls._lock_factory = lock_factory
        elif getattr(cls, '_lock_factory', None) is None: raise TypeError('asyncutils.properties.AsyncPropertyBase subclasses must specify lock_factory')
        super().__init_subclass__(**_)
class LazyAsyncProperty(AsyncPropertyBase, lock_factory=__import__('asyncio').Lock): __slots__, _wrap_aw = (), staticmethod(A.wrap_in_coro)
class ConcurrentAsyncProperty(AsyncPropertyBase, lock_factory=staticmethod(lambda _=A.anullcontext, /: _)): __slots__, _wrap_aw = (), LoopMixinBase.make
class RWLockedAsyncProperty(ConcurrentAsyncProperty):
    __slots__, _repr_helper = (), staticmethod(lambda v, _=n, /: _ if v is None else repr(v.__wrapped__))
    def _setup(self, f, /, fset=None, fdel=None, *, policy=A.RWLock, **k): w = (f := policy.lock(f)).writer; super()._setup(f, None if fset is None else w(fset), None if fdel is None else w(fdel), **k)
del abc, n, W, D
