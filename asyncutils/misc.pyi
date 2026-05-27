'''Utilities that cannot be easily classified into any submodule.'''
from ._internal.types import SupportsIteration, ExcType
from .mixins import ExecutorRequiredAsyncContextMixin
from _collections_abc import Awaitable, Callable, Generator, Iterable, Mapping
from collections import deque
from types import TracebackType
from typing import Any, Self, Literal, overload
__all__ = 'CallbackAccumulator', 'StateMachine', 'gather_with_limited_concurrency'
class StateMachine:
    '''A simple asynchronous state machine accepting string states.'''
    def __init__(self, state: str): '''Initialize the state machine with the given initial state.'''
    def add(self, from_state: str, to_state: str, condition: Callable[[str, str], Awaitable[Any]]|None=...) -> None:
        '''| Add a condition to the transition from `from_state` to `to_state`.
        | If any condition is `None` or returns a truthy value taking the current and new states as positional arguments, the transition is allowed.'''
    def on_enter[F: Callable[[], Awaitable[Any]]](self, state: str) -> Callable[[F], F]: '''Register an asynchronous handler to be called when `state` is entered.'''
    def on_exit[F: Callable[[], Awaitable[Any]]](self, state: str) -> Callable[[F], F]: '''Register an asynchronous handler to be called when `state` is exited.'''
    async def transition(self, state: str) -> bool: '''Transition from the current state to the new `state`.'''
@overload
async def gather_with_limited_concurrency[T](n: int=..., /, *coros: Awaitable[T], ret_exc: Literal[False]=...) -> list[T]: ...
@overload
async def gather_with_limited_concurrency[T](n: int=..., /, *coros: Awaitable[T], ret_exc: Literal[True]) -> list[T|BaseException]:
    '''| `n`, which defaults to :const:`context.GATHER_WITH_LIMITED_CONCURRENCY_DEFAULT_MAX_CONCURRENT`, is used to restrict the number of concurrently
    | running awaitables.
    | `ret_exc` is passed to :func:`asyncio.gather` as the `return_exceptions` argument.'''
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

        * `name` is the name of attribute gotten on the argument to :meth:`add`.
        * `maxlen` is the maximum number of callbacks that can be stored.
        * `default` is the default return value of the context manager if no callbacks are added or `call_once` is `False`.
        * If `call_once` is `True`, the callbacks will be called only once when the context manager exits, and then cleared. If `False`, they will be called every time the context manager exits until they are manually cleared.
        * `default_getter` is a function that returns the default arguments to call the callbacks with when the context manager exits. By default, it returns the exception info if `name` is `'__exit__'` and empty arguments otherwise.'''
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