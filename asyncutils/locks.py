__lazy_modules__ = frozenset(('heapq',))
import asyncutils as A, asyncio as I
from asyncutils._internal.helpers import LoopMixinBase, fullname, subscriptable
from asyncutils._internal.submodules import locks_all as __all__
from _collections import defaultdict, deque
from heapq import heappop, heappush
from time import monotonic
class DynamicBoundedSemaphore(I.BoundedSemaphore):
    def __init__(self, value=None): super().__init__(A.getcontext().DYNAMIC_BOUNDED_SEMAPHORE_DEFAULT_VALUE if value is None else value); self._waiters = deque()
    @property
    def bound(self): return self._bound_value
    @bound.setter
    def bound(self, value, /):
        if value < 0: raise ValueError('asyncutils.locks.DynamicBoundedSemaphore: bound must be non-negative')
        d, self._bound_value, f = value-self._bound_value, value, (W := self._waiters).popleft # ty: ignore[unresolved-attribute]
        while d and W:
            if not (w := f()).done(): w.set_result(None); d -= 1
def d(m, /, _=__import__('functools').wraps):
    async def w(self, *a, **k):
        async with self._lock: self.update_tokens_lock_held(); m(self, *a, **k)
    return _(m)(w)
class AdvancedRateLimit(LoopMixinBase, A.LockMixin):
    __slots__ = '__fair', '__lock', '__lu', '__waiters', 'capacity', 'rate', 'tokens'
    def __init__(self, rate, capacity=None, fair=True): super().__init__(); self.rate, self.__lock, self.__waiters, self.__fair, self.__lu = rate, I.Lock(), deque(), fair, monotonic(); self.tokens = self.capacity = capacity or rate
    async def acquire(self, tokens=None, timeout=None):
        async with self.__lock:
            self.update_tokens_lock_held()
            if tokens > self.tokens: w = self.__waiters; (w.append if self.__fair else w.appendleft)((A.getcontext().ADVANCED_RATE_LIMIT_DEFAULT_TOKENS if tokens is None else tokens, F := self.loop.create_future()))
            else: self.tokens -= tokens; return True
        try: await I.wait_for(F, timeout); return True
        except TimeoutError: return False
    @d
    def release(self, tokens=None): self.tokens = min(self.tokens+(A.getcontext().ADVANCED_RATE_LIMIT_DEFAULT_TOKENS if tokens is None else tokens), self.capacity)
    @d
    def set_rate(self, new): self.rate, self.capacity = new, max(self.capacity, new)
    def locked(self): return bool(self.__waiters)
    def update_tokens_lock_held(self):
        if not (w := self.__waiters): return
        e, p, self.__lu = (n := monotonic())-self.__lu, w.popleft, n; T = min(self.capacity, self.tokens+e*self.rate)
        while (t := p())[0] <= T and w:
            t, f = t; T -= t
            if not f.done(): f.set_result(None)
        self.tokens = T; w.appendleft(t)
class PrioritySemaphore(LoopMixinBase, A.LockMixin):
    __slots__ = '__tiebreak', '__value', '__waiters'
    def __init__(self, value=None): self.__value, self.__tiebreak, self.__waiters = A.getcontext().PRIORITY_SEMAPHORE_DEFAULT_VALUE if value is None else value, 0, []
    async def acquire(self, priority=0):
        self.__value -= 1; self.__tiebreak += 1; w = self.__waiters
        while self.__value < 0: heappush(w, (priority, self.__tiebreak, F := self.make_fut())); await F
        return True
    def release(self, strict=True):
        if w := self.__waiters: heappop(w)[-1].set_result(None)
        elif strict: raise RuntimeError('asyncutils.locks.PrioritySemaphore: release called too many times')
        self.__value += 1
    def locked(self): return self.__value < 0
    def reset(self):
        for *_, e in self.__waiters: e.set_result(None)
        self.__value, self.__tiebreak = 1, 0; self.__waiters.clear()
class KeyedCondition(LoopMixinBase, A.LockMixin):
    __slots__ = '__lock', '__sw'
    def __init__(self, lock=None): super().__init__(); self.__lock, self.__sw = lock or I.Lock(), defaultdict(set)
    async def acquire(self):
        with A.ignore_noncritical:
            if await self.__lock.acquire() != False: return True # noqa: E712
        return False
    async def release(self):
        if I.iscoroutine(r := self.__lock.release()): await r
    def locked(self): return self.__lock.locked()
    async def wait(self, key, timeout=None):
        self.assert_locked(); (s := self.__sw[key]).add(F := self.make_fut())
        try: await I.wait_for(F, timeout)
        finally: s.discard(F)
    async def wait_for(self, key, pred, per_wait_timeout=None):
        self.assert_locked(); f, g, h, F = (s := self.__sw[key]).add, s.discard, self.make_fut, None
        try:
            while not pred(): f(F := h()); await I.wait_for(F, per_wait_timeout); g(F)
        finally: g(F)
    async def wait_all(self, timeout=None): self.assert_locked(); await I.wait_for(I.gather(*frozenset().union(*self.__sw.values()), return_exceptions=True), timeout)
    def assert_locked(self):
        if not self.locked(): raise RuntimeError('asyncutils.locks.KeyedCondition: must acquire condition to notify')
    def notify(self, key, n=1, strict=False):
        if n <= 0:
            if strict: raise ValueError(f'{fullname(self)}: n must be positive')
            return
        self.assert_locked()
        if (s := (S := self.__sw).pop(key, None)) is None:
            if strict: raise ValueError(f'{fullname(self)}: no parties waiting for key {key!r}')
            return
        p = s.pop
        while s:
            if not (F := p()).done(): F.set_result(None); n -= 1
            if n == 0: break
        if s: S[key] = s
        if strict and n > 0: raise ValueError(f'{fullname(self)}: not enough parties to notify')
    def notify_all(self, key=None):
        self.assert_locked()
        l = 0
        for k in self.__sw if key is None else (key,):
            if (s := self.__sw.pop(k, None)) is None: break
            p = s.pop
            while s:
                if not (F := p()).done(): F.set_result(None)
            l += len(s); s.clear()
        return l
@subscriptable
class MultiCountDownLatch:
    __slots__ = '__cd', '__cts'
    def __init__(self, counts): self.__cd, self.__cts = KeyedCondition(), {k: v for k, v in counts.items() if v > 0}
    def _count_down_lock_held(self, key, strict):
        if (c := (d := self.__cts).get(key)) is None:
            if strict: raise KeyError(f'{fullname(self)}: cannot count down key {key!r} further')
            return
        if c > 1: d[key] = c-1
        else: del d[key]
        if c == 1: self.__cd.notify_all(key)
    async def count_down(self, key, strict=False):
        async with self.__cd: self._count_down_lock_held(key, strict)
    async def count_down_all(self):
        f = self._count_down_lock_held
        async with self.__cd:
            for key in self.__cts: f(key, True)
    async def wait(self, key, strict=False):
        if key in self.__cts:
            async with (C := self.__cd): await C.wait(key)
        elif strict: raise KeyError(f'{fullname(self)}: no count for key {key!r}')
    async def wait_all(self, timeout=None):
        async with (C := self.__cd): await C.wait_all(timeout)
    @property
    def broken(self): return not self.__cts
class RLock(A.LockWithOwnerMixin):
    __slots__ = '__cnt', '__lock', '__owner'
    def __init__(self, lock=None): self.__cnt, self.__owner, self.__lock = 0, None, lock or I.Lock()
    async def acquire(self):
        async with self.__lock:
            if self.is_owner: self.__cnt += 1; return True
        while True:
            async with self.__lock:
                if self.__owner is None: self.__owner, self.__cnt = I.current_task(), 1; return True
    def _release(self):
        if (c := self.__cnt) <= 0: raise RuntimeError(f'{fullname(self)}: release called too many times')
        if c == 1: self.__owner = None
        self.__cnt = c-1
    def locked(self): return self.__owner is not None
    @property
    def is_owner(self): return self.__owner is I.current_task()
class PriorityLock(LoopMixinBase, A.LockWithOwnerMixin):
    __slots__ = '__owner', '__tiebreak', '__waiters'
    def __init__(self): super().__init__(); self.__waiters, self.__tiebreak, self.__owner = [], 0, None
    async def acquire(self, priority=0, timeout=None):
        heappush(self.__waiters, (priority, self.__tiebreak, F := self.make_fut())); self.__tiebreak += 1
        try:
            if len(self.__waiters) == 1 and self.__owner is None: F.set_result(True)
            await I.wait_for(F, timeout); self.__owner = I.current_task(); return True
        except TimeoutError: return False
        finally:
            if not F.done(): F.cancel()
    def _release(self, raise_=True):
        self.__owner, w = None, self.__waiters
        while w:
            if not (F := heappop(w)[-1]).done(): return F.set_result(True)
        if raise_: raise RuntimeError(f'{fullname(self)}: release called too many times')
    def locked(self): return self.__owner is not None
    @property
    def is_owner(self): return self.__owner is I.current_task()
class PriorityRLock(RLock):
    __slots__ = ()
    def __init__(self): super().__init__(PriorityLock())
    @property
    def owner(self): o = self.__lock._owner = self._owner; return o # ty: ignore[invalid-assignment]
    @owner.setter
    def owner(self, val, /): self._owner = self.__lock._owner = val # ty: ignore[invalid-assignment]
    async def acquire(self, priority=0, timeout=None):
        if self.is_owner: self._count += 1; return True
        if await self.__lock.acquire(priority, timeout): self._count = 1; return True # ty: ignore[too-many-positional-arguments]
        return False
del d
