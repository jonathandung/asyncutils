from . import mixins as M
from .base import safe_cancel_batch
from .exceptions import Critical, LockForceRequest, CRITICAL
from ._internal import log
from ._internal.helpers import check_methods
from asyncio.coroutines import iscoroutine
from asyncio.locks import Event, Lock
from asyncio.tasks import wait_for, current_task, wait, gather
from _collections import deque, defaultdict # type: ignore[import-not-found]
from heapq import heappush, heappop
from time import monotonic
from ._internal.submodules import locks_all as __all__
class AdvancedRateLimit(M.EventualLoopMixin, M.LockMixin):
    __slots__ = '_last_update', '_lock', '_unfair', '_waiters', 'capacity', 'rate', 'tokens'
    def __init__(self, rate, capacity=None, fair=True): super().__init__(); self.rate, self._lock, self._waiters, self._unfair, self._last_update = rate, Lock(), deque(), not fair, monotonic(); self.tokens = self.capacity = capacity or rate
    async def acquire(self, tokens=1, timeout=None):
        async with self._lock:
            self.update_tokens()
            if tokens > self.tokens: w = self._waiters; (w.appendleft if self._unfair else w.append)((tokens, F := self.loop.create_future()))
            else: self.tokens -= tokens; return True
        try: await wait_for(F, timeout); return True
        except TimeoutError: return False
    async def release(self, tokens=1):
        async with self._lock: self.update_tokens(); self.tokens = min(self.tokens+tokens, self.capacity)
    async def set_rate(self, new):
        async with self._lock: self.update_tokens(); self.rate, self.capacity = new, max(self.capacity, new)
    def locked(self): return bool(self._waiters)
    def update_tokens(self):
        e, self._last_update = (n := monotonic())-self._last_update, n; self.tokens = min(self.capacity, self.tokens+e*self.rate)
        while self._waiters and self.tokens >= self._waiters[0][0]:
            t, f = self._waiters.popleft(); self.tokens -= t
            if not f.done(): f.set_result(None)
class PrioritySemaphore(M.LockMixin):
    __slots__ = '_tiebreak', '_value', '_waiters'
    def __init__(self, value=1): self._value, self._tiebreak, self._waiters = value, 0, []
    async def acquire(self, priority=0):
        self._value -= 1; self._tiebreak += 1; w = self._waiters
        while self._value < 0: heappush(w, (priority, self._tiebreak, e := Event())); await e.wait()
        return True
    def release(self, strict=False):
        if w := self._waiters: heappop(w)[-1].set()
        elif strict: raise RuntimeError('release called too many times')
        self._value += 1
    def locked(self): return self._value < 0
    def reset(self):
        for *_, e in self._waiters: e.set()
        self._value, self._tiebreak = 1, 0; self._waiters.clear()
class KeyedCondition(M.LockMixin, M.LoopContextMixin, M.AwaitableMixin):
    __slots__ = '__lock', '_specific_waiters', '_waiters'
    def __init__(self, lock=None): self.__lock, self._waiters, self._specific_waiters = lock or Lock(), set(), defaultdict(set)
    async def acquire(self): await self.__lock.acquire(); return True
    async def release(self):
        if iscoroutine(r := self.__lock.release()): await r
    def locked(self): return self.__lock.locked()
    async def wait(self, key=None, timeout=None):
        async with self.__lock: (s := self._waiters if key is None else self._specific_waiters[key]).add(F := self.loop.create_future())
        try: await wait_for(F, timeout)
        finally:
            async with self.__lock: s.discard(F)
    async def notify(self, n=1, key=None, strict=False):
        i = 0
        async with self.__lock:
            for i, F in enumerate((s := self._waiters if (c := key is None) else self._specific_waiters[key]).copy()):
                if i >= n: break
                if not F.done(): F.set_result(None)
                s.discard(F)
                if not (c or s): del self._specific_waiters[key]
            else:
                if strict and i+1 < n: raise ValueError(f'{type(self).__qualname__}: not enough parties to notify')
    async def notify_all(self, key=None):
        async with self.__lock:
            for F in (s := self._waiters if key is None else self._specific_waiters.pop(key)):
                if not F.done(): F.set_result(None)
            l = len(s); s.clear(); return l
class RLock(M.LockWithOwnerMixin):
    __slots__ = '__lock', '_count', '_owner'
    def __init__(self, lock=None): self._count, self._owner, self.__lock = 0, None, lock or Lock()
    async def acquire(self):
        async with self.__lock:
            if self.is_owner: self._count += 1; return True
        while True:
            async with self.__lock:
                if self._owner is None: self._owner, self._count = current_task(), 1; return True
    def _release(self):
        if (c := self._count) <= 0: raise RuntimeError(f'release called too many times on {type(self).__qualname__}')
        if c == 1: self._owner = None
        self._count = c-1
    def locked(self): return self._owner is not None
    @property
    def is_owner(self): return self._owner is current_task()
class PriorityLock(M.EventualLoopMixin, M.LockWithOwnerMixin):
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
        if raise_: raise RuntimeError('release called too many times on PriorityLock')
    def locked(self): return self._owner is not None
    @property
    def is_owner(self): return self._owner is current_task()
class PriorityRLock(RLock):
    __slots__ = ()
    def __init__(self): super().__init__(PriorityLock())
    def __del__(self): self.__lock.exiter() # type: ignore
    @property
    def owner(self): o = self.__lock._owner = self._owner; return o # type: ignore
    @owner.setter
    def owner(self, val, /): self._owner = self.__lock._owner = val # type: ignore
    async def acquire(self, priority=0, timeout=None):
        if self.is_owner: self._count += 1; return True
        if await self.__lock.acquire(priority, timeout): self._count = 1; return True # type: ignore
        return False
class LocksmithBase: # noqa: PLR0904
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
                except: return False
            r.add(lock); return True
    async def force(self, lock, /, info=None, *, purge_waiters=True): # noqa: PLR0912
        async with self._lock:
            if not self.can_force_lock_held(lock): return False
        if info is None: info = await self.get_info(lock)
        try:
            if iscoroutine(r := lock.release()): r = await r
        except CRITICAL: raise Critical
        except:
            if self.find_owner(lock) is (o := current_task()):
                if o is None: return self.throw_fallback(lock)
                if (c := o.get_coro()) is None: return self.eager_fallback(lock)
                F = self._loop.create_future()
                try: c.throw(LockForceRequest(self, F.set_result, lock, info))
                except CRITICAL as e: self.task_raised_critical(lock, e)
                except LockForceRequest as e:
                    if (r := e.requester) is self: await self.task_reraised_request(lock)
                    else: await gather(self.lock_busy(lock, r), r.lock_busy(lock, self)) # type: ignore
                except BaseException as e: self.raised_other(lock, e)
                else: self.answer_received(lock, await F)
            if callable(f := self.handlers.get(type(lock))) and iscoroutine(r := f(lock)): await r
            return True
        else: return self.release_returned_false(lock) if r is False else True
        finally:
            if purge_waiters: await self.purge_waiters(lock)
    async def purge_waiters(self, lock, /):
        if w := getattr(lock, '_waiters', None): await safe_cancel_batch(w, disembowel=True)
    async def host(self, task, lock, /, *, timeout1=None, timeout2=0.1, timeout3=None):
        await wait(f := tuple(map(self.wrap_task, (self.force(lock, purge_waiters=False), lock.acquire()))), return_when='FIRST_COMPLETED'); f, a = f
        if await wait_for(f, timeout1): await a
        else:
            try: await wait_for(a, timeout2)
            except TimeoutError: raise TimeoutError(f'failed to acquire lock {lock!r} within {timeout2} seconds') from None
        self.patch_owner(task := self.wrap_task(task), lock); return await wait_for(self._wait_on(task, lock), timeout3)
    async def _wait_on(self, task, lock, /):
        try: return await task
        finally:
            if lock.locked() and iscoroutine(a := lock.release()): await a
    async def lock_busy(self, lock, requester, /): log.info(f'lock busy: {lock}; requester: {requester}')
    async def task_reraised_request(self, lock, /): log.warning(f'{type(self).__qualname__}.force: running task did not handle request to release {type(lock).__qualname__} properly')
    def wrap_task(self, task): return self._loop.create_task(task)
    def patch_owner(self, task, lock, /):
        if hasattr(lock, '_owner'): lock._owner = task
    def find_owner(self, lock, /): return getattr(lock, '_owner', None)
    def throw_fallback(self, lock, /): return True # noqa: ARG002
    def eager_fallback(self, lock, /): return True # noqa: ARG002
    def release_returned_false(self, lock, /): return False # noqa: ARG002
    def answer_received(self, lock, answer, /): log.info(f'{self!r} received answer {answer!r} from {lock!r}')
    def raised_other(self, lock, exc, /):
        if not isinstance(exc, RuntimeError): log.error(f'error encountered in attempt to force {type(lock).__qualname__} at {id(lock):#x}', exc_info=exc)
    async def get_info(self, lock, /): return 'potential deadlock situation' # noqa: ARG002
    def preliminary_check_lock(self, lock, /): return check_methods(lock, 'acquire', 'release', 'locked')
    def task_raised_critical(self, lock, exc, /): raise exc from None # noqa: ARG002
    def can_force_lock_held(self, lock, /): return lock is self._lock or not (lock in self._recognized and lock.locked())