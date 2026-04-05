from .mixins import LoopContextMixin
from _collections_abc import Callable, Coroutine
from typing import Any, NoReturn, overload
__all__ = 'AsyncLRUCache', 'CacheWithBackgroundRefresh'
class CacheWithBackgroundRefresh[T, R](LoopContextMixin):
    '''A cache that automatically refreshes entries in the background before expiry. Use as a context manager.
    Maintains entries with TTL values and proactively reloads their values from registered loaders in the background when they approach expiration.
    This ensures availability of fresh data without blocking get operations.'''
    @overload
    def __init__(self, ttl: float|None=..., refresh: float|None=..., *, processor: Callable[[BaseException, bool], Any]=..., default_loader: Callable[[T], R]):
        '''`ttl` (optional): Time-to-live in seconds; default `context.BACKGROUND_REFRESH_CACHE_DEFAULT_TTL`.
        `refresh` (optional): Time before TTL expires to begin the refresh; default `context.BACKGROUND_REFRESH_CACHE_DEFAULT_REFRESH`.
        `processor` (optional): Error handler that takes two arguments `(exc, was_batched)`, where `exc` is the exception occurred and
        `was_batched` whether the exception was thrown during a batch refresh, in contrast to a single-item refresh.
        `default_loader` (optional): The loader to load values from keys for which specific loaders have not been registered.'''
    @overload
    def __init__(self, ttl: float|None=..., refresh: float|None=..., *, processor: Callable[[BaseException, bool], Any]=...): ...
    def __contains__(self, key: T) -> bool: '''Check if a key exists in the cache.'''
    def register_loader(self, key: T, loader: Callable[[T], R]) -> None: '''Register a specific loader for the key, that will take precedence over the default (if any).'''
    def expired(self, key: T) -> bool: '''Whether the key has overstayed its TTL.'''
    def should_refresh(self, key: T) -> bool: '''Whether the key should be refreshed at this instant.'''
    def time_past(self, key: T) -> float: '''Time having elapsed (in seconds) after the key was last reloaded.'''
    def configure(self, ttl: float, refresh: float, processor: Callable[[BaseException, bool], Any]=...) -> None: '''(Re)configure the cache.'''
    def get_loader(self, key: T) -> Callable[[T], R]: '''Get the loader registered for the key, raising LookupError if there is none.'''
    async def __setup__(self) -> None: ...
    async def __cleanup__(self) -> None: ...
    async def clear(self) -> None: '''Remove all entries from the cache asynchronously.'''
    async def get(self, key: T, loader: Callable[[T], R]|None=...) -> R:
        '''Get the value for the key from the cache.
        If the key is expired, it is immediately loaded; if it is within the refresh window, return the current value and trigger background refresh.'''
    async def invalidate(self, key: T) -> R|None: '''Remove a key from the cache, returning the corresponding value if it was in the cache.'''
    async def load_item(self, key: T) -> None: '''Load the entry for a key and store it in the cache.'''
    async def refresh_item(self, key: T) -> None: '''Refresh an entry in the background.'''
    async def refresh_loop(self) -> NoReturn: '''This task runs continuously in the background, checking for entries requiring refresh and spawning tasks to do so.'''
class AsyncLRUCache(LoopContextMixin):
    '''An async-compatible LRU cache with optional TTL. Use as a context manager and decorator.'''
    def __init__(self, maxsize: int|None=..., ttl: float|None=..., typed: bool=...):
        '''`maxsize` (optional): Maximum number of entries to cache; default `context.ASYNC_LRU_CACHE_DEFAULT_MAXSIZE`.
        `ttl` (optional): Time-to-live in seconds. If None, TTL is disabled.
        `typed` (optional): Whether to cache different argument types separately.'''
    @overload
    def __call__[T: Coroutine, **P](self, f: Callable[P, T], /) -> Callable[P, T]: '''The calls of the returned async function will now be cached in this cache.'''
    @overload
    def __call__[T, **P](self, f: Callable[P, T], /) -> Callable[P, Coroutine[Any, Any, T]]: ...
    def cache_clear(self) -> None: '''Clear all cache entries.'''