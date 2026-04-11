'''Extensions of `asyncio.Queue` with more methods and password protection, and a PotentQueueBase ABC.'''
from ._internal.protocols import SupportsIteration, B, G, P
from .exceptions import IgnoreErrors
from .mixins import EventualLoopMixin
from _collections_abc import AsyncGenerator, Awaitable, Callable, Coroutine, Generator
from abc import ABC, abstractmethod
from asyncio.futures import Future
from asyncio.queues import Queue
from contextlib import _AsyncGeneratorContextManager
from typing import Any, Final, Literal, Self, overload
__all__ = 'PotentQueueBase', 'SmartLifoQueue', 'SmartPriorityQueue', 'SmartQueue', 'UserPriorityQueue', 'ignore_qempty', 'ignore_qerrs', 'ignore_qfull', 'ignore_qshutdown', 'ignore_valerrs', 'password_queue'
ignore_qshutdown: Final[IgnoreErrors]
'''Instance of IgnoreErrors that suppresses asyncio.QueueShutDown.'''
ignore_qempty: Final[IgnoreErrors]
'''Instance of IgnoreErrors that suppresses asyncio.QueueShutDown and asyncio.QueueEmpty.'''
ignore_qfull: Final[IgnoreErrors]
'''Instance of IgnoreErrors that suppresses asyncio.QueueShutDown and asyncio.QueueFull.'''
ignore_qerrs: Final[IgnoreErrors]
'''Instance of IgnoreErrors that suppresses all asyncio queue-related errors.'''
ignore_valerrs: Final[IgnoreErrors]
'''Instance of IgnoreErrors that suppresses ValueError.'''
@overload
def password_queue[T, R](password_put: R, *, maxsize: int=..., protect_get: Literal[False]=..., protect_put: Literal[True]=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., put_from: str=..., puttyp: type[R]=..., init_items: SupportsIteration[T]=[]) -> P[R, T]:
    '''Returns a password-protected queue, the type of which does not inherit from `asyncio.Queue` but has the same interface, with maximum size `maxsize`. `priority` and `lifo` parameters determine if the queue is a priority queue and last-in-first-out.
    If `protect_get` is True, get and get_nowait will require a password, specified by password_get or retrieved from a variable in the caller's scope with name `get_from` (default `password`).
    If `protect_put` is True, put and put_nowait will require a password, specified by password_put or retrieved from a variable in the caller's scope with name `put_from` (default `password`).
    If `init_items` is specified, the items in that (async) iterable will be arranged to enter the queue.'''
@overload
def password_queue[T, R](*, maxsize: int=..., protect_get: Literal[False]=..., protect_put: Literal[True]=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., put_from: str=..., puttyp: type[R]=object, init_items: SupportsIteration[T]=[]) -> P[R, T]: ... # type: ignore[assignment]
@overload
def password_queue[T, R](*, password_get: R, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[False], can_change_get: bool=..., priority: bool=..., lifo: bool=..., get_from: str=..., gettyp: type[R]=..., init_items: SupportsIteration[T]=[]) -> G[R, T]: ...
@overload
def password_queue[T, R](*, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[False], can_change_get: bool=..., priority: bool=..., lifo: bool=..., get_from: str=..., gettyp: type[R]=object, init_items: SupportsIteration[T]=[]) -> G[R, T]: ... # type: ignore[assignment]
@overload
def password_queue[T, R, V](password_put: V, password_get: R, maxsize: int=..., *, protect_get: Literal[True], protect_put: Literal[True]=..., can_change_get: bool=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., get_from: str=..., put_from: str=..., gettyp: type[R]=..., puttyp: type[V]=..., init_items: SupportsIteration[T]=[]) -> B[R, V, T]: ...
@overload
def password_queue[T, R, V](password_put: V, *, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[True]=..., can_change_get: bool=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., get_from: str=..., put_from: str=..., gettyp: type[R]=object, puttyp: type[V]=..., init_items: SupportsIteration[T]=[]) -> B[R, V, T]: ... # type: ignore[assignment]
@overload
def password_queue[T, R, V](*, password_get: R, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[True]=..., can_change_get: bool=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., get_from: str=..., put_from: str=..., gettyp: type[R]=..., puttyp: type[V]=object, init_items: SupportsIteration[T]=[]) -> B[R, V, T]: ... # type: ignore[assignment]
@overload
def password_queue[T, R, V](*, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[True]=..., can_change_get: bool=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., get_from: str=..., put_from: str=..., gettyp: type[R]=object, puttyp: type[V]=object, init_items: SupportsIteration[T]=[]) -> B[R, V, T]: ... # type: ignore[assignment]
class PotentQueueBase[T](Queue[T], EventualLoopMixin, ABC):
    '''A base class for queues with much more methods, async- and sync-compatible.'''
    @abstractmethod
    def _init(self, maxsize: int) -> None: '''Initialize the queue given `maxsize`; called in `__init__`.'''
    @abstractmethod
    def _get(self) -> T: '''Get an item from the queue if not empty; called in `get` and `get_nowait`.'''
    @abstractmethod
    def _put(self, item: T) -> None: '''Put an item into the queue if not empty; called in `put` and `put_nowait`.'''
    @abstractmethod
    def peek_all(self) -> list[T]: '''Return a list of all the items in the queue.'''
    @abstractmethod
    def qsize(self) -> int: '''Return the size of the queue as an integer.'''
    async def smart_put(self, item: T, *, timeout: float|None=..., raising: bool=...) -> bool|None: '''Call put_nowait if a slot is immediately available, waiting for a slot with `timeout` otherwise; if the timeout expires and `raising` is True, throw TimeoutError.'''
    async def smart_get(self, *, timeout: float|None=..., default: T=...) -> T: '''Call get_nowait if an item is immediately available, waiting for a item with `timeout` otherwise; if the timeout expires and `default` is provided, return it.'''
    async def extend(self, it: SupportsIteration[T], timeout: float|None=...) -> None: '''Add the items from `it` into the queue within `timeout`.'''
    def sync_put(self, item: T, *, timeout: float|None=...) -> bool|None: '''Put an item into the queue synchronously. If that functionality is needed, you likely should be using a synchronous queue.'''
    def sync_get(self, *, timeout: float|None=..., default: T=...) -> T: '''Get an item from the queue synchronously. Above remark applies.'''
    def push(self, item: T) -> bool: '''Put an item into the queue immediately, popping if necessary; returns success.'''
    def drain_persistent(self, max: int|None=..., timeout: float|None=...) -> AsyncGenerator[T]: '''An async generator that gets items from the queue once available and yields them.'''
    def drain_until_empty(self, max: int|None=...) -> Generator[T]: '''A synchronous generator that gets items from the queue until it is emptied and returns.'''
    def drain_retlist(self, max: int|None=...) -> list[T]: '''Return a list of the items in the queue and empty it.'''
    def empty(self) -> bool: '''Whether the queue is empty.'''
    def __bool__(self) -> bool: '''Whether there are items in the queue.'''
    __iter__, __aiter__ = drain_until_empty, drain_persistent # noqa: PYI017
    def shutdown(self, immediate: bool=...) -> None: '''Shut down the queue. If `immediate` is True, pending gets raise immediately even if the queue is not empty.'''
    @property
    def is_shutdown(self) -> bool: '''Whether the queue is shutting down or has been shutdown.'''
    @is_shutdown.setter
    def is_shutdown(self, val: bool, /) -> None: ...
    @property
    def can_put_now(self) -> bool: '''Whether items can be put into the queue without blocking at this instant.'''
    @property
    def can_get_now(self) -> bool: '''Whether items can be get from the queue without blocking at this instant.'''
    @property
    def fully_functional(self) -> bool: '''queue.fully_functional == queue.can_put_now and queue.can_get_now.'''
    @property
    def capacity(self) -> int|float: '''The capacity of the queue. Can be float('inf').'''
    @property
    def remaining_capacity(self) -> int|float: '''The remaining number of slots in the queue. Can be float('inf').'''
    @property
    def utilization_rate(self) -> float: '''The number of items the queue divided by its capacity.'''
    def pushpop_nowait(self, item: T, raising: bool=...) -> T: '''Push an item into the queue and pop from the other end immediately.'''
    def poppush_nowait(self, item: T, raising: bool=...) -> T: '''Pop an item from the queue and push into the other end immediately.'''
    async def pushpop(self, item: T) -> T: '''The above, but done asynchronously and not immediately.'''
    async def poppush(self, item: T) -> T: '''Similar.'''
    def clear(self) -> None: '''Clear all the entries from the queue.'''
    def transaction(self) -> _AsyncGeneratorContextManager[Self]:
        '''Return an async context manager which begins a transaction on entry.
        If an error occurs within the context, the original items in the queue are restored and the error reraised, unless the error is critical and
        deemed to require immediate exit; otherwise, the transaction completes successfully and changes are committed on exit.'''
    @overload
    def map[R](self, f: Callable[[T], Awaitable[R]], stop_when: Future[None]|None=..., *, lifo: Literal[False]=...) -> SmartQueue[R]: ...
    @overload
    def map[R](self, f: Callable[[T], Awaitable[R]], stop_when: Future[None]|None=..., *, lifo: Literal[True]) -> SmartLifoQueue[R]: '''Return a queue that contains items from this queue with the function applied on each of them, emptying this queue in the process (transformation analogous to `builtins.map`).'''
    @overload
    def starmap[R, *Ts](self: PotentQueueBase[tuple[*Ts]], f: Callable[[*Ts], Awaitable[R]], stop_when: Future[None]|None=..., *, lifo: Literal[False]=...) -> SmartQueue[R]: ...
    @overload
    def starmap[R, *Ts](self: PotentQueueBase[tuple[*Ts]], f: Callable[[*Ts], Awaitable[R]], stop_when: Future[None]|None=..., *, lifo: Literal[True]) -> SmartLifoQueue[R]: '''Return a queue that contains items from this queue with the function applied on each of them starred, emptying this queue in the process (transformation analogous to `itertools.starmap`).'''
    @overload
    def filter(self, pred: Callable[[T], bool]=..., *, lifo: Literal[False]=...) -> SmartQueue[T]: '''Return a new queue from which getters can get the items in this queue that satisfy the predicate; items remaining in the original queue did not satisfy the predicate.'''
    @overload
    def filter(self, pred: Callable[[T], bool]=..., *, lifo: Literal[True]) -> SmartLifoQueue[T]: ...
    @overload
    def enumerate(self, *, lifo: Literal[False]=...) -> SmartQueue[tuple[int, T]]: '''Return a queue containing the items from enumerate applied on this queue and empty it in the process.'''
    @overload
    def enumerate(self, *, lifo: Literal[True]) -> SmartLifoQueue[tuple[int, T]]: ...
    def map_nowait[R](self, f: Callable[[T], Coroutine[Any, Any, R]], /) -> list[R]: '''Return a list containing the return values of the function applied on the items in the queue, emptying the queue.'''
    def starmap_nowait[R](self, f: Callable[..., Coroutine[Any, Any, R]], /) -> list[R]: '''Return a list containing the return values of the function applied on the items in the queue, starred,, emptying the queue.'''
    def filter_nowait(self, pred: Callable[[T], bool]=..., /) -> tuple[list[T], int]: '''Filter items in the queue by a predicate and return a list of removed items and an integer; the items in the returned list after the index corresponding to that integer were items rejected from the queue due to the queue being full.'''
    def enumerate_nowait(self) -> Generator[tuple[int, T], None, None]: '''Equivalent to `await iters.to_list(queue.drain_persistent())`.'''
class SmartQueue[T](PotentQueueBase[T]):
    def _init(self, maxsize: int) -> None: ...
    def _get(self) -> T: ...
    def _put(self, item: T) -> None: ...
    def peek(self) -> T: '''Look at the item that would be returned by `get` or `get_nowait` without actually getting it.'''
    def peek_all(self) -> list[T]: ...
    def qsize(self) -> int: ...
    def rotate(self, n: int=..., /) -> None: '''Rotate the items in the queue by `n` indices synchronously, which can be negative.'''
class SmartLifoQueue[T](PotentQueueBase[T]):
    def _init(self, maxsize: int) -> None: ...
    def _get(self) -> T: ...
    def _put(self, item: T) -> None: ...
    def peek(self, i: int=..., /) -> T: '''Look at the item at index `i`, defaulting to the item most recently put in (that would be returned by `get` or `get_nowait`).'''
    def peek_all(self) -> list[T]: ...
    def qsize(self) -> int: ...
class SmartPriorityQueue[T](PotentQueueBase[T]):
    '''A priority queue, where the priority of each item is determined by comparing it to other items.'''
    def __init__(self, maxsize: int=..., *, init_items: SupportsIteration[T]=[]): ...
    def _init(self, maxsize: int) -> None: ...
    def _get(self) -> T: ...
    def _put(self, item: T) -> None: ...
    def peek(self) -> T: '''Look at the item that would be returned by `get` or `get_nowait` without actually getting it.'''
    def peek_all(self) -> list[T]: ...
    def qsize(self) -> int: ...
class UserPriorityQueue[T](SmartPriorityQueue[tuple[int, int, T]]):
    '''A priority queue, where you put in items with an integer priority and the items are retrieved in ascending order of priority, with earlier items taking precedence in case of ties.'''
    @classmethod
    def from_iter_of_tuples(cls, items: SupportsIteration[tuple[int, int, T]], maxsize: int=...) -> Self: '''Build a queue from the (async) iterable of tuples (priority, tiebreak, item).'''
    def __init__(self, maxsize: int=..., *, init_priority: int=..., init_items: SupportsIteration[T]=[]): ...
    def put_nowait(self, item: T, priority: int=...) -> None: ... # type: ignore[override]
    def get_nowait(self) -> T: ... # type: ignore[override]
    async def put(self, item: T, priority: int=...) -> None: ... # type: ignore[override]
    async def get(self) -> T: ... # type: ignore[override]