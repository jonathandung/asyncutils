'''The most useful and fundamental patterns and helpers core to this module and are therefore required by the :mod:`asyncutils.console` submodule, among many others.'''
from ._internal.types import ExcType, GeneratorCoroutine, RaiseType, SupportsIteration, SupportsPop, SupportsPopLeft
from asyncio import AbstractEventLoop, Future
from collections.abc import AsyncGenerator, AsyncIterable, Awaitable, Callable, Generator, Iterable, MutableSequence
from types import TracebackType
from typing import Any, Final, Literal, Never, NoReturn, Self, final, overload
__all__ = 'adisembowel', 'adisembowelleft', 'aenumerate', 'aiter_to_gen', 'collect', 'collect_into', 'drop', 'dummy_task', 'event_loop', 'iter_to_agen', 'safe_cancel_batch', 'sleep_forever', 'take', 'yield_to_event_loop'
@final
class event_loop: # noqa: N801
    '''A context manager to manage lifecycles of native event loops. Has specialized handling for :mod:`asyncio` implementation details.'''
    constructor_args: Final = 'dont_release_loop_on_finalization', 'silent_on_finalize', 'dont_try_clear_tasks_on_reuse', 'close_existing_on_exit', 'dont_always_stop_on_exit', 'dont_close_created_on_exit', 'cancel_all_tasks', 'keep_loop', 'suppress_runtime_errors', 'fail_silent', 'dont_allow_reuse', 'dont_reuse', 'dont_attempt_enter', 'attempt_aenter', 'suppress_inner_exit_on_runtime_error', 'suppress_inner_aexit_on_runtime_error' # noqa: PYI015
    '''A tuple of all keyword arguments accepted by the constructor in order of the offset corresponding to the flag in the flags representation.'''
    def __new__(cls, *, dont_release_loop_on_finalization: bool=..., silent_on_finalize: bool=..., dont_try_clear_tasks_on_reuse: bool=..., close_existing_on_exit: bool=..., dont_always_stop_on_exit: bool=..., dont_close_created_on_exit: bool=..., cancel_all_tasks: bool=..., keep_loop: bool=..., suppress_runtime_errors: bool=..., fail_silent: bool=..., dont_allow_reuse: bool=..., dont_reuse: bool=..., dont_attempt_enter: bool=..., attempt_aenter: bool=..., suppress_inner_exit_on_runtime_error: bool=..., suppress_inner_aexit_on_runtime_error: bool=...) -> Self: '''Constructor arguments are self-explanatory. Pass as appropriate; all are applied on top of :const:`context.EVENT_LOOP_BASE_FLAGS`.'''
    def __enter__(self) -> AbstractEventLoop: '''Enter the context, returning the underlying :mod:`asyncio` event loop, which is fetched on demand.'''
    @overload
    def __exit__(self, t: None, v: None, b: None, /) -> Literal[False]: ...
    @overload
    def __exit__(self, t: ExcType, v: BaseException, b: TracebackType, /) -> bool: '''Exit the context. This stops and closes the event loop if the flags say so.'''
    def __reduce__(self) -> tuple[Callable[[int], Self], tuple[int]]: '''Support for pickling.'''
    def factory_reset(self) -> None: '''Restore the default settings from the context (i.e., set the flags to :const:`context.EVENT_LOOP_BASE_FLAGS`).'''
    def clear_flags(self, mask_to_keep: int=...) -> None: '''Reset the configuration of the manager to the equivalent of passing all keyword arguments as ``False``, except those covered by ``mask_to_keep``.'''
    def copy_flags(self) -> Self: '''Return an unentered instance with the same configuration as this that manages a different event loop.'''
    def __hash__(self) -> int: '''Return the flags of the manager as its hash, not considering its state.'''
    @overload
    def flags_eq(self, other: Self, /) -> bool: ...
    @overload
    def flags_eq(self, flags: int, /) -> bool: '''Return whether the configuration of this manager is the same as that of ``other``, regardless of their respective states.'''
    @classmethod
    def from_flags(cls, flags: int, /) -> Self: '''Construct an instance from ``flags``, a bitwise or of options (default :const:`context.EVENT_LOOP_BASE_FLAGS`).'''
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
    | When ``use_existing_executor=True`` is passed (default :const:`context.ITER_TO_AGEN_DEFAULT_USE_EXISTING_EXECUTOR`), the function will attempt to use
    | an existing executor as created by previous calls specifying ``create_executor=True`` (default :const:`context.ITER_TO_AGEN_DEFAULT_MAY_CREATE_EXECUTOR`)
    | to advance the iterable, and fall back to blocking the event loop every step without an executor.
    | If ``strict`` is ``True`` (default :const:`context.ITER_TO_AGEN_DEFAULT_STRICT`), only sync iterables are accepted.'''
@overload
def aiter_to_gen[T, R](ait: AsyncGenerator[T, R], *, use_futures: bool=..., loop: AbstractEventLoop|None=..., strict: bool=...) -> Generator[T, R]: ...
@overload
def aiter_to_gen[T](ait: AsyncIterable[T], *, use_futures: bool=..., loop: AbstractEventLoop|None=..., strict: bool=...) -> Generator[T]: ...
@overload
def aiter_to_gen[T](ait: Iterable[T], *, use_futures: bool=..., loop: AbstractEventLoop|None=..., strict: Literal[False]=...) -> Generator[T]:
    '''| Convert an async iterable ``ait`` to a sync generator.
    | If the event loop is currently running and ``use_futures`` is ``False`` (default :const:`context.AITER_TO_GEN_DEFAULT_ALLOW_FUTURES`), raise :exc:`RuntimeError` to clarify that :class:`concurrent.futures.Future` must be used in this case, one per item yielded,
    | which is somewhat inefficient, but that can't be helped.
    | If ``strict`` is ``True`` (default :const:`context.AITER_TO_GEN_DEFAULT_STRICT`), only async iterables are accepted.'''
def adisembowel[T](it: SupportsPop[T], /) -> AsyncGenerator[T]: '''Asynchronously disembowel an iterable from the right using its pop method and yield its items from right to left.'''
def adisembowelleft[T](it: SupportsPopLeft[T], /) -> AsyncGenerator[T]: '''Asynchronously disembowel an iterable from the left using its popleft method and yield its items from left to right.'''
@overload
async def safe_cancel_batch[T](batch: SupportsIteration[Future[T]], /, *, callback: Callable[[T|BaseException], object]|None=..., disembowel: Literal[False]=..., raising: bool=...) -> None: ...
@overload
async def safe_cancel_batch[T](batch: SupportsPop[Future[T]], /, *, callback: Callable[[T|BaseException], object]|None=..., disembowel: Literal[True], raising: bool=...) -> None:
    '''| Cancel an (async) iterable of futures, waiting for the cancellations to complete asynchronously.
    | The batch cancellation itself can be reliably cancelled.
    | Afterwards, if ``disembowel`` is ``True``, clear the iterable using its :meth:`~list.pop` method repeatedly, falling back to :meth:`~list.clear`.
    | The callback is called on each result or exception of the futures after :exc:`~asyncio.CancelledError` was thrown into them concurrently.
    | If ``raising`` is ``True``, all calls of the callback that themselves threw exceptions are collected into a :exc:`BaseExceptionGroup`,
    | which is then raised.'''
async def collect[T](it: SupportsIteration[T], n: int|None=..., *, default: T|RaiseType=...) -> list[T]:
    '''| Return a list of the first ``n`` items in the (async) iterable, consuming it up to that point exactly.
    | If there are less than ``n`` items to collect, throw :exc:`exceptions.ItemsExhausted` if default is :const:`constants.RAISE` and emit a debug
    | message through the logger before padding the behind of the list with copies of the default if passed otherwise.

    .. seealso::

      :func:`iters.basic_collect`
        a possibly slightly faster variant that doesn't accept a default.

      :func:`iters.to_list`
        the most barebones variant equivalent to the case when ``n`` is not passed.'''
async def collect_into[T](out: MutableSequence[T], it: SupportsIteration[T], n: int|None=..., *, default: T|RaiseType=...) -> None:
    '''| Extend a mutable sequence with the first ``n`` items in the (async) iterable, consuming it up to that point exactly.
    | If there are less than ``n`` items to collect, throw :exc:`exceptions.ItemsExhausted` if default is :const:`constants.RAISE` and emit a debug
    | message through the logger before padding the behind of the list with copies of the default if passed otherwise.'''
@overload
def take[T](it: SupportsIteration[T], n: int, *, default: T|RaiseType) -> AsyncGenerator[T]: ...
@overload
def take[T](it: SupportsIteration[T], n: int|None) -> AsyncGenerator[T]:
    '''Yield ``n`` items from the (async) iterable.

    .. tip::
      :collapsible:

      To ensure there are exactly ``n`` items in the resultant async generator, pass a default value.
      In particular, pass :const:`constants.RAISE` as ``default`` to cause :exc:`exceptions.ItemsExhausted` to be thrown in the case that there
      aren't enough items.
      If ``n`` is None, take all items.'''
def drop[T](it: SupportsIteration[T], n: int, *, raising: bool=...) -> AsyncGenerator[T]: '''Discard ``n`` items from the (async) iterable and yield the rest. If there are not enough items and raising is True, throw ``exceptions.ItemsExhausted``.'''
def aenumerate[T](it: SupportsIteration[T], start: int=..., *, step: int=...) -> AsyncGenerator[tuple[int, T]]: '''The async version of :class:`enumerate`, except it is not a class and additionally supports the ``step`` parameter.'''
async def sleep_forever() -> NoReturn: '''A coroutine that only completes when an exception is thrown in. The exception is propagated.'''
dummy_task: GeneratorCoroutine[Never, Any, Any]
'''An awaitable object that completes immediately. Also an exhausted generator.

.. admonition:: Implementation detail

  This is achieved by setting the :const:`inspect.CO_ITERABLE_COROUTINE` flag on the code of a generator function.'''
yield_to_event_loop: Awaitable[None]
'''An awaitable and picklable singleton that yields control to the event loop for exactly one iteration when awaited, much like ``asyncio.sleep(s)`` for non-positive ``s``.'''
