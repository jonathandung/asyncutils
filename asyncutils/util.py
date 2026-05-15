__lazy_modules__ = frozenset(('asyncutils._internal.running_console', 'functools'))
from asyncutils import CRITICAL, Critical, IgnoreErrors, ignore_typeerrs, aiter_to_gen, getcontext, iter_to_agen
from asyncutils.constants import _NO_DEFAULT
from asyncutils._internal.helpers import check_methods, create_executor, get_loop_and_set, fullname
from asyncutils._internal.patch import patch_function_signatures
from asyncutils._internal.submodules import util_all as __all__
from asyncio import BoundedSemaphore, CancelledError, Event, Lock, Semaphore, eager_task_factory, ensure_future, iscoroutine, run_coroutine_threadsafe, timeout as _timeout, wait_for
from functools import partial, wraps
from sys import audit, exc_info
from weakref import WeakKeyDictionary
ignore_cancellation = IgnoreErrors(CancelledError)
class anullcontext: # noqa: N801
    async def __aenter__(self): ...
    async def __aexit__(*_): ...
async def wrap_in_coro(aw, /):
    try: return await aw
    except CRITICAL: raise Critical
def done_evt(*, evtcls=Event): (E := evtcls()).set(); return E
def get_future(aw, loop=None): return (get_loop_and_set() if loop is None else loop).create_task(wrap_in_coro(aw))
def new_eager_tasks(*aws): (l := get_loop_and_set()).set_task_factory(eager_task_factory); yield from map(partial(get_future, loop=l), aws)
def to_sync(f, /, timeout=None, loop=None): audit('asyncutils.util.to_sync', fullname(f)); return wraps(f)(lambda *a, **k: sync_await(f(*a, **k), timeout=timeout, loop=loop))
def to_sync_from_loop(loop): return partial(to_sync, loop=loop)
def _set_call(F, f, /): F.set_result(f())
def transient_block(l, f, /, *a, _threadsafe_=False, **k): (l.call_soon_threadsafe if _threadsafe_ else l.call_soon)(_set_call, F := l.create_future(), partial(f, *a, **k)); return F
def transient_block_from_loop(loop, *, threadsafe=False): return partial(transient_block, loop, _threadsafe_=threadsafe)
def sync_await(aw, *, timeout=None, loop=None, _='_thread_id'):
    audit('asyncutils.util.sync_await', fullname(aw))
    if loop is None: loop = get_loop_and_set()
    return run_coroutine_threadsafe(wrap_in_coro(aw), loop).result(timeout) if loop.is_running() else loop.run_until_complete(wait_for(ensure_future(aw, loop=loop), timeout))
def semaphore(bounded=False, workers=None): return (BoundedSemaphore if bounded else Semaphore)(getcontext().SEMAPHORE_DEFAULT_VALUE if workers is None else workers)
def lockf(f, /, lf=Lock, _lc=WeakKeyDictionary()): # noqa: B008
    if (l := _lc.get(f)) is None: _lc[f] = l = lf()
    async def wrapped(*a, **k):
        async with l: return await f(*a, **k)
    return wraps(f)(wrapped)
def sync_lock(l, /, timeout=None):
    if not check_methods(l, 'acquire', 'release', 'locked'): raise TypeError('acquire, release and locked methods are required')
    def dec(f):
        async def wrapper(*a, **k):
            try:
                async with _timeout(timeout): await l.acquire(); return f(*a, **k)
            finally:
                if l.locked() and iscoroutine(r := l.release()): await r
        return wraps(f)(to_sync(wrapper))
    return dec
def sync_lock_from_binder(f, /, timeout=None):
    def dec(m, /):
        async def wrapper(self, *a, **k):
            if not check_methods(l := f(self), 'acquire', 'release', 'locked'): raise TypeError('acquire, release and locked methods are required')
            try:
                async with _timeout(timeout): await l.acquire(); return m(self, *a, **k)
            finally:
                if l and l.locked() and iscoroutine(l := l.release()): await l
        return wraps(m)(to_sync(wrapper))
    return dec
def to_async(f, /, loop=None):
    audit('asyncutils.util.to_async', fullname(f))
    if loop is None: loop = get_loop_and_set()
    async def wrapper(*a, **k):
        if (e := getattr(to_async, 'executor', None)) is None: e = create_executor(to_async)
        return await loop.run_in_executor(e, partial(f, *a, **k))
    return wraps(f)(wrapper)
async def aiter_from_f(f, s=_NO_DEFAULT, /):
    while True:
        if (r := await f()) is s or r == s: break
        yield r
async def safe_cancel(t, /):
    F = t.get_loop().create_future()
    def f(_):
        if not F.done(): F.set_result(None)
    t.add_done_callback(f)
    if not t.done(): t.cancel()
    try: await F
    finally: t.remove_done_callback(f)
class DualContextManager:
    __slots__ = '_aentered', '_ce', '_entered', '_gen', '_st', '_ue'
    def __init__(self, /, *_): self._gen, self._ce, self._ue, self._st = _; self._entered = self._aentered = False
    def __enter__(self):
        if self._aentered: raise RuntimeError('context manager already entered asynchronously')
        if self._entered: raise RuntimeError('context manager already entered')
        try: self._gen = g = aiter_to_gen(self._gen, strict=self._st, use_futures=True); self._entered = True; return next(g)
        except StopIteration: raise RuntimeError("generator didn't yield") from None
    def __exit__(self, t, v, b, /):
        if self._aentered: raise RuntimeError('cannot exit async context manager synchronously')
        if not self._entered: raise RuntimeError('context manager was never entered')
        g = self._gen
        if t is None:
            try: next(g)
            except StopIteration: return False
            try: raise RuntimeError("generator didn't stop")
            finally: g.close()
        if v is None: v = t()
        try: g.throw(v)
        except BaseException as e:
            f = e is v
            if isinstance(e, StopIteration): return not f
            if f or (isinstance(e, RuntimeError) and isinstance(v, StopIteration) and e.__cause__ is (e := v)): e.__traceback__ = b; return False
            raise
        try: raise RuntimeError("generator didn't stop after throw")
        finally: g.close()
    def __aenter__(self):
        if self._aentered: raise RuntimeError('async context manager already entered')
        if self._entered: raise RuntimeError('async context manager already entered synchronously')
        try: self._gen = g = iter_to_agen(self._gen, strict=self._st, use_existing_executor=self._ue, create_executor=self._ce); self._aentered = True; return anext(g)
        except StopAsyncIteration: raise RuntimeError("async generator didn't yield") from None
    async def __aexit__(self, t, v, b, /):
        if self._entered: raise RuntimeError('cannot exit sync context manager asynchronously')
        if not self._aentered: raise RuntimeError('async context manager was never entered')
        g = self._gen
        if t is None:
            try: await anext(g)
            except StopAsyncIteration: return False
            try: raise RuntimeError("async generator didn't stop")
            finally: await g.aclose()
        if v is None: v = t()
        try: await g.athrow(v)
        except BaseException as e:
            f = e is v
            if isinstance(e, StopAsyncIteration): return not f
            if f or (isinstance(e, RuntimeError) and isinstance(v, StopAsyncIteration) and e.__cause__ is (e := v)): e.__traceback__ = b; return False
            raise
        try: raise RuntimeError("async generator didn't stop after athrow")
        finally: await g.aclose()
def dualcontextmanager(f=None, /, _=DualContextManager, *, use_existing_executor=None, create_executor=None, strict=None):
    if f is None: return lambda f, /: dualcontextmanager(f, use_existing_executor=use_existing_executor, create_executor=create_executor, strict=strict)
    return wraps(f)(lambda *a, **k: _(f(*a, **k), getcontext().DUAL_CONTEXT_MANAGER_DEFAULT_USE_EXISTING_EXECUTOR if use_existing_executor is None else use_existing_executor, getcontext().DUAL_CONTEXT_MANAGER_DEFAULT_MAY_CREATE_EXECUTOR if create_executor is None else create_executor, getcontext().DUAL_CONTEXT_MANAGER_DEFAULT_STRICT if strict is None else strict))
def aawcmf2dcmff(**d):
    def f(f, /, _=dualcontextmanager(**d)): # noqa: B008
        async def g(*a, **k):
            c = f(*a, **k)
            with ignore_typeerrs: c = await c
            if check_methods(c, '__aenter__', '__aexit__'):
                async with c as r: yield r; return
            if (e := getattr(aawcmf2dcmff, 'executor', None)) is None: e = create_executor(aawcmf2dcmff)
            r = await (h := partial(get_loop_and_set().run_in_executor, e))(c.__enter__())
            try: yield r
            finally: await h(c.__exit__, *exc_info())
        return _(g)
    return f
aawcmf2dcmf = aawcmf2dcmff()
patch_function_signatures((lockf, 'f, /, lf={}'), (sync_await, 'aw, *, timeout=None, loop=None'), (dualcontextmanager, 'f=None, /, *, use_existing_executor=None, create_executor=None, strict=None'))
del DualContextManager