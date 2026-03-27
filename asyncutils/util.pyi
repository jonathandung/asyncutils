from .exceptions import IgnoreErrors
from ._internal.protocols import AsyncLockLike
from typing import Any, Literal, Concatenate, overload
from _collections_abc import Awaitable, Coroutine, Callable, Generator, AsyncGenerator
from asyncio.events import AbstractEventLoop
from asyncio.tasks import Task
from asyncio.locks import Semaphore, BoundedSemaphore, Lock
from asyncio.futures import Future
__all__ = 'get_future', 'new_tasks', 'to_sync', 'to_sync_from_loop', 'sync_await', 'semaphore', 'lockf', 'sync_lock', 'sync_lock_from_binder', 'to_async', 'get_aiter_fromf', 'safe_cancel'
_ignore_cancellation: IgnoreErrors
'''Context manager to ignore asyncio.CancelledError. This annotation is for module-internal use only.'''
def get_future[T](aw: Awaitable[T], loop: AbstractEventLoop|None=...) -> Future[T]:
    '''Wrap an arbitrary awaitable in a task under the provided event loop, creating one and setting if required, and begin waiting on it,
    wrapping critical exceptions in Critical.
    This is as opposed to `loop.create_task`, which only takes coroutines.'''
def new_tasks[T](*coro: Coroutine[Any, Any, T]) -> Generator[Task[T], None, None]: '''Yield tasks wrapping the coroutines under a new event loop in order.'''
def to_sync[R, **P](f: Callable[P, Awaitable[R]], /, timeout: float|None=..., loop: AbstractEventLoop|None=...) -> Callable[P, R]: '''Convert a function that returns an awaitable to an sync function with the same signature, using the event loop `loop` when required or creating when necessary.'''
class to_sync_from_loop:
    '''A version of `to_sync` that is a decorator factory, converting an async function to synchronous by running it in the specified `loop`.
    Not a class at runtime.'''
    def __init__(self, loop: AbstractEventLoop): ...
    def __call__[R, **P](self, f: Callable[P, Awaitable[R]], /, timeout: float|None=...) -> Callable[P, R]: '''The partial of `to_sync` under `loop=loop`.'''
def sync_await[T](aw: Awaitable[T], *, timeout: float|None=..., loop: AbstractEventLoop|None=...) -> T: '''Synchronously await the awaitable object `aw` under the given event loop `loop` with timeout `timeout`. It is preferred to use `asyncio.run` to synchronously run one single top-level async function that awaits the necessary awaitables.'''
@overload
def semaphore(bounded: Literal[False]=..., workers: int=...) -> Semaphore: '''Simple function to return a (bounded) semaphore of value `workers`.'''
@overload
def semaphore(bounded: Literal[True], workers: int=...) -> BoundedSemaphore: ...
def lockf[T, **P](f: Callable[P, Awaitable[T]], /, lf: type[AsyncLockLike]=...) -> Callable[P, Coroutine[Any, Any, T]]: '''Apply a lock that implements the async lock interface, as created by `lf`, to a function `f` that returns an awaitable, also converting it to an async function.'''
def sync_lock[R, **P](l: Lock, /, timeout: float|None=...) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, R]]: '''Decorator factory to ensure a function returning an awaitable only be called if a lock is acquired within `timeout`, also converting it to a sync function.'''
def sync_lock_from_binder[T, R, **P](f: Callable[[T], AsyncLockLike], /, timeout: float|None=...) -> Callable[[Callable[Concatenate[T, P], R]], Callable[Concatenate[T, P], R]]: '''Method version of `sync_lock`, where `binder` is a function returning a suitable lock from the instance.'''
def to_async[T, **P](f: Callable[P, T], /, loop: AbstractEventLoop|None=...) -> tuple[Callable[P, Coroutine[Any, Any, T]], Callable[[], None]]: '''Returns a tuple (asyncf, shutdown). asyncf is the async version of the original function (runs in an executor) and shutdown is a function to shut down the executor.'''
def get_aiter_fromf[T](f: Callable[[], Awaitable[T]], sentinel: T=..., /) -> AsyncGenerator[T, None]: '''Emulates the second form of the builtin iter function in async, which the aiter function does not have.'''
async def safe_cancel(t: Future) -> None: '''Cancel a single future and wait for the request to complete asynchronously. See `safe_cancel_batch` for a much more efficient way to cancel multiple futures at once.'''