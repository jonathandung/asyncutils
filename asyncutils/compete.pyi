from ._internal.types import FutWrapType, SupportsIteration
from _collections_abc import AsyncIterable, Callable, Coroutine, Generator, Iterable
from asyncio.events import AbstractEventLoop
from typing import Any, Literal, TypeGuard, overload
__all__ = 'convert_to_coro_iter', 'enhanced_gather', 'enhanced_staggered_race', 'first_completed', 'multi_winner_race_with_callback', 'race_with_callback'
@overload
async def first_completed[T](*C: Coroutine[Any, Any, T], ret_exc: Literal[True], timeout: float|None=..., loop: AbstractEventLoop|None=...) -> BaseException|T|None: ...
@overload
async def first_completed[T](*C: Coroutine[Any, Any, T], ret_exc: Literal[False]=..., timeout: float|None=..., loop: AbstractEventLoop|None=...) -> T|None:
    '''Return the result of the first coroutine that completes among those passed in.
    If ret_exc is True, the coroutine might have errored, in which case the exception it throws is returned.
    In any case, the losing coroutines are cancelled together and the function returns when the cancellations finish.'''
async def race_with_callback[T](*C: Coroutine[Any, Any, T], winner: Callable[[T], object]=..., loser: Callable[[Any|BaseException], object]=..., timeout: float|None=...) -> T|None:
    '''Return the result of the first coroutine to complete, which will have winner called on it.
    If no coroutine completes within `timeout`, None is returned.
    The loser callback is called on each return value of or exception raised by the losing coroutines after seeing CancelledError.'''
async def multi_winner_race_with_callback[T](*C: Coroutine[Any, Any, T], timeout: float, winner: Callable[[T], object]=..., loser: Callable[[Any|BaseException], object]=...) -> list[T]: '''Return a list of all the coroutines that completed within `timeout`, and cancel the rest, triggering callbacks similarly to race_with_callback.'''
def convert_to_coro_iter(cfs: SupportsIteration[Any], *, skip_invalid: bool=..., loop: AbstractEventLoop|None=..., corocheck: Callable[[Any], TypeGuard[Coroutine[Any, Any, Any]]]=..., futwrap: FutWrapType=..., handle_aiter: Callable[[AsyncIterable[Any]], object]=..., handle_iter: Callable[[Iterable[Any]], object]=...) -> Generator[Coroutine[Any, Any, Any], Any, None]:
    '''A helper function to convert a possibly async iterable of futures, coroutines and even (async) iterables to a plain generator of coroutines,
    such that it may be starred and passed into the functions in this module. Originally designed to complement :func:`~asyncio.staggered.staggered_race`.
    Due to the possibility of `cfs` being an async iterable and this function being designed to operate in a sync context, it is somewhat inefficient.'''
async def enhanced_staggered_race(cfs: SupportsIteration[Any], delay: float|None=..., *, loop: AbstractEventLoop|None=...) -> tuple[Any, int|None, list[Exception|None]]: ''':func:`asyncio.staggered.staggered_race`, but taking a larger variety of objects as the first argument using :func:`convert_to_coro_iter`; see above.'''
async def enhanced_gather(it: SupportsIteration[Any], return_exceptions: bool=False, *, loop: AbstractEventLoop|None=...) -> list[Any]: ''':func:`asyncio.gather`, but taking a larger variety of objects as the first argument using :func:`convert_to_coro_iter`; see above.'''