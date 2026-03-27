from ._internal.protocols import SupportsIteration
from asyncio.events import AbstractEventLoop
from asyncio.futures import Future
from _collections_abc import Coroutine, Awaitable, Callable, Generator, AsyncIterable, Iterable
from concurrent.futures._base import Future as _F
from typing import Any, Literal, TypeGuard, overload
__all__ = 'convert_to_coro_iter', 'enhanced_staggered_race', 'first_completed', 'race_with_callback', 'multi_winner_race_with_callback'
@overload
async def first_completed[T](*C: Coroutine[Any, Any, T], ret_exc: Literal[True], timeout: float|None=..., loop: AbstractEventLoop|None=...) -> BaseException|T|None: ...
@overload
async def first_completed[T](*C: Coroutine[Any, Any, T], ret_exc: Literal[False]=..., timeout: float|None=..., loop: AbstractEventLoop|None=...) -> T|None:
    '''Return the result of the first coroutine that completes among those passed in.
    If ret_exc is True, the coroutine might have errored, in which case the exception it throws is returned.
    In any case, the losing coroutines are cancelled together and the function returns when the cancellations finish.'''
async def race_with_callback[T](*C: Coroutine[Any, Any, T], winner: Callable[[T]]=..., loser: Callable[[Any|BaseException]]=..., timeout: float|None=...) -> T|None:
    '''Return the result of the first coroutine to complete, which will have winner called on it.
    If no coroutine completes within `timeout`, None is returned.
    The loser callback is called on each return value of or exception raised by the losing coroutines after seeing CancelledError.'''
async def multi_winner_race_with_callback[T](*C: Coroutine[Any, Any, T], timeout: float, winner: Callable[[T]]=..., loser: Callable[[Any|BaseException]]=...) -> list[T]: '''Return a list of all the coroutines that completed within `timeout`, and cancel the rest, triggering callbacks similarly to race_with_callback.'''
def convert_to_coro_iter(cfs: SupportsIteration[Awaitable|SupportsIteration], skip_invalid: bool=..., corocheck: Callable[[Any], TypeGuard[Coroutine]]=..., futwrap: Callable[[Future|_F], Future]=..., handle_aiter: Callable[[AsyncIterable], Any]=..., handle_iter: Callable[[Iterable], Any]=...) -> Generator[Coroutine[Any, Any, Any], Any, None]:
    '''A helper function to convert a possibly async iterable of futures, coroutines and even (async) iterables to a plain generator of coroutines,
    such that it may be starred and passed into the functions in this module. Originally designed to complement staggered.staggered_race.
    Due to the possibility of cfs being an async iterable and this function being designed to operate in a sync context, it is highly inefficient.'''
async def enhanced_staggered_race(cfs: SupportsIteration[Awaitable|SupportsIteration], delay: float|None=..., *, loop: AbstractEventLoop|None=...) -> tuple[Any, int|None, list[Exception|None]]: '''asyncio.staggered.staggered_race, but taking a larger variety of objects as the first argument using convert_to_coro_iter. See above.'''