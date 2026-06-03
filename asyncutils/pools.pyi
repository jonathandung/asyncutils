'''This module provides various pool implementations for concurrent execution and resource management in asynchronous contexts.'''
from ._internal.types import SupportsIteration, ExcType
from .config import Executor
from .mixins import LoopBoundMixin, LoopContextMixin
from asyncio import Future
from collections.abc import Callable, Iterable, Mapping
from types import TracebackType
from typing import Any, Self, overload
__all__ = 'AdvancedPool', 'ConnectionPool'
class AdvancedPool(LoopContextMixin):
    '''A pool implementation used to call sync functions concurrently in an async-first interface, managing event loop and threading resource shenanigans internally.

    .. caution:: Use instances of this class as async context managers only.'''
    def __init__(self, max_workers: int=..., min_workers: int=..., qsize: int=..., scaling: bool=..., kill_at_exit: bool=...):
        '''All arguments are optional:

        * `max_workers` controls the maximum number of workers (threads) that can run concurrently. Defaults to :const:`context.ADVANCED_POOL_DEFAULT_MAX_WORKERS`.
        * `min_workers` determines the least number of threads there will be at any instance. Defaults to :const:`context.ADVANCED_POOL_DEFAULT_MIN_WORKERS`.
        * `qsize` sets the maximum number of pending tasks that can be queued. If not passed, there is no limit.
        * `scaling` enables dynamic scaling of the pool based on workload. The default is ``True``.
        * `kill_at_exit` determines whether the shut down when the context manager exits should be immediate. Default ``False``.'''
    def raise_for_shutdown(self) -> None: '''Raise :exc:`~exceptions.PoolShutDown` if the pool is shutting down or has been shut down.'''
    @overload
    def submit_nowait[T, **P](self, f: Callable[P, T], *a: P.args, **k: P.kwargs) -> Future[T]: ...
    @overload
    def submit_nowait[T](self, f: Callable[..., T], *a: object, _priority_: int, **k: object) -> Future[T]: '''Schedule a sync function to be executed in a worker thread, raising :exc:`asyncio.QueueFull` if there is not enough space in the internal queue from which workers fetch tasks, and get an async future to access its result.'''
    @overload
    async def submit[T, **P](self, f: Callable[P, T], *a: P.args, **k: P.kwargs) -> Future[T]: ...
    @overload
    async def submit[T](self, f: Callable[..., T], *a: object, _priority_: int, **k: object) -> Future[T]: '''Schedule a sync function to be executed in a worker thread, waiting asynchronously until there is enough space in the internal queue from which workers fetch tasks if necessary, and get an async future to access its result.'''
    @overload
    async def complete[T, **P](self, f: Callable[P, T], *a: P.args, **k: P.kwargs) -> T: ...
    @overload
    async def complete[T](self, f: Callable[..., T], *a: object, _priority_: int, **k: object) -> T: '''Wait for a sync function to complete its execution by the pool asynchronously and get its result.'''
    async def shutdown(self, cancel_pending: bool=..., idle_timeout: float|None=..., total_timeout: float|None=...) -> float: '''Shut down the pool, waiting for all workers to finish their current tasks and exit. If `cancel_pending` is ``True``, pending tasks that have not been picked up by workers will be cancelled immediately. If `idle_timeout` is passed, it will limit the time waiting to join the task queue.'''
    async def join(self) -> list[int|BaseException]: '''Return a list containing the nunmber of tasks completed by each worker in a random order or an exception if a worker thread has been terminated by an unhandled exception.'''
    @overload
    async def map[R, T](self, f: Callable[[R], T], it: SupportsIteration[R], /, *, priority: int=..., strict: bool=...) -> list[T]: ...
    @overload
    async def map[R, V, T](self, f: Callable[[R, V], T], i1: SupportsIteration[R], i2: SupportsIteration[V], /, *, priority: int=..., strict: bool=...) -> list[T]: ...
    @overload
    async def map[R, V, U, T](self, f: Callable[[R, V, U], T], i1: SupportsIteration[R], i2: SupportsIteration[V], i3: SupportsIteration[U], /, *, priority: int=..., strict: bool=...) -> list[T]: ...
    @overload
    async def map[R, V, U, S, T](self, f: Callable[[R, V, U, S], T], i1: SupportsIteration[R], i2: SupportsIteration[V], i3: SupportsIteration[U], i4: SupportsIteration[S], /, *, priority: int=..., strict: bool=...) -> list[T]: ...
    @overload
    async def map[T](self, f: Callable[..., T], /, *its: SupportsIteration[Any], priority: int=..., strict: bool=...) -> list[T]: '''Apply the function `f` to the items from the iterables in a concurrent manner, returning the results in a list. If `strict` is ``True``, all iterables must have the same length.'''
    async def starmap[T, *Ts](self, f: Callable[[*Ts], T], it: SupportsIteration[tuple[*Ts]], /, priority: int=...) -> list[T]: '''Like :meth:`map`, but the iterables should yield tuples that are unpacked as arguments to the function.'''
    async def doublestarmap[T](self, f: Callable[..., T], it: SupportsIteration[Mapping[str, Any]], /, priority: int=...) -> list[T]: '''Like :meth:`map`, but the iterable should yield dicts that are unpacked as keyword arguments to the function.'''
    async def starmap_with_kwds[T](self, f: Callable[..., T], it: SupportsIteration[tuple[SupportsIteration[Any], Mapping[str, Any]]], /, priority: int=...) -> list[T]: '''Like :meth:`map`, but the iterable should yield tuples of the form ``(args, kwargs)``, where `args` is an iterable of positional arguments and `kwargs` is a mapping of keyword arguments.'''
    async def resize(self, min_workers: int, max_workers: int) -> None: '''Adjust the lower and upper limits of the pool size, and destroy or spawn threads accordingly.'''
    async def drain(self) -> None: '''Wait until all pending tasks have been completed.'''
    async def wait_for_slot(self, timeout: float|None=...) -> float: '''Wait until there is a slot in the internal queue for pending tasks, and return the time spent waiting. If `timeout` is passed, it will limit the waiting time.'''
    async def __cleanup__(self) -> None: ...
    def __del__(self) -> None: '''Shut down the pool synchronously with a timeout of 0.2 seconds if needed. To avoid this blocking up the GC process, shut down the pool explicitly by using it as an async context manager.'''
    @property
    def full(self) -> bool: '''Return whether the internal queue for pending tasks is full, such that :meth:`wait_for_slot` will block.'''
    @property
    def empty(self) -> bool: '''Return whether the internal queue for pending tasks is empty.'''
    @property
    def qsize(self) -> int: '''Return the current number of pending tasks in the internal queue.'''
    @property
    def idle(self) -> bool: '''Return whether all workers are idle, i.e. not executing any tasks currently. This also implies :attr:`empty` is ``True``.'''
    @property
    def uptime(self) -> float: '''Return the time in seconds since the pool started.'''
    @property
    def completed(self) -> int: '''Return the total number of tasks completed by the pool.'''
class ConnectionPool[T, **P](LoopBoundMixin):
    '''A pool managing resources in a simple and intuitive lock interface, with support for health checking, auto-recycling and dynamic rescaling.

    .. caution:: Use instances of this class as async context managers only.'''
    def __init__(self, factory: Callable[P, T], maxsize: int=..., minsize: int=..., maxlife: float=..., healthchecker: Callable[[T], bool]|None=..., cleaner: Callable[[T], None]|None=...):
        '''All arguments except `factory`, which should be a callable returning a connection, are optional:

        * `maxsize` controls the maximum number of connections that can be created. Defaults to :const:`context.CONNECTION_POOL_DEFAULT_MAX_SIZE`.
        * `minsize` determines the least number of connections that will be maintained at any instance. Defaults to :const:`context.CONNECTION_POOL_DEFAULT_MIN_SIZE`.
        * `maxlife` sets the maximum lifetime of a connection in seconds, after which it will be recycled. Defaults to :const:`context.CONNECTION_POOL_DEFAULT_MAX_LIFE`.
        * `healthchecker` is a function that takes a connection and returns whether it is healthy. If not passed, connections are assumed to always be healthy.
        * `cleaner` is a function that takes a connection and performs necessary cleanup before it is recycled. If not passed, no cleanup will be performed.'''
    def _is_healthy(self, conn: T, /) -> bool: ...
    @overload
    async def create_connection(self, *a: P.args, **k: P.kwargs) -> T: '''Call the connection factory with the given parameters and return a new connection'''
    @overload
    async def create_connection(self, *a: object, _executor_: Executor|None, **k: object) -> T: ...
    async def acquire(self, *a: P.args, **k: P.kwargs) -> T: '''Acquire a connection from the pool, waiting asynchronously until one is available if necessary. The arguments will be passed to the connection factory when creating new connections if needed.'''
    async def release(self, conn: T, /, *a: P.args, **k: P.kwargs) -> None: '''Release a connection back to the pool after use. The arguments will be passed to the connection factory when creating new connections if needed, and can be used by the cleaner for cleanup if necessary.'''
    async def _maintain(self) -> None: ...
    async def start(self, akgen: SupportsIteration[tuple[Iterable[Any], Mapping[str, Any]]]|None=..., executor: Executor|None=...) -> None: '''Spawn the connections using the arguments from the parameter generator. The factory is run in the executor passed to make it async.'''
    async def stop(self) -> None: '''Close all connections and stop the pool.'''
    async def __aenter__(self) -> Self: '''Start and return the pool.'''
    @overload
    async def __aexit__(self, exc_typ: ExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> None: ...
    @overload
    async def __aexit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> None: '''Stop the pool, closing all connections.'''
    @property
    def currsize(self) -> int: '''The current number of connections managed by the pool, including those in use and those available.'''
    @property
    def available(self) -> int: '''The number of connections currently available for acquisition.'''
    @property
    def in_use(self) -> int: '''The number of connections currently in use.'''
    @property
    def maxsize(self) -> int: '''The maximum number of connections that can be created by the pool.'''
    @property
    def minsize(self) -> int: '''The minimum number of connections that will be maintained by the pool.'''
    @property
    def maxlife(self) -> float: '''The maximum lifetime of a connection in seconds.'''