'''Utilities that cannot be easily classified into any submodule.'''
from _collections_abc import Awaitable, Callable
from typing import Any, Literal, overload
__all__ = 'StateMachine', 'gather_with_limited_concurrency'
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
async def gather_with_limited_concurrency[T](n: int=..., /, *coros: Awaitable[T], ret_exc: Literal[True]) -> list[T|BaseException]: '''`n`, which defaults to :const:`context.GATHER_WITH_LIMITED_CONCURRENCY_DEFAULT_MAX_CONCURRENT`, is used to restrict the number of concurrently running awaitables, whereas `ret_exc` is passed to :func:`asyncio.gather` as `return_exceptions`.'''