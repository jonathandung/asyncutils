from ._internal.helpers import check_methods, get_loop_and_set, stop_and_closer, fullname
from ._internal.running_console import _get_
from ._internal.submodules import util_all as __all__
from .config import Executor
from .constants import _NO_DEFAULT, SYNC_AWAIT
from .exceptions import CRITICAL, Critical, Deadlock, IgnoreErrors
from asyncio.coroutines import iscoroutine
from asyncio.events import _get_running_loop, new_event_loop, set_event_loop
from asyncio.locks import BoundedSemaphore, Lock, Semaphore
from asyncio.tasks import eager_task_factory, ensure_future, run_coroutine_threadsafe, wait_for
from asyncio.timeouts import timeout as _timeout
from functools import partial, wraps
from sys import audit
_ignore_cancellation = IgnoreErrors(__import__('asyncio.exceptions', fromlist=('',)).CancelledError)
def get_future(aw, loop=None):
    if loop is None: loop = get_loop_and_set()
    async def wrapper():
        try: return await aw
        except CRITICAL: raise Critical
    return loop.create_task(wrapper())
def new_tasks(*C): (l := get_loop_and_set()).set_task_factory(eager_task_factory); yield from map(l.create_task, C)
def to_sync(f, /, timeout=None, loop=None): audit('asyncutils.util.to_sync', fullname(f)); return wraps(f)(lambda *a, **k: sync_await(f(*a, **k), timeout=timeout, loop=loop))
def to_sync_from_loop(loop): return partial(to_sync, loop=loop)
def sync_await(aw, *, timeout=None, loop=None, _='_thread_id'):
    audit('asyncutils.util.sync_await', fullname(aw)); f = loop is None
    if (c := _get_()) and (f or loop is (l := c._loop) or getattr(loop, _, None) == getattr(l, _, NotImplemented)): raise Deadlock('cannot call sync_await within console; use the await statement directly instead', noticer=SYNC_AWAIT) # type: ignore
    if loop is (loop := _get_running_loop()):
        if f: loop = new_event_loop(); set_event_loop(loop)
        try: return loop.run_until_complete(wait_for(ensure_future(aw, loop=loop), timeout))
        finally:
            if f: loop.stop(); loop.close(); set_event_loop(None)
    async def wrapper(): return await aw
    return run_coroutine_threadsafe(wrapper(), loop).result(timeout)
def semaphore(bounded=False, workers=4): return (BoundedSemaphore if bounded else Semaphore)(workers)
def lockf(f, /, lf=Lock, _lc={}): # noqa: B006
    if (l := _lc.get(i := id(f))) is None: _lc[i] = l = lf()
    async def wrapped(*a, **k):
        async with l: return await f(*a, **k)
    wrapped.__del__ = partial(_lc.pop, i, None); return wraps(f)(wrapped)
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
        if (e := getattr(to_async, 'executor', None)) is None: audit('asyncutils/create_executor', 'util.to_async'); to_async.executor = e = Executor()
        return await loop.run_in_executor(e, partial(f, *a, **k))
    return wraps(f)(wrapper), stop_and_closer(loop)
async def aiter_from_f(f, s=_NO_DEFAULT, /):
    while True:
        if (r := await f()) is s or r == s: break
        yield r
async def safe_cancel(t):
    if not t.done(): t.cancel()
    with _ignore_cancellation: await t