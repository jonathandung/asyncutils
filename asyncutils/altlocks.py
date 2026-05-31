# ty: ignore[unresolved-attribute]
__lazy_modules__ = frozenset(('functools',))
from asyncutils.config import _randinst
from asyncutils.constants import _NO_DEFAULT
from asyncutils._internal import patch as P
from asyncutils._internal.helpers import fullname
from asyncutils._internal.submodules import altlocks_all as __all__
from _collections import deque
import asyncio as I, asyncutils as A
from functools import wraps
from itertools import count
from sys import audit
from time import monotonic
class Releasing:
    __slots__ = '_lock',
    def __init__(self, l, /): self._lock = l
    async def __aenter__(self):
        if not (l := self._lock).locked(): raise RuntimeError('asyncutils.altlocks.Releasing: lock is not acquired')
        if I.iscoroutine(r := l.release()): await r
    async def __aexit__(self, *_): await self._lock.acquire()
class ResourceGuard(RuntimeError, A.AsyncContextMixin):
    _inc_cnt = staticmethod(count(1).__next__); __slots__ = 'guarded',
    def __init__(self, action='using', rname=None): super().__init__(f'another task is already {action} resource{f" #{self._inc_cnt()}" if rname is None else f": {rname!r}"}'); self.guarded = False
    def __enter__(self):
        if self.guarded: raise self
        self.guarded = True
    def __exit__(self, /, *_, e=RuntimeError('asyncutils.altlocks.ResourceGuard: __aexit__ called without prior __aenter__ call')): # noqa: B008
        if not self.guarded: raise e
        self.guarded = False
    @classmethod
    def guard(cls, obj, /, *, action='using'): return cls(action, obj)
    P.patch_method_signatures((__exit__, P.xsig))
class UniqueResourceGuard(ResourceGuard):
    _cache = __import__('weakref').WeakValueDictionary(); __slots__ = '__weakref__',
    def __init_subclass__(cls, /, **_): raise TypeError('cannot subclass asyncutils.altlocks.UniqueResourceGuard')
    @classmethod
    def guard(cls, obj, /, **_):
        if (r := (c := cls._cache).get(obj)) is None: c[obj] = r = super().guard(obj, **_)
        audit('asyncutils.altlocks.UniqueResourceGuard', fullname(obj)); return r
    @classmethod
    def clear_cache(cls): audit('asyncutils.altlocks.UniqueResourceGuard.clear_cache'); cls._cache.clear() # pragma: no cover
    P.patch_method_signatures((guard, "obj, /, *, action='using'"))
class CircuitBreaker:
    CLOSED, HALF_OPEN, OPEN = range(3)
    __slots__ = '_exc', '_half_open_calls', '_lock', '_max_fails', '_max_half_open_calls', '_opened', '_reset', '_unlock', 'fails', 'name', 'state'; _inc_cnt = staticmethod(count(1).__next__)
    def __new__(cls, n, /, max_fails=None, reset=None, *, exc=Exception, max_half_open_calls=None, _='#%d'):
        f = None
        if callable(n) and (n := getattr(f := getattr(getattr(n, '__func__', n), '__wrapped__', n), '__qualname__', None)) is None is (n := getattr(f, '__name__', None)): n = _%cls._inc_cnt()
        audit('asyncutils.altlocks.CircuitBreaker', n, max_fails); s, C = super().__new__(cls), A.getcontext(); s.name, s._max_fails, s._reset, s._exc, s._opened, s._max_half_open_calls, s._unlock, s._lock, s.state = n, C.CIRCUIT_BREAKER_DEFAULT_MAX_FAILS if max_fails is None else max_fails, C.CIRCUIT_BREAKER_DEFAULT_RESET if reset is None else reset, exc, float('-inf'), C.CIRCUIT_BREAKER_DEFAULT_MAX_HALF_OPEN_CALLS if max_half_open_calls is None else max_half_open_calls, Releasing(l := I.Lock()), l, s.CLOSED; s.fails = s._half_open_calls = 0; return s if f is None else s(f)
    def __call__(self, f, /, *, timer=monotonic, default=_NO_DEFAULT):
        audit('asyncutils.altlocks.CircuitBreaker.__call__', self.name, fullname(f))
        async def g(*a, **k):
            async with self._lock:
                if (s := self.state) == self.OPEN:
                    if timer()-self._opened > self._reset: self.state, self._half_open_calls = self.HALF_OPEN, 0
                    else: raise A.CircuitOpen(f'asyncutils.altlocks.CircuitBreaker: circuit {self.name} is open')
                elif s == self.HALF_OPEN:
                    if (c := self._half_open_calls) == (m := self._max_half_open_calls): raise A.CircuitHalfOpen(f'asyncutils.altlocks.CircuitBreaker: breaker {self.name} exceeded the maximum of {m} calls in the half-open state')
                    self._half_open_calls = c+1
                try:
                    async with self._unlock: r = await f(*a, **k)
                    if s == self.HALF_OPEN: self._half_open_calls = self.fails = 0; self.state = self.CLOSED
                    return r
                except self._exc:
                    if (x := self.fails+1) < self._max_fails: self.fails = x
                    else: self._opened, self.state, self.fails = timer(), self.OPEN, 0
                    if default is _NO_DEFAULT: raise
                    return default
                except A.CRITICAL: raise A.Critical
                except BaseException as e: raise A.CircuitBreakerError(f'asyncutils.altlocks.CircuitBreaker: unexpected {fullname(e)} in {fullname(f)} under breaker {self.name!r}') from e
        return wraps(f)(g)
    P.patch_classmethod_signatures((__new__, 'name, /, max_fails=None, reset=None, *, exc={}, max_half_open_calls=None'))
class StatefulBarrier(A.AwaitableMixin):
    __slots__ = '_broken', '_cond', '_count', '_exc', '_initstate', '_parties', '_state'
    def __init__(self, parties, name='\b', initstate=(), maxstate=None): self._parties, self._exc, self._count, self._state, self._cond, self._initstate, self._broken = parties, I.BrokenBarrierError(f'{fullname(self)} {name} is broken'), 0, deque(maxlen=maxstate), I.Condition(), initstate, False
    async def _wait(self, state=None):
        async with (C := self._cond):
            self.raise_for_abort(); f = (S := self._state).append
            if (s := self._initstate) is not None:
                async for _ in A.iter_to_agen(s): f(_)
                self._initstate = None
            self._count = (c := self._count)+1
            if state is not None: f(state)
            if c == self._parties-1: self._count = 0; C.notify_all(); self._broken = True
            else:
                w = C.wait
                while not self._broken: await w()
            return c, S.copy()
    async def wait(self, state=None, timeout=None):
        try: return await I.wait_for(self._wait(state), timeout)
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
    __slots__ = '_fails', '_jitter', '_lb', '_lc', '_lf', '_lock', '_max', '_min', '_randf', '_rate', '_successes', '_timer', '_ub', '_uf', '_window'
    def __init__(self, init_rate, min_rate=None, max_rate=None, window=None, *, ubound=None, lbound=None, ufactor=None, lfactor=None, jitter=None, timer=monotonic, rand=lambda j, u=_randinst.uniform: u(-j, j)):
        C = A.getcontext()
        if min_rate is None: min_rate = C.DYNAMIC_THROTTLE_DEFAULT_MIN_RATE
        if max_rate is None: max_rate = C.DYNAMIC_THROTTLE_DEFAULT_MAX_RATE
        if not 0 < min_rate <= init_rate <= max_rate: raise ValueError('asyncutils.altlocks.DynamicThrottle: inconsistent rates after applying bounds')
        self._min, self._max, self._window, self._lock, self._timer, self._ub, self._lb, self._uf, self._lf, self.jitter, self._randf, self._rate, self._lc = min_rate, max_rate, C.DYNAMIC_THROTTLE_DEFAULT_WINDOW if window is None else window, I.Lock(), timer, C.DYNAMIC_THROTTLE_DEFAULT_UBOUND if ubound is None else ubound, C.DYNAMIC_THROTTLE_DEFAULT_LBOUND if lbound is None else lbound, C.DYNAMIC_THROTTLE_DEFAULT_UFACTOR if ufactor is None else ufactor, C.DYNAMIC_THROTTLE_DEFAULT_LFACTOR if lfactor is None else lfactor, C.DYNAMIC_THROTTLE_DEFAULT_JITTER if jitter is None else jitter, rand, init_rate, timer()-1.0/init_rate; self.reset()
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
    async def __aenter__(self): await I.sleep((1.0/self._rate-self.ctime+self._lc)*(1.0+self._randf(self._jitter))); self._lc = self.ctime
    async def __aexit__(self, e, /, *_):
        async with self._lock:
            if (t := (s := self._successes)+self._fails) >= self._window: self.rate *= self._uf if (r := s/t) > self._ub else self._lf if r < self._lb else 1.0; self.reset()
            if e is None: self._successes += 1
            else: self._fails += 1
    def reset(self): self._successes = self._fails = 0
    P.patch_method_signatures((__aexit__, P.xsig))
del _randinst, count, P