'''The most useful and fundamental patterns and helpers core to this module and are therefore required by the :mod:`asyncutils.console` submodule, among many others.'''
from ._internal.prots import ExcType, GeneratorCoroutine, RaiseType, SupportsIteration, SupportsPop, SupportsPopLeft
from asyncio import AbstractEventLoop, Future
from collections.abc import AsyncGenerator, AsyncIterable, Awaitable, Callable, Generator, Iterable, MutableSequence
from enum import IntFlag
from types import TracebackType
from typing import Any, Literal, Never, NoReturn, Self, final, overload
__all__ = 'adisembowel', 'adisembowelleft', 'aenumerate', 'aiter_to_gen', 'collect', 'collect_into', 'drop', 'dummy_task', 'event_loop', 'iter_to_agen', 'safe_cancel_batch', 'sleep_forever', 'take', 'yield_to_event_loop'
@final
class event_loop: # noqa: N801
    '''A context manager controlling lifecycles of native event loops. Has specialized handling for :mod:`asyncio` implementation details.'''
    class Flags(IntFlag):
        '''An enumeration of all keyword arguments accepted by the constructor in order of the offset corresponding to the flag in the flags representation.'''
        FLIP_RELEASE_LOOP_ON_FINALIZATION = 1
        SILENT_ON_FINALIZE = 2
        DONT_TRY_CLEAR_TASKS_ON_REUSE = 4
        CLOSE_EXISTING_ON_EXIT = 8
        DONT_ALWAYS_STOP_ON_EXIT = 16
        DONT_CLOSE_CREATED_ON_EXIT = 32
        CANCEL_ALL_TASKS = 64
        KEEP_LOOP = 128
        SUPPRESS_RUNTIME_ERRORS = 256
        FAIL_SILENT = 512
        DONT_ALLOW_REUSE = 1024
        DONT_REUSE = 2048
        DONT_ATTEMPT_ENTER = 4096
        ATTEMPT_AENTER = 8192
        SUPPRESS_INNER_EXIT_ON_RUNTIME_ERROR = 16384
        SUPPRESS_INNER_AEXIT_ON_RUNTIME_ERROR = 32768
    def __new__(cls, *, flip_release_loop_on_finalization: bool=..., silent_on_finalize: bool=..., dont_try_clear_tasks_on_reuse: bool=..., close_existing_on_exit: bool=..., dont_always_stop_on_exit: bool=..., dont_close_created_on_exit: bool=..., cancel_all_tasks: bool=..., keep_loop: bool=..., suppress_runtime_errors: bool=..., fail_silent: bool=..., dont_allow_reuse: bool=..., dont_reuse: bool=..., dont_attempt_enter: bool=..., attempt_aenter: bool=..., suppress_inner_exit_on_runtime_error: bool=..., suppress_inner_aexit_on_runtime_error: bool=...) -> Self: '''Constructor arguments are self-explanatory. Pass as appropriate; all are applied on top of :const:`~asyncutils.context.Context.EVENT_LOOP_BASE_FLAGS`.'''
    def __enter__(self) -> AbstractEventLoop: '''Enter the context, returning the underlying :mod:`asyncio` event loop, which is fetched on demand.'''
    @overload
    def __contains__(self, flagname: str, /) -> bool: ...
    @overload
    def __contains__(self, flag: int, /) -> bool: '''Return whether the manager has the flag specified by ``name`` or ``flag``.'''
    @overload
    def __exit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> Literal[False]: ...
    @overload
    def __exit__(self, exc_typ: ExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> bool: '''Exit the context. This stops and closes the event loop if the flags say so.'''
    def __reduce__(self) -> tuple[Callable[[int], Self], tuple[int]]: '''Support for pickling.'''
    def __del__(self) -> None: '''Finalize the manager by calling :meth:`__exit__` if necessary.'''
    def factory_reset(self) -> None: '''Restore the default settings from the context (i.e., set the flags to :const:`~asyncutils.context.Context.EVENT_LOOP_BASE_FLAGS`).'''
    def clear_flags(self, mask_to_keep: int=...) -> None: '''Reset the configuration of the manager to the equivalent of passing all keyword arguments as ``False``, except those covered by ``mask_to_keep``.'''
    def copy_flags(self) -> Self: '''Return an unentered instance with the same configuration as this that manages a different event loop.'''
    def __hash__(self) -> int: '''Return the flags of the manager as its hash, not considering its state.'''
    @overload
    def flags_eq(self, other: Self, /) -> bool: ...
    @overload
    def flags_eq(self, flags: int, /) -> bool: '''Return whether the configuration of this manager is the same as that of ``other``, regardless of their respective states.'''
    @classmethod
    def from_flags(cls, flags: int, /) -> Self: '''Construct an instance from ``flags``, a bitwise or of options (default :const:`~asyncutils.context.Context.EVENT_LOOP_BASE_FLAGS`).'''
    def _get_unclosed_loop(self, factory: Callable[[], AbstractEventLoop]=...) -> AbstractEventLoop: '''Return a usable :mod:`asyncio` event loop from the internal pool, or a new event loop if there are none.'''
@overload
def iter_to_agen[T, R](it: AsyncGenerator[T, R], sentinel: T=..., *, use_existing_executor: bool=..., create_executor: bool=..., strict: Literal[False]=...) -> AsyncGenerator[T, R]: ...
@overload
def iter_to_agen[T](it: AsyncIterable[T], sentinel: T=..., *, use_existing_executor: bool=..., create_executor: bool=..., strict: Literal[False]=...) -> AsyncGenerator[T]: ...
@overload
def iter_to_agen[T](it: Iterable[T], *, use_existing_executor: bool=..., create_executor: bool=..., strict: bool=...) -> AsyncGenerator[T]: ...
@overload
def iter_to_agen[T](it: Iterable[T], sentinel: T, *, use_existing_executor: bool=..., create_executor: bool=..., strict: bool=...) -> AsyncGenerator[T]:
    '''| Convert the (async) iterable ``it`` to an async generator as non-blockingly as possible.
    | If ``it`` is an async generator and ``sentinel`` is not passed, it is returned as is.
    | Values sent to the return async generator will be passed through to the original.
    | The async generator will stop when it encounters an item identical to ``sentinel``.
    | When ``use_existing_executor=True`` is passed (default :const:`~asyncutils.context.Context.ITER_TO_AGEN_DEFAULT_USE_EXISTING_EXECUTOR`), the function will attempt to use an existing executor as created by previous calls specifying ``create_executor=True`` (default :const:`~asyncutils.context.Context.ITER_TO_AGEN_DEFAULT_MAY_CREATE_EXECUTOR`) to advance the iterable, and fall back to blocking the event loop every step without an executor.
    | If ``strict`` is ``True`` (default :const:`~asyncutils.context.Context.ITER_TO_AGEN_DEFAULT_STRICT`), only sync iterables are accepted.'''
@overload
def aiter_to_gen[T, R](ait: AsyncGenerator[T, R], *, use_futures: bool=..., loop: AbstractEventLoop|None=..., strict: bool=...) -> Generator[T, R]: ...
@overload
def aiter_to_gen[T](ait: AsyncIterable[T], *, use_futures: bool=..., loop: AbstractEventLoop|None=..., strict: bool=...) -> Generator[T]: ...
@overload
def aiter_to_gen[T](ait: Iterable[T], *, use_futures: bool=..., loop: AbstractEventLoop|None=..., strict: Literal[False]=...) -> Generator[T]:
    '''| Convert an async iterable ``ait`` to a sync generator.
    | If the event loop is currently running and ``use_futures`` is ``False`` (default :const:`~asyncutils.context.Context.AITER_TO_GEN_DEFAULT_ALLOW_FUTURES`), raise :exc:`RuntimeError` to clarify that :class:`concurrent.futures.Future` must be used in this case, one per item yielded, which is somewhat inefficient, but that can't be helped.
    | If ``strict`` is ``True`` (default :const:`~asyncutils.context.Context.AITER_TO_GEN_DEFAULT_STRICT`), only async iterables are accepted.'''
def adisembowel[T](it: SupportsPop[T], /) -> AsyncGenerator[T]: '''Asynchronously disembowel an iterable from the right using its pop method and yield its items from right to left.'''
def adisembowelleft[T](it: SupportsPopLeft[T], /) -> AsyncGenerator[T]: '''Asynchronously disembowel an iterable from the left using its popleft method and yield its items from left to right.'''
@overload
async def safe_cancel_batch[T](batch: SupportsIteration[Future[T]], /, *, callback: Callable[[T|BaseException], object]|None=..., disembowel: Literal[False]=..., raising: bool=...) -> None: ...
@overload
async def safe_cancel_batch[T](batch: SupportsPop[Future[T]], /, *, callback: Callable[[T|BaseException], object]|None=..., disembowel: Literal[True], raising: bool=...) -> None:
    '''| Cancel an (async) iterable of futures, waiting for the cancellations to complete asynchronously.
    | The batch cancellation itself can be cancelled, but less reliably and granularly than :func:`~asyncutils.util.safe_cancel`.
    | Afterwards, if ``disembowel`` is ``True``, clear the iterable using its :meth:`~list.pop` method repeatedly, falling back to :meth:`~list.clear`.
    | The callback is called on each result or exception of the futures after :exc:`~asyncio.CancelledError` was thrown into them concurrently.
    | If ``raising`` is ``True``, all calls of the callback that themselves threw exceptions are collected into a :exc:`BaseExceptionGroup`, which is then raised.'''
async def collect[T](it: SupportsIteration[T], n: int|None=..., *, default: T|RaiseType=...) -> list[T]:
    '''| Return a list of the first ``n`` items in the (async) iterable, consuming it up to that point exactly.
    | If there are less than ``n`` items to collect, throw :exc:`~asyncutils.exceptions.ItemsExhausted` if default is :const:`~asyncutils.constants.RAISE` and emit a debug message through the logger before padding the behind of the list with copies of the default if passed otherwise.

    .. seealso::

      :func:`~asyncutils.iters.basic_collect`
        a possibly slightly faster variant that doesn't accept a default.

      :func:`~asyncutils.iters.to_list`
        the most barebones variant equivalent to the case when ``n`` is not passed.'''
async def collect_into[T](out: MutableSequence[T], it: SupportsIteration[T], n: int|None=..., *, default: T|RaiseType=...) -> None:
    '''| Extend a mutable sequence with the first ``n`` items in the (async) iterable, consuming it up to that point exactly.
    | If there are less than ``n`` items to collect, throw :exc:`~asyncutils.exceptions.ItemsExhausted` if default is :const:`~asyncutils.constants.RAISE` and emit a debug message through the logger before padding the behind of the list with copies of the default if passed otherwise.'''
@overload
def take[T](it: SupportsIteration[T], n: int, *, default: T|RaiseType) -> AsyncGenerator[T]: ...
@overload
def take[T](it: SupportsIteration[T], n: int|None) -> AsyncGenerator[T]:
    '''Yield ``n`` items from the (async) iterable. If ``n`` is None, take all items.

    .. tip::
      :collapsible:

      To ensure there are exactly ``n`` items in the resultant async generator, pass a default value.
      In particular, pass :const:`~asyncutils.constants.RAISE` as ``default`` to cause :class:`~asyncutils.exceptions.ItemsExhausted` to be thrown in the case that there aren't enough items.'''
def drop[T](it: SupportsIteration[T], n: int, *, raising: bool=...) -> AsyncGenerator[T]: '''Discard ``n`` items from the (async) iterable and yield the rest. If there are not enough items and ``raising`` is ``True``, throw :exc:`~asyncutils.exceptions.ItemsExhausted`.'''
def aenumerate[T](it: SupportsIteration[T], start: int=..., *, step: int=...) -> AsyncGenerator[tuple[int, T]]: '''The async version of :class:`enumerate`, except it is not a class and additionally supports the ``step`` parameter.'''
async def sleep_forever() -> NoReturn: '''A coroutine that only completes when an exception is thrown in. The exception is propagated.'''
dummy_task: GeneratorCoroutine[Never, Any, Any]
'''An awaitable object that completes immediately. Also an exhausted generator.

.. admonition:: Implementation detail

  This is achieved by setting the :data:`inspect.CO_ITERABLE_COROUTINE` flag on the code of a generator function.'''
yield_to_event_loop: Awaitable[None]
'''An awaitable and picklable singleton that yields control to the event loop for exactly one iteration when awaited, much like ``asyncio.sleep(s)`` for non-positive ``s``.'''
