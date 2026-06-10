'''Utilities that cannot be easily classified into any submodule.'''
from ._internal.prots import ExcType, SupportsIteration, Timer
from .mixins import ExecutorRequiredAsyncContextMixin, LoopContextMixin
from collections import deque
from collections.abc import Awaitable, Callable, Generator, Iterable, Mapping
from types import TracebackType
from typing import Any, NoReturn, Self, Literal, overload
__all__ = 'CacheWithBackgroundRefresh', 'CallbackAccumulator', 'StateMachine', 'gather_with_limited_concurrency'
class StateMachine:
    '''A simple asynchronous state machine accepting string states.'''
    def __init__(self, state: str): '''Initialize the state machine with the given initial state.'''
    def add(self, from_state: str, to_state: str, condition: Callable[[str, str], Awaitable[Any]]|None=...) -> None:
        '''| Add a condition to the transition from ``from_state`` to ``to_state``.
        | If any condition is ``None`` or returns a truthy value taking the current and new states as positional arguments, the transition is allowed.'''
    def on_enter[T: Callable[[], Awaitable[Any]]](self, state: str) -> Callable[[T], T]: '''Register an asynchronous handler to be called when ``state`` is entered.'''
    def on_exit[T: Callable[[], Awaitable[Any]]](self, state: str) -> Callable[[T], T]: '''Register an asynchronous handler to be called when ``state`` is exited.'''
    async def transition(self, state: str) -> bool: '''Transition from the current state to the new ``state``.'''
@overload
async def gather_with_limited_concurrency[T](n: int=..., /, *coros: Awaitable[T], ret_exc: Literal[False]=...) -> list[T]: ...
@overload
async def gather_with_limited_concurrency[T](n: int=..., /, *coros: Awaitable[T], ret_exc: Literal[True]) -> list[T|BaseException]:
    '''| ``n``, which defaults to :const:`~asyncutils.context.Context.GATHER_WITH_LIMITED_CONCURRENCY_DEFAULT_MAX_CONCURRENT`, is used to restrict the number of
    | concurrently running awaitables.
    | ``ret_exc`` is passed to :func:`asyncio.gather` as the ``return_exceptions`` argument.'''
class CallbackAccumulator[T, **P](deque[Callable[P, T]], ExecutorRequiredAsyncContextMixin[CallbackAccumulator[T, P]]):
    '''A utility class to store synchronous callbacks and call them sequentially in an executor when the context manager exits.

    .. tip:: To iterate through the callbacks at this moment safely, use the :attr:`callbacks` attribute.
    .. note:: This class is no longer used by the pools after a massive rewrite, and only remains here for backwards compatibility.
    .. admonition:: Implementation detail

      The fact that this class currently subclasses :class:`~collections.deque` is subject to change.'''
    @overload
    def __init__(self, name: str, it: SupportsIteration[Callable[P, T]], maxlen: int|None=..., default: object=..., call_once: bool=..., default_getter: Callable[[], tuple[Iterable[object], Mapping[str, object]]]=...): ...
    @overload
    def __init__(self, name: str, *, maxlen: int|None=..., default: object=..., call_once: bool=..., default_getter: Callable[[], tuple[Iterable[object], Mapping[str, object]]]=...):
        '''Initialize the accumulator.

        * ``name`` is the name of attribute gotten on the argument to :meth:`add`.
        * ``maxlen`` is the maximum number of callbacks that can be stored.
        * ``default`` is the default return value of the context manager if no callbacks are added or ``call_once`` is ``False``.
        * If ``call_once`` is ``True``, the callbacks will be called only once when the context manager exits, and then cleared. If ``False``, they will be called every time the context manager exits until they are manually cleared.
        * ``default_getter`` is a function that returns the default arguments to call the callbacks with when the context manager exits. By default, it returns the exception info if ``name`` is ``'__exit__'`` and empty arguments otherwise.'''
    def __call__(self, *a: P.args, **k: P.kwargs) -> None: ...
    def __enter__(self) -> Self: '''Enter the context manager.'''
    @overload
    def __exit__(self, exc_typ: ExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> None: ...
    @overload
    def __exit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> None: '''Call the callbacks.'''
    def add(self, o: object, /) -> None: '''Get the method on the object with the name specified and queue it to be called.'''
    def offer_last(self, o: object, /) -> bool: '''Add a callback from object only if there is space in the accumulator, and return whether it was added.'''
    @property
    def callbacks(self) -> Self: '''Return a view of the callbacks currently stored in the accumulator.'''
    def __iter__(self) -> Generator[Callable[P, T]]: '''Iterate through the callbacks.'''
class CacheWithBackgroundRefresh[T, R](LoopContextMixin):
    '''| A cache that automatically refreshes entries in the background before expiry. Use as an async context manager only.
    | Maintains entries with TTL values and proactively reloads their values from registered loaders in the background when they approach expiration.
    | This ensures availability of fresh data without blocking get operations.'''
    @overload
    def __init__(self, ttl: float|None=..., refresh: float|None=..., *, default_loader: Callable[[T], R], processor: Callable[[BaseException, bool], object]=..., timer: Timer=...): ...
    @overload
    def __init__(self, ttl: float|None=..., refresh: float|None=..., *, processor: Callable[[BaseException, bool], object]=..., timer: Timer=...):
        '''All arguments are optioanl:

        * ``ttl``: Time-to-live in seconds; default :const:`~asyncutils.context.Context.BACKGROUND_REFRESH_CACHE_DEFAULT_TTL`.
        * ``refresh``: Time before TTL expires to begin the refresh; default :const:`~asyncutils.context.Context.BACKGROUND_REFRESH_CACHE_DEFAULT_REFRESH`.
        * ``processor``: Error handler that takes two arguments ``(exc, was_batched)``, where ``exc`` is the exception occurred and
        * ``was_batched`` whether the exception was thrown during a batch refresh, in contrast to a single-item refresh.
        * ``default_loader``: The loader to load values from keys for which specific loaders have not been registered.'''
    def __contains__(self, key: T) -> bool: '''Check if a key exists in the cache.'''
    def register_loader(self, key: T, loader: Callable[[T], R]) -> None: '''Register a specific loader for the key, that will take precedence over the default (if any).'''
    def expired(self, key: T) -> bool: '''Whether the key has overstayed its TTL.'''
    def should_refresh(self, key: T) -> bool: '''Whether the key should be refreshed at this instant.'''
    def time_past(self, key: T) -> float: '''Time having elapsed (in seconds) after the key was last reloaded.'''
    def configure(self, ttl: float, refresh: float, processor: Callable[[BaseException, bool], object]=...) -> None: '''(Re-)configure the cache with the given ``ttl``, ``refresh`` and ``processor``.'''
    def get_loader(self, key: T) -> Callable[[T], R]: '''Get the loader registered for the key, raising :exc:`LookupError` if there is none.'''
    async def __setup__(self) -> None: ...
    async def __cleanup__(self) -> None: ...
    async def clear(self) -> None: '''Remove all entries from the cache asynchronously.'''
    async def get(self, key: T, loader: Callable[[T], R]|None=...) -> R:
        '''| Get the value for the key from the cache.
        | If the key is expired, it is immediately loaded; if it is within the refresh window, return the current value and trigger background refresh.'''
    async def invalidate(self, key: T) -> R|None: '''Remove a key from the cache, returning the corresponding value if it was in the cache.'''
    async def load_item(self, key: T) -> None: '''Load the entry for a key and store it in the cache.'''
    async def refresh_item(self, key: T) -> None: '''Refresh an entry in the background.'''
    async def refresh_loop(self) -> NoReturn: '''This task runs continuously in the background, checking for entries requiring refresh and spawning tasks to do so.'''
