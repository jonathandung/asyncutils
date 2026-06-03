'''Functions of utility one tier below the :mod:`base` submodule, such that they are not worth preloading but still quite useful.'''
from ._internal.types import AsyncLockLike, DCRV, DualContextManager, EventProt, ExceptionWrapper, ExcType, FutProt, IncompleteFut, SupportsIteration, ToSyncFromLoopRV, TransientBlockFromLoopRV
from .exceptions import IgnoreErrors
from asyncio import AbstractEventLoop, BoundedSemaphore, Event, Future, Lock, Semaphore, Task
from collections.abc import AsyncIterable, AsyncGenerator, Awaitable, Callable, Generator, Iterable
from contextlib import AbstractAsyncContextManager, AbstractContextManager
from ty_extensions import Not
from types import CoroutineType, TracebackType
from typing import Any, Concatenate, Literal, Never, overload
__all__ = 'aawcmf2dcmf', 'aawcmf2dcmff', 'afcopy', 'aiter_from_f', 'anullcontext', 'dcm', 'done_evt', 'done_fut', 'dualcontextmanager', 'get_future', 'ignore_cancellation', 'lockf', 'new_eager_tasks', 'safe_cancel', 'semaphore', 'sync_await', 'sync_lock', 'sync_lock_from_binder', 'to_async', 'to_sync', 'to_sync_from_loop', 'transient_block', 'transient_block_from_loop', 'wrap_in_coro'
ignore_cancellation: IgnoreErrors
'''Context manager to ignore :exc:`~asyncio.CancelledError`.'''
async def wrap_in_coro[T](aw: Awaitable[T], /) -> T: '''Return a coroutine resolving to the result of the awaitable ``aw``, such that it can be passed to :func:`asyncio.create_task`.'''
class anullcontext: # noqa: N801
    '''Simple async-only version of :class:`contextlib.nullcontext` that does not depend on :mod:`contextlib`.

    .. note:: This does not support the ``enter_result`` argument of the original.'''
    async def __aenter__(self) -> None: ...
    @overload
    async def __aexit__(self, exc_typ: ExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> None: ...
    @overload
    async def __aexit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> None: ...
@overload
def done_evt[E: EventProt](*, evtcls: type[E]) -> E: ...
@overload
def done_evt() -> Event: '''Return a new async event that is already set, with type ``evtcls`` if passed and :class:`asyncio.Event` by default.'''
@overload
def done_fut(exc: ExceptionWrapper, /, *, futcls: type[FutProt[Any]]) -> IncompleteFut[Never]: ...
@overload
def done_fut(res: None=..., *, futcls: type[FutProt[Any]]) -> IncompleteFut[None]: ...
@overload
def done_fut[T: Not[ExceptionWrapper]](res: T, *, futcls: type[FutProt[Any]]) -> IncompleteFut[T]: ...
@overload
def done_fut(exc: ExceptionWrapper, /) -> Future[Never]: ...
@overload
def done_fut(res: None=...) -> Future[None]: ...
@overload
def done_fut[T: Not[ExceptionWrapper]](res: T) -> Future[T]: '''Return a future that is already done with the result ``res`` or the exception wrapped by the wrapper ``exc`` if it is an exception wrapper returned by :func:`exceptions.wrap_exc`, with type ``futcls`` if passed and :class:`asyncio.Future` by default.'''
def afcopy[T, **P](f: Callable[P, Awaitable[T]], /) -> Callable[P, CoroutineType[Any, Any, T]]: '''Return a copy of the async function ``f`` with the same signature and attributes.'''
def get_future[T](aw: Awaitable[T], loop: AbstractEventLoop|None=...) -> Future[T]:
    '''| Wrap an arbitrary awaitable ``aw`` in a task under ``loop``, creating one and setting if required, and begin waiting on it.
    | Critical exceptions are wrapped in :exc:`~exceptions.Critical`.
    | This is as opposed to :meth:`~asyncio.loop.create_task`, which only takes coroutines.'''
def new_eager_tasks[T](*aws: Awaitable[T]) -> Generator[Task[T]]: '''Yield eagerly started tasks wrapping the coroutines under the running loop (or a new one that is set as the current if required) in order.'''
def to_sync[T, **P](f: Callable[P, Awaitable[T]], /, timeout: float|None=..., loop: AbstractEventLoop|None=...) -> Callable[P, T]: '''Convert a function that returns an awaitable to an sync function with the same signature, using the event loop ``loop`` when required or creating when necessary.'''
def to_sync_from_loop(loop: AbstractEventLoop) -> ToSyncFromLoopRV: '''A version of :func:`to_sync` that is a decorator factory, returning its partial under ``loop=loop``.'''
def sync_await[T](aw: Awaitable[T], *, timeout: float|None=..., loop: AbstractEventLoop|None=...) -> T: '''Synchronously await the awaitable object ``aw`` under the given event loop ``loop`` with timeout ``timeout``. It is preferred to use :func:`asyncio.run` to synchronously run one single top-level async function that awaits the necessary awaitables.'''
@overload
def semaphore(bounded: Literal[False]=..., workers: int=...) -> Semaphore: ...
@overload
def semaphore(bounded: Literal[True], workers: int=...) -> BoundedSemaphore: '''Simple helper function returning a (bounded) semaphore of value ``workers``, defaulting to :const:`context.SEMAPHORE_DEFAULT_VALUE`.'''
def lockf[T, **P](f: Callable[P, Awaitable[T]], /, lf: type[AsyncLockLike[Any]]=...) -> Callable[P, CoroutineType[Any, Any, T]]: '''Apply a lock that implements the async lock interface, as constructed and returned by ``lf``, to a function ``f`` that returns an awaitable, also converting it to an async function.'''
def sync_lock[T, **P](l: Lock, /, timeout: float|None=...) -> Callable[[Callable[P, Awaitable[T]]], Callable[P, T]]: '''Decorator factory to ensure a function returning an awaitable only be called if a lock is acquired within ``timeout``, also converting it to a sync function.'''
def sync_lock_from_binder[T, R, **P](f: Callable[[T], AsyncLockLike[Any]], /, timeout: float|None=...) -> Callable[[Callable[Concatenate[T, P], R]], Callable[Concatenate[T, P], R]]: '''Method version of :func:`sync_lock`, where ``binder`` is a function returning a suitable lock from the instance.'''
def to_async[T, **P](f: Callable[P, T], /) -> Callable[P, CoroutineType[Any, Any, T]]:
    '''| Return the async version of the original function with all the attributes from its instance dictionary, which runs in an executor lazy
    | initialized and shared by all :func:`to_async`-transformed callables.
    | If the argument was returned by :func:`to_sync`, a copy of the original async function is returned.

    .. warning:: This function may create reference cycles. If memory is a concern, call :func:`gc.collect` regularly.
    .. seealso::

      :class:`pools.AdvancedPool`
        an async-first thread pool executor-like class.'''
def aiter_from_f[T](f: Callable[[], Awaitable[T]], sentinel: T=..., /) -> AsyncGenerator[T]: '''Emulate the second form of the builtin :func:`iter` function in async, which the :func:`aiter` function does not have.'''
async def safe_cancel(fut: Future[Any], /) -> None:
    '''| Cancel a single future and wait for the cancellation to complete asynchronously.
    | Advertises itself as safe, because the cancellation itself can be reliably cancelled.

    .. seealso::

      :func:`~base.safe_cancel_batch`
        a much more efficient way to cancel multiple futures at once without compromising cancellability.'''
@overload
def transient_block[T, **P](loop: AbstractEventLoop, f: Callable[P, T], /, *a: P.args, **k: P.kwargs) -> Future[T]: ...
@overload
def transient_block[T](loop: AbstractEventLoop, f: Callable[..., T], /, *a: object, _threadsafe_: Literal[True], **k: object) -> Future[T]:
    '''| Run a sync function ``f``, with the provided parameters passed straight through, in the event loop ``loop``, and return an async future
    | resolving to its result or exception.
    | This function avoids incurring the overhead of calling :meth:`~asyncio.loop.run_in_executor` by instead scheduling the function to run at the
    | next iteration of the loop. To avoid overhead, the function should return fast.
    | If ``_threadsafe_`` is ``True``, then the function is scheduled in a thread-safe way, so that this can be called from threads not owning the loop.'''
def transient_block_from_loop(loop: AbstractEventLoop, *, threadsafe: bool=...) -> TransientBlockFromLoopRV: '''Return the partial of :func:`transient_block` under the specified `loop`.'''
@overload
def dualcontextmanager[T, **P](*, use_existing_executor: bool, strict: Literal[True]) -> Callable[[Callable[P, Iterable[T]]], Callable[P, AbstractContextManager[T, bool]]]: ...
@overload
def dualcontextmanager[T, **P](*, create_executor: bool, strict: Literal[True]) -> Callable[[Callable[P, Iterable[T]]], Callable[P, AbstractContextManager[T, bool]]]: ...
@overload
def dualcontextmanager[T, **P](*, use_existing_executor: bool, create_executor: bool, strict: Literal[True]) -> Callable[[Callable[P, Iterable[T]]], Callable[P, AbstractContextManager[T, bool]]]: ...
@overload
def dualcontextmanager[T, **P](*, use_existing_executor: bool, strict: Literal[False]) -> Callable[[Callable[P, Iterable[T]]], Callable[P, DualContextManager[T]]]: ...
@overload
def dualcontextmanager[T, **P](*, create_executor: bool, strict: Literal[False]) -> Callable[[Callable[P, Iterable[T]]], Callable[P, DualContextManager[T]]]: ...
@overload
def dualcontextmanager[T, **P](*, use_existing_executor: bool, create_executor: bool, strict: Literal[False]) -> Callable[[Callable[P, Iterable[T]]], Callable[P, DualContextManager[T]]]: ...
@overload
def dualcontextmanager(*, strict: Literal[True]) -> DCRV: ...
@overload
def dualcontextmanager[T, **P](*, strict: Literal[False]) -> Callable[[Callable[P, SupportsIteration[T]]], Callable[P, DualContextManager[T]]]: ...
@overload
def dualcontextmanager[T, **P](*, strict: bool=...) -> Callable[[Callable[P, SupportsIteration[T]]], Callable[P, DualContextManager[T]]]: ...
@overload
def dualcontextmanager[T, **P](gfunc: Callable[P, Iterable[T]], /, *, use_existing_executor: bool=..., create_executor: bool=..., strict: Literal[True]) -> Callable[P, AbstractContextManager[T, bool]]: ...
@overload
def dualcontextmanager[T, **P](gfunc: Callable[P, Iterable[T]], /, *, use_existing_executor: bool=..., create_executor: bool=..., strict: Literal[False]) -> Callable[P, DualContextManager[T]]: ...
@overload
def dualcontextmanager[T, **P](gfunc: Callable[P, Iterable[T]], /, *, use_existing_executor: bool=..., create_executor: bool=..., strict: bool=...) -> Callable[P, DualContextManager[T]]: ...
@overload
def dualcontextmanager[T, **P](agfunc: Callable[P, AsyncIterable[T]], /, *, strict: Literal[True]) -> Callable[P, AbstractAsyncContextManager[T, bool]]: ...
@overload
def dualcontextmanager[T, **P](agfunc: Callable[P, AsyncIterable[T]], /, *, strict: Literal[False]) -> Callable[P, DualContextManager[T]]: ...
@overload
def dualcontextmanager[T, **P](agfunc: Callable[P, AsyncIterable[T]], /, *, strict: bool=...) -> Callable[P, DualContextManager[T]]: '''Convert a callable that returns an (async) iterable, usually an (async) generator function, over exactly one item, into a function returning a non-reusable sync- and async-compatible context manager. Essentially combines :func:`contextlib.contextmanager` and :func:`contextlib.asynccontextmanager` into one decorator.'''
def dcm[T, **P](f: Callable[P, SupportsIteration[T]], /) -> Callable[P, DualContextManager[T]]: '''Equivalent to :func:`dualcontextmanager` with the default arguments at the time of definition, rather than when the function is decorated.'''
def aawcmf2dcmff[T, **P](*, use_existing_executor: bool=..., create_executor: bool=..., strict: bool=...) -> Callable[[Callable[P, Awaitable[AbstractContextManager[T]|AbstractAsyncContextManager[T]]]], Callable[P, DualContextManager[T]]]: '''A decorator factory converting a function giving an awaitable resolving to an async context manager into a function returning a non-reusable dual context manager using :func:`dualcontextmanager`.'''
def aawcmf2dcmf[T, **P](f: Callable[P, Awaitable[AbstractContextManager[T]|AbstractAsyncContextManager[T]]], /) -> Callable[P, DualContextManager[T]]: '''Equivalent to `aawcmf2dcmff()(f)`.'''