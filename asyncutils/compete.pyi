from ._internal.prots import ExceptionWrapper, FutWrapType, SupportsIteration
from asyncio import AbstractEventLoop
from collections.abc import AsyncIterable, Awaitable, Callable, Coroutine, Generator, Iterable
from typing import Any, Literal, TypeGuard, overload
__all__ = 'convert_to_coro_iter', 'enhanced_gather', 'enhanced_staggered_race', 'first_completed', 'multi_winner_race_with_callback', 'race_with_callback'
@overload
async def first_completed[T](*C: Awaitable[T], ret_exc: Literal[True], timeout: float|None=...) -> ExceptionWrapper|T|None: ...
@overload
async def first_completed[T](*C: Awaitable[T], ret_exc: Literal[False]=..., timeout: float|None=...) -> T|None:
    '''| Return the result of the first coroutine that completes among those passed in.
    | If ``ret_exc`` is ``True``, the coroutine might have errored, in which case the exception it throws is returned in a wrapped form
    | unpackable using :func:`exceptions.unwrap_exc` after checking with :func:`exceptions.exception_occurred`.
    | In any case, the losing coroutines are cancelled together and the function returns when the cancellations finish.'''
async def race_with_callback[T](*C: Awaitable[T], winner: Callable[[T], object]=..., loser: Callable[[Any|BaseException], object]=..., timeout: float|None=...) -> T|None:
    '''| Return the result of the first coroutine to complete, which will have ``winner`` called on it.
    | If no coroutine completes within ``timeout``, ``None`` is returned.
    | The ``loser`` callback is called on each return value of or exception raised by the losing coroutines after seeing :exc:`~asyncio.CancelledError`.'''
async def multi_winner_race_with_callback[T](*C: Awaitable[T], timeout: float, winner: Callable[[T], object]=..., loser: Callable[[Any|BaseException], object]=...) -> list[T]: '''Return a list of all the coroutines that completed within ``timeout``, and cancel the rest, triggering callbacks similarly to :func:`race_with_callback`.'''
def convert_to_coro_iter(cfs: SupportsIteration[Any], *, skip_invalid: bool=..., loop: AbstractEventLoop|None=..., corocheck: Callable[[Any], TypeGuard[Coroutine[Any, Any, Any]]]=..., futwrap: FutWrapType=..., handle_aiter: Callable[[AsyncIterable[Any]], Coroutine[Any, Any, Any]]=..., handle_iter: Callable[[Iterable[Any]], Coroutine[Any, Any, Any]]=...) -> Generator[Coroutine[Any, Any, Any], Any]:
    '''| A helper function to convert a possibly async iterable of futures, coroutines and even (async) iterables `cfs` to a plain generator of
    | coroutines, such that it may be starred and passed into the functions in this module.
    | Originally designed to complement :func:`~asyncio.staggered.staggered_race`.
    | Due to the possibility of ``cfs`` being async and this function being designed to operate in a sync context, it is somewhat inefficient.
    | ``skip_invalid``, which determines whether to raise :exc:`TypeError` for unconvertible items or simply to skip them, defaults to
    | :data:`context.CONVERT_TO_CORO_ITER_DEFAULT_SKIP_INVALID`.
    | ``handle_aiter`` and ``handle_iter`` should be callables taking an async iterable and a sync iterable respectively and returning a coroutine.'''
async def enhanced_staggered_race(cfs: SupportsIteration[Any], delay: float|None=..., *, loop: AbstractEventLoop|None=...) -> tuple[Any, int|None, list[Exception|None]]: ''':func:`asyncio.staggered.staggered_race`, but taking a larger variety of objects as the first argument using :func:`convert_to_coro_iter`; see above.'''
async def enhanced_gather(it: SupportsIteration[Any], return_exceptions: bool=False, *, loop: AbstractEventLoop|None=...) -> list[Any]:
    '''Version of :func:`asyncio.gather` that takes a larger variety of objects as the first argument, using :func:`convert_to_coro_iter` under the hood.

    .. seealso::

      :func:`iters.agather`
        if you just want to pass in an async iterable; this version materializes a list of all the items within but avoids creating the intermediate
        sync futures, which in many cases is a better strategy
'''
