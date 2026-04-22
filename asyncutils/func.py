from ._internal import log
from ._internal.helpers import fullname, get_loop_and_set
from ._internal.submodules import func_all as __all__
from . import context as C
from .base import iter_to_aiter
from .config import _randinst
from .constants import _NO_DEFAULT, RAISE
from .exceptions import CRITICAL, Critical, MaxIterationsError, RateLimitExceeded, wrap_exc
from .util import ignore_cancellation, safe_cancel
from asyncio.coroutines import iscoroutine
from asyncio.exceptions import CancelledError
from asyncio.locks import Lock
from asyncio.tasks import eager_task_factory, sleep, wait_for
from collections import deque, namedtuple
from functools import partial, wraps
from sys import audit, maxsize as I
from time import perf_counter
async def areduce(f, it, initial=_NO_DEFAULT, *, await_=True):
    async for _ in iter_to_aiter(it): initial = _ if initial is _NO_DEFAULT else (await f(initial, _)) if await_ else f(initial, _)
    return initial
def star(f, /):
    async def wrapper(a=(), k=None, /): return await f(*a, **(k or {}))
    return wraps(f)(wrapper)
def unstar(f, /):
    async def wrapper(*a, **k): return await f(a, k)
    return wraps(f)(wrapper)
def every(intvl, /, *, stop_when=None, count_f=True, verbose=False, stop_on_exc=True, wait_first=False, loop=None, max_iterations=I, timer=perf_counter, supplied_args=(), supplied_kwargs=None, default=_NO_DEFAULT, s='periodic coroutine %s reached the maximum of %d iterations'):
    if loop is None: loop = get_loop_and_set()
    def dec(f, /):
        n = getattr(f, '__qualname__', '<name unknown>')
        if stop_when and stop_when.done(): log.warning('every: future to stop periodic coroutine %s is already done', n)
        async def wrapper(*a, **k):
            log.debug('every: periodic task started'); q = default is _NO_DEFAULT; nonlocal stop_when
            if stop_when is None: stop_when = loop.create_future()
            if wait_first: await sleep(intvl)
            for _ in range(max_iterations):
                t = timer()
                try: await f(*supplied_args, *a, **(supplied_kwargs or {}), **k)
                except CRITICAL: raise Critical
                except BaseException:
                    if stop_on_exc:
                        if stop_when.done(): return stop_when.result()
                        if verbose: raise
                        break
                    (log.error if verbose else log.warning)('every: error in periodic coroutine %s on iteration %d', n, _, exc_info=True)
                try: return await wait_for(stop_when, intvl+t-timer() if count_f else intvl)
                except CancelledError:
                    if stop_on_exc:
                        if verbose: raise
                        break
                    (log.info if verbose else log.debug)('every: future to stop periodic coroutine %s was cancelled on iteration %d', n, _, exc_info=True); stop_when = loop.create_future()
                except TimeoutError: continue
            else:
                T = n, max_iterations
                if stop_on_exc or default is RAISE: raise MaxIterationsError(s%T)
                (log.info if verbose or q else log.debug)(s, *T)
            if not q: return default
        return wraps(f)(wrapper)
    return dec
def everymethod(intvl, /, *, stop_when_getter=None, count_f=True, verbose=False, stop_on_exc=True, wait_first=False, loop=None, max_iterations=I, timer=perf_counter, supplied_args=(), supplied_kwargs=None, default=_NO_DEFAULT, s='everymethod: periodic coroutine %s reached the maximum of %d iterations'):
    if loop is None: loop = get_loop_and_set()
    def dec(f, /):
        n = getattr(f, '__qualname__', '<name unknown>')
        async def wrapper(self, /, *a, **k):
            log.debug('everymethod: periodic task started'); q = default is _NO_DEFAULT
            if (stop_when := loop.create_future() if stop_when_getter is None else stop_when_getter(self)).done(): log.warning('everymethod: future to stop periodic coroutine %s is already done', n)
            if wait_first: await sleep(intvl)
            for _ in range(max_iterations):
                t = timer()
                try: await f(self, *supplied_args, *a, **(supplied_kwargs or {}), **k)
                except CRITICAL: raise Critical
                except: # noqa: E722
                    if stop_on_exc:
                        if stop_when.done(): return stop_when.result()
                        if verbose: raise
                        break
                    (log.error if verbose else log.warning)('everymethod: error in periodic coroutine %s on iteration %d', n, _, exc_info=True)
                try: return await wait_for(stop_when, intvl+t-timer() if count_f else intvl)
                except CancelledError:
                    if stop_on_exc:
                        if verbose: raise
                        break
                    (log.info if verbose else log.debug)('everymethod: future to stop periodic coroutine %s was cancelled on iteration %d', n, _, exc_info=True); stop_when = loop.create_future()
                except TimeoutError: continue
            else:
                T = n, max_iterations
                if stop_on_exc or default is RAISE: raise MaxIterationsError(s%T)
                (log.info if verbose or q else log.debug)(s, *T)
            if not q: return default
        return wraps(f)(wrapper)
    return dec
def timer(f, /, *, precision=None, expected=Exception, should_log=True, timer=perf_counter, ns=False):
    if precision is None: precision = C.TIMER_DEFAULT_PRECISION-ns*9
    async def wrapper(*a, **k):
        s = timer()
        try:
            r = await f(*a, **k); e = timer()-s
            if should_log: log.info('function %s executed in %.*f %sseconds.', fullname(f), precision, e, 'nano'*ns)
            return r, e
        except CRITICAL: raise Critical
        except expected as _:
            e = timer()-s
            if should_log: log.warning('function %s encountered %s after %.*f %sseconds: %s', fullname(f), fullname(type(_)), precision, e, 'nano'*ns, _)
            return wrap_exc(_), e
    return wraps(f)(wrapper)
def retry(tries=None, delay=None, *, max_delay=None, backoff=None, jitter=None, exc=Exception, on_retry=(_ := lambda *_: None), on_success=_, random=_randinst.random):
    c = C.getcontext()
    if tries is None: tries = c.RETRY_DEFAULT_TRIES
    if delay is None: delay = c.RETRY_DEFAULT_DELAY
    if backoff is None: backoff = c.RETRY_DEFAULT_BACKOFF
    if max_delay is None: max_delay = c.RETRY_DEFAULT_MAX_DELAY
    if jitter is None: jitter = c.RETRY_DEFAULT_JITTER
    def dec(f):
        async def wrapper(*a, **k):
            c, l, b = 0, 0.0, 1
            for i in range(tries-1):
                try: r = await f(*a, **k)
                except exc as e:
                    c += 1
                    if iscoroutine(t := on_retry(i, e)): await t
                    await sleep(l := min(max(delay*b+(c*delay)*(1+(random()*2-1)*jitter), delay), max_delay)); b *= backoff
                else:
                    if iscoroutine(t := on_success(i, l)): await t
                    return r
            return await f(*a, **k)
        return wraps(f)(wrapper)
    return dec
def throttle(lim, timer=perf_counter):
    l = 0.0
    def dec(f, /):
        async def wrapper(*a, **k):
            nonlocal l
            if w := max(0, 1/lim-timer()+l): await sleep(w)
            l = timer(); return await f(*a, **k)
        return wraps(f)(wrapper)
    return dec
def debounce(wait):
    def dec(f, l=None):
        (L := get_loop_and_set()).set_task_factory(eager_task_factory); g, h = L.create_task, sleep.__get__(wait)
        async def wrapper(*a, **k):
            nonlocal l
            if l: await safe_cancel(l)
            l = g(h())
            with ignore_cancellation: await l; return await f(*a, **k)
        return wraps(f)(wrapper)
    return dec
async def measure(f, timer=perf_counter): s = timer(); return await f(), timer()-s
async def benchmark(f, /, times=None, warmup=None, *, _f=namedtuple('BenchmarkResult', 'min max total avg iterations', module='asyncutils.func')):
    c = C.getcontext()
    if times is None: times = c.BENCHMARK_DEFAULT_TIMES
    if warmup is None: warmup = c.BENCHMARK_DEFAULT_WARMUP
    for _ in range(warmup): await f()
    g = measure.__get__(f); audit('asyncutils.func.benchmark', fullname(f), T := times+warmup); return _f(min(t := [(await g())[1] for _ in range(times)]), max(t), S := sum(t), S/times, T)
class RateLimited:
    __slots__ = '_call_times', '_calls', '_func', '_lock', '_period', '_raise', '_timer'
    def __new__(cls, f, calls, period=None, *, raise_=False, timer=perf_counter, lock_impl=Lock, _=partial):
        if period is None: return _(cls, calls=f, period=calls, raise_=raise_, timer=timer)
        audit('asyncutils.func.RateLimited', fullname(f), calls, period); (_ := super().__new__(cls))._func, _._period, _._call_times, _._lock, _._calls, _._raise, _._timer = f, float(period), deque(), lock_impl(), int(calls), raise_, timer; return _
    async def __call__(self, *a, **k):
        p, A, P, C, f = (T := self._call_times).popleft, T.appendleft, self._period, self._calls, self._func
        async with self._lock: # type: ignore
            d = (n := self._timer())-P
            while T:
                if (x := p()) > d: A(x); break
            if (l := len(T)-self._calls+1) > 0:
                if self._raise: raise RateLimitExceeded(f, a, k, C, P, l)
                await sleep(p()-d)
            T.append(n)
        return await f(*a, **k)
    def __repr__(self): return f'{fullname(self)}({self._func!r}, {self._calls}, {self._period:.6f}, raise_={self._raise}, timer={self._timer!r})'
del _, I, perf_counter, partial, Lock