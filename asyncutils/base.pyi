from ._internal.protocols import GeneratorCoroutine, Sentinel, SupportsIteration, SupportsPop, SupportsPopLeft, ValidExcType
from _collections_abc import AsyncGenerator, AsyncIterable, AsyncIterator, Awaitable, Callable, Generator, Iterable, Iterator
from asyncio.events import AbstractEventLoop
from asyncio.futures import Future
from types import TracebackType
from typing import Any, ClassVar, Literal, NoReturn, Self, overload
__all__ = 'adisembowel', 'adisembowelleft', 'aenumerate', 'aiter_to_iter', 'collect', 'drop', 'dummy_task', 'event_loop', 'iter_to_aiter', 'safe_cancel_batch', 'sleep_forever', 'take', 'yield_to_event_loop'
class event_loop: # noqa: N801
    '''A context manager to manage lifecycles of asyncio-native event loops.'''
    _ENTERED: ClassVar[int]
    _INNER_AEXIT: ClassVar[int]
    _INNER_EXIT: ClassVar[int]
    _INTERNAL_MASK: ClassVar[int]
    _SHOULD_CLOSE: ClassVar[int]
    def __new__(cls, *, dont_release_loop_on_finalization: bool=..., silent_on_finalize: bool=..., check_running: bool=..., close_existing_on_exit: bool=..., dont_always_stop_on_exit: bool=..., dont_close_created_on_exit: bool=..., cancel_all_tasks: bool=..., keep_loop: bool=..., suppress_runtime_errors: bool=..., fail_silent: bool=..., dont_allow_reuse: bool=..., dont_reuse: bool=..., dont_attempt_enter: bool=..., attempt_aenter: bool=..., suppress_inner_exit_on_runtime_error: bool=..., suppress_inner_aexit_on_runtime_error: bool=...) -> Self: '''Constructor arguments are self-explanatory. Pass as appropriate; all default to `False`.'''
    def __enter__(self) -> AbstractEventLoop: '''Enter the context, returning the underlying asyncio event loop, which is fetched on demand.'''
    @overload
    def __exit__(self, t: None, v: None, b: None, /) -> Literal[False]: ...
    @overload
    def __exit__(self, t: ValidExcType, v: BaseException, b: TracebackType, /) -> bool: '''Exit the context. This stops and closes the event loop if the flags say so.'''
    def __reduce__(self) -> tuple[Callable[[int], Self], tuple[int]]: '''Support for pickling.'''
    def clear_flags(self, mask_to_keep: int=...) -> None: '''Reset the configuration to the defaults.'''
    def copy_flags(self) -> Self: '''Return an unentered instance with the same configuration as this, but managing a different event loop.'''
    @classmethod
    def from_flags(cls, flags: int, /) -> Self: '''Construct an instance from `flags`, a bitwise or of options.'''
    def _get_unclosed_loop(self, factory: Callable[[], AbstractEventLoop]) -> AbstractEventLoop: '''Return a usable asyncio event loop from the internal pool, or a new event loop if there are none.'''
@overload
def iter_to_aiter[T, R](it: AsyncGenerator[T, R]) -> AsyncGenerator[T, R]: ...
@overload
def iter_to_aiter[T, R](it: AsyncGenerator[T, R], sentinel: T) -> AsyncGenerator[T, R]: ...
@overload
def iter_to_aiter[I: AsyncIterator[Any]](it: I) -> I: ...
@overload
def iter_to_aiter[T](it: AsyncIterable[T], sentinel: T) -> AsyncGenerator[T]: ...
@overload
def iter_to_aiter[T](it: AsyncIterable[T]) -> AsyncIterator[T]: ...
@overload
def iter_to_aiter[T](it: Iterable[T], *, use_existing_executor: bool=..., create_executor: bool=...) -> AsyncGenerator[T]: ...
@overload
def iter_to_aiter[T](it: Iterable[T], sentinel: T, *, use_existing_executor: bool=..., create_executor: bool=...) -> AsyncGenerator[T]:
    '''Convert the (async) iterable `it` to an async generator as non-blockingly as possible.
    If `it` is already an async iterator, it is returned as is.
    Values sent to the return async generator will be passed to the original.
    The async generator will stop when it encounters an item identical to `sentinel`.
    When `use_existing_executor=True` is passed, the function will attempt to use an existing executor as created by previous calls
    specifying `create_executor=True` to advance the iterable, and fall back to blocking the event loop every step without an executor.
    When `create_executor` is `True`, the function will create a new executor to run the `__next__` calls if needed.'''
@overload
def aiter_to_iter[T, R](ait: AsyncGenerator[T, R]) -> Generator[T, R]: ...
@overload
def aiter_to_iter[T](ait: AsyncIterable[T]) -> Generator[T]: ...
@overload
def aiter_to_iter[I: Iterator[Any]](ait: I) -> I: ...
@overload
def aiter_to_iter[T](ait: Iterable[T]) -> Iterator[T]: '''Convert an (async) iterable `ait` to a sync generator, or the object itself if it is already an iterator.'''
def adisembowel[T](it: SupportsPop[T], /) -> AsyncGenerator[T]: '''Asynchronously disembowel an iterable from the right using its pop method and yield its items from right to left.'''
def adisembowelleft[T](it: SupportsPopLeft[T], /) -> AsyncGenerator[T]: '''Asynchronously disembowel an iterable from the left using its popleft method and yield its items from left to right,'''
@overload
async def safe_cancel_batch[T](t: SupportsIteration[Future[T]], *, callback: Callable[[T|BaseException], object]|None=..., disembowel: Literal[False]=..., raising: bool=...) -> None: ...
@overload
async def safe_cancel_batch[T](t: SupportsPop[Future[T]], *, callback: Callable[[T|BaseException], object]|None=..., disembowel: Literal[True], raising: bool=...) -> None:
    '''Cancel an (async) iterable of futures, waiting for the cancellations to complete asynchronously.
    Afterwards, if disembowel is True, clear the iterable using its pop() method repeatedly, falling back to clear().
    The callback is called on each result or exception of the futures after CancelledError was thrown into them concurrently.
    If `raising` is True, all calls of the callback that themselves threw exceptions are collected into a BaseExceptionGroup, which is then raised.'''
async def collect[T](it: SupportsIteration[T], n: int=..., default: T|Sentinel=...) -> list[T]:
    '''Collect `n` items from the (async) iterable into a list and return that list.
    When `n` is not passed, equivalent to `iters.to_list` but slower.
    Refer to `iters.basic_collect` for a marginally faster variant that doesn't accept a default.
    If default is `constants.RAISE` and there are less than `n` items to collect, throw `exceptions.ItemsExhausted`.
    When default is not passed, a warning is still emitted by the logger in that case.
    Otherwise, pad the behind of the list with copies of the default.'''
@overload
def take[T](it: SupportsIteration[T], n: int, *, default: T|Sentinel) -> AsyncGenerator[T]: ...
@overload
def take[T](it: SupportsIteration[T], n: int|None) -> AsyncGenerator[T]:
    '''Yield `n` items from the (async) iterable.
    To ensure there are exactly `n` items in the resultant async generator, pass a default value.
    In particular, pass `constants.RAISE` as `default` to cause `exceptions.ItemsExhausted` to be thrown in the case that there are not enough items.
    If `n` is None, take all items.'''
def drop[T](it: SupportsIteration[T], n: int, raising: bool=...) -> AsyncGenerator[T]: '''Discard `n` items from the (async) iterable and yield the rest. If there are not enough items and raising is True, throw `exceptions.ItemsExhausted`.'''
def aenumerate[T](it: SupportsIteration[T], start: int=..., *, step: int=...) -> AsyncGenerator[tuple[int, T], None]: '''The async version of enumerate, except it is not a class, with the addition of the step parameter.'''
async def sleep_forever() -> NoReturn: '''A coroutine that never completes (unless an exception is thrown in, of course).'''
dummy_task: GeneratorCoroutine[None, Any, Any]
'''An awaitable object that completes immediately and is also an exhausted generator, with the `CO_ITERABLE_COROUTINE` flag set.'''
yield_to_event_loop: Awaitable[None]
'''An awaitable object that yields control to the event loop for one iteration when awaited.'''