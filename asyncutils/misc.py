__lazy_modules__ = frozenset(('asyncio',))
import asyncutils as A, asyncio as I, collections as c
from asyncutils.constants import _NO_DEFAULT
from asyncutils._internal import helpers as H, patch as P
from asyncutils._internal.submodules import misc_all as __all__
from sys import audit, exc_info, intern
from time import monotonic
class StateMachine:
    __slots__ = '_entries', '_exits', '_lock', '_state', '_transitions'
    def __init__(self, state): self._state, self._transitions, self._entries, self._exits, self._lock = intern(state), c.defaultdict(lambda: c.defaultdict(set)), {}, {}, I.Lock()
    def add(self, from_state, to_state, condition=None): self._transitions[intern(from_state)][intern(to_state)].add(condition)
    on_enter, on_exit = map(lambda attr: lambda self, state: lambda h, /: dict.__setitem__(getattr(self, attr), state, h) or h, __slots__[:2])
    async def transition(self, state):
        state, s = intern(state), self._state
        async with self._lock:
            if None not in (S := self._transitions[s][state]):
                for _ in S:
                    if await _(s, state): break
                else: return False
            await self._helper(1); self._state = state; await self._helper(0); return True
    async def _helper(self, i, /, _=A.IgnoreErrors(KeyError), s=__slots__):
        async with _: await getattr(self, s[i])[self._state]()
    P.patch_method_signatures((_helper, 'attr'))
async def gather_with_limited_concurrency(n=None, /, *coros, ret_exc=False):
    async def wrapped(c, s=I.Semaphore(A.getcontext().GATHER_WITH_LIMITED_CONCURRENCY_DEFAULT_MAX_CONCURRENT if n is None else n)): # noqa: B008
        async with s: return await c
    return await I.gather(*map(wrapped, coros), return_exceptions=ret_exc)
class CallbackAccumulator(c.deque, A.ExecutorRequiredAsyncContextMixin):
    __slots__ = 'call_once', 'default_getter', 't'
    def __init__(self, name, it=(), maxlen=None, default=_NO_DEFAULT, call_once=True, default_getter=None): super().__init__(A.aiter_to_gen(it, use_futures=True), maxlen); self.t, self.call_once, self.default_getter = tuple(H.filter_out(name, default, s=_NO_DEFAULT)), call_once, (lambda: (exc_info(), {}) if name == '__exit__' else ((), {})) if default_getter is None else default_getter
    def __call__(self, *a, **k):
        for f in self: f(*a, **k)
    def __enter__(self): return self
    def __exit__(self, /, *_): a, k = self.default_getter(); self(*a, **k)
    def add(self, o, /): self.append(getattr(o, *self.t))
    def offer_last(self, o, /):
        if (x := self.maxlen) is None or x > len(self): self.add(o); return True
        return False
    @property
    def callbacks(self): return self.copy()
    def __iter__(self):
        if self.call_once:
            p = self.popleft
            while self: yield p()
        else: yield from self.callbacks
class CacheWithBackgroundRefresh(A.LoopContextMixin):
    _executor = None; __slots__ = '_cache', '_event', '_loaders', '_lock', '_processor', '_refresh', '_task', '_timer', '_ttl'
    def __init__(self, ttl=None, refresh=None, *, processor=None, default_loader=None, timer=monotonic):
        C = A.getcontext()
        if ttl is None: ttl = C.BACKGROUND_REFRESH_CACHE_DEFAULT_TTL
        if refresh is None: refresh = C.BACKGROUND_REFRESH_CACHE_DEFAULT_REFRESH
        audit(H.fullname(self), ttl, refresh); super().__init__(); self._cache, self._lock, self._loaders, self._task, self._event, self._timer = {}, I.Lock(), c.defaultdict(lambda: default_loader), None, I.Event(), timer; self.configure(ttl, refresh, processor)
    def __contains__(self, key): return key in self._cache
    def register_loader(self, key, loader): self._loaders[key] = loader
    def expired(self, key): return self.time_past(key) > self._ttl
    def should_refresh(self, key): return self.time_past(key) > self._ttl-self._refresh if key in self else False
    def time_past(self, key): return self._timer()-self._cache[key].timestamp
    def configure(self, ttl, refresh, processor=None, _=lambda *_: None): self._ttl, self._refresh, self._processor = max(ttl, refresh), min(ttl, refresh), processor or getattr(self, '_processor', _)
    def get_loader(self, key):
        if (k := self._loaders[key]) is None: raise LookupError(f'asyncutils.misc.CacheWithBackgroundRefresh: no loader registered for key {key!r}')
        return k
    async def _process_error(self, e, b, /):
        if (x := (c := type(self))._executor) is None: x = H.create_executor(c)
        if I.iscoroutine(r := await self.loop.run_in_executor(x, self._processor, e, b)): await r
    async def get(self, key, loader=None):
        async with self._lock:
            if loader is not None: self.register_loader(key, loader)
            if self.should_refresh(key): await self.refresh_item(key)
            if key not in self._cache or self.expired(key): await self.load_item(key)
            return self._cache[key].value
    async def __setup__(self):
        if self._task is None: self._event.clear(); self._task = self.make(self.refresh_loop())
    async def __cleanup__(self):
        if self._task: self._event.set(); await A.safe_cancel(self._task); self._task = None
    async def load_item(self, key, _=c.namedtuple('CacheEntry', 'value timestamp loading', module='asyncutils.misc')):
        _ = _(await self.get_loader(key)(key), self._timer(), False)
        async with self._lock: self._cache[key] = _
    async def refresh_item(self, key):
        async with self._lock:
            if key not in self._loaders or (t := self._cache.get(key)) is None or t.loading: return
            t.loading = True
        try: await self.load_item(key)
        except A.CRITICAL: raise A.Critical
        except BaseException as e: t.loading = False; await self._process_error(e, False) # noqa: BLE001
    async def refresh_loop(self):
        r, t = self._refresh, []
        while True:
            await I.sleep(r)
            try:
                async with self._lock: d, f = self._timer()-self._ttl+self._refresh, self.refresh_item; t.extend(self.make_multiple(f(k) for k, v in self._cache.items() if not v.loading and d > v.timestamp))
                if t: await I.gather(*t); t.clear()
            except A.CRITICAL: raise A.Critical
            except I.CancelledError: raise
            except BaseException as e: await self._process_error(e, True) # noqa: BLE001
    async def invalidate(self, key):
        async with self._lock: return self._cache.pop(key, None)
    async def clear(self):
        async with self._lock: self._cache.clear()
    P.patch_method_signatures((__init__, 'ttl=None, refresh=None, *, processor=None, default_loader=None, timer={}'), (configure, 'ttl, refresh, processor=None'), (load_item, 'key'))