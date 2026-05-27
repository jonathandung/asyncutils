'''| Locking primitives, more advanced than or supplementing the functionality of those in :mod:`asyncio`.
| All classes strictly follow the asynchronous lock interface as defined by :class:`asyncio.Lock` and made explicit in the :class:`_internal.types.AsyncLockLike` protocol, besides
| :class:`MultiCountDownLatch`, since it uses :class:`KeyedCondition` internally and it is not desired for :mod:`altlocks` to import :mod:`locks` as well.'''
from ._internal.types import AsyncLockLike
from .mixins import LoopBoundMixin, LockMixin, LockWithOwnerMixin, LoopContextMixin
from _collections_abc import Callable, Hashable, Mapping
from asyncio.locks import BoundedSemaphore, Lock
from asyncio.tasks import Task
from typing import Any, Literal
__all__ = 'AdvancedRateLimit', 'DynamicBoundedSemaphore', 'KeyedCondition', 'MultiCountDownLatch', 'PriorityLock', 'PriorityRLock', 'PrioritySemaphore', 'RLock'
class DynamicBoundedSemaphore(BoundedSemaphore):
    '''A subclass of :class:`asyncio.BoundedSemaphore` whose bound can be set by the user via the `bound` property.'''
    def __init__(self, value: int=...): '''`value`, the initial value of the semaphore, defaults to :const:`context.DYNAMIC_BOUNDED_SEMAPHORE_DEFAULT_VALUE`.'''
    @property
    def bound(self) -> int: '''Return the bound of the semaphore.'''
    @bound.setter
    def bound(self, value: int, /) -> None: '''Set the bound of the semaphore to `value`, and coerce the internal value to the bound, waking up waiters in that case.'''
class AdvancedRateLimit(LoopBoundMixin, LockMixin[None]):
    '''A rate limiter that supports a mode in which waiters can cut the queue.'''
    def __init__(self, rate: float, capacity: float=..., fair: bool=...):
        '''| `rate` (required): The initial rate at which tokens refill.
        | `capacity`: The maximum rate, defaulting to the current rate.
        | `fair`: Whether to maintain FIFO (first in, first out) for waiters; default `True`.'''
    async def acquire(self, tokens: float=..., timeout: float|None=...) -> Literal[True]: '''Acquire the specified number of tokens from the rate limiter (default :const:`context.ADVANCED_RATE_LIMIT_DEFAULT_TOKENS`), waiting until the timeout expires and signalling :exc:`TimeoutError` if necessary.'''
    async def release(self, tokens: float=...) -> None: '''Release the specified number of tokens back to the rate limiter (default :const:`context.ADVANCED_RATE_LIMIT_DEFAULT_TOKENS`).'''
    async def set_rate(self, new: float) -> None: '''Set the rate of the limiter to `new`.'''
    def locked(self) -> bool: '''Return `True` if the limiter is currently locked, such that :meth:`acquire` must block to wait for tokens.'''
    def update_tokens_lock_held(self) -> None: '''Perform necessary processing before further operations on the token count. It is guaranteed that the rate limiter only calls this when holding the internal lock.'''
    @property
    def rate(self) -> float: '''Return the current rate of the limiter.'''
    @property
    def tokens(self) -> float: '''Return the current number of tokens available.'''
    @property
    def capacity(self) -> float: '''Return the capacity of the limiter.'''
class PrioritySemaphore(LoopBoundMixin, LockMixin[None]):
    '''A semaphore that allows waiters with a lower priority value to enter first.'''
    def __init__(self, value: int=...): '''`value`, the initial value as an integer, defaults to :const:`context.PRIORITY_SEMAPHORE_DEFAULT_VALUE`.'''
    async def acquire(self, priority: int=...) -> Literal[True]: '''Acquire the semaphore with the specified priority (default :const:`context.PRIORITY_SEMAPHORE_DEFAULT_PRIORITY`).'''
    def release(self, strict: bool=...) -> None: '''Release the semaphore. If `strict` is `True` (the default) and the number of releases is more than the number of acquisitions, a :exc:`RuntimeError` is raised.'''
    def locked(self) -> bool: '''Return `True` if the semaphore is currently locked.'''
    def reset(self) -> None: '''Reset the semaphore to its initial state.'''
class KeyedCondition[T](LockMixin[KeyedCondition[T]], LoopContextMixin):
    '''A condition variable that allows waiting on and notifying individual keys, or all keys at once.'''
    def __init__(self, lock: Lock|LockMixin[Any]|None=...): '''Initialize the condition variable with the given lock, or create a new one if not passed.'''
    async def acquire(self) -> bool: '''Wrap the acquire method of the underlying lock to only reraise critical errors and return success.'''
    async def release(self) -> None: '''Await the release method of the underlying lock if it is a coroutine.'''
    def locked(self) -> bool: '''Return whether the underlying lock is currently locked.'''
    def assert_locked(self) -> None: '''Assert that the underlying lock is currently locked, and raise a :exc:`RuntimeError` if not.'''
    async def wait(self, key: T, timeout: float|None=...) -> None: '''Wait for the given key `key` to be notified within `timeout`.'''
    async def wait_all(self, timeout: float|None=...) -> None: '''Wait for all the current waiters to be notified within `timeout`.'''
    async def wait_for(self, key: T, pred: Callable[[], bool], per_wait_timeout: float|None=...) -> None: '''Keep waiting for the given key `key` to be notified within `per_wait_timeout` seconds until the predicate `pred` returns `True`.'''
    def notify(self, key: T, n: int=..., strict: bool=...) -> None: '''Notify `n` waiters waiting on the given key `key` (default 1). If `strict` is `True` and the key doesn't exist, :exc:`KeyError` is raised.'''
    def notify_all(self, key: T|None=...) -> int: '''Notify all waiters waiting on the given key `key`, or all waiters if `key` is `None`. Return the number of waiters that were notified.'''
class MultiCountDownLatch[H: Hashable]:
    '''A collection of count-down latches, each identified by a key, supporting waiting on individual latches or on all of them at once.'''
    def __init__(self, counts: Mapping[H, int]): '''Initialize the latch with the given mapping of keys to counts. No more keys can be added after this stage.'''
    async def count_down(self, key: H, strict: bool=...) -> None: '''Decrement the count of the latch with the given key by one. If it reaches zero, wake up all waiters. If `strict` is `True` and the key doesn't exist, :exc:`KeyError` is raised.'''
    async def count_down_all(self) -> None: '''Decrement the count of each latch by one.'''
    async def wait(self, key: H, strict: bool=...) -> None: '''Wait for the latch with the given key to reach zero. If `strict` is `True` and the key doesn't exist, :exc:`KeyError` is raised.'''
    async def wait_all(self, timeout: float|None=...) -> None: '''Wait for the count of all latches to reach zero.'''
    @property
    def broken(self) -> bool: '''If this returns `True`, it means that :meth:`wait_all` will return immediately.'''
class RLock(LockWithOwnerMixin[None]):
    '''An async reentrant lock that is somehow missing from :mod:`asyncio`.'''
    def __init__(self, lock: AsyncLockLike[Any]|None=...): ...
    async def acquire(self) -> Literal[True]: ...
    def _release(self) -> None: ...
    def locked(self) -> bool: ...
    @property
    def is_owner(self) -> bool: ...
class PriorityLock(LoopBoundMixin, LockWithOwnerMixin[None]):
    '''A lock allowing waiters with a lower priority value to enter first.'''
    async def acquire(self, priority: int=..., timeout: float|None=...) -> bool: ...
    def _release(self, raise_: bool=...) -> None: ...
    def locked(self) -> bool: ...
    @property
    def is_owner(self) -> bool: ...
class PriorityRLock(RLock):
    '''A reentrant lock supporting priority.'''
    def __init__(self) -> None: ...
    @property
    def owner(self) -> Task[Any]|None: ...
    async def acquire(self, priority: int=..., timeout: float|None=...) -> bool: ... # ty: ignore[invalid-method-override]