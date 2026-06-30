from asyncutils._internal.compat import Placeholder, partial
from asyncutils._internal.helpers import LoopMixinBase, fullname, subscriptable
from asyncutils._internal.submodules import properties_all as __all__
from _collections import deque
from weakref import WeakKeyDictionary as W
import asyncutils as A, abc as a
class Deleters(__import__('enum').IntFlag): CANNOT_SET_AFTER_DELETE = SILENT = 1; DEFAULT, CAN_DELETE_AGAIN, NO_DELETER = 0, 2, 4
d, n = Deleters.DEFAULT, 'None'
class D(W):
    def __init__(self, v, d=None, /): super().__init__(); self.c, self.v, self.d = bool, v, d
    def __set_name__(self, o, n, /, _=frozenset(('__doc__', '__module__', '__name__'))):
        if n not in _: raise TypeError
        self.c = o
    def __get__(self, o, t=None, /):
        if not (t is None or issubclass(t, self.c)): raise TypeError('descriptor bound incorrectly')
        return self.v if o is None else self.get(o, self.d)
    def __str__(self, _=n, /): return _ if (v := self.v) is None else v
    def __repr__(self, _=n, /): return _ if (v := self.v) is None else repr(v)
    __set__, __delete__ = W.__setitem__, W.__delitem__
@subscriptable
class AsyncPropertyBase(LoopMixinBase, metaclass=type('AsyncPropertyMeta', (a.ABCMeta,), {'__prepare__': classmethod(lambda c, n, b, _=D, /, **k: (p := c.__base__.__prepare__(n, b, **k)).update(__doc__=_(None), __name__=_(n)) or p), '__new__': lambda m, n, b, d, _=D, /, **k: d.__setitem__('__module__', _('asyncutils.properties')) or m.__base__.__new__(m, n, b, d, **k)})):
    __slots__ = '__ca', '__cls', '__deleted', '__hide', '__lock', '__mutable', '__queue', '__strict', '__weakref__', 'fdel', 'fget', 'fset'; _repr_accessor = staticmethod(repr)
    def _init(self, f, /, fset=None, fdel=d, *, _='<unknown>', doc=None, strict=True, mutable=False, assert_modifiers_return_none=True, hide=False): self.fget, self.fset, self.fdel, self.__doc__, self.__module__, self.__deleted, self.__strict, self.__hide, self.__ca, self.__queue, self.__lock, self.__mutable, self.__cls = f, fset, fdel, getattr(f, '__doc__', None) if doc is None else doc, getattr(f, '__module__', _), set(), strict, hide, assert_modifiers_return_none, deque(), self._lock_factory(), mutable, None
    @a.abstractmethod
    def wrap_aw(self, _, /): raise NotImplementedError
    def __new__(cls, fget=None, *a, **k):
        if fget is None: return partial(cls, *((Placeholder, *a) if a else ()), **k)
        (_ := object.__new__(cls))._init(fget, *a, **k); return _
    def __default_deleter(self, o, f, /):
        if f&Deleters.NO_DELETER: self.__raise('asyncutils.properties.AsyncPropertyBase: undeletable attribute', o, not f&Deleters.SILENT)
        if o in (d := self.__deleted): return self.__raise('asyncutils.properties.AsyncPropertyBase: attribute was already deleted', o, not f&Deleters.CAN_DELETE_AGAIN)
        d.add(o)
    async def __get__(self, o, _=None, /):
        if self.__check_instance(o, not (h := self.__hide)): ...
        elif self.fget is None: self.__raise('asyncutils.properties.AsyncPropertyBase: unreadable attribute', o, self.__strict or h)
        elif o in self.__deleted:
            if type(d := self.fdel) is Deleters: self.__raise('asyncutils.properties.AsyncPropertyBase: attribute was deleted', o, not d&Deleters.NO_DELETER)
            else: raise A.StateCorrupted('async property internal', 'default deleter was called on property with proper deleter')
        else: return await self.__get(o)
        return self
    def __set__(self, o, v, /):
        if self.__check_instance(o): return
        if (f := self.fset) is None: self.__raise('asyncutils.properties.AsyncPropertyBase: immutable attribute', o, self.__strict); return
        if o in (s := self.__deleted): self.__raise('asyncutils.properties.AsyncPropertyBase: cannot set deleted attribute', o, type(d := self.fdel) is Deleters and d&Deleters.CANNOT_SET_AFTER_DELETE); s.discard(o)
        self.__helper(f, 'set', o, v)
    def __delete__(self, o, /):
        if not self.__check_instance(o): self.__default_deleter(o, f) if isinstance(f := self.fdel, Deleters) else self.__helper(f, 'delete', o)
    def __set_name__(self, /, *_): self.__cls, self.__name__ = _
    def __repr__(self): return f'asyncutils.properties.{type(self).__name__}({', '.join(map(self._repr_accessor, (self.fget, self.fset, self.fdel)))}, doc={self.__doc__!r}, strict={self.__strict}, mutable={self.__mutable}, assert_modifiers_return_none={self.__ca}, hide={self.__hide})'
    def __reduce__(self):
        if self.__hide: raise TypeError('asyncutils.properties.AsyncPropertyBase: cannot pickle hidden property')
        return f'{self.__check_unbound().__name__}.{self.__name__}'
    def __check_unbound(self):
        if (c := self.__cls) is None: raise TypeError(f'{self!r} is not bound to a class')
        return c
    def __check_instance(self, o, b=None, /):
        c = self.__check_unbound()
        if o is None: self.__raise('asyncutils.properties.AsyncPropertyBase.__get__ called incorrectly', c, not (self.__mutable if b is None else b)); return True
        self.__raise('asyncutils.properties.AsyncPropertyBase.__get__ called incorrectly', o, not isinstance(o, c)); return False
    async def __get(self, o, /):
        p, b, r = (q := self.__queue).popleft, self.__ca, self.__raise
        async with self.__lock:
            while q: r('asyncutils.properties.AsyncPropertyBase: setter or deleter returned non-None value', o, await p() is not None and b)
        return await self.fget(o)
    def __raise(self, m, o, c=True, /):
        if c: raise AttributeError(m, name=self.__name__, obj=o) from None
    def __helper(self, f, c, /, *a):
        if (r := f(*a)) is None: return
        try: self.__queue.append(self.wrap_aw(r))
        except A.CRITICAL: raise A.Critical
        except TypeError:
            if self.__ca: raise
        except BaseException as e: self.__raise(f'failed to {c} attribute due to {fullname(e)}: {e}', a[0]) # noqa: BLE001
    def getter(self, f, /): return type(self)(f, self.fset, self.fdel, doc=self.__doc__, strict=self.__strict, mutable=self.__mutable, assert_modifiers_return_none=self.__ca, hide=self.__hide)
    def setter(self, f, /): return type(self)(self.fget, f, self.fdel, doc=self.__doc__, strict=self.__strict, mutable=self.__mutable, assert_modifiers_return_none=self.__ca, hide=self.__hide)
    def deleter(self, f, /): return type(self)(self.fget, self.fset, f, doc=self.__doc__, strict=self.__strict, mutable=self.__mutable, assert_modifiers_return_none=self.__ca, hide=self.__hide)
    def __getattr__(self, n, /):
        if (f := self.fget) is None: raise AttributeError('asyncutils.properties.AsyncPropertyBase: property has no getter to find attribute on', name=n, obj=self)
        return getattr(f, n)
    def __init_subclass__(cls, /, *, lock_factory=None, **k):
        if not isinstance(cls.__dict__.get('__slots__'), tuple): raise TypeError('subclass of asyncutils.properties.AsyncPropertyBase must define tuple __slots__')
        if lock_factory is not None: cls._lock_factory = lock_factory
        elif getattr(cls, '_lock_factory', None) is None: raise TypeError('asyncutils.properties.AsyncPropertyBase subclasses must specify lock_factory')
        super().__init_subclass__(**k)
class LazyAsyncProperty(AsyncPropertyBase, lock_factory=__import__('asyncio').Lock): __slots__, wrap_aw = (), staticmethod(A.wrap_in_coro)
class ConcurrentAsyncProperty(AsyncPropertyBase, lock_factory=staticmethod(lambda _=A.anullcontext, /: _)): __slots__, wrap_aw = (), LoopMixinBase.make
class RWLockedAsyncProperty(ConcurrentAsyncProperty):
    __slots__, _repr_accessor = (), staticmethod(lambda v, _=n, /: _ if v is None else repr(v) if type(v) is Deleters else repr(v.__wrapped__))
    def _init(self, f, /, fset=None, fdel=d, *, policy=A.RWLock, **k):
        if not issubclass(policy, A.RWLock): raise TypeError('asyncutils.properties.RWLockedAsyncProperty: policy must be a subclass of asyncutils.rwlocks.RWLock')
        w = (f := policy.lock(f)).writer; super()._init(f, None if fset is None else w(fset), fdel if fdel is Deleters.DEFAULT else w(fdel), **k)
del a, d, n, W, D
