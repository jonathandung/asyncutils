from .mixins import LoopContextMixin
from .base import yield_to_event_loop, event_loop
from .util import safe_cancel, to_async
from .exceptions import CRITICAL, Critical
from . import context
from time import monotonic
from functools import lru_cache, wraps
from asyncio.locks import Lock, Event
from asyncio.coroutines import iscoroutine
from asyncio.tasks import sleep, gather
from asyncio.exceptions import CancelledError
from ._internal.submodules import caches_all as __all__
class CacheWithBackgroundRefresh(LoopContextMixin):
    __slots__ = '_cache', '_lock', '_loaders', '_ttl', '_refresh', '_processor', '_task', '_event'
    def __init__(self, ttl=None, refresh=None, processor=None, default_loader=None, _d=__import__('_collections').defaultdict): super().__init__(); self._cache, self._lock, self._loaders, self._task, self._event = {}, Lock(), _d(lambda _=default_loader, /: _), None, Event(); self.configure(context.BACKGROUND_REFRESH_CACHE_DEFAULT_TTL if ttl is None else ttl, context.BACKGROUND_REFRESH_CACHE_DEFAULT_REFRESH if refresh is None else refresh, processor)
    def __contains__(self, key): return key in self._cache
    def register_loader(self, key, loader): self._loaders[key] = loader
    def expired(self, key): return self.time_past(key) > self._ttl
    def should_refresh(self, key): return self.time_past(key) > self._ttl-self._refresh if key in self else False
    def time_past(self, key): return monotonic()-self._cache[key].timestamp
    def configure(self, ttl, refresh, processor=None, _=lambda *_: None): self._ttl, self._refresh, self._processor = max(ttl, refresh), min(ttl, refresh), processor or getattr(self, '_processor', _)
    def get_loader(self, key):
        if (k := self._loaders[key]) is None: raise LookupError(f'no loader registered for key {key!r}')
        return k
    async def _process_error(self, e, b, /):
        if iscoroutine(r := await self.loop.run_in_executor(self._processor, e, b)): await r
    async def get(self, key, loader=None):
        async with self._lock:
            if loader: self.register_loader(key, loader)
            if self.should_refresh(key): await self.refresh_item(key)
            if key not in self._cache or self.expired(key): await self.load_item(key)
            return self._cache[key].value
    async def __setup__(self):
        if self._task is None: self._event.clear(); self._task = self.make(self.refresh_loop())
    async def __cleanup__(self):
        if self._task: self._event.set(); await safe_cancel(self._task); self._task = None
    async def load_item(self, key, _=__import__('collections').namedtuple('CacheEntry', 'value timestamp loading', module='asyncutils.caches')):
        _ = _(await self.get_loader(key)(key), monotonic(), False)
        async with self._lock: self._cache[key] = _
    async def refresh_item(self, key):
        async with self._lock:
            if key not in self._loaders or (t := self._cache.get(key)) is None or t.loading: return
            t.loading = True
        try: await self.load_item(key)
        except CRITICAL: raise Critical
        except BaseException as e: t.loading = False; await self._process_error(e, False)
    async def refresh_loop(self):
        r, t = self._refresh, []
        while True:
            try:
                await sleep(r)
                async with self._lock:
                    n = monotonic()
                    for k in self._cache:
                        if not self._cache[k].loading and n-self._cache[k].timestamps > self._ttl-self._refresh: t.append(self.make(self.refresh_item(k)))
                if t: await gather(*t, return_exceptions=True); t.clear()
            except CRITICAL: raise Critical
            except CancelledError: raise
            except BaseException as e: await self._process_error(e, True)
    async def invalidate(self, key):
        async with self._lock: return self._cache.pop(key, None)
    async def clear(self):
        async with self._lock: self._cache.clear()
class AsyncLRUCache:
    __slots__ = '_ttl', '_factory', '_timestamps', '_caches', '_make_key', '_loopctx'
    def __init__(self, maxsize=None, ttl=None, typed=False):
        if maxsize is None: maxsize = context.ASYNC_LRU_CACHE_DEFAULT_MAXSIZE
        self._ttl, self._factory, self._timestamps, self._caches, self._loopctx = ttl, lru_cache(maxsize, typed), {}, {}, event_loop.from_flags(0x200)
    def __call__(self, f, /, _=lambda f, a, k: id(f)<<0x80|hash(a)<<0x40|hash(frozenset(k.items()))):
        self._caches[f] = c = self._factory(f)
        if not hasattr(self, '_make_key'): self._make_key = to_async(_, self.loop)[0]
        async def wrapper(*a, **k):
            K = await self._make_key(f, a, k)
            if self._ttl and monotonic()-self._timestamps.get(K, 0) > self._ttl: c.cache_clear(); del self._timestamps[K]
            if iscoroutine(r := c(*a, **k)): r = await r
            if self._ttl: self._timestamps[K] = monotonic()
            return r
        return wraps(f)(wraps(c, ('cache_info', 'cache_clear'), ())(wrapper))
    async def cache_clear(self):
        self._timestamps.clear(); C = self._caches
        while C: C.popitem()[1].cache_clear(); await yield_to_event_loop
    def __del__(self): self._loopctx.__exit__(None, None, None)
    @property
    def loop(self): return self._loopctx.__enter__()