__lazy_modules__ = frozenset(('functools',))
from asyncutils import AsyncContextMixin, AwaitableMixin, CircuitBreakerError, CircuitHalfOpen, CircuitOpen, Critical, getcontext, iter_to_agen, CRITICAL
from asyncutils.config import _randinst
from asyncutils.constants import _NO_DEFAULT
from asyncutils._internal.helpers import fullname
from asyncutils._internal.submodules import altlocks_all as __all__
from _collections import deque # type: ignore[import-not-found]
from asyncio import BoundedSemaphore, BrokenBarrierError, Condition, Lock, iscoroutine, sleep, timeout as _timeout
from functools import wraps
from itertools import count
from sys import audit
from time import monotonic
class Releasing:
    __slots__ = '_lock',
    def __init__(self, lock, /): self._lock = lock
    async def __aenter__(self):
        if iscoroutine(r := self._lock.release()): r = await r
        return r
    async def __aexit__(self, *_): await self._lock.acquire()
class DynamicBoundedSemaphore(BoundedSemaphore):
    def __init__(self, value=None): super().__init__(getcontext().DYNAMIC_BOUNDED_SEMAPHORE_DEFAULT_VALUE if value is None else value); self._waiters = deque() # type: deque
    @property
    def bound(self): return self._bound_value
    @bound.setter
    def bound(self, value, /):
        if value < 0: raise ValueError('bound must be non-negative')
        d, self._bound_value, f = value-self._bound_value, value, (W := self._waiters).popleft
        while d and W:
            if not (w := f()).done(): w.set_result(None); d -= 1
class ResourceGuard(RuntimeError, AsyncContextMixin):
    _inc_cnt = staticmethod(count(1).__next__); __slots__ = 'guarded',
    def __init__(self, action='using', rname=None): super().__init__(f'another task is already {action} resource{f" #{self._inc_cnt()}" if rname is None else f": {rname!r}"}'); self.guarded = False
    def __enter__(self):
        if self.guarded: raise self
        self.guarded = True
    def __exit__(self, /, *_, e=RuntimeError('__aexit__ called without prior __aenter__ call')): # noqa: B008
        if not self.guarded: raise e
        self.guarded = False
    @classmethod
    def guard(cls, obj, /, *, action='using'): return cls(action, obj)
class UniqueResourceGuard(ResourceGuard):
    _cache, __slots__ = {}, ()
    def __init_subclass__(cls, /, **_): raise TypeError('cannot subclass asyncutils.altlocks.UniqueResourceGuard')
    @classmethod
    def guard(cls, obj, /, *, action='using'):
        if (r := (c := cls._cache).get(k := id(obj))) is None: c[k] = r = cls(action, obj)
        audit('asyncutils.altlocks.UniqueResourceGuard', fullname(type(obj))); return r
    @classmethod
    def clear_cache(cls): audit('asyncutils.altlocks.UniqueResourceGuard.clear_cache'); cls._cache.clear()
class CircuitBreaker:
    __slots__ = '_exc', '_half_open_calls', '_lock', '_max_fails', '_max_half_open_calls', '_opened', '_reset', '_unlock', 'fails', 'name', 'state'; _inc_cnt = staticmethod(count(1).__next__)
    def __new__(cls, name, /, max_fails=None, reset=None, *, exc=Exception, max_half_open_calls=None, _='#%d'):
        f = None
        if callable(name) and (name := getattr(f := getattr(getattr(name, '__func__', name), '__wrapped__', name), '__qualname__', None)) is None is (name := getattr(f, '__name__', None)): name = _%cls._inc_cnt()
        audit('asyncutils.altlocks.CircuitBreaker', name, max_fails); self, C = super().__new__(cls), getcontext(); self.name, self._max_fails, self._reset, self._exc, self._opened, self._half_open_calls, self._max_half_open_calls, self._unlock, self._lock = name, C.CIRCUIT_BREAKER_DEFAULT_MAX_FAILS if max_fails is None else max_fails, C.CIRCUIT_BREAKER_DEFAULT_RESET if reset is None else reset, exc, float('-inf'), 0, C.CIRCUIT_BREAKER_DEFAULT_MAX_HALF_OPEN_CALLS if max_half_open_calls is None else max_half_open_calls, Releasing(l := Lock()), l; self._set(0); return self if f is None else self(f)
    def __call__(self, f, /, *, timer=monotonic, default=_NO_DEFAULT):
        audit('asyncutils.altlocks.CircuitBreaker.__call__', self.name, fullname(f))
        async def wrapper(*a, **k):
            async with self._lock: # type: ignore
                if (s := self.state) == 2: # noqa: PLR2004
                    if timer()-self._opened > self._reset: self.state, self._half_open_calls = 1, 0
                    else: raise CircuitOpen(f'circuit {self.name} is open')
                elif s == 1:
                    if (c := self._half_open_calls) == (m := self._max_half_open_calls): raise CircuitHalfOpen(f'circuit {self.name} exceeded the maximum of {m} calls in the half-open state')
                    self._half_open_calls = c+1
                try:
                    async with self._unlock: r = await f(*a, **k) # type: ignore
                except self._exc:
                    self.fails = x = self.fails+1
                    if x >= self._max_fails: self._opened = timer(); self._set(2)
                    if default is _NO_DEFAULT: raise
                    return default
                except CRITICAL: raise Critical
                except BaseException as e: raise CircuitBreakerError(f'unexpected {fullname(e)} in {fullname(f)} under {fullname(self)} {self.name!r}: {e}') from None # noqa: BLE001
                else:
                    if s == 1: self._half_open_calls = 0; self._set(0)
                    return r
        return wraps(f)(wrapper)
    def _set(self, state, /): self.state, self.fails = state, 0
class StatefulBarrier(AwaitableMixin):
    __slots__ = '_broken', '_cond', '_count', '_exc', '_initstate', '_parties', '_state'
    def __init__(self, parties, name='\b', initstate=(), maxstate=None): self._parties, self._exc, self._count, self._state, self._cond, self._initstate, self._broken = parties, BrokenBarrierError(f'{fullname(self)} {name} is broken'), 0, deque(maxlen=maxstate), Condition(), initstate, False
    async def wait(self, state=None, *, timeout=None):
        try:
            async with _timeout(timeout), (C := self._cond):
                self.raise_for_abort(); f = (S := self._state).append
                if (s := self._initstate) is not None:
                    async for _ in iter_to_agen(s): f(_)
                    self._initstate = None
                self._count = (c := self._count)+1
                if state is not None: f(state)
                if c == self._parties-1: self._count = 0; C.notify_all(); self._broken = True
                else:
                    w = C.wait
                    while not self._broken: await w()
                return c, S.copy()
        except TimeoutError: await self.abort(); raise
    async def abort(self):
        async with (C := self._cond):
            if not self._broken: self._broken = True; C.notify_all()
    def raise_for_abort(self):
        if self._broken: raise self._exc
    @property
    def broken(self): return self._broken
    @property
    def remaining_parties(self): return self._parties-self._count
    @property
    def parties(self): return self._parties
    @property
    def n_waiting(self): return self._count
class DynamicThrottle:
    __slots__ = '_fails', '_jitter', '_last_call', '_lbound', '_lfactor', '_lock', '_max', '_min', '_randf', '_rate', '_successes', '_timer', '_ubound', '_ufactor', '_window'
    def __init__(self, init_rate, min_rate=None, max_rate=None, window=None, *, ubound=None, lbound=None, ufactor=None, lfactor=None, jitter=None, timer=monotonic, rand=lambda j, u=_randinst.uniform: u(-j, j)):
        C = getcontext()
        if min_rate is None: min_rate = C.DYNAMIC_THROTTLE_DEFAULT_MIN_RATE
        if max_rate is None: max_rate = C.DYNAMIC_THROTTLE_DEFAULT_MAX_RATE
        if not 0 < min_rate <= init_rate <= max_rate: raise ValueError('inconsistent rates')
        self._min, self._max, self._window, self._lock, self._timer, self._ubound, self._lbound, self._ufactor, self._lfactor, self.jitter, self._randf = min_rate, max_rate, C.DYNAMIC_THROTTLE_DEFAULT_WINDOW if window is None else window, Lock(), timer, C.DYNAMIC_THROTTLE_DEFAULT_UBOUND if ubound is None else ubound, C.DYNAMIC_THROTTLE_DEFAULT_LBOUND if lbound is None else lbound, C.DYNAMIC_THROTTLE_DEFAULT_UFACTOR if ufactor is None else ufactor, C.DYNAMIC_THROTTLE_DEFAULT_LFACTOR if lfactor is None else lfactor, C.DYNAMIC_THROTTLE_DEFAULT_JITTER if jitter is None else jitter, rand; self.rate = init_rate; self.reset()
    @property
    def rate(self): return self._rate
    @rate.setter
    def rate(self, rate, /, _=0.02):
        if abs(1-self._rate/(rate := max(self._min, min(self._max, rate)))) > _: self._rate = rate
    @property
    def jitter(self): return self._jitter
    @jitter.setter
    def jitter(self, jitter, /): self._jitter = max(0.0, float(jitter))
    @property
    def ctime(self): return self._timer()
    @property
    def successes(self): return self._successes
    @property
    def fails(self): return self._fails
    async def __aenter__(self): await sleep((1.0/self._rate-self.ctime+self._last_call)*(1.0+self._randf(self._jitter))); self._last_call = self.ctime
    async def __aexit__(self, e, *_):
        async with self._lock:
            if (t := (s := self._successes)+self._fails) >= self._window: self.rate *= self._ufactor if (r := s/t) > self._ubound else self._lfactor if r < self._lbound else 1.0; self._successes = self._fails = 0
            if e is None: self._successes += 1
            else: self._fails += 1
    def reset(self): self._successes = self._fails = 0; self._last_call = self.ctime-1.0/self._rate
del _randinst, count