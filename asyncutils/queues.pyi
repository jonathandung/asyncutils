'''Extensions of `asyncio.Queue` with more methods and password protection, and a PotentQueueBase ABC.'''
from .exceptions import IgnoreErrors, PasswordQueueError as PasswordQueueError, PasswordRetrievalError as PasswordRetrievalError, GetPasswordRetrievalError as GetPasswordRetrievalError, PutPasswordRetrievalError as PutPasswordRetrievalError, ForbiddenOperation as ForbiddenOperation, PasswordError as PasswordError, WrongPassword as WrongPassword, WrongPasswordType as WrongPasswordType
from .mixins import EventualLoopMixin
from ._internal.protocols import SupportsIteration
from abc import ABCMeta, abstractmethod
from _collections_abc import Callable, Generator, AsyncGenerator, Awaitable, Coroutine
from contextlib import _AsyncGeneratorContextManager
from typing import Any, Protocol, Literal, Self, Final, overload, type_check_only
from asyncio.futures import Future
from asyncio.queues import Queue
__all__ = 'ignore_qempty', 'ignore_qfull', 'ignore_qshutdown', 'ignore_qerrs', 'ignore_valerrs', 'GetPasswordRetrievalError', 'PutPasswordRetrievalError', 'ForbiddenOperation', 'WrongPassword', 'WrongPasswordType', 'password_queue', 'PotentQueueBase', 'SmartQueue', 'SmartLifoQueue', 'SmartPriorityQueue', 'UserPriorityQueue'
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
@type_check_only
class _Q[R, T](Protocol):
    '''A protocol representing password-protected queues. Does not exist at runtime.'''
    async def get(self) -> T: ...
    async def put(self, item: T) -> None: ...
    def get_nowait(self) -> T: ...
    def put_nowait(self, item: T) -> None: ...
    def qsize(self) -> int: ...
    def task_done(self) -> None: ...
    @property
    def maxsize(self) -> int: ...
    def cancel_extend(self, msg: Any=...) -> None: ...
    def empty(self) -> bool: ...
    def full(self) -> bool: ...
    async def join(self) -> None: ...
    def shutdown(self, immediate: bool=...) -> None: ...
    def change_get_password(self, old_pwd: R, new_pwd: R) -> bool: '''Attempts to change the get password of the password-protected queue to new_pwd; returns success.'''
    def change_put_password(self, old_pwd: R, new_pwd: R) -> bool: '''Attempts to change the put password of the password-protected queue to new_pwd; returns success.'''
@type_check_only
class _G[R, T](_Q[R, T], Protocol):
    '''Does not exist at runtime.'''
    async def get(self, pwd: R) -> T:
        '''Removes and returns an item from the password-protected queue, if the password provided was correct; raises WrongPassword otherwise.
        If the queue is empty, waits until an item is available.'''
    def get_nowait(self, pwd: R) -> T:
        '''Removes and returns an item from the password-protected queue, if the password provided was correct; raises WrongPassword otherwise.
        If the queue is empty, raises asyncio.QueueEmpty.'''
@type_check_only
class _P[R, T](_Q[R, T], Protocol):
    '''Does not exist at runtime.'''
    async def put(self, item: T, pwd: R) -> None:
        '''Puts an item into the password-protected queue, if the password provided was correct; raises WrongPassword otherwise.
        If the queue is full, waits until a free slot is available.'''
    def put_nowait(self, item: T, pwd: R) -> None:
        '''Puts an item into the password-protected queue, if the password provided was correct; raises WrongPassword otherwise.
        If the queue is full, raises asyncio.QueueFull.'''
@type_check_only
class _B[R, V, T](_G[R, T], _P[V, T], Protocol): '''Does not exist at runtime.'''
@overload
def password_queue[T, R](password_put: R, *, maxsize: int=..., protect_get: Literal[False]=..., protect_put: Literal[True]=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., put_from: str=..., puttyp: type[R]=..., init_items: SupportsIteration[T]=[], auditf: Callable[[Literal['asyncutils.queues.password_queue'], Literal[False], Literal[True], str, str], None]=...) -> _P[R, T]:
    '''Returns a password-protected queue, the type of which does not inherit from `asyncio.Queue` but has the same interface, with maximum size `maxsize`. `priority` and `lifo` parameters determine if the queue is a priority queue and last-in-first-out.
    If `protect_get` is True, get and get_nowait will require a password, specified by password_get or retrieved from a variable in the caller's scope with name `get_from` (default `password`).
    If `protect_put` is True, put and put_nowait will require a password, specified by password_put or retrieved from a variable in the caller's scope with name `put_from` (default `password`).
    If `init_items` is specified, the items in that (async) iterable will be arranged to enter the queue.
    `auditf` (default sys.audit) is an audit function that takes the event name (`'asyncutils.queues.password_queue'`), `protect_get`, `protect_put`, `get_from`, `put_from` and returns None; note that the passwords are not passed to the audit function.'''
@overload
def password_queue[T, R](*, maxsize: int=..., protect_get: Literal[False]=..., protect_put: Literal[True]=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., put_from: str=..., puttyp: type[R]=object, init_items: SupportsIteration[T]=[], auditf: Callable[[Literal['asyncutils.queues.password_queue'], Literal[False], Literal[True], str, str], None]=...) -> _P[R, T]: ...
@overload
def password_queue[T, R](*, password_get: R, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[False], can_change_get: bool=..., priority: bool=..., lifo: bool=..., get_from: str=..., gettyp: type[R]=..., init_items: SupportsIteration[T]=[], auditf: Callable[[Literal['asyncutils.queues.password_queue'], Literal[True], Literal[False], str, str], None]=...) -> _G[R, T]: ...
@overload
def password_queue[T, R](*, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[False], can_change_get: bool=..., priority: bool=..., lifo: bool=..., get_from: str=..., gettyp: type[R]=object, init_items: SupportsIteration[T]=[], auditf: Callable[[Literal['asyncutils.queues.password_queue'], Literal[True], Literal[False], str, str], None]=...) -> _G[R, T]: ...
@overload
def password_queue[T, R, V](password_put: V, password_get: R, maxsize: int=..., *, protect_get: Literal[True], protect_put: Literal[True]=..., can_change_get: bool=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., get_from: str=..., put_from: str=..., gettyp: type[R]=..., puttyp: type[V]=..., init_items: SupportsIteration[T]=[], auditf: Callable[[Literal['asyncutils.queues.password_queue'], Literal[True], Literal[True], str, str], None]=...) -> _B[R, V, T]: ...
@overload
def password_queue[T, R, V](password_put: V, *, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[True]=..., can_change_get: bool=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., get_from: str=..., put_from: str=..., gettyp: type[R]=object, puttyp: type[V]=..., init_items: SupportsIteration[T]=[], auditf: Callable[[Literal['asyncutils.queues.password_queue'], Literal[True], Literal[True], str, str], None]=...) -> _B[R, V, T]: ...
@overload
def password_queue[T, R, V](*, password_get: R, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[True]=..., can_change_get: bool=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., get_from: str=..., put_from: str=..., gettyp: type[R]=..., puttyp: type[V]=object, init_items: SupportsIteration[T]=[], auditf: Callable[[Literal['asyncutils.queues.password_queue'], Literal[True], Literal[True], str, str], None]=...) -> _B[R, V, T]: ...
@overload
def password_queue[T, R, V](*, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[True]=..., can_change_get: bool=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., get_from: str=..., put_from: str=..., gettyp: type[R]=object, puttyp: type[V]=object, init_items: SupportsIteration[T]=[], auditf: Callable[[Literal['asyncutils.queues.password_queue'], Literal[True], Literal[True], str, str], None]=...) -> _B[R, V, T]: ...
class PotentQueueBase[T](Queue[T], EventualLoopMixin, metaclass=ABCMeta):
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
    def drain_persistent(self, max: int|None=..., timeout: float|None=...) -> AsyncGenerator[T, None]: '''An async generator that gets items from the queue once available and yields them.'''
    def drain_until_empty(self, max: int|None=...) -> Generator[T, None, None]: '''A synchronous generator that gets items from the queue until it is emptied and returns.'''
    def drain_retlist(self, max: int|None=...) -> list[T]: '''Return a list of the items in the queue and empty it.'''
    def empty(self) -> bool: '''Whether the queue is empty.'''
    def __bool__(self) -> bool: '''Whether there are items in the queue.'''
    __iter__, __aiter__ = drain_until_empty, drain_persistent
    def shutdown(self, immediate: bool=...) -> None: '''Shut down the queue. If `immediate` is True, pending gets raise immediately even if the queue is not empty.'''
    @property
    def is_shutdown(self) -> bool: '''Whether the queue is shutting down or has been shutdown.'''
    @is_shutdown.setter
    def is_shutdown(self, val: bool, /): ...
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
        If an error occurs within the context, the original items in the queue are restored and the error reraised; otherwise, changes are committed on exit.'''
    @overload
    def map[R](self, f: Callable[[T], Awaitable[R]], stop_when: Future[None]|None=..., *, lifo: Literal[False]=...) -> SmartQueue[R]: '''Return a queue that contains items from this queue with the function applied on each of them, emptying this queue in the process.'''
    @overload
    def map[R](self, f: Callable[[T], Awaitable[R]], stop_when: Future[None]|None=..., *, lifo: Literal[True]) -> SmartLifoQueue[R]: ...
    @overload
    def starmap[R, *Ts](self: PotentQueueBase[tuple[*Ts]], f: Callable[[*Ts], Awaitable[R]], stop_when: Future|None=..., *, lifo: Literal[False]=...) -> SmartQueue[R]: '''Return a queue that contains items from this queue with the function applied on each of them starred, emptying this queue in the process.'''
    @overload
    def starmap[R, *Ts](self: PotentQueueBase[tuple[*Ts]], f: Callable[[*Ts], Awaitable[R]], stop_when: Future|None=..., *, lifo: Literal[True]) -> SmartLifoQueue[R]: ...
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
    def peek(self) -> T: ...
    def peek_all(self) -> list[T]: ...
    def qsize(self) -> int: ...
    def rotate(self, n: int=..., /) -> None: '''Rotate the items in the queue by `n` indices synchronously, which can be negative.'''
class SmartLifoQueue[T](PotentQueueBase[T]):
    def _init(self, maxsize: int) -> None: ...
    def _get(self) -> T: ...
    def _put(self, item: T) -> None: ...
    def peek(self, i: int=..., /) -> T: ...
    def peek_all(self) -> list[T]: ...
    def qsize(self) -> int: ...
class SmartPriorityQueue[T](PotentQueueBase[T]):
    def __init__(self, maxsize: int=..., *, init_items: SupportsIteration[T]=[]): ...
    def _init(self, maxsize: int) -> None: ...
    def _get(self) -> T: ...
    def _put(self, item: T) -> None: ...
    def peek(self) -> T: ...
    def peek_all(self) -> list[T]: ...
    def qsize(self) -> int: ...
class UserPriorityQueue[T](SmartPriorityQueue[tuple[int, int, T]]):
    @classmethod
    def from_iter_of_tuples(cls, items: SupportsIteration[tuple[int, int, T]], maxsize: int=...) -> Self: '''Build a queue from the (async) iterable of tuples (priority, tiebreak, item).'''
    def __init__(self, maxsize: int=..., *, init_priority: int=..., init_items: SupportsIteration[T]=[]): ...
    def put_nowait(self, item: T, priority: int=...) -> None: ...
    def get_nowait(self) -> T: ...
    async def put(self, item: T, priority: int=...) -> None: ...
    async def get(self) -> T: ...