'''Object-oriented (async) iteration helpers.'''
from ._internal.types import SupportsIteration, ValidSlice
from .mixins import LoopBoundMixin, LoopContextMixin
from _collections_abc import AsyncGenerator, Callable
from typing import Self, SupportsIndex, overload
__all__ = 'abucket', 'achain', 'apeekable'
class achain[T]:
    '''Async version of :class:`itertools.chain` that takes async or sync iterables.'''
    @classmethod
    def from_iterable(cls, it_of_its: SupportsIteration[SupportsIteration[T]]) -> Self:
        '''Construct an :class:`achain` from `its`, an (async) iterable of (async) iterables to chain.
        The outer iterable is advanced on demand, so it can combine items from different sources.'''
    def __new__(cls, *its: SupportsIteration[T]) -> Self: '''Construct an :class:`achain` from the (async) iterables.'''
    def __aiter__(self) -> AsyncGenerator[T]: '''Yield items from the first iterable until exhausted, then start on the second, etc.'''
class apeekable[T](LoopBoundMixin):
    '''Async version of :class:`more_itertools.peekable`.'''
    def __init__(self, it: SupportsIteration[T]=[]): '''Wraps an (async) iterable in an asynchronous iterator and sequence APIs, supporting lookahead and prependage.'''
    def __aiter__(self) -> Self: '''Return the :class:`apeekable` instance itself.'''
    def __bool__(self) -> bool: '''Check whether any items are left in the underlying iterable without advancing it.'''
    async def peek(self, default: T=...) -> T: '''Return the next item of the underlying iterable without advancing it, or `default` if the items have run out.'''
    def prepend(self, /, *items: T) -> None: '''Make the apeekable yield the prepended items first instead of advancing the underlying iterable.'''
    async def __anext__(self) -> T: '''Return the next item, advancing the iterable.'''
    @overload
    async def __getitem__(self, idx: ValidSlice, /) -> tuple[T, ...]: ...
    @overload
    async def __getitem__(self, idx: SupportsIndex, /) -> T: '''Index access. Must be awaited.'''
class abucket[T, R](LoopContextMixin):
    '''Async version of :class:`more_itertools.bucket`.'''
    def __init__(self, it: SupportsIteration[T], key: Callable[[T], R], validator: Callable[[R], bool]): ...
    def __contains__(self, v: R) -> bool: ...
    def __aiter__(self) -> AsyncGenerator[T]: ...
    def __getitem__(self, val: R, /) -> AsyncGenerator[T]: ...