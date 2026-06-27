'''Object-oriented (async) iteration helpers.'''
from ._internal.helpers import LoopMixinBase
from ._internal.prots import SupportsIteration, ValidSlice
from .mixins import LoopContextMixin
from collections.abc import Callable
from types import AsyncGeneratorType
from typing import Self, SupportsIndex, overload
__all__ = 'ABucket', 'AChain', 'APeekable'
class AChain[T]:
    '''Async version of :func:`~itertools.chain` that takes async or sync iterables.'''
    @classmethod
    def from_iterable(cls, it_of_its: SupportsIteration[SupportsIteration[T]]) -> Self:
        '''Construct an :class:`AChain` from ``it_of_its``, an (async) iterable of (async) iterables to chain. If some iterables are chains themselves, their internal iterable of iterables are flattened into that of the returned :class:`AChain`, which may cause unexpected behaviour when iterating through these sources themselves.

        .. tip:: Since the outer iterable is advanced on demand, a possible use case would be to combine chunks of items from different sources as they arrive.
        '''
    def __new__(cls, *its: SupportsIteration[T]) -> Self: '''Construct an :class:`AChain` from the (async) iterables.'''
    def __aiter__(self) -> AsyncGeneratorType[T]: '''Yield items from the first iterable until exhausted, then start on the second, etc.'''
class APeekable[T](LoopMixinBase):
    '''Async version of :class:`more_itertools.peekable`.'''
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, it: SupportsIteration[T]): '''Wrap an (async) iterable in an asynchronous iterator and sequence APIs, supporting lookahead and prepending.'''
    def __aiter__(self) -> Self: '''Return the instance itself.'''
    async def can_peek(self) -> bool: '''Check whether any items are left in the underlying iterable without advancing it.'''
    async def peek(self, default: T=...) -> T: '''Return the next item of the underlying iterable without advancing it, or ``default`` if the items have run out.'''
    def prepend(self, /, *items: T) -> None: '''Yield the prepended items in the order passed in first instead of advancing the underlying iterable.'''
    async def __anext__(self) -> T: '''Return the next item, advancing the iterable.'''
    @overload
    async def __getitem__(self, idx: ValidSlice, /) -> tuple[T, ...]: ...
    @overload
    async def __getitem__(self, idx: SupportsIndex, /) -> T: '''Slice or index access. Must be awaited.'''
class ABucket[T, R](LoopContextMixin):
    '''Async version of :func:`more_itertools.bucket`.'''
    def __init__(self, it: SupportsIteration[T], key: Callable[[T], R], validator: Callable[[R], bool]): '''Divide items from the (async) iterable ``it`` into child generators according to a ``key`` function.'''
    async def contains(self, key: R, /) -> bool: '''If ``validator`` returns ``False`` for ``key``, return ``False`` immediately. Otherwise, advance the iterable and store items until an item mapping to ``key`` under the key function is seen.'''
    def __aiter__(self) -> AsyncGeneratorType[T]: '''Yield the keys of all buckets. When this async generator is exhausted, the original iterable is fully consumed. Unlike the sync version, an exhausted bucket has no keys.'''
    def __getitem__(self, key: R, /) -> AsyncGeneratorType[T]: '''Return an async generator of the items in the original iterable for which the key function gives this key.'''
