from .mixins import LoopContextMixin
from ._internal.log import error
from .util import safe_cancel
from .exceptions import CRITICAL, Critical
from . import constants
from time import monotonic
from functools import lru_cache, wraps
from asyncio.locks import Lock, Event
from asyncio.coroutines import iscoroutine
from asyncio.tasks import sleep, gather
from asyncio.exceptions import CancelledError
from ._internal.submodules import caches_all as __all__
class CacheWithBackgroundRefresh(LoopContextMixin):
    __slots__ = '_cache', '_lock', '_loaders', '_ttl', '_refresh', '_processor', '_task', '_event'
    def __init__(self, ttl=None, refresh=None, processor=None, default_loader=None, _d=__import__('_collections').defaultdict): super().__init__(); self._cache, self._lock, self._loaders, self._task, self._event = {}, Lock(), _d(lambda: default_loader), None, Event(); self.configure(constants.BACKGROUND_REFRESH_CACHE_DEFAULT_TTL if ttl is None else ttl, constants.BACKGROUND_REFRESH_CACHE_DEFAULT_REFRESH if refresh is None else refresh, processor)
    def __contains__(self, key): return key in self._cache
    def register_loader(self, key, loader): self._loaders[key] = loader
    def expired(self, key): return self.time_past(key) > self._ttl
    def should_refresh(self, key): return self.time_past(key) > self._ttl-self._refresh if key in self else False
    def time_past(self, key): return monotonic()-self._cache[key]['timestamp']
    def configure(self, ttl, refresh, processor=None, _d=lambda x, *_: error(x)): self._ttl, self._refresh, self._processor = *map(lambda f: f(ttl, refresh), (max, min)), processor or getattr(self, '_processor', _d)
    def get_loader(self, key):
        if (k := self._loaders[key]) is None: raise LookupError(f'no loader registered for key {key!r}')
        return k
    async def get(self, key, loader=None):
        async with self._lock:
            if loader: self.register_loader(key, loader)
            if self.should_refresh(key): await self.refresh_item(key)
            if key not in self._cache or self.expired(key): await self.load_item(key)
            return self._cache[key]['value']
    async def __setup__(self):
        if self._task is None: self._event.clear(); self._task = self.make(self.refresh_loop())
    async def __cleanup__(self):
        if self._task: self._event.set(); await safe_cancel(self._task); self._task = None
    async def load_item(self, key): self._cache[key] = {'value': await self.get_loader(key)(), 'timestamp': monotonic(), 'loading': False}
    async def refresh_item(self, key):
        e = None
        async with self._lock:
            if key not in self._loaders or key not in self or self._cache[key]['loading']: return
            self._cache[key]['loading'] = True
            try: await self.load_item(key)
            except CRITICAL: raise Critical
            except BaseException as e:
                if key in self._cache: self._cache[key]['loading'] = False
        if e: self._processor(e, False)
    async def refresh_loop(self):
        r, t = self._refresh, []
        while True:
            try:
                await sleep(r); t.clear()
                async with self._lock:
                    n = monotonic()
                    for k in self._cache:
                        if not self._cache[k]['loading'] and n-self._cache[k]['timestamp'] > self._ttl-self._refresh: t.append(self.make(self.refresh_item(k)))
                if t: await gather(*t, return_exceptions=True)
            except CRITICAL: raise Critical
            except CancelledError: break
            except BaseException as e: self._processor(e, True)
    async def invalidate(self, key):
        async with self._lock: return self._cache.pop(key, None)
    async def clear(self):
        async with self._lock: self._cache.clear()
class AsyncLRUCache:
    __slots__ = '_ttl', '_factory', '_timestamps', '_caches'
    def __init__(self, maxsize=None, ttl=None, typed=False):
        if maxsize is None: maxsize = constants.ASYNC_LRU_CACHE_DEFAULT_MAXSIZE
        self._ttl, self._factory, self._timestamps, self._caches = ttl, lru_cache(maxsize, typed), {}, {}
    def __call__(self, f):
        self._caches[f] = c = self._factory(f)
        async def wrapper(*a, **k):
            K = self._make_key(f, a, k)
            if self._ttl and monotonic()-self._timestamps.get(K, 0) > self._ttl: c.cache_clear(); del self._timestamps[K]
            r = c(*a, **k)
            if iscoroutine(r): r = await r
            if self._ttl: self._timestamps[K] = monotonic()
            return r
        wrapper.__dict__.update({k: getattr(c, k) for k in ('cache_info', 'cache_clear')}); return wraps(f)(wrapper)
    def _make_key(self, f, a, k): return (id(f), a, frozenset(k.items()))
    def cache_clear(self):
        self._timestamps.clear(); C = self._caches
        while C: C.popitem()[1].cache_clear()