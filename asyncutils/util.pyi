'''Functions of utility one tier below the :mod:`base` submodule, such that they are not worth preloading but still quite useful.'''
from ._internal.types import AsyncLockLike, DualContextManager, SupportsIteration, ToSyncFromLoopRV, TransientBlockFromLoopRV, ExcType
from .exceptions import IgnoreErrors
from _collections_abc import AsyncGenerator, Awaitable, Callable, Coroutine, Generator
from asyncio.events import AbstractEventLoop
from asyncio.futures import Future
from asyncio.locks import BoundedSemaphore, Lock, Semaphore
from asyncio.tasks import Task
from types import TracebackType
from typing import Any, Concatenate, Literal, overload
__all__ = 'aiter_from_f', 'anullcontext', 'dualcontextmanager', 'get_future', 'ignore_cancellation', 'lockf', 'new_tasks', 'safe_cancel', 'semaphore', 'sync_await', 'sync_lock', 'sync_lock_from_binder', 'to_async', 'to_sync', 'to_sync_from_loop', 'transient_block', 'transient_block_from_loop'
ignore_cancellation: IgnoreErrors
'''Context manager to ignore :exc:`~asyncio.exceptions.CancelledError`.'''
class anullcontext: # noqa: N801
    '''Simple async-only version of :class:`contextlib.nullcontext`, implemented here to avoid importing :mod:`contextlib`.'''
    async def __aenter__(self) -> None: ...
    @overload
    async def __aexit__(self, exc_typ: ExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> None: ...
    @overload
    async def __aexit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> None: ...
def get_future[T](aw: Awaitable[T], loop: AbstractEventLoop|None=...) -> Future[T]:
    '''Wrap an arbitrary awaitable `aw` in a task under `loop`, creating one and setting if required, and begin waiting on it.
    Critical exceptions are wrapped in :exc:`~exceptions.Critical`.
    This is as opposed to :meth:`~asyncio.base_events.BaseEventLoop.create_task`, which only takes coroutines.'''
def new_tasks[T](*coro: Coroutine[Any, Any, T]) -> Generator[Task[T]]: '''Yield eagerly started tasks wrapping the coroutines under a new event loop in order.'''
def to_sync[T, **P](f: Callable[P, Awaitable[T]], /, timeout: float|None=..., loop: AbstractEventLoop|None=...) -> Callable[P, T]: '''Convert a function that returns an awaitable to an sync function with the same signature, using the event loop `loop` when required or creating when necessary.'''
def to_sync_from_loop(loop: AbstractEventLoop) -> ToSyncFromLoopRV: '''A version of :func:`to_sync` that is a decorator factory, returning its partial under `loop=loop`.'''
def sync_await[T](aw: Awaitable[T], *, timeout: float|None=..., loop: AbstractEventLoop|None=...) -> T: '''Synchronously await the awaitable object `aw` under the given event loop `loop` with timeout `timeout`. It is preferred to use :func:`asyncio.run` to synchronously run one single top-level async function that awaits the necessary awaitables.'''
@overload
def semaphore(bounded: Literal[False]=..., workers: int=...) -> Semaphore: ...
@overload
def semaphore(bounded: Literal[True], workers: int=...) -> BoundedSemaphore: '''Simple helper to return a (bounded) semaphore of value `workers`, default :const:`context.SEMAPHORE_DEFAULT_VALUE`.'''
def lockf[T, **P](f: Callable[P, Awaitable[T]], /, lf: type[AsyncLockLike[Any]]=...) -> Callable[P, Coroutine[Any, Any, T]]: '''Apply a lock that implements the async lock interface, as created by `lf`, to a function `f` that returns an awaitable, also converting it to an async function.'''
def sync_lock[T, **P](l: Lock, /, timeout: float|None=...) -> Callable[[Callable[P, Awaitable[T]]], Callable[P, T]]: '''Decorator factory to ensure a function returning an awaitable only be called if a lock is acquired within `timeout`, also converting it to a sync function.'''
def sync_lock_from_binder[T, R, **P](f: Callable[[T], AsyncLockLike[Any]], /, timeout: float|None=...) -> Callable[[Callable[Concatenate[T, P], R]], Callable[Concatenate[T, P], R]]: '''Method version of :func:`sync_lock`, where `binder` is a function returning a suitable lock from the instance.'''
def to_async[T, **P](f: Callable[P, T], /, loop: AbstractEventLoop|None=...) -> Callable[P, Coroutine[Any, Any, T]]: '''Return the async version of the original function (runs in an executor).'''
def aiter_from_f[T](f: Callable[[], Awaitable[T]], sentinel: T=..., /) -> AsyncGenerator[T]: '''Emulate the second form of the builtin :func:`iter` function in async, which the :func:`aiter` function does not have.'''
async def safe_cancel(fut: Future[Any], /) -> None:
    '''Cancel a single future and wait for the cancellation to complete asynchronously. The cancellation itself can be reliably cancelled.
    See :func:`~base.safe_cancel_batch` for a much more efficient way to cancel multiple futures at once.'''
@overload
def transient_block[T, **P](loop: AbstractEventLoop, f: Callable[P, T], /, *a: P.args, **k: P.kwargs) -> Future[T]: ...
@overload
def transient_block[T](loop: AbstractEventLoop, f: Callable[..., T], /, *a: Any, _threadsafe_: Literal[True], **k: Any) -> Future[T]: # type: ignore[overload-cannot-match]
    '''Run a function `f`, with the provided parameters passed straight through, in the event loop `loop`, and return a future for it.
    Assumes the loop is already running, so that its :meth:`run_in_executor` method is not used.
    Instead, schedule the function to run at the next iteration of the loop. To avoid overhead, the function should thus return fast.
    If `_threadsafe_` is `True`, then the function is scheduled in a thread-safe way, so that this can be called from threads not owning the loop.'''
def transient_block_from_loop(loop: AbstractEventLoop, *, threadsafe: bool=...) -> TransientBlockFromLoopRV: '''Return the partial of :func:`transient_block` under the specified `loop`.'''
def dualcontextmanager[T, **P](func: Callable[P, SupportsIteration[T]], /) -> Callable[P, DualContextManager[T]]: '''Convert a callable that returns an (async) iterable, usually an (async) generator function, over exactly one item, into a function returning a non-reusable sync- and async-compatible context manager. Essentially combines :func:`contextlib.contextmanager` and :func:`contextlib.asynccontextmanager` into one decorator.'''