from .base import event_loop, aiter_to_iter, collect, safe_cancel_batch
from .util import safe_cancel, new_tasks
from .exceptions import CRITICAL, Critical
from ._internal import helpers as H
from ._internal.log import debug as _
from asyncio.futures import wrap_future
from asyncio.tasks import wait, wait_for
from asyncio.coroutines import iscoroutine
from asyncio.staggered import staggered_race
from sys import audit, exc_info
from ._internal.submodules import compete_all as __all__
f = H.pkgpref.__add__
async def first_completed(*C, ret_exc=False, loop=None, ename=f('compete.first_completed')):
    audit(ename, C); c = None
    if loop is None: loop = (c := event_loop.from_flags(0)).__enter__()
    try:
        for _ in (await wait(t := tuple(loop.create_task(c) for c in C), return_when='FIRST_COMPLETED'))[0]: return e if ret_exc and (e := _.exception()) else _.result()
    finally:
        if c: c.__exit__(*exc_info())
        await safe_cancel_batch(t)
async def race(*C, timeout=None, loop=None, _=_):
    _('race started'); c = None
    if loop is None: loop = (c := event_loop.from_flags(0)).__enter__()
    try: return await wait_for(t := loop.create_task(first_completed(*C, loop=loop)), timeout)
    finally:
        if c: c.__exit__(*exc_info())
        _('race ended'); await safe_cancel(t)
async def race_with_callback(*C, winner=None, loser=None, timeout=None, ename=f('compete.race_with_callback')):
    if not C: raise TypeError('pass in at least one coroutine to race_with_callback')
    audit(ename, C); d, p = await wait(_ := tuple(new_tasks(*C)), return_when='FIRST_COMPLETED', timeout=timeout)
    if not d: return
    try:
        w = d.pop().result()
        if winner: await winner(w)
        for t in p:
            t.cancel()
            if loser:
                try: await t
                except CRITICAL: raise Critical
                except BaseException as e: await loser(e)
        return w
    finally: await safe_cancel_batch(_)
def convert_to_coro_iter(cfs, skip_invalid=True, corocheck=iscoroutine, futwrap=wrap_future, handle_aiter=collect, handle_iter=collect, _c=H._check_methods):
    for i in aiter_to_iter(cfs):
        if corocheck(i): yield i; continue
        try: i = futwrap(i)
        except CRITICAL: raise Critical
        except AssertionError, TypeError:
            if not _c(i, '__await__'):
                if _c(i, '__aiter__'): yield handle_aiter(i)
                elif _c(i, '__iter__'): yield handle_iter(i)
                elif not skip_invalid: raise TypeError(f'invalid item in {cfs!r}: {i!r}') from None
                continue
        async def wrapper(): return await i
        yield wrapper()
def enhanced_staggered_race(cfs, delay, *, loop=None): return staggered_race(map(lambda c: lambda: c, convert_to_coro_iter(cfs)), delay, loop=loop)
del H, f, _