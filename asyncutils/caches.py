__lazy_modules__ = frozenset(('asyncio', 'functools'))
from asyncutils import CRITICAL, Critical, LoopContextMixin, event_loop, getcontext, safe_cancel, to_async
from asyncutils._internal import patch as P
from asyncutils._internal.helpers import fullname
from asyncutils._internal.submodules import caches_all as __all__
from asyncio import CancelledError, Event, Lock, gather, iscoroutine, sleep
from collections import defaultdict, namedtuple
from functools import lru_cache, wraps
from sys import audit
from time import monotonic
class CacheWithBackgroundRefresh(LoopContextMixin):
    __slots__ = '_cache', '_event', '_loaders', '_lock', '_processor', '_refresh', '_task', '_timer', '_ttl'
    def __init__(self, ttl=None, refresh=None, *, processor=None, default_loader=None, timer=monotonic, _=defaultdict):
        C = getcontext()
        if ttl is None: ttl = C.BACKGROUND_REFRESH_CACHE_DEFAULT_TTL
        if refresh is None: refresh = C.BACKGROUND_REFRESH_CACHE_DEFAULT_REFRESH
        audit(fullname(self), ttl, refresh); super().__init__(); self._cache, self._lock, self._loaders, self._task, self._event, self._timer = {}, Lock(), _(lambda _=default_loader, /: _), None, Event(), timer; self.configure(ttl, refresh, processor)
    def __contains__(self, key): return key in self._cache
    def register_loader(self, key, loader): self._loaders[key] = loader
    def expired(self, key): return self.time_past(key) > self._ttl
    def should_refresh(self, key): return self.time_past(key) > self._ttl-self._refresh if key in self else False
    def time_past(self, key): return self._timer()-self._cache[key].timestamp
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
    async def load_item(self, key, _=namedtuple('CacheEntry', 'value timestamp loading', module='asyncutils.caches')):
        _ = _(await self.get_loader(key)(key), self._timer(), False)
        async with self._lock: self._cache[key] = _
    async def refresh_item(self, key):
        async with self._lock:
            if key not in self._loaders or (t := self._cache.get(key)) is None or t.loading: return
            t.loading = True
        try: await self.load_item(key)
        except CRITICAL: raise Critical
        except BaseException as e: t.loading = False; await self._process_error(e, False) # noqa: BLE001
    async def refresh_loop(self):
        r, t = self._refresh, []
        while True:
            try:
                await sleep(r)
                async with self._lock: n, d, f = self._timer(), self._ttl-self._refresh, self.refresh_item; t.extend(self.make_multiple(f(k) for k, v in self._cache.items() if not v.loading and n > d+v.timestamp))
                if t: await gather(*t, return_exceptions=True); t.clear()
            except CRITICAL: raise Critical
            except CancelledError: raise
            except BaseException as e: await self._process_error(e, True) # noqa: BLE001
    async def invalidate(self, key):
        async with self._lock: return self._cache.pop(key, None)
    async def clear(self):
        async with self._lock: self._cache.clear()
    P.patch_method_signatures((__init__, 'ttl=None, refresh=None, *, processor=None, default_loader=None, timer={}'), (configure, 'ttl, refresh, processor=None'), (load_item, 'key'))
class AsyncLRUCache:
    __slots__ = '_caches', '_factory', '_loopctx', '_make_key', '_timer', '_timestamps', '_ttl'
    def __init__(self, maxsize=None, ttl=None, *, typed=False, timer=monotonic):
        if maxsize is None: maxsize = getcontext().ASYNC_LRU_CACHE_DEFAULT_MAX_SIZE
        audit(fullname(self), maxsize, ttl)
        self._ttl, self._factory, self._timestamps, self._caches, self._loopctx, self._timer = ttl, lru_cache(maxsize, typed), {}, {}, event_loop.from_flags(0x200), timer
    def __call__(self, f, /, _=lambda f, a, k, s=0x3d, t=0x7a: id(f)<<t|hash(a)<<s|hash(frozenset(k.items()))):
        self._caches[f] = c = self._factory(f)
        if not hasattr(self, '_make_key'): self._make_key = to_async(_, self.loop)
        async def wrapper(*a, **k):
            K, t, T, S = await self._make_key(f, a, k), self._ttl, self._timer, self._timestamps
            if None is not t < T()-S.get(K, 0.0): c.cache_clear(); del S[K]
            if iscoroutine(r := c(*a, **k)): r = await r
            if t: S[K] = T()
            return r
        return wraps(f)(wraps(c, ('cache_info', 'cache_clear'), ())(wrapper))
    def cache_clear(self):
        self._timestamps.clear(); C = self._caches
        while C: C.popitem()[1].cache_clear()
    def __del__(self): self._loopctx.__exit__(None, None, None)
    @property
    def loop(self): return self._loopctx.__enter__()
    P.patch_method_signatures((__init__, 'maxsize=None, ttl=None, *, typed=False, timer={}'), (__call__, 'func, /'))
del defaultdict, namedtuple