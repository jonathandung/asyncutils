lazy from .config import Executor
from ._internal.helpers import _LoopMixinBase, get_loop_and_set, subscriptable
from functools import cached_property, partial
from abc import ABCMeta, abstractmethod
lazy from asyncio.coroutines import iscoroutine
lazy from asyncio.timeouts import timeout as _timeout
from ._internal.submodules import mixins_all as __all__
class EventualLoopMixin(_LoopMixinBase): __slots__ = ()
class LoopContextMixin(_LoopMixinBase):
    __slots__ = ()
    async def __setup__(self): ...
    async def __cleanup__(self): ...
    async def __aenter__(self): await self.__setup__(); return self
    async def __aexit__(self, *_): await self.__cleanup__(); self.exiter()
@subscriptable
class AwaitableMixin(metaclass=ABCMeta):
    __slots__ = ()
    def __await__(self): yield from self.wait().__await__() # type: ignore
    @abstractmethod
    def wait(self): ...
@subscriptable
class AsyncContextMixin(metaclass=ABCMeta):
    @cached_property
    def runner(self):
        __import__('sys').audit('asyncutils/create_executor', 'mixins.AsyncContextMixin')
        if (l := getattr(self, 'loop', None)) is None is (l := getattr(self, '_loop', None)): l = get_loop_and_set()
        return partial(l.run_in_executor, Executor()) # type: ignore[attr-defined]
    def __enter__(self): return self
    @abstractmethod
    def __exit__(self, /, *_): ...
    async def __aenter__(self): return await self.runner(self.__enter__)
    async def __aexit__(self, *_): return await self.runner(self.__exit__, *_)
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
    async def acknowledge_locksmith_lock_held(self, _, /): return True
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
class EventMixin(AwaitableMixin, metaclass=ABCMeta):
    _loop = None
    def _set_loop(self):
        from asyncio import events as m
        loop = m._get_running_loop() or m.new_event_loop()
        if self._loop is None: self._loop = loop
        if loop is not self._loop: raise RuntimeError('loop binding failed')
        return loop
    @cached_property
    def loop(self): return self._set_loop()
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