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
        '''Construct an :class:`achain` from `it_of_its`, an (async) iterable of (async) iterables to chain.

        .. tip:: Since the outer iterable is advanced on demand, a possible use case would be to combine chunks of items from different sources as they arrive.'''
    def __new__(cls, *its: SupportsIteration[T]) -> Self: '''Construct an :class:`achain` from the (async) iterables.'''
    def __aiter__(self) -> AsyncGenerator[T]: '''Yield items from the first iterable until exhausted, then start on the second, etc.'''
class apeekable[T](LoopBoundMixin):
    '''Async version of :class:`more_itertools.peekable`.'''
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, it: SupportsIteration[T]): '''Wraps an (async) iterable in an asynchronous iterator and sequence APIs, supporting lookahead and prependage.'''
    def __aiter__(self) -> Self: '''Return the instance itself.'''
    def __bool__(self) -> bool: '''Check whether any items are left in the underlying iterable without advancing it.'''
    async def peek(self, default: T=...) -> T: '''Return the next item of the underlying iterable without advancing it, or `default` if the items have run out.'''
    def prepend(self, /, *items: T) -> None: '''Yield the prepended items in the order passed in first instead of advancing the underlying iterable.'''
    async def __anext__(self) -> T: '''Return the next item, advancing the iterable.'''
    @overload
    async def __getitem__(self, idx: ValidSlice, /) -> tuple[T, ...]: ...
    @overload
    async def __getitem__(self, idx: SupportsIndex, /) -> T: '''Slice or index access. Must be awaited.'''
class abucket[T, R](LoopContextMixin):
    '''Async version of :class:`more_itertools.bucket`.'''
    def __init__(self, it: SupportsIteration[T], key: Callable[[T], R], validator: Callable[[R], bool]): '''Divide items from the (async) iterable `it` into child generators according to a `key` function.'''
    def __contains__(self, key: R, /) -> bool: '''If `validator` returns `False` for `key`, return `False` immediately. Otherwise, advance the iterable and store items until an item mapping to `key` under the key function is seen.'''
    def __aiter__(self) -> AsyncGenerator[T]: '''Yield the keys of all buckets. When this async generator is exhausted, the original iterable is fully consumed.'''
    def __getitem__(self, key: R, /) -> AsyncGenerator[T]: '''Return an async generator of the items in the original iterable for which the key function gives this key.'''