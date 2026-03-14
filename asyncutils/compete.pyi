from ._internal.protocols import SupportsIteration
from _collections_abc import Coroutine, Awaitable, Callable, Generator, AsyncIterable, Iterable
from typing import Any, Literal, TypeGuard, overload
from asyncio.futures import Future
from asyncio.events import AbstractEventLoop
from concurrent.futures._base import Future as _F
__all__ = 'convert_to_coro_iter', 'enhanced_staggered_race', 'first_completed', 'race_with_callback'
@overload
async def first_completed[T](*C: Coroutine[Any, Any, T], ret_exc: Literal[True], timeout: float|None=..., loop: AbstractEventLoop|None=...) -> BaseException|T|None: ...
@overload
async def first_completed[T](*C: Coroutine[Any, Any, T], ret_exc: Literal[False]=..., timeout: float|None=..., loop: AbstractEventLoop|None=...) -> T|None:
    '''Return the result of the first coroutine that completes among those passed in.
    If ret_exc is True, the coroutine might have errored, in which case the exception it throws is returned.
    In any case, the losing coroutines are cancelled together and the function returns when the cancellations finish.'''
async def race_with_callback[T](*C: Coroutine[Any, Any, T], winner: Callable[[T], Awaitable[None]]|None=..., loser: Callable[[BaseException], Awaitable[None]]|None=..., timeout: float|None=...) -> T|None: ...
def convert_to_coro_iter(cfs: SupportsIteration[Awaitable|SupportsIteration], skip_invalid: bool=..., corocheck: Callable[[Any], TypeGuard[Coroutine[Any, Any, Any]]]=..., futwrap: Callable[[Future|_F], Future]=..., handle_aiter: Callable[[AsyncIterable], Any]=..., handle_iter: Callable[[Iterable], Any]=...) -> Generator[Coroutine[Any, Any, Any], Any, None]: '''A helper function to convert a possibly async iterable of futures, coroutines and even (async) iterables to a plain generator of coroutines, such that it may be starred and passed into the functions in this module. Originally designed to complement staggered.staggered_race.'''
async def enhanced_staggered_race(cfs: SupportsIteration[Awaitable|SupportsIteration], delay: float|None=..., *, loop: AbstractEventLoop|None=...) -> tuple[Any, int|None, list[Exception|None]]: ...