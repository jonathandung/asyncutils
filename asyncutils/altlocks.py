from .mixins import AsyncContextMixin, AwaitableMixin
from .config import _NO_DEFAULT, _randinst
from .base import iter_to_aiter
from .exceptions import CircuitHalfOpen, CircuitOpen, CircuitBreakerError, Critical, CRITICAL
from .constants import getcontext
from asyncio.locks import Lock, Event, BoundedSemaphore
from asyncio.exceptions import BrokenBarrierError
from asyncio.tasks import wait_for, sleep
from time import monotonic
from functools import wraps
from _collections import deque
from itertools import count
from ._internal.submodules import altlocks_all as __all__
class DynamicBoundedSemaphore(BoundedSemaphore):
    def __init__(self, value=1): super().__init__(value); self._waiters = deque()
    @property
    def bound(self): return self._bound_value
    @bound.setter
    def bound(self, value, /):
        if value < 0: raise ValueError('bound must be non-negative')
        d, self._bound_value, f = value-self._bound_value, value, (W := self._waiters).popleft
        while d and W:
            if not (w := f()).done(): w.set_result(None); d -= 1
class ResourceGuard(RuntimeError, AsyncContextMixin):
    __slots__, _inc_cnt = 'guarded', staticmethod(count(1).__next__)
    def __init__(self, action='using', rname=None): super().__init__(f"another task is already {action} resource {'#%d'%self._inc_cnt() if rname is None else repr(rname)}"); self.guarded = False
    async def __aenter__(self):
        if self.guarded: raise self
        self.guarded = True
    async def __aexit__(self, /, *_, _e='__aexit__ called without prior __aenter__ call'):
        if not self.guarded: raise RuntimeError(_e)
        self.guarded = False
    @classmethod
    def guard(cls, obj, /, *, action='using'): return cls(action, obj)
class UniqueResourceGuard(ResourceGuard):
    _cache, __slots__ = {}, ()
    @classmethod
    def guard(cls, obj, /, *, action='using'):
        if (r := (c := cls._cache).get(k := id(obj))) is None: c[k] = r = cls(action, obj)
        return r
class CircuitBreaker:
    __slots__ = '_name', '_max_fails', '_reset', '_exc', '_fails', '_opened', '_half_open_calls', '_max_half_open_calls', '_call_lock', '_state'; _inc_cnt = staticmethod(count(1).__next__)
    def __new__(cls, name, /, max_fails=3, reset=None, exc=Exception, max_half_open_calls=None, _fmt='#%d'):
        f = None
        if callable(name) and (name := getattr(f := getattr(getattr(name, '__func__', name), '__wrapped__', name), '__name__', None)) is None is (name := getattr(f, '__qualname__', None)): name = _fmt%cls._inc_cnt()
        self, C = super().__new__(cls), getcontext(); self._name, self._max_fails, self._reset, self._exc, self._opened, self._half_open_calls, self._max_half_open_calls = name, max_fails, C.CIRCUIT_BREAKER_DEFAULT_RESET if reset is None else reset, exc, float('-inf'), 0, C.CIRCUIT_BREAKER_DEFAULT_MAX_HALF_OPEN_CALLS if max_half_open_calls is None else max_half_open_calls; self._set(0); self._init_lock(); return self if f is None else self(f)
    def _init_lock(self): self._call_lock = Lock()
    def __call__(self, f, /, timer=monotonic, default=_NO_DEFAULT):
        async def wrapper(*a, **k):
            async with self._call_lock:
                if (s := self._state) == 2:
                    if timer()-self._opened > self._reset: self._state, self._half_open_calls = 1, 0
                    else: raise CircuitOpen(f'circuit {self.name} is open')
                elif s == 1:
                    if (c := self._half_open_calls) == (m := self._max_half_open_calls): raise CircuitHalfOpen(f'circuit {self.name} exceeded the maximum of {m} calls in the half-open state')
                    self._half_open_calls = c+1
                try:
                    r = await f(*a, **k)
                    if s == 1: self._half_open_calls = 0; self._set(0)
                    return r
                except self._exc:
                    self._fails = x = self._fails+1
                    if x >= self._max_fails: self._opened = timer(); self._set(2)
                    if default is _NO_DEFAULT: raise
                    return default
                except CRITICAL: raise Critical
                except BaseException as e: raise CircuitBreakerError(f'unexpected {type(e).__qualname__} in {f!r} under CircuitBreaker {self.name!r}: {e}') from None
        return wraps(f)(wrapper)
    def _set(self, state, /): self._state, self._fails = state, 0
    @property
    def fails(self): return self._fails
    @property
    def name(self): return self._name
class StatefulBarrier(AwaitableMixin):
    __slots__ = '_parties', '_exc', '_count', '_state', '_event', '_lock', '_gen', '_initstate'
    def __init__(self, parties, name='\b', initstate=(), maxstate=None): self._parties, self._exc, self._count, self._state, self._event, self._lock, self._gen, self._initstate = parties, BrokenBarrierError(f'{type(self).__qualname__} {name} is broken'), 0, deque(maxlen=maxstate), Event(), Lock(), 0, initstate
    async def wait(self, state=None, timeout=None):
        self.raise_for_abort(); S = self._state.append
        if (s := self._initstate) is None:
            async for _ in iter_to_aiter(s): S(_)
        async with self._lock:
            g = self._gen; self._count += 1
            if state is not None: S(state)
            if self._count == self._parties: self._event.set(); r = self._parties-1, self._state.copy(); self._reset(); return r
        try:
            await wait_for(self._event.wait(), timeout)
            if g != self._gen: return -1, deque()
            async with self._lock: return self._count-1, self._state.copy()
        except TimeoutError: self.abort(); raise
    def _reset(self): self._count = 0; self._state.clear(); self._event.clear(); self._gen += 1
    def abort(self): self._event.set()
    def raise_for_abort(self):
        if self.broken: raise self._exc
    @property
    def broken(self): return self._event.is_set()
    @property
    def remaining_parties(self): return self._parties-self._count
    @property
    def parties(self): return self._parties
class DynamicThrottle:
    __slots__ = '_min', '_max', '_window', '_successes', '_fails', '_ubound', '_lbound', '_ufactor', '_lfactor', '_lock', '_rate', '_timer', '_last_call', '_jitter', '_randf'
    def __init__(self, init_rate, min_rate=float('-inf'), max_rate=float('inf'), window=None, *, ubound=None, lbound=None, ufactor=None, lfactor=None, jitter=None, timer=monotonic, rand=lambda j, u=_randinst.uniform: u(-j, j)):
        if min_rate > max_rate: raise ValueError('inconsistent rates')
        C = getcontext(); self._min, self._max, self._window, self._lock, self._timer, self._ubound, self._lbound, self._ufactor, self._lfactor, self.jitter, self._randf = min_rate, max_rate, C.DYNAMIC_THROTTLE_DEFAULT_WINDOW if window is None else window, Lock(), timer, C.DYNAMIC_THROTTLE_DEFAULT_UBOUND if ubound is None else ubound, C.DYNAMIC_THROTTLE_DEFAULT_LBOUND if lbound is None else lbound, C.DYNAMIC_THROTTLE_DEFAULT_UFACTOR if ufactor is None else ufactor, C.DYNAMIC_THROTTLE_DEFAULT_LFACTOR if lfactor is None else lfactor, C.DYNAMIC_THROTTLE_DEFAULT_JITTER if jitter is None else jitter, rand; self.rate = init_rate; self.reset()
    @property
    def rate(self): return self._rate
    @rate.setter
    def rate(self, rate, /): self._rate = max(self._min, min(self._max, rate))
    @property
    def jitter(self): return self._jitter
    @jitter.setter
    def jitter(self, jitter, /): self._jitter = max(0.0, float(jitter))
    @property
    def time(self): return self._timer()
    @property
    def successes(self): return self._successes
    @property
    def fails(self): return self._fails
    async def __aenter__(self): await sleep((1.0/self._rate-self.time+self._last_call)*(1.0+self._randf(self.jitter))); self._last_call = self.time
    async def __aexit__(self, e, *_):
        async with self._lock:
            if (t := self._successes+self._fails) >= self._window: self.rate *= self._ufactor if (r := self._successes/t) > self._ubound else self._lfactor if r < self._lbound else 1.0; self._successes = self._fails = 0
            if e is None: self._successes += 1
            else: self._fails += 1
    def reset(self): self._successes = self._fails = 0; self._last_call = self.time-1.0/self._rate
del _randinst
