from .config import Executor
from ._internal.helpers import _LoopMixinBase, _get_loop_and_set, subscriptable
from functools import cached_property, partial
from abc import ABCMeta, abstractmethod
from asyncio.coroutines import iscoroutine
from asyncio.timeouts import timeout
from asyncio.events import _get_running_loop, new_event_loop
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
    def __await__(self): yield from self.wait().__await__()
    @abstractmethod
    async def wait(self): ...
@subscriptable
class AsyncContextMixin(metaclass=ABCMeta):
    @cached_property
    def runner(self, _=_get_loop_and_set): __import__('sys').audit('asyncutils/create_executor', 'mixins.AsyncContextMixin'); return partial(_().run_in_executor, Executor())
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
    def _set_loop(self, g=_get_running_loop, n=new_event_loop):
        loop = g() or n()
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
    async def wait_for_value(self, val, timeout=None, *, set_at_timeout=False, _=timeout):
        try:
            async with _(timeout):
                while val is not await self: continue
        except TimeoutError:
            if set_at_timeout: self.set(val)
            raise
    async def wait(self, timeout=None, **k):
        try: return self.get()
        except ValueError: return await self.wait_for_next(timeout, **k)
    async def stream_history_for(self, duration=None, _=timeout):
        try:
            async with _(duration):
                while True: yield await self
        except TimeoutError: return
del timeout, _get_running_loop, new_event_loop, _get_loop_and_set