from ._internal.helpers import _get_loop_no_exit, copy_and_clear, pkgpref
from ._internal import log
from .config import RAISE, _NO_DEFAULT, _randinst
from .base import iter_to_aiter
from .util import safe_cancel, _ignore_cancellation
from .exceptions import wrap_exc, CRITICAL, MaxIterationsError
from .constants import getcontext
from time import perf_counter
from functools import wraps
from sys import audit, maxsize as INF
from collections import deque, namedtuple
from asyncio.tasks import sleep, wait_for, eager_task_factory
from asyncio.locks import Lock
from asyncio.exceptions import CancelledError
from asyncio.coroutines import iscoroutine
from ._internal.submodules import func_all as __all__
async def areduce(f, it, initial=_NO_DEFAULT, *, await_=True):
    async for _ in iter_to_aiter(it): initial = _ if initial is _NO_DEFAULT else (await f(initial, _)) if await_ else f(initial, _)
    return initial
def every(intvl, /, *, stop_when=None, count_f=True, verbose=False, stop_on_exc=True, wait_first=False, loop=None, max_iterations=INF, timer=perf_counter, supplied_args=(), supplied_kwargs={}, default=_NO_DEFAULT):
    if loop is None: loop = _get_loop_no_exit()
    def dec(f, /):
        n = f.__name__
        if stop_when and stop_when.done(): log.warning(f'future to stop periodic coroutine {n} is already done')
        async def wrapper(*a, **k):
            log.debug('periodic task started; source: every'); q = default is _NO_DEFAULT; nonlocal stop_when
            if stop_when is None: stop_when = loop.create_future()
            if wait_first: await sleep(intvl)
            for _ in range(max_iterations):
                try: t = timer(); await f(*supplied_args, *a, **supplied_kwargs, **k); t = timer()-t
                except CRITICAL: raise
                except BaseException:
                    if stop_on_exc:
                        if stop_when.done(): return stop_when.result()
                        if verbose: raise
                        break
                    if verbose: log.error(f'error in periodic coroutine {n}', exc_info=True)
                try: return await wait_for(stop_when, intvl-t*count_f)
                except CancelledError:
                    if stop_on_exc:
                        if verbose: raise
                        break
                    if verbose: log.info(f'future to stop periodic coroutine {n} was cancelled')
                    stop_when = loop.create_future()
                except TimeoutError: continue
            else:
                s = f'periodic coroutine {n} reached the maximum of {max_iterations} iterations'
                if stop_on_exc or default is RAISE: raise MaxIterationsError(s)
                if verbose or q: log.info(s)
                else: log.debug(s)
            if not q: return default
        return wraps(f)(wrapper)
    return dec
def everymethod(intvl, /, *, stop_when_getter=None, count_f=True, verbose=False, stop_on_exc=True, wait_first=False, loop=None, max_iterations=INF, timer=perf_counter, supplied_args=(), supplied_kwargs={}, default=_NO_DEFAULT):
    if loop is None: loop = _get_loop_no_exit()
    def dec(f, /):
        n = f.__name__
        async def wrapper(self, /, *a, **k):
            log.debug('periodic task started; source: everymethod'); q = default is _NO_DEFAULT
            if (stop_when := loop.create_future() if stop_when_getter is None else stop_when_getter(self)).done(): log.warning(f'future to stop periodic coroutine {n} is already done')
            if wait_first: await sleep(intvl)
            for _ in range(max_iterations):
                try: t = timer(); await f(self, *supplied_args, *a, **supplied_kwargs, **k); t = timer()-t
                except CRITICAL: raise
                except BaseException:
                    if stop_on_exc:
                        if stop_when.done(): return stop_when.result()
                        if verbose: raise
                        break
                    if verbose: log.error(f'error in periodic coroutine {n}', exc_info=True)
                try: return await wait_for(stop_when, intvl-t*count_f)
                except CancelledError:
                    if stop_on_exc:
                        if verbose: raise
                        break
                    if verbose: log.info(f'future to stop periodic coroutine {n} was cancelled')
                    stop_when = loop.create_future()
                except TimeoutError: continue
            else:
                s = f'periodic coroutine {n} reached the maximum of {max_iterations} iterations'
                if stop_on_exc or default is RAISE: raise MaxIterationsError(s)
                if verbose or q: log.info(s)
            if not q: return default
        return wraps(f)(wrapper)
    return dec
def timer(f, /, *, precision=6, expected=Exception, log=True, timer=perf_counter, ns=False):
    async def wrapper(*a, **k):
        try:
            s = timer(); r = await f(*a, **k); e = timer()-s
            if log: log.info(f'function {f.__qualname__} executed in {e:.{precision}f} {'nano'*ns}seconds.')
            return r, e
        except CRITICAL: raise
        except expected as _:
            e = timer()-s
            if log: log.warning(f'function {f.__qualname__} encountered {type(_).__qualname__}: {_}')
            return wrap_exc(_), e
    return wraps(f)(wrapper)
def retry(tries=None, delay=None, max_delay=None, backoff=None, jitter=None, exc=Exception, on_retry=lambda *_: None, on_success=lambda *_: None, random=_randinst.random):
    C = getcontext()
    if tries is None: tries = C.RETRY_DEFAULT_TRIES
    if delay is None: delay = C.RETRY_DEFAULT_DELAY
    if backoff is None: backoff = C.RETRY_DEFAULT_BACKOFF
    if max_delay is None: max_delay = C.RETRY_DEFAULT_MAX_DELAY
    if jitter is None: jitter = C.RETRY_DEFAULT_JITTER
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
        (L := _get_loop_no_exit()).set_task_factory(eager_task_factory)
        async def wrapper(*a, **k):
            nonlocal l
            if l: await safe_cancel(l)
            l = L.create_task(sleep(wait))
            with _ignore_cancellation: await l; return await f(*a, **k)
        return wraps(f)(wrapper)
    return dec
def rate_limit(calls, period, timer=perf_counter):
    def dec(f):
        async def wrapper(*a, _c_=deque(), _l_=Lock(), **k):
            async with _l_:
                audit(f'{pkgpref}func.rate_limit', f, a, k, calls, period); n, C = timer(), copy_and_clear(_c_)
                for i in C:
                    if i > n-period: _c_.append(i)
                if len(_c_) >= calls: await sleep(period-n+_c_.popleft())
                _c_.append(timer())
            return await f(*a, **k)
        return wraps(f)(wrapper)
    return dec
async def measure(f, timer=perf_counter): s = timer(); return await f(), timer()-s
async def benchmark(f, /, times=1, warmup=0, *, _f=namedtuple('BenchmarkResult', 'min max total avg iterations', module=pkgpref+'func')):
    for _ in range(warmup): await f()
    g = measure.__get__(f); audit(f'{pkgpref}func.benchmark', f, t := [(await g())[1] for _ in range(times)]); return _f(min(t), max(t), (S := sum(t)), S/len(t), times+warmup)