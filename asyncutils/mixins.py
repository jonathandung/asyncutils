from ._internal.helpers import LoopMixinBase, create_executor, get_loop_and_set, subscriptable
from ._internal.submodules import mixins_all as __all__
from abc import ABCMeta, abstractmethod
from asyncio.coroutines import iscoroutine
from asyncio.events import _get_running_loop
from asyncio.timeouts import timeout as _timeout
from functools import cached_property, partial
class EventualLoopMixin(LoopMixinBase): __slots__ = ()
class LoopContextMixin(LoopMixinBase):
    __slots__ = ()
    async def __setup__(self): ...
    async def __cleanup__(self): ...
    async def __aenter__(self): await self.__setup__(); return self
    async def __aexit__(self, *_): await self.__cleanup__(); self.exiter()
class LoopBoundMixin:
    _loop = None
    def make_fut(self):
        if (l := self._loop) is None: self._loop = l = get_loop_and_set()
        elif l is not _get_running_loop(): raise RuntimeError('could not bind loop')
        return l.create_future()
@subscriptable
class AwaitableMixin(metaclass=ABCMeta):
    __slots__ = ()
    def __await__(self): yield from self.wait().__await__() # type: ignore
    @abstractmethod
    def wait(self): ...
@subscriptable
class AsyncContextMixin(metaclass=ABCMeta):
    __slots__ = ()
    def __enter__(self): return self
    @abstractmethod
    def __exit__(self, /, *_): ...
    async def __aenter__(self): return self.__enter__()
    async def __aexit__(self, /, *_): return self.__exit__(*_)
@subscriptable
class ExecutorRequiredAsyncContextMixin(metaclass=ABCMeta):
    @cached_property
    def runner(self):
        if (l := getattr(self, 'loop', None)) is None is (l := getattr(self, '_loop', None)): l = get_loop_and_set()
        return partial(l.run_in_executor, create_executor(self, False)) # type: ignore[attr-defined]
    def __enter__(self): return self
    @abstractmethod
    def __exit__(self, /, *_): ...
    async def __aenter__(self): return await self.runner(self.__enter__)
    async def __aexit__(self, /, *_): return await self.runner(self.__exit__, *_)
@subscriptable
class LockMixin(metaclass=ABCMeta):
    __slots__ = ()
    def __init_subclass__(cls, *, _lock_factory=lambda _: None, **_): cls._lock_factory = _lock_factory
    @abstractmethod
    async def acquire(self): ...
    @abstractmethod
    def release(self): ...
    @abstractmethod
    def locked(self): ...
    async def __aenter__(self):
        if await self.acquire(): return self._lock_factory()
        raise RuntimeError('failed to acquire lock')
    async def __aexit__(self, *_):
        if iscoroutine(a := self.release()): await a # type: ignore
    async def acknowledge_locksmith_lock_held(self, smith, /): return True # noqa: ARG002,PLR6301
@subscriptable
class LockWithOwnerMixin(LockMixin):
    __slots__ = ()
    @property
    @abstractmethod
    def is_owner(self): ...
    @abstractmethod
    def _release(self): ...
    def release(self):
        if not self.is_owner: raise RuntimeError(f'{type(self).__name__} is not acquired by current task')
        return self._release()
@subscriptable
class EventMixin(AwaitableMixin, LoopBoundMixin, metaclass=ABCMeta):
    __slots__ = ()
    @abstractmethod
    async def wait_for_next(self, timeout=None, **k): ...
    @abstractmethod
    def is_set(self): ...
    @abstractmethod
    def get(self): ...
    @abstractmethod
    def set(self, value): ...
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
    async def stream_history_for(self, duration=None):
        try:
            async with _timeout(duration):
                while True: yield await self
        except TimeoutError: return