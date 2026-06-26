__lazy_modules__ = frozenset(('asyncio',))
from asyncutils import AsyncContextMixin, getcontext
from asyncutils._internal.helpers import LoopMixinBase, fullname
from asyncutils._internal.submodules import buckets_all as __all__
from asyncio import Lock, sleep
from sys import audit
from time import monotonic
class TokenBucket:
    __slots__ = '__cap', '__lock', '__lu', '__rate', '__timer', '__tokens'
    def __init__(self, rate, capacity, timer=monotonic): audit(fullname(self), rate, capacity); self.__cap = self.__tokens = capacity; self.__rate, self.__lock, self.__lu, self.__timer = rate, Lock(), timer(), timer
    async def consume(self, tokens=None):
        if tokens is None: tokens = float(getcontext().TOKEN_BUCKET_DEFAULT_CONSUME_TOKENS)
        async with self.__lock:
            e, self.__lu = (n := self.__timer())-self.__lu, n; self.__tokens = d = min(self.__cap, self.__tokens+e*self.__rate)
            if (d := d-tokens) >= 0: self.__tokens = d
            else: await sleep(-d/self.__rate); self.__tokens = 0
    @property
    def capacity(self): return self.__cap
class LeakyBucket(AsyncContextMixin, LoopMixinBase):
    __slots__ = '__cap', '__dr', '__efs', '__factor', '__hf', '__last', '__leak', '__lf', '__timer', '_tokens'
    def __init__(self, capacity, leak, min_factor=None, max_factor=None, external_factor_settable=None, timer=monotonic): audit(fullname(self), capacity, leak); C = getcontext(); self.__leak, self.__last, self.__dr, self.__factor, self.__lf, self.__hf, self.__efs, self.__timer = leak, timer(), None, 1.0, C.LEAKY_BUCKET_DEFAULT_MIN_FACTOR if min_factor is None else min_factor, C.LEAKY_BUCKET_DEFAULT_MAX_FACTOR if max_factor is None else max_factor, C.LEAKY_BUCKET_DEFAULT_EXT_CAN_SET_FACTOR if external_factor_settable is None else external_factor_settable, timer; self.__cap = self.__tokens = capacity
    def _adjust_from_params(self, a, b, c, d, /):
        if (f := self.__factor) < abs((n := min(f*b, self.__hf) if (r := self.__tokens/self.__cap) <= a else max(f*d, self.__lf) if r >= c else min(f*1.05, 1) if f < 1 else f)-f)*100: self.__factor = n
    def _add_tokens(self, amount):
        if (s := self.__tokens+amount) <= self.__cap: self.__tokens = s; return True
        return False
    def _set_tokens(self): e, self.__last = (c := self.__timer())-self.__last, c; self.__tokens = max(0, self.__tokens-e*self.__leak*self.__factor)
    async def _drain(self):
        while True: self._set_tokens(); self._adjust(); await sleep(min(1/(self.__leak*self.__factor), 1))
    async def acquire(self, amount=None): self._set_tokens(); return self._add_tokens(getcontext().LEAKY_BUCKET_DEFAULT_ACQUIRE_TOKENS if amount is None else amount)
    async def wait_for_tokens(self, amount=None):
        c = getcontext()
        if amount is None: amount = c.LEAKY_BUCKET_DEFAULT_WAIT_FOR_TOKENS_TOKENS
        w, m = 0.0, c.LEAKY_BUCKET_WAIT_FOR_TOKENS_TICK
        while True:
            self._set_tokens(); self._adjust()
            if self._add_tokens(amount): return w
            await sleep(_ := min(m, (amount-self.__cap+self.__tokens)/(self.__leak*self.__factor))); w += _
    @property
    def capacity(self): return self.__cap
    @property
    def factor(self): return self.__factor
    @factor.setter
    def factor(self, value, /):
        if self.__efs: self.__factor = max(self.__lf, min(self.__hf, value))
        else: raise ValueError(f'{fullname(self)}: external_factor_settable=True not passed; cannot set factor')
    @factor.deleter
    def factor(self): self.__factor = 1
    def _adjust(self):
        c = self.__cap
        for b, t in getcontext().LEAKY_BUCKET_ADJMAP:
            if c >= b: return self._adjust_from_params(*t)
    def __enter__(self):
        if self.__dr is None: self.__dr = self.make(self._drain())
        return self
    def __exit__(self, /, *a):
        if d := self.__dr: self.__dr = None; d.cancel(a[1])
