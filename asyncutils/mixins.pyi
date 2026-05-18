'''Mixins classes for some common or specialized patterns that provide methods based on some abstract methods.'''
from ._internal.helpers import LoopMixinBase
from ._internal.types import ExcType
from .locks import LocksmithBase
from _collections_abc import AsyncGenerator, Awaitable, Callable, Coroutine, Generator
from abc import ABC, abstractmethod
from asyncio.events import AbstractEventLoop
from asyncio.futures import Future
from asyncio.tasks import Task
from functools import cached_property
from types import TracebackType
from typing import Any, Literal, Self, overload
__all__ = 'AsyncContextMixin', 'AwaitableMixin', 'EventMixin', 'ExecutorRequiredAsyncContextMixin', 'LockMixin', 'LockWithOwnerMixin', 'LoopBoundMixin', 'LoopContextMixin'
class LoopContextMixin(LoopMixinBase):
    ''':meth:`__setup__` will be called when the context is entered and :meth:`__cleanup__` when it is exited.'''
    @property
    def running_tasks(self) -> set[Task[Any]]: '''A set of all tasks currently running in the underlying loop.'''
    @property
    def loop(self) -> AbstractEventLoop: ...
    async def __setup__(self) -> None: ...
    async def __cleanup__(self) -> None: ...
    async def __aenter__(self) -> Self: ...
    @overload
    async def __aexit__(self, exc_typ: ExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> None: ...
    @overload
    async def __aexit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> None: ...
class AwaitableMixin[T](ABC):
    '''A subclass that implements the async :meth:`wait` method automatically becomes awaitable, resolving to the return value of that method.'''
    def __await__(self) -> Generator[Any, None, T]: ...
    @abstractmethod
    def wait(self) -> Awaitable[T]: ...
class AsyncContextMixin[T](ABC):
    '''A mixin to derive :meth:`__aenter__` and :meth:`__aexit__` from :meth:`__enter__` (optional; returns self by default, but that cannot be typed accurately) and :meth:`__exit__` of subclasses.'''
    def __enter__(self) -> T: ...
    @overload
    @abstractmethod
    def __exit__(self, exc_typ: ExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> bool|None: ...
    @overload
    @abstractmethod
    def __exit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> Literal[False]|None: ...
    async def __aenter__(self) -> T: ...
    @overload
    async def __aexit__(self, exc_typ: ExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> bool|None: ...
    @overload
    async def __aexit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> Literal[False]|None: ...
class ExecutorRequiredAsyncContextMixin[T](ABC):
    '''The above, but using an executor to convert the sync context manager methods to async in an event loop.'''
    @cached_property
    def runner[R, *Ts](self) -> Callable[[Callable[[*Ts], R], *Ts], Future[R]]: ...
    def __enter__(self) -> T: ...
    @overload
    @abstractmethod
    def __exit__(self, exc_typ: ExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> bool|None: ...
    @overload
    @abstractmethod
    def __exit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> Literal[False]|None: ...
    async def __aenter__(self) -> T: ...
    @overload
    async def __aexit__(self, exc_typ: ExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> bool|None: ...
    @overload
    async def __aexit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> Literal[False]|None: ...
class LockMixin[T](ABC):
    '''A mixin to derive :meth:`__aenter__` and :meth:`__aexit__` from :meth:`acquire` and :meth:`release` of subclasses.'''
    def __init_subclass__(cls, *, _lock_factory: Callable[[Self], T]=..., **k: Any) -> None: ...
    @abstractmethod
    async def acquire(self) -> bool: '''Acquire the lock, waiting if necessary. Return whether the lock was acquired successfully. Some locks may raise an error if not; that is up to the implementation.'''
    @abstractmethod
    def release(self) -> Coroutine[Any, Any, None]|None: ...
    @abstractmethod
    def locked(self) -> bool: '''Return whether the lock is currently held by a task satisfying a certain criterion (e.g. it is the task awaited the acquiry).'''
    def acknowledge_locksmith_lock_held(self, smith: LocksmithBase, /) -> bool|Coroutine[Any, Any, bool]: '''Optional method to cooperate with locksmiths in case of unusually long wait times for the lock which may indicate deadlock, livelock or starvation.'''
    async def __aenter__(self) -> T: '''Acquire the lock and return an object of the implementation's choice.'''
    @overload
    async def __aexit__(self, exc_typ: ExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> None: ...
    @overload
    async def __aexit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> None: '''Release the lock and optionally perform handling according to the exception occurred.'''
class LockWithOwnerMixin[T: (None, Coroutine[Any, Any, None])](LockMixin[None]):
    '''| Mixin for locks that can report their owner (the task currently holding it).
    | :attr:`is_owner` should evaluate to `True` if the current task is the owner of the lock, and :meth:`release` will wrap :meth:`_release` to throw :exc:`RuntimeError` if this does not hold.'''
    @property
    @abstractmethod
    def is_owner(self) -> bool: ...
    @abstractmethod
    def _release(self) -> T: ...
    def release(self) -> T: ...
class LoopBoundMixin(LoopMixinBase): '''Mixin to bind event loops lazily for classes that need to create futures.'''
class EventMixin[T](AwaitableMixin[T], LoopBoundMixin, ABC):
    '''| Mixin for event classes that don't inherit from :class:`asyncio.Event` but provide enhanced functionality with the same API and some mixin
    | methods, most notably making the event itself awaitable. This is simply syntactic sugar for calling the wait method, but more convenient and
    | intuitive when thinking of events as reusable futures.'''
    @abstractmethod
    async def wait_for_next(self, timeout: float|None=...) -> T: '''Wait for the next time the event is set, and return the value it was set to. Should always block even if there is currently a value set.'''
    @abstractmethod
    def is_set(self) -> bool: '''Return whether the event currently holds a value.'''
    @abstractmethod
    def get(self) -> T: '''Return the value currently held by the event, or raise an exception if there is no value set. The implementations in this library have a dedicated exception type, :exc:`~exceptions.EventValueError`, for this.'''
    @abstractmethod
    def set(self, value: T) -> None: '''Set the value of the event and wake up all waiters. Implementations may not choose to clear the value within this method.'''
    @abstractmethod
    def clear(self) -> None: '''Clear the value of the event.'''
    async def wait(self, timeout: float|None=...) -> T: '''Wait for the event with an optional `timeout` and return its value.'''
    async def wait_for_value(self, val: T, timeout: float|None=..., *, set_at_timeout: bool=...) -> None: '''Wait for the event to be set to a specific value `val`, with an optional `timeout`. If `set_at_timeout` is `True`, the event will be set to `val` when the timeout occurs, and waiters will be woken up. The value will persist on the event by default in this case.'''
    def stream_values_for(self, duration: float|None=...) -> AsyncGenerator[T]: '''Yield the values set on the event for `duration` seconds, or indefinitely if not passed.'''