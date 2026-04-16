'''Object-oriented (async) iteration helpers.'''
from ._internal.types import SupportsIteration, ValidExcType, ValidSlice
from .mixins import EventualLoopMixin, LoopContextMixin
from _collections_abc import AsyncGenerator, Callable
from types import TracebackType
from typing import Any, Self, SupportsIndex, overload
__all__ = 'abucket', 'achain', 'anullcontext', 'apeekable', 'online_sorter'
class anullcontext:
    '''Simple async-only version of `contextlib.nullcontext`, implemented here to avoid importing `contextlib`.'''
    async def __aenter__(self) -> None: ...
    @overload
    async def __aexit__(self, exc_typ: ValidExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> None: ...
    @overload
    async def __aexit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> None: ...
class achain[T]:
    '''Async version of `itertools.chain`, taking async or sync iterables.'''
    @classmethod
    def from_iterable(cls, it_of_its: SupportsIteration[SupportsIteration[T]]) -> Self: '''Construct an `achain` from `its`, an (async) iterable of (async) iterables to chain.'''
    def __new__(cls, *its: SupportsIteration[T]) -> Self: '''Construct an `achain` from the (async) iterables.'''
    def __aiter__(self) -> AsyncGenerator[T]: '''Yield items from the first iterable until exhausted, then start on the second, etc.'''
class apeekable[T](EventualLoopMixin):
    '''Async version of `more_itertools.peekable`.'''
    def __init__(self, it: SupportsIteration[T]=[]): '''Wraps an (async) iterable in an asynchronous iterator and sequence APIs, supporting lookahead and prependage.'''
    def __aiter__(self) -> Self: '''Return the `apeekable` instance itself.'''
    def __bool__(self) -> bool: '''Check whether any items are left in the underlying iterable without advancing it.'''
    async def peek(self, default: T=...) -> T: '''Return the next item of the underlying iterable without advancing it, or `default` if the items have run out.'''
    def prepend(self, /, *items: T) -> None: '''Make the apeekable yield the prepended items first instead of advancing the underlying iterable.'''
    async def __anext__(self) -> T: '''Return the next item, advancing the iterable.'''
    @overload
    async def __getitem__(self, idx: ValidSlice, /) -> tuple[T, ...]: '''Slice access. Must be awaited.'''
    @overload
    async def __getitem__(self, idx: SupportsIndex, /) -> T: '''Index access. Must be awaited.'''
class abucket[T, R](LoopContextMixin):
    '''Async version of `more_itertools.bucket`.'''
    def __init__(self, it: SupportsIteration[T], key: Callable[[T], R], validator: Callable[[R], bool]): ...
    def __contains__(self, v: R) -> bool: ...
    def __aiter__(self) -> AsyncGenerator[T]: ...
    def __getitem__(self, val: R, /) -> AsyncGenerator[T]: ...
class online_sorter[T]:
    '''A class implementing an async generator-like interface that sorts items as they arrive.'''
    def __init__(self, it: SupportsIteration[T]): ''''''
    def __aiter__(self) -> Self: ...
    async def __anext__(self) -> T: ...
    async def asend(self, item: T) -> None: ...
    @overload
    async def athrow(self, typ: ValidExcType, val: BaseException|None=..., tb: TracebackType|None=...) -> Any: ...
    @overload
    async def athrow(self, exc: BaseException, /) -> Any: ...
    async def aclose(self) -> None: ...