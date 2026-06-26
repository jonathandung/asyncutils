# ty: ignore[unresolved-attribute]
__lazy_modules__ = frozenset(('functools',))
from asyncutils.config import _randinst
from asyncutils.constants import _NO_DEFAULT
from asyncutils._internal import patch as P
from asyncutils._internal.helpers import fullname, subscriptable
from asyncutils._internal.submodules import altlocks_all as __all__
from _collections import deque
import asyncio as I, asyncutils as A
from functools import wraps
from itertools import count
from sys import audit
from time import monotonic
from _warnings import warn
class Releasing:
    __slots__ = '_lock',
    def __init__(self, l, /): self._lock = l
    async def __aenter__(self):
        if not (l := self._lock).locked(): raise RuntimeError('asyncutils.altlocks.Releasing: lock is not acquired')
        if I.iscoroutine(r := l.release()): await r
    async def __aexit__(self, *_): await self._lock.acquire()
class Resource:
    _inc_cnt = staticmethod(count(1).__next__); __slots__ = '_',
    def __init__(self): self._ = f'anonymous resource #{self._inc_cnt()}'
    def __repr__(self): return self._
@subscriptable
class ResourceGuard(RuntimeError, A.AsyncContextMixin):
    __slots__ = '__', '_t', '_u', 'action', 'guarded'
    def __new__(cls, rsrc=_NO_DEFAULT, *, action='using', t=Resource):
        if rsrc is _NO_DEFAULT: rsrc = t()
        (_ := RuntimeError.__new__(cls)).__, _.action, _.guarded = rsrc, action, False; _._t = _._u = 0; return _
    def __enter__(self):
        r = self.__; self._t += 1
        if self.guarded: raise A.ResourceBusy(f'another task is already {self.action} resource: {r!r}')
        self.guarded = True; self._u += 1
    def __exit__(self, /, *_, e='asyncutils.altlocks.ResourceGuard: __aexit__ called without prior __aenter__ call'):
        if not self.guarded: raise RuntimeError(e)
        self.guarded = False
    @A.dualcontextmanager(use_existing_executor=False, create_executor=False, strict=False)
    def yields_resource(self, t=Resource):
        if not isinstance(_ := self.__, t): raise TypeError('asyncutils.altlocks.ResourceGuard.yields_resource expected resource guard to have been instantiated with a resource')
        with self: yield _
    @property
    def success_ratio(self): return u/self._t if (u := self._u) else 0.0
    P.patch_method_signatures((__exit__, P.exit_sig), (yields_resource, ''), (__new__, "rsrc={0}, *, action='using'"))
class UniqueResourceGuard(ResourceGuard):
    _cache = __import__('weakref').WeakValueDictionary(); __slots__ = '__weakref__',
    def __init_subclass__(cls, /, **_): raise TypeError('cannot subclass asyncutils.altlocks.UniqueResourceGuard')
    def __new__(cls, rsrc, **_):
        if (r := (c := cls._cache).get(i := id(rsrc))) is None: audit('asyncutils.altlocks.UniqueResourceGuard', fullname(rsrc)); c[i] = r = super().__new__(cls, rsrc, **_)
        elif _: warn('asyncutils.altlocks.UniqueResourceGuard: ignoring keyword arguments in favour of pre-existing guard', RuntimeWarning, 2)
        return r
    @classmethod
    def clear_cache(cls): audit('asyncutils.altlocks.UniqueResourceGuard.clear_cache'); cls._cache.clear()
class CircuitBreaker:
    State = __import__('enum').IntEnum('State', ('CLOSED', 'HALF_OPEN', 'OPEN'), module=__name__)
    __slots__ = '__exc', '_half_open_calls', '_lock', '_max_fails', '_max_half_open_calls', '_opened', '_reset', '_unlock', 'fails', 'name', 'state'; _inc_cnt = staticmethod(count(1).__next__)
    def __new__(cls, n, /, max_fails=None, reset=None, *, exc=Exception, max_half_open_calls=None, _='#%d'):
        f = None
        if callable(n) and (n := getattr(f := getattr(getattr(n, '__func__', n), '__wrapped__', n), '__qualname__', None)) is None is (n := getattr(f, '__name__', None)): n = _%cls._inc_cnt()
        audit('asyncutils.altlocks.CircuitBreaker', n, max_fails); s, C = super().__new__(cls), A.getcontext(); s.name, s._max_fails, s._reset, s.__exc, s._opened, s._max_half_open_calls, s._unlock, s._lock, s.state = n, C.CIRCUIT_BREAKER_DEFAULT_MAX_FAILS if max_fails is None else max_fails, C.CIRCUIT_BREAKER_DEFAULT_RESET if reset is None else reset, exc, float('-inf'), C.CIRCUIT_BREAKER_DEFAULT_MAX_HALF_OPEN_CALLS if max_half_open_calls is None else max_half_open_calls, Releasing(l := I.Lock()), l, cls.State.CLOSED; s.fails = s._half_open_calls = 0; return s if f is None else s(f)
    def __call__(self, f, /, *, timer=monotonic, default=_NO_DEFAULT):
        audit('asyncutils.altlocks.CircuitBreaker.__call__', self.name, fullname(f))
        async def g(*a, **k):
            C = self.State
            async with self._lock:
                if (s := self.state) == C.OPEN:
                    if timer()-self._opened > self._reset: self.state, self._half_open_calls = C.HALF_OPEN, 0
                    else: raise A.CircuitOpen(f'asyncutils.altlocks.CircuitBreaker: circuit {self.name} is open')
                elif s == C.HALF_OPEN:
                    if (c := self._half_open_calls) == (m := self._max_half_open_calls): raise A.CircuitHalfOpen(f'asyncutils.altlocks.CircuitBreaker: breaker {self.name} exceeded the maximum of {m} calls in the half-open state')
                    self._half_open_calls = c+1
                try:
                    async with self._unlock: r = await f(*a, **k)
                    if s == C.HALF_OPEN: self._half_open_calls = self.fails = 0; self.state = C.CLOSED
                    return r
                except self.__exc:
                    if (x := self.fails+1) < self._max_fails: self.fails = x
                    else: self._opened, self.state, self.fails = timer(), C.OPEN, 0
                    if default is _NO_DEFAULT: raise
                    return default
                except A.CRITICAL: raise A.Critical
                except BaseException as e: raise A.CircuitBreakerError(f'asyncutils.altlocks.CircuitBreaker: unexpected {fullname(e)} in {fullname(f)} under breaker {self.name!r}') from e
        return wraps(f)(g)
    P.patch_classmethod_signatures((__new__, 'name, /, max_fails=None, reset=None, *, exc={}, max_half_open_calls=None'))
class StatefulBarrier(A.AwaitableMixin):
    __slots__ = '__br', '__cd', '__cn', '__exc', '__ist', '__ps', '__st'
    def __init__(self, parties, name='\b', init_state=(), max_state=None): self.__ps, self.__exc, self.__cn, self.__st, self.__cd, self.__ist, self.__br = parties, I.BrokenBarrierError(f'{fullname(self)} {name} is broken'), 0, deque(maxlen=max_state), I.Condition(), init_state, False
    async def _wait(self, x, /):
        self.raise_for_abort(); f = (S := self.__st).append
        if (s := self.__ist) is not None:
            async for i in A.iter_to_agen(s): f(i)
            self.__ist = None
        self.__cn, C = (c := self.__cn)+1, self.__cd
        if x is not None: f(x)
        if c == self.__ps-1: self.__cn = 0; C.notify_all(); self.__br = True
        else:
            w = C.wait
            while not self.__br: await w()
        return c, S.copy()
    async def wait(self, state=None, timeout=None):
        try:
            async with I.timeout(timeout), self.__cd: return await self._wait(state)
        except TimeoutError: await self.abort(); raise
    async def abort(self):
        async with (C := self.__cd):
            if not self.__br: self.__br = True; C.notify_all()
    def raise_for_abort(self):
        if self.__br: raise self.__exc
    @property
    def broken(self): return self.__br
    @property
    def remaining_parties(self): return self.__ps-self.__cn
    @property
    def parties(self): return self.__ps
    @property
    def n_waiting(self): return self.__cn
class DynamicThrottle:
    __slots__ = '_fails', '_jitter', '_lb', '_lc', '_lf', '_lock', '_max', '_min', '_rate', '_rf', '_successes', '_timer', '_ub', '_uf', '_window'
    def __init__(self, init_rate, min_rate=None, max_rate=None, window=None, *, ubound=None, lbound=None, ufactor=None, lfactor=None, jitter=None, timer=monotonic, rand=lambda j, u=_randinst.uniform: u(-j, j)): # noqa: PLR0913
        C = A.getcontext()
        if min_rate is None: min_rate = C.DYNAMIC_THROTTLE_DEFAULT_MIN_RATE
        if max_rate is None: max_rate = C.DYNAMIC_THROTTLE_DEFAULT_MAX_RATE
        if not 0 < min_rate <= init_rate <= max_rate: raise ValueError('asyncutils.altlocks.DynamicThrottle: inconsistent rates after applying bounds')
        self._min, self._max, self._window, self._lock, self._timer, self._ub, self._lb, self._uf, self._lf, self.jitter, self._rf, self._rate, self._lc = min_rate, max_rate, C.DYNAMIC_THROTTLE_DEFAULT_WINDOW if window is None else window, I.Lock(), timer, C.DYNAMIC_THROTTLE_DEFAULT_UBOUND if ubound is None else ubound, C.DYNAMIC_THROTTLE_DEFAULT_LBOUND if lbound is None else lbound, C.DYNAMIC_THROTTLE_DEFAULT_UFACTOR if ufactor is None else ufactor, C.DYNAMIC_THROTTLE_DEFAULT_LFACTOR if lfactor is None else lfactor, C.DYNAMIC_THROTTLE_DEFAULT_JITTER if jitter is None else jitter, rand, init_rate, timer()-1.0/init_rate; self.reset()
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
    async def __aenter__(self): await I.sleep((1.0/self._rate-self.ctime+self._lc)*(1.0+self._rf(self._jitter))); self._lc = self.ctime
    async def __aexit__(self, e, /, *_):
        async with self._lock:
            if (t := (s := self._successes)+self._fails) >= self._window: self.rate *= self._uf if (r := s/t) > self._ub else self._lf if r < self._lb else 1.0; self.reset()
            if e is None: self._successes += 1
            else: self._fails += 1
    def reset(self): self._successes = self._fails = 0
    P.patch_method_signatures((__aexit__, P.exit_sig))
del Resource, _randinst, count, P
