# ty: ignore[invalid-method-override]
'''Non-inheriting extensions of :class:`asyncio.Queue` with more methods and password protection, and a :class:`PotentQueueBase` ABC.'''
from ._internal.helpers import LoopMixinBase
from ._internal.prots import SupportsIteration, GetAndPutProtectedQProt, GetProtectedQProt, PutProtectedQProt
from .exceptions import IgnoreErrors
from abc import ABC, abstractmethod
from asyncio import Future, Queue
from collections.abc import AsyncGenerator, Awaitable, Callable, Generator
from contextlib import AbstractContextManager
from typing import Any, Final, Literal, Self, overload
__all__ = 'PotentQueueBase', 'SmartLifoQueue', 'SmartPriorityQueue', 'SmartQueue', 'UserPriorityQueue', 'ignore_qempty', 'ignore_qerrs', 'ignore_qfull', 'ignore_qshutdown', 'password_queue'
ignore_qshutdown: Final[IgnoreErrors]
'''Instance of :class:`~exceptions.IgnoreErrors` that suppresses :exc:`~asyncio.QueueShutDown`.'''
ignore_qempty: Final[IgnoreErrors]
'''Instance of :class:`~exceptions.IgnoreErrors` that suppresses :exc:`~asyncio.QueueShutDown` and :exc:`~asyncio.QueueEmpty`.'''
ignore_qfull: Final[IgnoreErrors]
'''Instance of :class:`~exceptions.IgnoreErrors` that suppresses :exc:`~asyncio.QueueShutDown` and :exc:`~asyncio.QueueFull`.'''
ignore_qerrs: Final[IgnoreErrors]
'''Instance of :class:`~exceptions.IgnoreErrors` that suppresses all asyncio queue-related errors.'''
@overload
def password_queue[T, R](password_put: R, *, maxsize: int=..., protect_get: Literal[False]=..., protect_put: Literal[True]=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., puttyp: type[R]=..., init_items: SupportsIteration[T], strict: bool=...) -> PutProtectedQProt[R, T]: ...
@overload
def password_queue[T](*, maxsize: int=..., protect_get: Literal[False]=..., protect_put: Literal[True]=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., put_from: str=..., init_items: SupportsIteration[T], strict: bool=...) -> PutProtectedQProt[Any, T]: ...
@overload
def password_queue[T, R](*, maxsize: int=..., protect_get: Literal[False]=..., protect_put: Literal[True]=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., put_from: str=..., puttyp: type[R], init_items: SupportsIteration[T], strict: bool=...) -> PutProtectedQProt[R, T]: ...
@overload
def password_queue[T, R](*, password_get: R, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[False], can_change_get: bool=..., priority: bool=..., lifo: bool=..., get_from: str=..., gettyp: type[R]=..., init_items: SupportsIteration[T], strict: bool=...) -> GetProtectedQProt[R, T]: ...
@overload
def password_queue[T, R](*, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[False], can_change_get: bool=..., priority: bool=..., lifo: bool=..., get_from: str=..., gettyp: type[R], init_items: SupportsIteration[T], strict: bool=...) -> GetProtectedQProt[R, T]: ...
@overload
def password_queue[T](*, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[False], can_change_get: bool=..., priority: bool=..., lifo: bool=..., get_from: str=..., init_items: SupportsIteration[T], strict: bool=...) -> GetProtectedQProt[Any, T]: ...
@overload
def password_queue[T, R, V](password_put: V, password_get: R, maxsize: int=..., *, protect_get: Literal[True], protect_put: Literal[True]=..., can_change_get: bool=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., gettyp: type[R]=..., puttyp: type[V]=..., init_items: SupportsIteration[T], strict: bool=...) -> GetAndPutProtectedQProt[R, V, T]: ...
@overload
def password_queue[T, R, V](password_put: V, *, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[True]=..., can_change_get: bool=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., get_from: str=..., gettyp: type[R], puttyp: type[V]=..., init_items: SupportsIteration[T], strict: bool=...) -> GetAndPutProtectedQProt[R, V, T]: ...
@overload
def password_queue[T, V](password_put: V, *, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[True]=..., can_change_get: bool=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., get_from: str=..., puttyp: type[V]=..., init_items: SupportsIteration[T], strict: bool=...) -> GetAndPutProtectedQProt[Any, V, T]: ...
@overload
def password_queue[T, R, V](*, password_get: R, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[True]=..., can_change_get: bool=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., put_from: str=..., gettyp: type[R]=..., puttyp: type[V], init_items: SupportsIteration[T], strict: bool=...) -> GetAndPutProtectedQProt[R, V, T]: ...
@overload
def password_queue[T, R](*, password_get: R, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[True]=..., can_change_get: bool=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., put_from: str=..., gettyp: type[R]=..., init_items: SupportsIteration[T], strict: bool=...) -> GetAndPutProtectedQProt[R, Any, T]: ...
@overload
def password_queue[T, R, V](*, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[True]=..., can_change_get: bool=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., get_from: str=..., put_from: str=..., gettyp: type[R], puttyp: type[V], init_items: SupportsIteration[T], strict: bool=...) -> GetAndPutProtectedQProt[R, V, T]: ...
@overload
def password_queue[T, R](*, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[True]=..., can_change_get: bool=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., get_from: str=..., put_from: str=..., gettyp: type[R], init_items: SupportsIteration[T], strict: bool=...) -> GetAndPutProtectedQProt[R, Any, T]: ...
@overload
def password_queue[T, V](*, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[True]=..., can_change_get: bool=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., get_from: str=..., put_from: str=..., puttyp: type[V], init_items: SupportsIteration[T], strict: bool=...) -> GetAndPutProtectedQProt[Any, V, T]: ...
@overload
def password_queue[T](*, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[True]=..., can_change_get: bool=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., get_from: str=..., put_from: str=..., init_items: SupportsIteration[T], strict: bool=...) -> GetAndPutProtectedQProt[Any, Any, T]: ...
@overload
def password_queue[R](password_put: R, *, maxsize: int=..., protect_get: Literal[False]=..., protect_put: Literal[True]=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., puttyp: type[R]=..., strict: bool=...) -> PutProtectedQProt[R, Any]: ...
@overload
def password_queue[R](*, maxsize: int=..., protect_get: Literal[False]=..., protect_put: Literal[True]=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., put_from: str=..., puttyp: type[R], strict: bool=...) -> PutProtectedQProt[R, Any]: ...
@overload
def password_queue(*, maxsize: int=..., protect_get: Literal[False]=..., protect_put: Literal[True]=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., put_from: str=..., strict: bool=...) -> PutProtectedQProt[Any, Any]: ...
@overload
def password_queue[R](*, password_get: R, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[False], can_change_get: bool=..., priority: bool=..., lifo: bool=..., gettyp: type[R]=..., strict: bool=...) -> GetProtectedQProt[R, Any]: ...
@overload
def password_queue[R](*, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[False], can_change_get: bool=..., priority: bool=..., lifo: bool=..., gettyp: type[R], strict: bool=...) -> GetProtectedQProt[R, Any]: ...
@overload
def password_queue(*, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[False], can_change_get: bool=..., priority: bool=..., lifo: bool=..., get_from: str=..., strict: bool=...) -> GetProtectedQProt[Any, Any]: ...
@overload
def password_queue[R, V](password_put: V, password_get: R, maxsize: int=..., *, protect_get: Literal[True], protect_put: Literal[True]=..., can_change_get: bool=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., gettyp: type[R]=..., puttyp: type[V]=..., strict: bool=...) -> GetAndPutProtectedQProt[R, V, Any]: ...
@overload
def password_queue[R, V](password_put: V, *, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[True]=..., can_change_get: bool=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., get_from: str=..., gettyp: type[R], puttyp: type[V]=..., strict: bool=...) -> GetAndPutProtectedQProt[R, V, Any]: ...
@overload
def password_queue[V](password_put: V, *, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[True]=..., can_change_get: bool=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., get_from: str=..., puttyp: type[V]=..., strict: bool=...) -> GetAndPutProtectedQProt[Any, V, Any]: ...
@overload
def password_queue[R, V](*, password_get: R, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[True]=..., can_change_get: bool=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., put_from: str=..., gettyp: type[R]=..., puttyp: type[V], strict: bool=...) -> GetAndPutProtectedQProt[R, V, Any]: ...
@overload
def password_queue[R](*, password_get: R, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[True]=..., can_change_get: bool=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., put_from: str=..., gettyp: type[R]=..., strict: bool=...) -> GetAndPutProtectedQProt[R, Any, Any]: ...
@overload
def password_queue[R, V](*, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[True]=..., can_change_get: bool=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., get_from: str=..., put_from: str=..., gettyp: type[R], puttyp: type[V], strict: bool=...) -> GetAndPutProtectedQProt[R, V, Any]: ...
@overload
def password_queue[R](*, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[True]=..., can_change_get: bool=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., get_from: str=..., put_from: str=..., gettyp: type[R], strict: bool=...) -> GetAndPutProtectedQProt[R, Any, Any]: ...
@overload
def password_queue[V](*, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[True]=..., can_change_get: bool=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., get_from: str=..., put_from: str=..., puttyp: type[V], strict: bool=...) -> GetAndPutProtectedQProt[Any, V, Any]: ...
@overload
def password_queue(*, maxsize: int=..., protect_get: Literal[True], protect_put: Literal[True]=..., can_change_get: bool=..., can_change_put: bool=..., priority: bool=..., lifo: bool=..., get_from: str=..., put_from: str=..., strict: bool=...) -> GetAndPutProtectedQProt[Any, Any, Any]:
    '''| Return a thread-unsafe password-protected queue, the type of which does not inherit from :class:`asyncio.Queue` but has the same interface.
    | The queue has maximum size ``maxsize``. ``priority`` and ``lifo`` parameters determine if the queue is a priority queue and last-in-first-out.
    | If ``protect_get`` is ``True``, get and get_nowait will require a password, specified by ``password_get`` or retrieved from a variable in the
    | caller's scope with name ``get_from`` (default :const`context.PASSWORD_QUEUE_DEFAULT_GET_FROM`).
    | If ``protect_put`` is ``True``, put and put_nowait will require a password, specified by ``password_put`` or retrieved from a variable in the
    | caller's scope with name ``put_from`` (default :const`context.PASSWORD_QUEUE_DEFAULT_PUT_FROM`).
    | If ``init_items`` is specified, the items in that (async) iterable will be arranged to enter the queue eventually.

    .. danger::
      This function is meant not for cryptographic purposes, because no hashing of the password is performed! Attackers may obtain sensitive
      information, namely the passwords used by the queue, from the memory address of the returned object alone, or worse still, access and
      modify the internal stack/queue storing the items directly.
    .. note::
      The excessive amount of overloads here cannot be helped due to accurate typing needs. When we drop support for Python 3.12, we will use
      default values in the type parameters here to cut this number in half.
    .. note::
      The overloads do not cover the technically valid but useless case with both ``protect_get`` and ``protect_put`` being ``False``.
    .. note::
      Little type validation for the argument combinations is done at runtime; it is hoped that type checkers will catch most misuses.
'''
class PotentQueueBase[T](Queue[T], LoopMixinBase, ABC):
    '''A base class for queues with much more methods, async- and sync-compatible.'''
    @abstractmethod
    def _init(self, maxsize: int) -> None: '''Initialize the queue given ``maxsize``; called by :meth:`__init__`.'''
    @abstractmethod
    def _get(self) -> T: '''Get an item from the queue if not empty; called by :meth:`get` and :meth:`get_nowait`.'''
    @abstractmethod
    def _put(self, item: T) -> None: '''Put an item into the queue if not empty; called by :meth:`put` and :meth:`put_nowait`.'''
    @abstractmethod
    def peek_all(self) -> list[T]: '''Return a list of all the items in the queue.'''
    @abstractmethod
    def qsize(self) -> int: '''Return the size of the queue as an integer.'''
    def reset(self) -> None: '''Revert the queue to an empty state.'''
    async def smart_put(self, item: T, *, timeout: float|None=..., raising: bool=...) -> bool|None: '''Call :meth:`put_nowait` if a slot is immediately available, waiting for a slot with ``timeout`` otherwise; if the timeout expires and ``raising`` is True, throw :exc:`TimeoutError`.'''
    async def smart_get(self, *, timeout: float|None=..., default: T=...) -> T: '''Call :meth:`get_nowait` if an item is immediately available, waiting for a item with ``timeout`` otherwise; if the timeout expires and ``default`` is provided, return it.'''
    async def extend(self, it: SupportsIteration[T], timeout: float|None=...) -> None: '''Add the items from ``it`` into the queue within ``timeout``.'''
    def push(self, item: T) -> bool: '''Put an item into the queue immediately, popping if necessary; returns success.'''
    def drain_persistent(self, max_items: int|None=..., timeout: float|None=...) -> AsyncGenerator[T]: '''An async generator that gets items from the queue once available and yields them.'''
    def drain_until_empty(self, max_items: int|None=...) -> Generator[T]: '''A synchronous generator that gets items from the queue until it is emptied and returns.'''
    def drain_retlist(self, max_items: int|None=...) -> list[T]: '''Empty the queue and return a list of the items within.'''
    def empty(self) -> bool: '''Whether the queue is empty.'''
    def __bool__(self) -> bool: '''Whether there are items in the queue.'''
    def __iter__(self) -> Generator[T]: '''Equivalent to :meth:`drain_until_empty`.'''
    def __aiter__(self) -> AsyncGenerator[T]: '''Equivalent to :meth:`drain_persistent`.'''
    def shutdown(self, immediate: bool=...) -> None: '''Shut down the queue. If ``immediate`` is ``True``, pending gets raise immediately even if the queue is not empty.'''
    @property
    def is_shutdown(self) -> bool: '''Whether the queue is shutting down or has been shutdown.'''
    @is_shutdown.setter
    def is_shutdown(self, val: bool, /) -> None: '''If set to ``True``, shut down the queue; if set to ``False``, restart the queue.'''
    @property
    def can_put_now(self) -> bool: '''Whether items can be put into the queue without blocking at this instant.'''
    @property
    def can_get_now(self) -> bool: '''Whether items can be get from the queue without blocking at this instant.'''
    @property
    def fully_functional(self) -> bool: '''``queue.fully_functional == queue.can_put_now and queue.can_get_now``.'''
    @property
    def capacity(self) -> int|float: '''The capacity of the queue. Can be :const:`math.inf`.'''
    @property
    def remaining_capacity(self) -> int|float: '''The remaining number of slots in the queue. Can be :const:`math.inf`.'''
    @property
    def utilization_rate(self) -> float: '''The number of items the queue divided by its capacity.'''
    def pushpop_nowait(self, item: T, raising: bool=...) -> T: '''Push an item into the queue and pop from the other end immediately.'''
    def poppush_nowait(self, item: T, raising: bool=...) -> T: '''Pop an item from the queue and push into the other end immediately.'''
    async def pushpop(self, item: T) -> T: '''The above, but done asynchronously and not immediately.'''
    async def poppush(self, item: T) -> T: '''Similar.'''
    def clear(self) -> None: '''Clear all the entries from the queue.'''
    def transaction(self) -> AbstractContextManager[Self, None]:
        '''| Return an async context manager which begins a transaction on entry.
        | If an error occurs within the context, the original items in the queue are restored and the error reraised, unless the error is critical
        | and deemed to require immediate exit. Otherwise, the transaction completes successfully and changes are committed on exit.'''
    @overload
    def map[R](self, f: Callable[[T], Awaitable[R]], stop_when: Future[None]|None=..., *, lifo: Literal[False]=...) -> SmartQueue[R]: ...
    @overload
    def map[R](self, f: Callable[[T], Awaitable[R]], stop_when: Future[None]|None=..., *, lifo: Literal[True]) -> SmartLifoQueue[R]: '''Return a queue that contains items from this queue with the function applied on each of them, emptying this queue in the process (transformation analogous to :class:`map`).'''
    @overload
    def starmap[R, *Ts](self: PotentQueueBase[tuple[*Ts]], f: Callable[[*Ts], Awaitable[R]], stop_when: Future[None]|None=..., *, lifo: Literal[False]=...) -> SmartQueue[R]: ...
    @overload
    def starmap[R, *Ts](self: PotentQueueBase[tuple[*Ts]], f: Callable[[*Ts], Awaitable[R]], stop_when: Future[None]|None=..., *, lifo: Literal[True]) -> SmartLifoQueue[R]: '''Return a queue that contains items from this queue with the function applied on each of them starred, emptying this queue in the process (transformation analogous to :func:`itertools.starmap`).'''
    @overload
    def filter(self, pred: Callable[[T], bool]=..., *, lifo: Literal[False]=...) -> SmartQueue[T]: ...
    @overload
    def filter(self, pred: Callable[[T], bool]=..., *, lifo: Literal[True]) -> SmartLifoQueue[T]: '''Return a new queue from which getters can get the items in this queue that satisfy the predicate; items remaining in the original queue did not satisfy the predicate.'''
    @overload
    def enumerate(self, *, lifo: Literal[False]=...) -> SmartQueue[tuple[int, T]]: ...
    @overload
    def enumerate(self, *, lifo: Literal[True]) -> SmartLifoQueue[tuple[int, T]]: '''Return a queue containing the items from enumerate applied on this queue and empty it in the process.'''
    def filter_nowait(self, pred: Callable[[T], bool]=..., /) -> tuple[list[T], int]: '''Filter items in the queue by a predicate and return a list of removed items and an integer; the items in the returned list after the index corresponding to that integer were items rejected from the queue due to the queue being full.'''
    def enumerate_nowait(self, start: int=..., *, step: int=...) -> Generator[tuple[int, T]]: '''Do the equivalent of zipping ``itertools.count(start, step)`` with the items of the queue. When the returned generator is advanced and the queue is empty at that moment, the generator stops entirely.'''
class SmartQueue[T](PotentQueueBase[T]):
    def _init(self, maxsize: int) -> None: ...
    def _get(self) -> T: ...
    def _put(self, item: T) -> None: ...
    def peek(self) -> T: '''Look at the item that would be returned by :meth:`~asyncio.Queue.get` or :meth:`~asyncio.Queue.get_nowait` without actually removing it from the queue.'''
    def peek_all(self) -> list[T]: ...
    def qsize(self) -> int: ...
    def rotate(self, n: int=..., /) -> None: '''Rotate the items in the queue by ``n`` indices synchronously, which can be negative.'''
class SmartLifoQueue[T](PotentQueueBase[T]):
    def _init(self, maxsize: int) -> None: ...
    def _get(self) -> T: ...
    def _put(self, item: T) -> None: ...
    def peek(self, i: int=..., /) -> T: '''Look at the item at index ``i``, defaulting to the item most recently put in (that would be returned by :meth:`~asyncio.Queue.get` or :meth:`~asyncio.Queue.get_nowait`).'''
    def peek_all(self) -> list[T]: ...
    def qsize(self) -> int: ...
class SmartPriorityQueue[T](PotentQueueBase[T]):
    '''A priority queue, where the priority of each item is determined by comparing it to other items, meaning each item should at least implement :meth:`~object.__lt__`.'''
    @overload
    def __init__(self, maxsize: int=..., *, init_items: SupportsIteration[T]): ...
    @overload
    def __init__(self, maxsize: int=...): ...
    async def start(self, maxsize: int, init_items: SupportsIteration[T]) -> None: ...
    def _init(self, maxsize: int) -> None: ...
    def _get(self) -> T: ...
    def _put(self, item: T) -> None: ...
    def peek(self) -> T: '''Look at the item that would be returned by :meth:`~asyncio.Queue.get` or :meth:`~asyncio.Queue.get_nowait` without actually removing it from the queue.'''
    def peek_all(self) -> list[T]: ...
    def qsize(self) -> int: ...
class UserPriorityQueue[T](SmartPriorityQueue[tuple[int, int, T]]):
    '''| A priority queue, where you put in items with an integer priority and the items are retrieved in ascending order of priority, with earlier
    | items taking precedence in case of ties.
    | The :meth:`put` and :meth:`put_nowait` methods of this class take an additional ``priority`` parameter, representing the priority of the item.'''
    @classmethod
    def from_iter_of_tuples(cls, items: SupportsIteration[tuple[int, int, T]], maxsize: int=...) -> Self: '''Build a queue from the (async) iterable of tuples (priority, tiebreak, item).'''
    @overload
    def __init__(self, maxsize: int=..., *, init_priority: int=..., init_items: SupportsIteration[T]): ...
    @overload
    def __init__(self, maxsize: int=..., *, init_priority: int=...): ...
    def put_nowait(self, item: T, priority: int=...) -> None: ...
    def get_nowait(self) -> T: ...
    async def put(self, item: T, priority: int=...) -> None: ...
    async def get(self) -> T: ...
