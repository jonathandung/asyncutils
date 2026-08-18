import asyncio as I, asyncutils as A, asyncutils._internal.helpers as H
from functools import partial, wraps
from sys import audit, exc_info
from asyncutils._internal.patch import patch_function_signatures
from asyncutils._internal.submodules import util_all as __all__
def avalify(v):
    async def g(*_a, **_): return v # ruff: ignore[unused-async]
    return g
afalsify, atruthify, anullify = map(avalify, (False, True, None))
anullcontext = object.__new__(type('anullcontext', (), {'__new__': lambda _, /: anullcontext, '__aenter__': anullify, '__aexit__': anullify}))
async def wrap_in_coro(a, /):
    try: return await a
    except A.CRITICAL: raise A.Critical
def done_evt(*, evtcls=I.Event): (E := evtcls()).set(); return E
def done_fut(res=None, *, futcls=I.Future): F = futcls(); F.set_exception(A.unwrap_exc(res)) if A.exception_occurred(res) else F.set_result(res); return F
async def locked_lock(*, lcls=I.Lock): await (l := lcls()).acquire(); return l
def get_future(aw, loop=None): return (H.get_loop_and_set() if loop is None else loop).create_task(wrap_in_coro(aw))
def new_eager_tasks(*aws): (l := H.get_loop_and_set()).set_task_factory(I.eager_task_factory); yield from map(partial(get_future, loop=l), aws)
def transient_block(l, f, /, *a, _callback_=lambda f, c, /: f.set_result(c()), _threadsafe_=False, **k): (l.call_soon_threadsafe if _threadsafe_ else l.call_soon)(_callback_, F := l.create_future(), partial(f, *a, **k)); return F
def transient_block_from_loop(loop, *, threadsafe=False): return partial(transient_block, loop, _threadsafe_=threadsafe)
def sync_await(aw, loop=None, *, never_block=True, timeout=None):
    audit('asyncutils.util.sync_await', H.fullname(aw))
    if loop is None: loop = H.get_loop_and_set()
    return (A.raise_exc(A.Deadlock, 'asyncutils.util.sync_await: cannot await in the current loop without blocking it') if loop is I._get_running_loop() else I.run_coroutine_threadsafe(wrap_in_coro(aw), loop).result(timeout)) if never_block or loop.is_running() else loop.run_until_complete(I.wait_for(I.ensure_future(aw, loop=loop), timeout))
def semaphore(bounded=False, workers=None):
    if workers is None: workers = A.getcontext().SEMAPHORE_DEFAULT_VALUE
    return (I.Lock() if workers == 1 else I.BoundedSemaphore(workers)) if bounded else I.Semaphore(workers)
def lockf(f, /, lf=I.Lock, _lc=__import__('weakref').WeakKeyDictionary()): # ruff: ignore[function-call-in-default-argument]
    if (l := _lc.get(f)) is None: _lc[f] = l = lf()
    async def r(*a, **k):
        async with l: return await f(*a, **k)
    return wraps(f)(r)
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
        if self._aentered: raise RuntimeError('asyncutils.util.dualcontextmanager: context manager already entered asynchronously')
        if self._entered: raise RuntimeError('asyncutils.util.dualcontextmanager: context manager already entered')
        try: self._gen = g = A.aiter_to_gen(self._gen, strict=self._st, use_futures=True); self._entered = True; return next(g)
        except StopIteration: raise RuntimeError("asyncutils.util.dualcontextmanager: generator didn't yield") from None
    def __exit__(self, t, v, b, /):
        if self._aentered: raise RuntimeError('asyncutils.util.dualcontextmanager: cannot exit async context manager synchronously')
        if not self._entered: raise RuntimeError('asyncutils.util.dualcontextmanager: context manager was never entered')
        g = self._gen
        if t is None:
            try: next(g)
            except StopIteration: return False
            try: raise RuntimeError("asyncutils.util.dualcontextmanager: generator didn't stop")
            finally: g.close()
        if v is None: v = t()
        try: g.throw(v)
        except BaseException as e:
            f = e is v
            if isinstance(e, StopIteration): return not f
            if f or (isinstance(e, RuntimeError) and isinstance(v, StopIteration) and e.__cause__ is (e := v)): e.__traceback__ = b; return False
            raise
        try: raise RuntimeError("asyncutils.util.dualcontextmanager: generator didn't stop after throw")
        finally: g.close()
    def __aenter__(self):
        if self._aentered: raise RuntimeError('asyncutils.util.dualcontextmanager: async context manager already entered')
        if self._entered: raise RuntimeError('asyncutils.util.dualcontextmanager: async context manager already entered synchronously')
        try: self._gen = g = A.iter_to_agen(self._gen, strict=self._st, use_existing_executor=self._ue, create_executor=self._ce); self._aentered = True; return anext(g)
        except StopAsyncIteration: raise RuntimeError("asyncutils.util.dualcontextmanager: async generator didn't yield") from None
    async def __aexit__(self, t, v, b, /):
        if self._entered: raise RuntimeError('asyncutils.util.dualcontextmanager: cannot exit sync context manager asynchronously')
        if not self._aentered: raise RuntimeError('asyncutils.util.dualcontextmanager: async context manager was never entered')
        g = self._gen
        if t is None:
            try: await anext(g)
            except StopAsyncIteration: return False
            try: raise RuntimeError("asyncutils.util.dualcontextmanager: async generator didn't stop")
            finally: await g.aclose()
        if v is None: v = t()
        try: await g.athrow(v)
        except BaseException as e:
            f = e is v
            if isinstance(e, StopAsyncIteration): return not f
            if f or (isinstance(e, RuntimeError) and isinstance(v, StopAsyncIteration) and e.__cause__ is (e := v)): e.__traceback__ = b; return False
            raise
        try: raise RuntimeError("asyncutils.util.dualcontextmanager: async generator didn't stop after athrow")
        finally: await g.aclose()
def dualcontextmanager(f=None, /, _=DualContextManager, *, use_existing_executor=None, create_executor=None, strict=None):
    if f is None: return lambda f, /: dualcontextmanager(f, use_existing_executor=use_existing_executor, create_executor=create_executor, strict=strict)
    return wraps(f)(lambda *a, **k: (c := A.getcontext()) and _(f(*a, **k), c.DUAL_CONTEXT_MANAGER_DEFAULT_USE_EXISTING_EXECUTOR if use_existing_executor is None else use_existing_executor, c.DUAL_CONTEXT_MANAGER_DEFAULT_MAY_CREATE_EXECUTOR if create_executor is None else create_executor, c.DUAL_CONTEXT_MANAGER_DEFAULT_STRICT if strict is None else strict))
def aawcmf2dcmff(**d):
    def f(f, /, _=dualcontextmanager(**d)): # ruff: ignore[function-call-in-default-argument]
        async def g(*a, **k):
            c = f(*a, **k)
            with A.ignore_typeerrs: c = await c
            if H.check_methods(c, '__aenter__', '__aexit__'):
                async with c as r: yield r; return # ruff: ignore[yield-in-context-manager-in-async-generator]
            if (e := getattr(aawcmf2dcmff, 'executor', None)) is None: e = H.create_executor(aawcmf2dcmff)
            r = await (h := partial(H.get_loop_and_set().run_in_executor, e))(c.__enter__)
            try: yield r
            finally: await h(c.__exit__, *exc_info())
        return _(g)
    f.__text_signature__ = '(f, /)'; return f # ty: ignore[unresolved-attribute]
def make_task_factory(tcls, eager=None):
    if eager is None: eager = A.getcontext().MAKE_TASK_FACTORY_DEFAULT_EAGER
    return lambda loop, coro, eager_start=eager, **k: tcls(coro, loop=loop, eager_start=eager_start, **k)
dcm, ignore_cancellation = (aawcmf2dcmf := aawcmf2dcmff()).__defaults__[0], A.IgnoreErrors(I.CancelledError)
patch_function_signatures((lockf, 'f, /, lf={}'), (dualcontextmanager, 'f=None, /, *, use_existing_executor=None, create_executor=None, strict=None'))
del DualContextManager
