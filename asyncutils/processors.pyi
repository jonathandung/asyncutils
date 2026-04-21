'''Processors for asynchronous tasks.'''
from ._internal.types import Exceptable, SupportsIteration, Timer
from .mixins import LoopContextMixin
from _collections_abc import AsyncGenerator, Awaitable, Callable, Coroutine
from typing import Any, Literal
__all__ = 'BatchProcessor', 'BoundedBatchProcessor', 'Bulkhead'
class BoundedBatchProcessor[T, R]:
    '''Call a processor with items batched to a certain size from different sources with bounded concurrency.'''
    def __init__(self, processor: Callable[[list[T]], Awaitable[R]], batch: int=..., max_concurrent: int=...) -> None: '''`batch` defaults to :const:`context.BOUNDED_BATCH_PROCESSOR_DEFAULT_BATCH_SIZE` and `max_concurrent` :const:`context.BOUNDED_BATCH_PROCESSOR_DEFAULT_MAX_CONCURRENT`.'''
    def process(self, items: SupportsIteration[T]) -> AsyncGenerator[R]: '''Call the processor on batches of items from the source and yield the results as they arrive.'''
class BatchProcessor[T](LoopContextMixin):
    '''Call a processor with items batched to a certain size from different sources, with an optional time limit for batches.
    Use instances of this class as async context managers to ensure proper cleanup.'''
    def __init__(self, processor: Callable[[list[T]], Awaitable[None]], *, maxsize: int=..., maxtime: float=..., timer: Timer=...) -> None: '''`maxsize` defaults to :const:`context.BATCH_PROCESSOR_DEFAULT_MAX_SIZE`, `maxtime` to :const:`context.BATCH_PROCESSOR_DEFAULT_MAX_TIME`, and `timer` :func:`time.monotonic`.'''
    async def add(self, item: T) -> None: '''Add an item to the current batch. If the batch is full, process it asynchronously before returning.'''
    async def flush(self) -> None: '''Process the items in the buffer, even if the batch size is not reached.'''
    @property
    def time_since_last_process(self) -> float: '''Return the time in seconds since the last batch was processed.'''
    async def __setup__(self) -> None: ...
    async def __cleanup__(self) -> None: ...
class Bulkhead(LoopContextMixin):
    '''Limit the number of concurrent executions of a processor, with an optional queue for pending executions and an optional callback for handling exceptions raised by the processor.
    Use instances of this class as async context managers to ensure proper cleanup.'''
    def __init__(self, max_concurrent: int, *, max_queue: int=..., max_rej: int=..., exc: Exceptable=..., processor: Callable[[BaseException], Awaitable[None]]=...) -> None:
        '''`max_concurrent`: maximum number of concurrent executions allowed
        `max_queue`: maximum number of pending executions allowed in the queue; if the queue is full, new executions will be rejected until there is space in the queue. Non-positive value means no limit (there is currently no way to get a zero-capacity queue). Default :const:`context.BULKHEAD_DEFAULT_MAX_QUEUE`.
        `max_rej`: maximum number of rejections allowed before the bulkhead shuts down and rejects all new executions. Negative value means no limit. Default :const:`context.BULKHEAD_DEFAULT_MAX_REJ`.
        `exc`: the type of exceptions that the processor may raise and should be caught and passed to the `processor` callback. Default `Exception`.'''
    async def __cleanup__(self) -> None: ...
    async def execute(self, coro: Coroutine[Any, Any, Any]) -> None: '''Execute a coroutine, applying the bulkhead constraints.'''
    @property
    def available_slots(self) -> int: ...
    @property
    def active_tasks(self) -> int: ...
    @property
    def curr_qsize(self) -> int: ...
    @property
    def max_qsize(self) -> int: ...
    @property
    def available_qslots(self) -> int: ...
    @property
    def is_available(self) -> bool: ...
    @property
    def is_shutdown(self) -> bool: ...
    @property
    def rejected(self) -> int: ...
    async def wait_until_idle(self, timeout: float|None=...) -> Literal[True]: ...
    async def shutdown(self, timeout: float|None=...) -> list[Coroutine[Any, Any, Any]]: ...