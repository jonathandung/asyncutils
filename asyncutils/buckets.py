from .mixins import AsyncContextMixin, EventualLoopMixin
from . import context
from time import monotonic
from asyncio.locks import Lock
from asyncio.tasks import sleep
from ._internal.submodules import buckets_all as __all__
class TokenBucket:
    __slots__ = '_capacity', '_tokens', '_rate', '_last_update', '_timer', '_lock'
    def __init__(self, rate, capacity, timer=monotonic): self._capacity = self._tokens = capacity; self._rate, self._lock, self._last_update, self._timer = rate, Lock(), timer(), timer
    async def consume(self, tokens=None):
        if tokens is None: tokens = float(context.TOKEN_BUCKET_DEFAULT_CONSUME_TOKENS)
        async with self._lock:
            e, self._last_update = (n := self._timer())-self._last_update, n; self._tokens = min(self._capacity, self._tokens+e*self._rate)
            if self._tokens >= tokens: self._tokens -= tokens; return
            await sleep((tokens-self._tokens)/self._rate); self._tokens = 0
    @property
    def capacity(self): return self._capacity
class LeakyBucket(AsyncContextMixin, EventualLoopMixin):
    def __init__(self, capacity, leak, min_factor=None, max_factor=None, external_factor_settable=None, timer=monotonic): C = context.getcontext(); self._leak, self._last, self._lock, self._drainer, self._factor, self._min_factor, self._max_factor, self._external_factor_settable, self._timer = leak, timer(), Lock(), None, 1.0, C.LEAKY_BUCKET_DEFAULT_MINFACTOR if min_factor is None else min_factor, C.LEAKY_BUCKET_DEFAULT_MAXFACTOR if max_factor is None else max_factor, C.LEAKY_BUCKET_DEFAULT_EXT_CAN_SET_FACTOR if external_factor_settable is None else external_factor_settable, timer; self._capacity = self._tokens = capacity
    def _adjust_from_params(self, a, b, c, d, /):
        if abs((n := min(self._factor*b, self._max_factor) if (r := self._tokens/self._capacity) <= a else max(self._factor*d, self._min_factor) if r >= c else min(self._factor*1.05, 1) if self._factor < 1 else self._factor)-self._factor) > 0.02: self._factor = n
    def _add_tokens(self, amount):
        if (s := self._tokens+amount) <= self._capacity: self._tokens = s; return True
        return False
    def _set_tokens(self): e, self._last = (c := self._timer())-self._last, c; self._tokens = max(0, self._tokens-e*self._leak*self._factor)
    async def _drain(self):
        while True:
            async with self._lock: self._set_tokens(); self._adjust()
            await sleep(min(1/self._leak/self._factor, 1))
    async def acquire(self, amount=1):
        async with self._lock: self._set_tokens(); return self._add_tokens(amount)
    async def wait_for_tokens(self, amount=1):
        w, m = 0.0, context.LEAKY_BUCKET_WAIT_FOR_TOKENS_TICK
        while True:
            async with self._lock:
                self._set_tokens(); self._adjust()
                if self._add_tokens(amount): return w
            await sleep(_ := min(m, (amount-self._capacity+self._tokens)/self._leak/self._factor)); w += _
    @property
    def factor(self): return self._factor
    @factor.setter
    def factor(self, value, /):
        if self._external_factor_settable: self._factor = max(self._min_factor, min(self._max_factor, value))
        else: raise ValueError('LeakyBucket.factor is read-only')
    @factor.deleter
    def factor(self): self._factor = 1
    def _adjust(self): self._adjust_from_params(*((0.15, 1.1, 0.85, 0.9) if (c := self._capacity) > 0x100 else (0.23, 1.2, 0.77, 0.81) if c > 0x80 else (0.3, 1.4, 0.7, 0.73)))
    def __enter__(self):
        if self._drainer is None: self._drainer = self.make(self._drain())
        return self
    def __exit__(self, /, *_):
        if self._drainer: self._drainer.cancel(); self._drainer = None