# type: ignore
__lazy_modules__ = frozenset(('_heapq', 'asyncio'))
from asyncutils import Critical, LoopBoundMixin, LockForceRequest, LockMixin, LockWithOwnerMixin, getcontext, safe_cancel_batch, CRITICAL
from asyncutils.constants import _NO_DEFAULT
from asyncutils._internal import log
from asyncutils._internal.helpers import check_methods, fullname, subscriptable
from asyncutils._internal.submodules import locks_all as __all__
from _collections import defaultdict, deque
from _heapq import heappop, heappush
from asyncio import Lock, current_task, gather, iscoroutine, wait, wait_for
from time import monotonic
class AdvancedRateLimit(LoopBoundMixin, LockMixin):
    __slots__ = '_lock', '_lu', '_unfair', '_waiters', 'capacity', 'rate', 'tokens'
    def __init__(self, rate, capacity=None, fair=True): super().__init__(); self.rate, self._lock, self._waiters, self._unfair, self._lu = rate, Lock(), deque(), not fair, monotonic(); self.tokens = self.capacity = capacity or rate
    async def acquire(self, tokens=None, timeout=None):
        async with self._lock:
            self.update_tokens_lock_held()
            if tokens > self.tokens: w = self._waiters; (w.appendleft if self._unfair else w.append)((getcontext().ADVANCED_RATE_LIMIT_DEFAULT_TOKENS if tokens is None else tokens, F := self.loop.create_future()))
            else: self.tokens -= tokens; return True
        try: await wait_for(F, timeout); return True
        except TimeoutError: return False
    async def release(self, tokens=None):
        async with self._lock: self.update_tokens_lock_held(); self.tokens = min(self.tokens+(getcontext().ADVANCED_RATE_LIMIT_DEFAULT_TOKENS if tokens is None else tokens), self.capacity)
    async def set_rate(self, new):
        async with self._lock: self.update_tokens_lock_held(); self.rate, self.capacity = new, max(self.capacity, new)
    def locked(self): return bool(self._waiters)
    def update_tokens_lock_held(self):
        e, p, self._lu = (n := monotonic())-self._lu, (w := self._waiters).popleft, n; T = min(self.capacity, self.tokens+e*self.rate)
        while w and (t := p())[0] <= T:
            t, f = t; T -= t
            if not f.done(): f.set_result(None)
        self.tokens = T; w.appendleft(t)
class PrioritySemaphore(LoopBoundMixin, LockMixin):
    __slots__ = '_tiebreak', '_value', '_waiters'
    def __init__(self, value=None): self._value, self._tiebreak, self._waiters = getcontext().PRIORITY_SEMAPHORE_DEFAULT_VALUE if value is None else value, 0, []
    async def acquire(self, priority=0):
        self._value -= 1; self._tiebreak += 1; w = self._waiters
        while self._value < 0: heappush(w, (priority, self._tiebreak, F := self.make_fut())); await F
        return True
    def release(self, strict=False):
        if w := self._waiters: heappop(w)[-1].set_result(None)
        elif strict: raise RuntimeError('release called too many times')
        self._value += 1
    def locked(self): return self._value < 0
    def reset(self):
        for *_, e in self._waiters: e.set_result(None)
        self._value, self._tiebreak = 1, 0; self._waiters.clear()
@subscriptable
class KeyedCondition(LoopBoundMixin, LockMixin):
    __slots__ = '__lock', '_specific_waiters'
    def __init__(self, lock=None): super().__init__(); self.__lock, self._specific_waiters = lock or Lock(), defaultdict(set)
    async def acquire(self): await self.__lock.acquire(); return True
    async def release(self):
        if iscoroutine(r := self.__lock.release()): await r
    def locked(self): return self.__lock.locked()
    async def wait(self, key, timeout=None):
        self.assert_locked(); (s := self._specific_waiters[key]).add(F := self.make_fut())
        try: await wait_for(F, timeout)
        finally: s.discard(F)
    async def wait_for(self, key, pred, per_wait_timeout=None):
        self.assert_locked(); f, g, h, F = (s := self._specific_waiters[key]).add, s.discard, self.make_fut, None
        try:
            while not pred(): f(F := h()); await wait_for(F, per_wait_timeout); g(F)
        finally: g(F)
    async def wait_all(self, timeout=None): self.assert_locked(); await wait_for(gather(*frozenset().union(*self._specific_waiters.values()), return_exceptions=True), timeout)
    def assert_locked(self):
        if not self.locked(): raise RuntimeError('must acquire condition to notify')
    def notify(self, key, n=1, strict=False):
        if n <= 0:
            if strict: raise ValueError(f'{fullname(self)}: n must be positive')
            return
        self.assert_locked()
        if (s := (S := self._specific_waiters).pop(key, None)) is None:
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
        for k in self._specific_waiters if key is None else (key,):
            if (s := self._specific_waiters.pop(k, None)) is None: break
            p = s.pop
            while s:
                if not (F := p()).done(): F.set_result(None)
            l += len(s); s.clear()
        return l
@subscriptable
class MultiCountDownLatch:
    __slots__ = '_cond', '_counts'
    def __init__(self, counts): self._cond, self._counts = KeyedCondition(), {k: v for k, v in counts.items() if v > 0}
    def _count_down_lock_held(self, key, strict):
        if (c := (d := self._counts).get(key)) is None:
            if strict: raise KeyError(f'{fullname(self)}: cannot count down key {key!r} further')
            return
        if c > 1: d[key] = c-1
        else: del d[key]
        if c == 1: self._cond.notify_all(key)
    async def count_down(self, key, strict=False):
        async with self._cond: self._count_down_lock_held(key, strict)
    async def count_down_all(self, strict=False):
        f = self._count_down_lock_held
        async with self._cond:
            for key in self._counts: f(key, strict)
    async def wait(self, key, strict=False):
        if key in self._counts:
            async with (C := self._cond): await C.wait(key)
        elif strict: raise KeyError(f'{fullname(self)}: no count for key {key!r}')
    async def wait_all(self, timeout=None):
        async with (C := self._cond): await C.wait_all(timeout)
    @property
    def broken(self): return not self._counts
class RLock(LockWithOwnerMixin):
    __slots__ = '__lock', '_count', '_owner'
    def __init__(self, lock=None): self._count, self._owner, self.__lock = 0, None, lock or Lock()
    async def acquire(self):
        async with self.__lock:
            if self.is_owner: self._count += 1; return True
        while True:
            async with self.__lock:
                if self._owner is None: self._owner, self._count = current_task(), 1; return True
    def _release(self):
        if (c := self._count) <= 0: raise RuntimeError(f'release called too many times on {fullname(self)}')
        if c == 1: self._owner = None
        self._count = c-1
    def locked(self): return self._owner is not None
    @property
    def is_owner(self): return self._owner is current_task()
class PriorityLock(LoopBoundMixin, LockWithOwnerMixin):
    __slots__ = '_owner', '_tiebreak', '_waiters'
    def __init__(self): super().__init__(); self._waiters, self._tiebreak, self._owner = [], 0, None
    async def acquire(self, priority=0, timeout=None):
        heappush(self._waiters, (priority, self._tiebreak, F := self.make_fut())); self._tiebreak += 1
        try:
            if len(self._waiters) == 1 and self._owner is None: F.set_result(True)
            await wait_for(F, timeout); self._owner = current_task(); return True
        except TimeoutError: return False
        finally:
            if not F.done(): F.cancel()
    def _release(self, raise_=True):
        self._owner, w = None, self._waiters
        while w:
            if not (F := heappop(w)[-1]).done(): return F.set_result(True)
        if raise_: raise RuntimeError(f'release called too many times on {fullname(self)}')
    def locked(self): return self._owner is not None
    @property
    def is_owner(self): return self._owner is current_task()
class PriorityRLock(RLock):
    __slots__ = ()
    def __init__(self): super().__init__(PriorityLock())
    @property
    def owner(self): o = self.__lock._owner = self._owner; return o
    @owner.setter
    def owner(self, val, /): self._owner = self.__lock._owner = val
    async def acquire(self, priority=0, timeout=None):
        if self.is_owner: self._count += 1; return True
        if await self.__lock.acquire(priority, timeout): self._count = 1; return True
        return False
class LocksmithBase:
    __slots__ = '_lock', '_loop', '_recognized'; handlers = {} # noqa: RUF012
    @classmethod
    def register_handler(cls, h, /, *, shadow=True):
        def register(t, H=cls.handlers, h=h):
            if not isinstance(t, type): raise TypeError('non-type cannot be registered')
            if shadow: H[t] = h
            elif h is not (h := H.setdefault(t, h)): raise KeyError('handler for type already registered', t, h)
            return t
        return register
    @property
    def currently_recognized(self): return frozenset(self._recognized)
    def __init__(self, loop, ltyp=Lock): self._recognized, self._loop, self._lock = __import__('_weakrefset').WeakSet(), loop, ltyp()
    async def recognize_lock(self, lock, /):
        if not self.preliminary_check_lock(lock): return False
        async with self._lock:
            if lock in (r := self._recognized): return False
            if callable(f := getattr(lock, 'acknowledge_locksmith_lock_held', None)):
                try: return bool((await f) if iscoroutine(f := f(self)) else f)
                except: return False # noqa: E722
            r.add(lock); return True
    async def force(self, lock, /, info=None, *, purge_waiters=True):
        async with self._lock:
            if not self.can_force_lock_held(lock): return False
        if info is None: info = await self.get_info(lock)
        try:
            if iscoroutine(r := lock.release()): r = await r
        except CRITICAL: raise Critical
        except: # noqa: E722
            if self.find_owner(lock) is (o := current_task()):
                if o is None: return self.throw_fallback(lock)
                if (c := o.get_coro()) is None: return self.eager_fallback(lock)
                F = self._loop.create_future()
                try: c.throw(LockForceRequest(self, F.set_result, lock, info))
                except CRITICAL as e: self.task_raised_critical(lock, e)
                except LockForceRequest as e:
                    if (r := e.requester) is self: await self.task_reraised_request(lock)
                    else: await gather(self.lock_busy(lock, r), r.lock_busy(lock, self))
                except BaseException as e: self.raised_other(lock, e) # noqa: BLE001
                else: self.answer_received(lock, await F)
            if callable(f := self.handlers.get(type(lock))) and iscoroutine(r := f(lock)): await r
            return True
        else: return self.release_returned_false(lock) if r is False else True
        finally:
            if purge_waiters: await self.purge_waiters(lock)
    async def purge_waiters(self, lock, /):
        if w := getattr(lock, '_waiters', None): await safe_cancel_batch(w, disembowel=True)
    async def host(self, task, lock, /, *, timeout1=_NO_DEFAULT, timeout2=_NO_DEFAULT, timeout3=_NO_DEFAULT):
        await wait(f := tuple(map(self.wrap_task, (self.force(lock, purge_waiters=False), lock.acquire()))), return_when='FIRST_COMPLETED'); f, a = f
        if await wait_for(f, getcontext().LOCKSMITH_DEFAULT_TIMEOUTS[0] if timeout1 is _NO_DEFAULT else timeout1): await a
        else:
            try: await wait_for(a, getcontext().LOCKSMITH_DEFAULT_TIMEOUTS[1] if timeout2 is _NO_DEFAULT else timeout2)
            except TimeoutError: raise TimeoutError(f'failed to acquire lock {lock!r} within {timeout2} seconds') from None
        self.patch_owner(task := self.wrap_task(task), lock); return await wait_for(self._wait_on(task, lock), getcontext().LOCKSMITH_DEFAULT_TIMEOUTS[2] if timeout3 is _NO_DEFAULT else timeout3)
    async def _wait_on(self, task, lock, /):
        try: return await task
        finally:
            if lock.locked() and iscoroutine(a := lock.release()): await a
    async def lock_busy(self, lock, requester, /): log.info('lock busy: %r; requester: %r', lock, requester)
    async def task_reraised_request(self, lock, /): log.warning('%s.force: running task did not handle request to release %s at %#x properly', fullname(self), fullname(lock), id(lock))
    def wrap_task(self, a, /):
        async def f(): return await a
        return self._loop.create_task(f())
    def patch_owner(self, task, lock, /):
        if hasattr(lock, '_owner'): lock._owner = task
    def find_owner(self, lock, /): return getattr(lock, '_owner', None)
    def throw_fallback(self, lock, /): return True
    def eager_fallback(self, lock, /): return True
    def release_returned_false(self, lock, /): return False
    def answer_received(self, lock, answer, /): log.info('%r received answer %r from %r', self, answer, lock)
    def raised_other(self, lock, exc, /):
        if not isinstance(exc, RuntimeError): log.error('error encountered in attempt to force %s at %#x', fullname(lock), id(lock), exc_info=exc)
    async def get_info(self, lock, /): return 'potential deadlock situation'
    def preliminary_check_lock(self, lock, /): return check_methods(lock, 'acquire', 'release', 'locked')
    def task_raised_critical(self, lock, exc, /): raise exc from None
    def can_force_lock_held(self, lock, /): return lock is self._lock or not (lock in self._recognized and lock.locked())