from .base import event_loop, aiter_to_iter, safe_cancel_batch
from .util import new_tasks
from .exceptions import CRITICAL, Critical
from ._internal import helpers as H
from sys import audit, exc_info
from ._internal.submodules import compete_all as __all__
from asyncio.staggered import staggered_race
import asyncio as A
async def first_completed(*C, ret_exc=False, timeout=None, loop=None, _=A.timeout):
    audit('asyncutils.compete.first_completed/start', C); c = None
    if loop is None: loop = (c := event_loop.from_flags(0)).__enter__()
    try:
        async with _(timeout):
            for _ in (await A.wait(t := tuple(loop.create_task(c) for c in C), return_when='FIRST_COMPLETED'))[0]: return e if ret_exc and (e := _.exception()) else _.result()
    finally:
        if c: c.__exit__(*exc_info()) # type: ignore
        audit('asyncutils.compete.first_completed/end', C); await safe_cancel_batch(t)
async def race_with_callback(*C, winner=None, loser=None, timeout=None):
    if not C: raise TypeError('pass in at least one coroutine to race_with_callback')
    audit('asyncutils.compete.race_with_callback/start', C); d, p = await A.wait(new_tasks(*C), return_when='FIRST_COMPLETED', timeout=timeout)
    try:
        if not d: return
        w = d.pop().result()
        if winner is not None and A.iscoroutine(r := winner(w)): await r
        return w
    finally: audit('asyncutils.compete.race_with_callback/end', C); await safe_cancel_batch(p, callback=loser)
async def multi_winner_race_with_callback(*C, timeout, winner=None, loser=None, _=__import__('_operator').methodcaller('result')):
    if not C: raise TypeError('pass in at least one coroutine to multi_winner_race_with_callback')
    audit('asyncutils.compete.multi_winner_race_with_callback/start', C); d, p = await A.wait(new_tasks(*C), timeout=timeout); d = map(_, d)
    try:
        if winner is None: return list(d)
        f = (r := []).append
        async def g(a, /, _=winner):
            if A.iscoroutine(a := _(a)): await a
        for _ in d:
            try: await g(_); f(_)
            except CRITICAL: raise Critical
        return r
    finally: audit('asyncutils.compete.multi_winner_race_with_callback/end', C); await safe_cancel_batch(p, callback=loser)
def convert_to_coro_iter(cfs, skip_invalid=True, corocheck=A.iscoroutine, futwrap=A.wrap_future, handle_aiter=None, handle_iter=None, _c=H.check_methods):
    if handle_iter is None: from .iters import to_list as handle_iter
    if handle_aiter is None: from .iters import to_list as handle_aiter
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
def enhanced_staggered_race(cfs, delay=None, *, loop=None): return staggered_race(map(lambda c: lambda: c, convert_to_coro_iter(cfs)), delay, loop=loop)
del H