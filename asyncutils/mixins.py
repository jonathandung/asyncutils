import functools as F, asyncutils._internal.helpers as H
from abc import ABCMeta, abstractmethod
from asyncio import iscoroutine
from asyncio import timeout as _timeout
from asyncutils._internal.submodules import mixins_all as __all__
@H.subscriptable
class AwaitableMixin(metaclass=ABCMeta):
    __slots__ = ()
    def __await__(self): yield from self.wait().__await__()
    @abstractmethod
    async def wait(self): raise NotImplementedError
@H.subscriptable
class AsyncContextMixin(metaclass=ABCMeta):
    __slots__ = ()
    def __enter__(self): return self
    @abstractmethod
    def __exit__(self, /, *_): raise NotImplementedError
    async def __aenter__(self): return self.__enter__()
    async def __aexit__(self, /, *_): return self.__exit__(*_)
@H.subscriptable
class ExecutorRequiredAsyncContextMixin(metaclass=ABCMeta):
    @F.cached_property
    def runner(self):
        if (l := getattr(self, 'loop', None)) is None is (l := getattr(self, '_loop', None)): self.loop = l = H.get_loop_and_set()
        return F.partial(l.run_in_executor, H.create_executor(self, False)) # ty: ignore[unresolved-attribute]
    def __enter__(self): return self
    @abstractmethod
    def __exit__(self, /, *_): raise NotImplementedError
    async def __aenter__(self):
        if __class__.__enter__ is (m := type(self).__enter__): return self
        return await self.runner(m, self)
    async def __aexit__(self, /, *_): return await self.runner(self.__exit__, *_)
@H.subscriptable
class LockMixin(metaclass=ABCMeta):
    __slots__ = ()
    def __init_subclass__(cls, *, _lock_factory_=lambda _: None, **_): cls._lock_factory = _lock_factory_; super().__init_subclass__(**_)
    @abstractmethod
    async def acquire(self): raise NotImplementedError
    @abstractmethod
    def release(self): raise NotImplementedError
    @abstractmethod
    def locked(self): raise NotImplementedError
    async def __aenter__(self):
        if await self.acquire(): return self._lock_factory()
        raise RuntimeError('asyncutils.mixins.LockMixin: failed to acquire lock')
    async def __aexit__(self, *_):
        if iscoroutine(a := self.release()): await a
    def acknowledge_locksmith_lock_held(self, _, /): return True # ruff: ignore[no-self-use]
class LockWithOwnerMixin(LockMixin):
    __slots__ = ()
    @property
    @abstractmethod
    def is_owner(self): raise NotImplementedError
    @abstractmethod
    def _release(self): raise NotImplementedError
    def release(self):
        if not self.is_owner: raise RuntimeError(f'{H.fullname(self)} is not acquired by current task')
        return self._release()
class EventMixin(AwaitableMixin, H.LoopMixinBase, metaclass=ABCMeta):
    __slots__ = ()
    @abstractmethod
    async def wait_for_next(self, timeout=None, **_): raise NotImplementedError
    @abstractmethod
    def is_set(self): raise NotImplementedError
    @abstractmethod
    def get(self): raise NotImplementedError
    @abstractmethod
    def set(self, value): raise NotImplementedError
    @abstractmethod
    def clear(self): raise NotImplementedError
    async def wait_for_value(self, val, timeout=None, *, set_at_timeout=False):
        try:
            async with _timeout(timeout):
                while val is not await self: continue
        except TimeoutError:
            if set_at_timeout: self.set(val)
            raise
    async def wait(self, timeout=None, **k):
        try: return self.get()
        except ValueError: return await self.wait_for_next(timeout, **k)
