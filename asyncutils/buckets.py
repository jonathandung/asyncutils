__lazy_modules__ = frozenset(('asyncio',))
from asyncutils import AsyncContextMixin, LoopBoundMixin, getcontext
from asyncutils._internal.helpers import fullname
from asyncutils._internal.submodules import buckets_all as __all__
from asyncio import Lock, sleep
from sys import audit
from time import monotonic
class TokenBucket:
    __slots__ = '_capacity', '_last_update', '_lock', '_rate', '_timer', '_tokens'
    def __init__(self, rate, capacity, timer=monotonic): audit(fullname(self), rate, capacity); self._capacity = self._tokens = capacity; self._rate, self._lock, self._last_update, self._timer = rate, Lock(), timer(), timer
    async def consume(self, tokens=None):
        if tokens is None: tokens = float(getcontext().TOKEN_BUCKET_DEFAULT_CONSUME_TOKENS)
        async with self._lock:
            e, self._last_update = (n := self._timer())-self._last_update, n; self._tokens = d = min(self._capacity, self._tokens+e*self._rate)
            if (d := d-tokens) >= 0: self._tokens = d
            else: await sleep(-d/self._rate); self._tokens = 0
    @property
    def capacity(self): return self._capacity
class LeakyBucket(AsyncContextMixin, LoopBoundMixin):
    __slots__ = '_capacity', '_drainer', '_external_factor_settable', '_factor', '_last', '_leak', '_lock', '_max_factor', '_min_factor', '_timer', '_tokens'
    def __init__(self, capacity, leak, min_factor=None, max_factor=None, external_factor_settable=None, timer=monotonic): audit(fullname(self), capacity, leak); C = getcontext(); self._leak, self._last, self._lock, self._drainer, self._factor, self._min_factor, self._max_factor, self._external_factor_settable, self._timer = leak, timer(), Lock(), None, 1.0, C.LEAKY_BUCKET_DEFAULT_MIN_FACTOR if min_factor is None else min_factor, C.LEAKY_BUCKET_DEFAULT_MAX_FACTOR if max_factor is None else max_factor, C.LEAKY_BUCKET_DEFAULT_EXT_CAN_SET_FACTOR if external_factor_settable is None else external_factor_settable, timer; self._capacity = self._tokens = capacity
    def _adjust_from_params(self, a, b, c, d, /):
        if (f := self._factor) < abs((n := min(f*b, self._max_factor) if (r := self._tokens/self._capacity) <= a else max(f*d, self._min_factor) if r >= c else min(f*1.05, 1) if f < 1 else f)-f)*100: self._factor = n
    def _add_tokens(self, amount):
        if (s := self._tokens+amount) <= self._capacity: self._tokens = s; return True
        return False
    def _set_tokens(self): e, self._last = (c := self._timer())-self._last, c; self._tokens = max(0, self._tokens-e*self._leak*self._factor)
    async def _drain(self):
        while True:
            async with self._lock: self._set_tokens(); self._adjust()
            await sleep(min(1/(self._leak*self._factor), 1))
    async def acquire(self, amount=None):
        async with self._lock: self._set_tokens(); return self._add_tokens(getcontext().LEAKY_BUCKET_DEFAULT_ACQUIRE_TOKENS if amount is None else amount)
    async def wait_for_tokens(self, amount=None):
        c = getcontext()
        if amount is None: amount = c.LEAKY_BUCKET_DEFAULT_WAIT_FOR_TOKENS_TOKENS
        w, m = 0.0, c.LEAKY_BUCKET_WAIT_FOR_TOKENS_TICK
        while True:
            async with self._lock:
                self._set_tokens(); self._adjust()
                if self._add_tokens(amount): return w
            await sleep(_ := min(m, (amount-self._capacity+self._tokens)/(self._leak*self._factor))); w += _
    @property
    def factor(self): return self._factor
    @factor.setter
    def factor(self, value, /):
        if self._external_factor_settable: self._factor = max(self._min_factor, min(self._max_factor, value))
        else: raise ValueError(f'{fullname(self)}.factor is read-only')
    @factor.deleter
    def factor(self): self._factor = 1
    def _adjust(self):
        c = self._capacity
        for b, t in getcontext().LEAKY_BUCKET_ADJMAP:
            if c >= b: return self._adjust_from_params(*t)
    def __enter__(self):
        if self._drainer is None: self._drainer = self.make(self._drain())
        return self
    def __exit__(self, /, *_):
        if d := self._drainer: d.cancel(); self._drainer = None