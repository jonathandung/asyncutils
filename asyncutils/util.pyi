'''Functions of utility one tier below the `base` submodule, such that they are not worth preloading but still quite useful.'''
from ._internal.types import AsyncLockLike
from .exceptions import IgnoreErrors
from _collections_abc import AsyncGenerator, Awaitable, Callable, Coroutine, Generator
from asyncio.events import AbstractEventLoop
from asyncio.futures import Future
from asyncio.locks import BoundedSemaphore, Lock, Semaphore
from asyncio.tasks import Task
from typing import Any, Concatenate, Literal, overload
__all__ = 'aiter_from_f', 'get_future', 'lockf', 'new_tasks', 'safe_cancel', 'semaphore', 'sync_await', 'sync_lock', 'sync_lock_from_binder', 'to_async', 'to_sync', 'to_sync_from_loop'
_ignore_cancellation: IgnoreErrors
'''Context manager to ignore asyncio.CancelledError. This annotation is for module-internal use only.'''
def get_future[T](aw: Awaitable[T], loop: AbstractEventLoop|None=...) -> Future[T]:
    '''Wrap an arbitrary awaitable in a task under the provided event loop `loop`, creating one and setting if required, and begin waiting on it.
    Critical exceptions are wrapped in `Critical`.
    This is as opposed to `loop.create_task`, which only takes coroutines.'''
def new_tasks[T](*coro: Coroutine[Any, Any, T]) -> Generator[Task[T]]: '''Yield eagerly started tasks wrapping the coroutines under a new event loop in order.'''
def to_sync[T, **P](f: Callable[P, Awaitable[T]], /, timeout: float|None=..., loop: AbstractEventLoop|None=...) -> Callable[P, T]: '''Convert a function that returns an awaitable to an sync function with the same signature, using the event loop `loop` when required or creating when necessary.'''
class to_sync_from_loop: # noqa: N801
    '''A version of `to_sync` that is a decorator factory. Not a class at runtime.'''
    def __init__(self, loop: AbstractEventLoop): '''Convert an async function to synchronous by running it in the specified `loop`'''
    def __call__[R, **P](self, f: Callable[P, Awaitable[R]], /, timeout: float|None=...) -> Callable[P, R]: '''The partial of `to_sync` under `loop=loop`.'''
def sync_await[T](aw: Awaitable[T], *, timeout: float|None=..., loop: AbstractEventLoop|None=...) -> T: '''Synchronously await the awaitable object `aw` under the given event loop `loop` with timeout `timeout`. It is preferred to use `asyncio.run` to synchronously run one single top-level async function that awaits the necessary awaitables.'''
@overload
def semaphore(bounded: Literal[False]=..., workers: int=...) -> Semaphore: ...
@overload
def semaphore(bounded: Literal[True], workers: int=...) -> BoundedSemaphore: '''Simple helper to return a (bounded) semaphore of value `workers`.'''
def lockf[T, **P](f: Callable[P, Awaitable[T]], /, lf: type[AsyncLockLike[Any]]=...) -> Callable[P, Coroutine[Any, Any, T]]: '''Apply a lock that implements the async lock interface, as created by `lf`, to a function `f` that returns an awaitable, also converting it to an async function.'''
def sync_lock[T, **P](l: Lock, /, timeout: float|None=...) -> Callable[[Callable[P, Awaitable[T]]], Callable[P, T]]: '''Decorator factory to ensure a function returning an awaitable only be called if a lock is acquired within `timeout`, also converting it to a sync function.'''
def sync_lock_from_binder[T, R, **P](f: Callable[[T], AsyncLockLike[Any]], /, timeout: float|None=...) -> Callable[[Callable[Concatenate[T, P], R]], Callable[Concatenate[T, P], R]]: '''Method version of `sync_lock`, where `binder` is a function returning a suitable lock from the instance.'''
def to_async[T, **P](f: Callable[P, T], /, loop: AbstractEventLoop|None=...) -> tuple[Callable[P, Coroutine[Any, Any, T]], Callable[[], None]]: '''Returns a tuple (asyncf, shutdown). asyncf is the async version of the original function (runs in an executor) and shutdown is a function to shut down the executor.'''
def aiter_from_f[T](f: Callable[[], Awaitable[T]], sentinel: T=..., /) -> AsyncGenerator[T]: '''Emulates the second form of the builtin iter function in async, which the aiter function does not have.'''
async def safe_cancel(t: Future[Any]) -> None: '''Cancel a single future and wait for the request to complete asynchronously. See `safe_cancel_batch` for a much more efficient way to cancel multiple futures at once.'''