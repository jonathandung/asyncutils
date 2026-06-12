# ty: ignore[unresolved-attribute]
__lazy_modules__ = frozenset(('functools',))
from asyncutils.config import _randinst
from asyncutils.constants import _NO_DEFAULT
from asyncutils._internal import log, patch as P
from asyncutils._internal.helpers import fullname, get_loop_and_set
from asyncutils._internal.submodules import func_all as __all__
import asyncio as I, asyncutils as A
from collections import deque, namedtuple
from functools import partial, update_wrapper, wraps
from itertools import count, repeat
from sys import audit
from time import perf_counter
def acompose(*F, wrap_last=True, _=I.iscoroutine):
    async def g(*a, **k):
        if _(r := next(i := reversed(F))(*a, **k)): r = await r
        for f in i:
            if _(r := f(r)): r = await r
        return r
    if wrap_last: update_wrapper(g, F[-1])
    return g
async def areduce(f, it, initial=_NO_DEFAULT, *, await_=True):
    async for _ in A.iter_to_agen(it): initial = _ if initial is _NO_DEFAULT else (await f(initial, _)) if await_ else f(initial, _)
    return initial
def star(f, /):
    async def g(a=(), k=None, /): return await f(*a, **(k or {}))
    return wraps(f)(g)
def unstar(f, /):
    async def g(*a, **k): return await f(a, k)
    return wraps(f)(g)
def every(intvl, /, *, stop_when=None, count_f=True, verbose=False, stop_on_exc=True, wait_first=False, loop=None, max_iterations=None, timer=perf_counter, supplied_args=(), supplied_kwargs=None, default=_NO_DEFAULT, default_fname='<name unknown>', _='func.every: periodic coroutine %s reached the maximum of %d iterations'):
    if loop is None: loop = get_loop_and_set()
    def dec(f, /):
        n = getattr(f, '__qualname__', default_fname)
        if stop_when and stop_when.done(): log.warning('func.every: future to stop periodic coroutine %s is already done', n)
        async def g(*a, **k):
            log.debug('func.every: periodic task started'); q = default is _NO_DEFAULT; nonlocal stop_when
            if stop_when is None: stop_when = loop.create_future()
            if wait_first: await I.sleep(intvl)
            for i in count() if max_iterations is None else range(max_iterations):
                t = timer()
                try: await f(*supplied_args, *a, **(supplied_kwargs or {}), **k)
                except A.CRITICAL: raise A.Critical
                except:
                    if stop_on_exc:
                        if stop_when.done(): return stop_when.result()
                        break
                    (log.error if verbose else log.warning)('func.every: error in periodic coroutine %s on iteration %d', n, i, exc_info=True)
                try: return await I.wait_for(stop_when, intvl+t-timer() if count_f else intvl)
                except I.CancelledError:
                    if stop_on_exc: break
                    (log.info if verbose else log.debug)('func.every: future to stop periodic coroutine %s was cancelled on iteration %d', n, i, exc_info=True); stop_when = loop.create_future()
                except TimeoutError: continue
            else:
                T = n, max_iterations
                if stop_on_exc or default is A.RAISE: raise A.MaxIterationsError(_%T)
                (log.info if verbose or q else log.debug)(_, *T)
            if not q: return default
        return wraps(f)(g)
    return dec
def everymethod(intvl, /, *, stop_when_getter=None, count_f=True, verbose=False, stop_on_exc=True, wait_first=False, loop=None, max_iterations=None, timer=perf_counter, supplied_args=(), supplied_kwargs=None, default=_NO_DEFAULT, default_fname='<name unknown>', _='func.everymethod: periodic coroutine %s reached the maximum of %d iterations'):
    if loop is None: loop = get_loop_and_set()
    def dec(f, /):
        n = getattr(f, '__qualname__', default_fname)
        async def g(self, /, *a, **k):
            log.debug('func.everymethod: periodic task started'); q = default is _NO_DEFAULT
            if (stop_when := loop.create_future() if stop_when_getter is None else stop_when_getter(self)).done(): log.warning('func.everymethod: future to stop periodic coroutine %s is already done', n)
            if wait_first: await I.sleep(intvl)
            for i in count() if max_iterations is None else range(max_iterations):
                t = timer()
                try: await f(self, *supplied_args, *a, **(supplied_kwargs or {}), **k)
                except A.CRITICAL: raise A.Critical
                except:
                    if stop_on_exc:
                        if stop_when.done(): return stop_when.result()
                        break
                    (log.error if verbose else log.warning)('func.everymethod: error in periodic coroutine %s on iteration %d', n, i, exc_info=True)
                try: return await I.wait_for(stop_when, intvl+t-timer() if count_f else intvl)
                except I.CancelledError:
                    if stop_on_exc: break
                    (log.info if verbose else log.debug)('func.everymethod: future to stop periodic coroutine %s was cancelled on iteration %d', n, i, exc_info=True); stop_when = loop.create_future()
                except TimeoutError: continue
            else:
                T = n, max_iterations
                if stop_on_exc or default is A.RAISE: raise A.MaxIterationsError(_%T)
                (log.info if verbose or q else log.debug)(_, *T)
            if not q: return default
        return wraps(f)(g)
    return dec
def timer(f, /, *, precision=None, expected=Exception, should_log=True, timer=perf_counter, ns=False, _='nano', c='func.timer: function %s finished in %.*f %sseconds.', d='func.timer: received expected error from function %s after %.*f %sseconds: %s'):
    if precision is None: precision = A.getcontext().TIMER_DEFAULT_PRECISION-ns*9
    async def g(*a, **k):
        s = timer()
        try:
            r = await f(*a, **k); e = timer()-s
            if should_log: log.info(c, fullname(f), precision, e, _ if ns else '')
            return r, e
        except A.CRITICAL: raise A.Critical
        except expected as b:
            e = timer()-s
            if should_log: log.warning(d, fullname(f), precision, e, _ if ns else '', b, exc_info=True)
            return A.wrap_exc(b), e
    return wraps(f)(g)
def retry(tries=None, delay=None, *, max_delay=None, backoff=None, jitter=None, exc=Exception, on_retry=(_ := lambda *_: None), on_success=_, random=_randinst.random):
    c = A.getcontext()
    if tries is None: tries = c.RETRY_DEFAULT_TRIES
    if delay is None: delay = c.RETRY_DEFAULT_DELAY
    if backoff is None: backoff = c.RETRY_DEFAULT_BACKOFF
    if max_delay is None: max_delay = c.RETRY_DEFAULT_MAX_DELAY
    if jitter is None: jitter = c.RETRY_DEFAULT_JITTER
    def dec(f):
        async def g(*a, **k):
            c, l, b = 0, 0.0, 1
            for i in range(tries-1):
                try: r = await f(*a, **k)
                except exc as e:
                    c += 1
                    if I.iscoroutine(t := on_retry(i, e)): await t
                    await I.sleep(l := min(max(delay*b+(c*delay)*(1+(random()*2-1)*jitter), delay), max_delay)); b *= backoff
                else:
                    if I.iscoroutine(t := on_success(i, l)): await t
                    return r
            return await f(*a, **k)
        return wraps(f)(g)
    return dec
def throttle(lim, timer=perf_counter):
    l = 0.0
    def dec(f, /):
        async def g(*a, **k):
            nonlocal l
            if w := max(0, 1/lim-timer()+l): await I.sleep(w)
            l = timer(); return await f(*a, **k)
        return wraps(f)(g)
    return dec
def debounce(wait):
    def dec(f, /, l=None):
        (L := get_loop_and_set()).set_task_factory(I.eager_task_factory); g, h = L.create_task, I.sleep.__get__(wait)
        async def j(*a, **k):
            nonlocal l
            if l: await A.safe_cancel(l)
            l = g(h())
            with A.ignore_cancellation: await l; return await f(*a, **k)
        return wraps(f)(j)
    return dec
def iterf(n, /):
    def dec(f, /):
        async def g(x, /):
            for _ in repeat(None, n): x = await f(x)
            return x
        return wraps(f)(g)
    return dec
async def measure(f, /, *, timer=perf_counter): s = timer(); return await f(), timer()-s
async def measure2(f, /, **k): return (await measure(f, **k))[1]
async def benchmark(f, /, times=None, warmup=None, _f=namedtuple('BenchmarkResult', 'min max total avg iterations', module='asyncutils.func'), *, sequential=None):
    c, g = A.getcontext(), measure2.__get__(f)
    if sequential is None: sequential = c.BENCHMARK_DEFAULT_SEQUENTIAL
    if times is None: times = c.BENCHMARK_DEFAULT_TIMES
    if warmup is None: warmup = c.BENCHMARK_DEFAULT_WARMUP
    if sequential:
        for _ in repeat(None, warmup): await f()
    else: await I.gather(*(f() for _ in repeat(None, warmup)))
    audit('asyncutils.func.benchmark', fullname(f), T := times+warmup); return _f(min(t := [await g() for _ in repeat(None, times)] if sequential else await I.gather(*(g() for _ in repeat(None, times)))), max(t), S := sum(t), S/times, T)
P.patch_function_signatures((measure, _ := 'f, /, *, timer={}'), (measure, _), (benchmark, 'f, /, times=None, warmup=None'))
class RateLimited:
    __slots__ = '_call_times', '_calls', '_func', '_lock', '_period', '_raise', '_timer'
    def __new__(cls, f, /, calls, period=None, *, raise_=False, timer=perf_counter, lock_impl=None):
        if period is None: return partial(cls, calls=f, period=calls, raise_=raise_, timer=timer, lock_impl=lock_impl)
        audit('asyncutils.func.RateLimited', fullname(f), calls, period); (_ := super().__new__(cls))._func, _._period, _._call_times, _._lock, _._calls, _._raise, _._timer = f, float(period), deque(), (I.Lock if lock_impl is None else lock_impl)(), int(calls), raise_, timer; return _
    async def __call__(self, *a, **k):
        p, m, P, C, f = (T := self._call_times).popleft, T.appendleft, self._period, self._calls, self._func
        async with self._lock:
            d = (n := self._timer())-P
            while T:
                if (x := p()) > d: m(x); break
            if (l := len(T)-self._calls+1) > 0:
                if self._raise: raise A.RateLimitExceeded(f, a, k, C, P, l)
                await I.sleep(p()-d)
            T.append(n)
        return await f(*a, **k)
    def __repr__(self): return f'{fullname(self)}({self._func!r}, {self._calls}, {self._period:.6f}, raise_={self._raise}, timer={self._timer!r}, lock_impl={fullname(self._lock)})'
    P.patch_classmethod_signatures((__new__, 'f, /, calls, period=None, *, raise_=False, timer={}, lock_impl=None'))
del _, perf_counter, P
