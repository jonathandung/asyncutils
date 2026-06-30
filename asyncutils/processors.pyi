'''Processors for asynchronous tasks.'''
from ._internal.prots import CanExcept, SupportsIteration, Timer
from .mixins import LoopContextMixin
from collections.abc import Awaitable, Callable
from types import AsyncGeneratorType
from typing import Any, Literal
__all__ = 'BatchProcessor', 'BoundedBatchProcessor', 'Bulkhead'
class BoundedBatchProcessor[T, R]:
    '''Call a processor with items batched to a certain size from different sources with bounded concurrency.'''
    def __init__(self, processor: Callable[[list[T]], Awaitable[R]], batch: int=..., max_concurrent: int=...) -> None: '''``batch`` defaults to :const:`~asyncutils.context.Context.BOUNDED_BATCH_PROCESSOR_DEFAULT_BATCH_SIZE` and ``max_concurrent`` :const:`~asyncutils.context.Context.BOUNDED_BATCH_PROCESSOR_DEFAULT_MAX_CONCURRENT`.'''
    def process(self, items: SupportsIteration[T]) -> AsyncGeneratorType[R]: '''Call the processor on batches of items from the source and yield the results as they arrive.'''
class BatchProcessor[T](LoopContextMixin):
    '''Call a processor with items batched to a certain size from different sources, with an optional time limit for batches.

    .. caution:: Use instances of this class as async context managers to ensure proper cleanup.
    '''
    def __init__(self, processor: Callable[[list[T]], Awaitable[None]], *, maxsize: int=..., maxtime: float=..., timer: Timer=...) -> None: '''``maxsize`` defaults to :const:`~asyncutils.context.Context.BATCH_PROCESSOR_DEFAULT_MAX_SIZE`, ``maxtime`` to :const:`~asyncutils.context.Context.BATCH_PROCESSOR_DEFAULT_MAX_TIME`, and ``timer`` :func:`time.monotonic`.'''
    async def add(self, item: T) -> None: '''Add an item to the current batch. If the batch is full, process it asynchronously before returning.'''
    async def flush(self) -> None: '''Process the items in the buffer, even if the batch size is not reached.'''
    @property
    def time_since_last_process(self) -> float: '''The time in seconds since the last batch was processed.'''
    async def __setup__(self) -> None: ...
    async def __cleanup__(self) -> None: ...
class Bulkhead(LoopContextMixin):
    '''Limit the number of concurrent executions of coroutines, with an optional queue for pending executions and an optional callback that handles exceptions raised by the processor.

    .. caution:: Use instances of this class as async context managers to ensure proper cleanup.
    '''
    def __init__(self, max_concurrent: int, *, max_queue: int=..., max_rej: int=..., exc: CanExcept=..., processor: Callable[[BaseException], Awaitable[None]]=...) -> None:
        '''* ``max_concurrent`` (required): maximum number of concurrent executions allowed
        * ``max_queue``: maximum number of pending executions allowed in the queue; if the queue is full, new executions will be rejected until there is space in the queue. Non-positive value means no limit (there is currently no way to get a zero-capacity queue). Default :const:`~asyncutils.context.Context.BULKHEAD_DEFAULT_MAX_QUEUE`.
        * ``max_rej``: maximum number of rejections allowed before the bulkhead shuts down and rejects all new executions. Negative value means no limit. Default :const:`~asyncutils.context.Context.BULKHEAD_DEFAULT_MAX_REJ`.
        * ``exc``: the type of exceptions that the processor may raise and should be caught and passed to the ``processor`` callback. Default :exc:`Exception`.
        '''
    async def __cleanup__(self) -> None: ...
    async def execute(self, coro: Awaitable[Any]) -> None: '''Queue a coroutine ``coro`` to be executed and execute a coroutine that may not be the same as ``coro``. Bulkhead constraints are applied, and the return value is lost.'''
    @property
    def available_slots(self) -> int: '''The number of slots available on the bulkhead.'''
    @property
    def active_tasks(self) -> int: '''The number of currently running tasks.'''
    @property
    def curr_qsize(self) -> int: '''The current size of the task queue.'''
    @property
    def max_qsize(self) -> int: '''The maximum size of the task queue.'''
    @property
    def available_queue_slots(self) -> float: '''The number of available slots in the task queue. Gives an integer, unless the queue is unbounded, in which case :data:`math.inf` is returned.'''
    @property
    def is_shutdown(self) -> bool: '''Whether the bulkhead is shutting down or has been shut down, possibly because too many executions were rejected.'''
    @property
    def rejected(self) -> int: '''The number of rejected executions so far.'''
    async def wait_until_idle(self, timeout: float|None=...) -> Literal[True]: '''Wait until no tasks are running.'''
    async def wait_for_shutdown(self, timeout: float|None=...) -> None: '''Wait until the bulkhead enters the shutdown phase.'''
    async def shutdown(self, timeout: float|None=...) -> list[Awaitable[Any]]: '''Shut down the bulkhead and return all incomplete tasks.'''
