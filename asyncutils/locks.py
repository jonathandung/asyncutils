# type: ignore
from . import context as C, mixins as M
from ._internal import log
from ._internal.helpers import check_methods, fullname
from ._internal.submodules import locks_all as __all__
from .base import safe_cancel_batch
from .constants import _NO_DEFAULT
from .exceptions import CRITICAL, Critical, LockForceRequest
from .properties import coercedmethod
from .queues import ignore_valerrs
from _collections import defaultdict, deque
from asyncio.coroutines import iscoroutine
from asyncio.locks import Condition, Event, Lock
from asyncio.tasks import current_task, gather, wait, wait_for
from contextlib import asynccontextmanager
from heapq import heappop, heappush
from time import monotonic
class AdvancedRateLimit(M.EventualLoopMixin, M.LockMixin):
    __slots__ = '_lock', '_lu', '_unfair', '_waiters', 'capacity', 'rate', 'tokens'
    def __init__(self, rate, capacity=None, fair=True): super().__init__(); self.rate, self._lock, self._waiters, self._unfair, self._lu = rate, Lock(), deque(), not fair, monotonic(); self.tokens = self.capacity = capacity or rate
    async def acquire(self, tokens=None, timeout=None):
        async with self._lock:
            self.update_tokens_lock_held()
            if tokens > self.tokens: w = self._waiters; (w.appendleft if self._unfair else w.append)((C.ADVANCED_RATE_LIMIT_DEFAULT_TOKENS if tokens is None else tokens, F := self.loop.create_future()))
            else: self.tokens -= tokens; return True
        try: await wait_for(F, timeout); return True
        except TimeoutError: return False
    async def release(self, tokens=None):
        async with self._lock: self.update_tokens_lock_held(); self.tokens = min(self.tokens+(C.ADVANCED_RATE_LIMIT_DEFAULT_TOKENS if tokens is None else tokens), self.capacity)
    async def set_rate(self, new):
        async with self._lock: self.update_tokens_lock_held(); self.rate, self.capacity = new, max(self.capacity, new)
    def locked(self): return bool(self._waiters)
    def update_tokens_lock_held(self):
        e, p, self._lu = (n := monotonic())-self._lu, (w := self._waiters).popleft, n; T = min(self.capacity, self.tokens+e*self.rate)
        while w and (t := p())[0] <= T:
            t, f = t; T -= t
            if not f.done(): f.set_result(None)
        self.tokens = T; w.appendleft(t)
class PrioritySemaphore(M.LockMixin):
    __slots__ = '_tiebreak', '_value', '_waiters'
    def __init__(self, value=None): self._value, self._tiebreak, self._waiters = C.PRIORITY_SEMAPHORE_DEFAULT_VALUE if value is None else value, 0, []
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
        (s := self._waiters if key is None else self._specific_waiters[key]).add(F := self.loop.create_future())
        try: await wait_for(F, timeout)
        finally: s.discard(F)
    async def wait_all(self): await gather(*map(self.wait, self._specific_waiters), return_exceptions=True)
    def assert_locked(self):
        if not self.locked(): raise RuntimeError('must acquire condition to notify')
    def notify(self, n=1, key=None, strict=False):
        self.assert_locked(); i = 0
        for i, F in enumerate((s := self._waiters if (c := key is None) else self._specific_waiters[key]).copy()):
            if i >= n: break
            if not F.done(): F.set_result(None)
            s.discard(F)
            if not (c or s): del self._specific_waiters[key]
        else:
            if strict and i+1 < n: raise ValueError(f'{fullname(self)}: not enough parties to notify')
    def notify_all(self, key=None):
        self.assert_locked()
        for F in (s := self._waiters if key is None else self._specific_waiters.pop(key)):
            if not F.done(): F.set_result(None)
        l = len(s); s.clear(); return l
class MultiCountDownLatch:
    __slots__ = '_cond', '_counts'
    def __init__(self, counts): self._cond, self._counts = KeyedCondition(), dict(counts)
    async def count_down(self, key):
        async with (C := self._cond):
            if (c := (d := self._counts).get(key)) is None or c <= 0: del d[key]; raise KeyError(key)
            if c == 1: C.notify_all(key); del d[key]
            else: d[key] = c-1
    async def wait(self, key):
        async with (C := self._cond): await C.wait(key)
    async def wait_all(self): await self._cond.wait_all()
class Base:
    __slots__ = '__wrapped__', 'reader', 'reading', 'writer', 'writing'
    def __init__(self, l, f, /, _=__slots__[1:]):
        for s in _: setattr(self, s, getattr(l, s))
        self.__wrapped__ = f
    def __init_subclass__(cls, /, **_):
        if getattr(cls, '__slots__', True): raise TypeError('__slots__ should be empty tuple')
    def __getattr__(self, n, /): return getattr(self.__wrapped__, n)
def _rwlock_sub_new(cls, /): (_ := object.__new__(cls)).setup(); return _
class RWLock:
    __slots__ = ('_wa',)
    def __new__(cls, /, prefer_writers=None): return _rwlock_sub_new(WritePreferredRWLock if (C.RWLOCK_DEFAULT_PREFER_WRITERS if prefer_writers is None else prefer_writers) else ReadPreferredRWLock)
    @coercedmethod
    class reader(Base):
        __slots__ = ()
        async def __call__(self, *a, **k):
            async with self.reading(): return await self.__wrapped__(*a, **k)
    @coercedmethod
    class writer(Base):
        __slots__ = ()
        async def __call__(self, *a, **k):
            async with self.writing(): return await self.__wrapped__(*a, **k)
    def locked(self): return self._wa
    def __init_subclass__(cls, /, **_):
        if not isinstance(getattr(cls, '__slots__', None), tuple): raise TypeError('__slots__ must be a tuple')
        cls.__new__ = _rwlock_sub_new
class ReadPreferredRWLock(RWLock):
    __slots__ = '_cm', '_readers'
    def setup(self): self._readers, self._cm, self._wa = 0, Lock(), Lock()
    @asynccontextmanager
    async def reading(self):
        async with self._cm:
            if (r := self._readers+1) == 1: await self._wa.acquire()
            self._readers = r
        try: yield
        finally:
            async with self._cm:
                if (r := self._readers-1) == 0: self._wa.release()
                self._readers = r
    @asynccontextmanager
    async def writing(self):
        async with self._wa: yield
    def locked(self): return self._wa.locked()
class WritePreferredRWLock(RWLock):
    __slots__ = '_cond', '_nr', '_nw'
    def setup(self): self._cond, self._wa = Condition(), False; self._nr = self._nw = 0
    @asynccontextmanager
    async def reading(self):
        async with (C := self._cond):
            w = C.wait
            while self._wa or self._nw > 0: await w()
            self._nr += 1
        try: yield
        finally:
            async with C:
                if (r := self._nr-1) == 0: C.notify_all()
                self._nr = r
    @asynccontextmanager
    async def writing(self):
        async with (C := self._cond):
            w = C.wait; self._nw += 1
            while self._wa or self._nr > 0: await w()
            self._nw -= 1; self._wa = True
        try: yield
        finally:
            async with C: self._wa = False; C.notify_all()
class FairRWLock(RWLock):
    __slots__ = '_cond', '_qd', '_readers'
    def setup(self): self._cond, self._wa, self._readers, self._qd = Condition(), False, 0, deque()
    @asynccontextmanager
    async def reading(self):
        async with (C := self._cond):
            F, w = C._get_loop().create_future(), C.wait
            (Q := self._qd).append(E := (False, F))
            try:
                while True:
                    if Q[0][1] is not F or self._wa: await w()
                    else: self._readers += 1; Q.popleft(); F.set_result(True); break
            except:
                with ignore_valerrs: Q.remove(E)
                raise
        try: yield
        finally:
            async with C:
                if (r := self._readers-1) == 0: C.notify_all()
                self._readers = r
    @asynccontextmanager
    async def writing(self):
        async with (C := self._cond):
            F, w = C._get_loop().create_future(), C.wait
            (Q := self._qd).append(E := (True, F))
            try:
                while True:
                    if Q[0][1] is not F or self._wa or self._readers > 0: await w()
                    else: self._wa = True; Q.popleft(); F.set_result(True); break
            except:
                with ignore_valerrs: Q.remove(E)
                raise
        try: yield
        finally:
            async with C: self._wa = False; C.notify_all()
class PriorityRWLock(RWLock):
    __slots__ = '_cond', '_count', '_ilock', '_qd', '_readers'
    def setup(self): self._cond, self._count, self._ilock, self._wa, self._readers, self._qd = Condition(), 0, Lock(), False, 0, []
    async def _push_item(self, priority, is_writer):
        async with self._ilock: self._count = (c := self._count)+1
        heappush(self._qd, E := (priority, *((is_writer, c) if isinstance(self, WritePreferredPriorityRWLock) else (c, is_writer)), self._cond._get_loop().create_future())); return E
    @asynccontextmanager
    async def reading(self, priority=0):
        async with (C := self._cond):
            F, Q, w = (E := await self._push_item(priority, False))[-1], self._qd, C.wait
            try:
                while True:
                    if Q[0][-1] is not F or self._wa: await w()
                    else: self._readers += 1; heappop(Q); F.set_result(True); break
            except:
                with ignore_valerrs: Q.remove(E)
                raise
        try: yield
        finally:
            async with C:
                if (r := self._readers-1) == 0: C.notify_all()
                self._readers = r
    @asynccontextmanager
    async def writing(self, priority=0):
        async with (C := self._cond):
            F, Q, w = (E := await self._push_item(priority, True))[-1], self._qd, C.wait
            try:
                while True:
                    if Q[0][-1] is not F or self._wa or self._readers > 0: await w()
                    else: self._wa = True; heappop(Q); F.set_result(True); break
            except:
                with ignore_valerrs: Q.remove(E)
                raise
        try: yield
        finally:
            async with C: self._wa = False; C.notify_all()
class WritePreferredPriorityRWLock(PriorityRWLock): __slots__ = ()
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
    def __del__(self): self.__lock.exiter()
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
        if await wait_for(f, C.LOCKSMITH_DEFAULT_TIMEOUTS if timeout1 is _NO_DEFAULT else timeout1): await a
        else:
            try: await wait_for(a, C.LOCKSMITH_DEFAULT_TIMEOUTS if timeout2 is _NO_DEFAULT else timeout2)
            except TimeoutError: raise TimeoutError(f'failed to acquire lock {lock!r} within {timeout2} seconds') from None
        self.patch_owner(task := self.wrap_task(task), lock); return await wait_for(self._wait_on(task, lock), C.LOCKSMITH_DEFAULT_TIMEOUTS if timeout3 is _NO_DEFAULT else timeout3)
    async def _wait_on(self, task, lock, /):
        try: return await task
        finally:
            if lock.locked() and iscoroutine(a := lock.release()): await a
    async def lock_busy(self, lock, requester, /): log.info('lock busy: %r; requester: %r', lock, requester)
    async def task_reraised_request(self, lock, /): log.warning('%s.force: running task did not handle request to release %s properly', type(self).__qualname__, type(lock).__qualname__)
    def wrap_task(self, a, /):
        async def f(): return await a
        return self._loop.create_task(f())
    def patch_owner(self, task, lock, /):
        if hasattr(lock, '_owner'): lock._owner = task
    def find_owner(self, lock, /): return getattr(lock, '_owner', None)
    # ruff: disable[ARG002]
    def throw_fallback(self, lock, /): return True
    def eager_fallback(self, lock, /): return True
    def release_returned_false(self, lock, /): return False
    def answer_received(self, lock, answer, /): log.info('%r received answer %r from %r', self, answer, lock)
    def raised_other(self, lock, exc, /):
        if not isinstance(exc, RuntimeError): log.error('error encountered in attempt to force %s at %#x', type(lock).__qualname__, id(lock), exc_info=exc)
    async def get_info(self, lock, /): return 'potential deadlock situation'
    def preliminary_check_lock(self, lock, /): return check_methods(lock, 'acquire', 'release', 'locked')
    def task_raised_critical(self, lock, exc, /): raise exc from None
    def can_force_lock_held(self, lock, /): return lock is self._lock or not (lock in self._recognized and lock.locked())
    # ruff: enable[ARG002]
del Base