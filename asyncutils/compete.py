from asyncutils._internal import helpers as H, patch as P
from asyncutils._internal.submodules import compete_all as __all__
import asyncio as I, asyncutils as A
from asyncio.staggered import staggered_race
from sys import audit
async def first_completed(*C, ret_exc=False, timeout=None):
    audit('asyncutils.compete.first_completed/start', L := len(C)); t = tuple(A.new_eager_tasks(*C))
    try:
        async with I.timeout(timeout):
            for F in (await I.wait(t, return_when='FIRST_COMPLETED'))[0]: return A.wrap_exc(e) if ret_exc and (e := F.exception()) else F.result()
    finally: audit('asyncutils.compete.first_completed/end', L); await A.safe_cancel_batch(t)
async def race_with_callback(*C, winner=None, loser=None, timeout=None):
    if not C: raise TypeError('asyncutils.compete.race_with_callback: pass in at least one coroutine')
    audit('asyncutils.compete.race_with_callback/start', L := len(C)); d, p = await I.wait(A.new_eager_tasks(*C), return_when='FIRST_COMPLETED', timeout=timeout)
    try:
        if not d: return None
        w = d.pop().result()
        if winner is not None and I.iscoroutine(r := winner(w)): await r
        return w
    finally: audit('asyncutils.compete.race_with_callback/end', L); await A.safe_cancel_batch(p, callback=loser)
async def multi_winner_race_with_callback(*C, timeout, winner=None, loser=None, _=__import__('operator').methodcaller('result')): # noqa: B008
    if not C: raise TypeError('asyncutils.compete.multi_winner_race_with_callback: pass in at least one coroutine')
    audit('asyncutils.compete.multi_winner_race_with_callback/start', L := len(C)); d, p = await I.wait(A.new_eager_tasks(*C), timeout=timeout); d = map(_, d)
    try:
        if winner is None: return list(d)
        async def g(a, /, _=winner, f=(r := []).append):
            if I.iscoroutine(x := _(a)): await x
            f(a)
        await I.gather(*map(g, d)); return r
    except A.CRITICAL: raise A.Critical
    finally: audit('asyncutils.compete.multi_winner_race_with_callback/end', L); await A.safe_cancel_batch(p, callback=loser)
def convert_to_coro_iter(cfs, *, loop=None, skip_invalid=None, corocheck=I.iscoroutine, futwrap=I.wrap_future, handle_aiter=None, handle_iter=None, _c=H.check_methods):
    if handle_iter is None: from asyncutils import to_list as handle_iter
    if handle_aiter is None: from asyncutils import to_list as handle_aiter
    if skip_invalid is None: from asyncutils.context import CONVERT_TO_CORO_ITER_DEFAULT_SKIP_INVALID as skip_invalid # noqa: N811
    for i in A.aiter_to_gen(cfs, loop=loop):
        if corocheck(i): yield i; continue
        try: i = futwrap(i, loop=loop) # noqa: PLW2901
        except A.CRITICAL: raise A.Critical
        except (AssertionError, TypeError):
            if not _c(i, '__await__'):
                if _c(i, '__aiter__'): yield handle_aiter(i)
                elif _c(i, '__iter__'): yield handle_iter(i)
                elif not skip_invalid: raise TypeError(f'asyncutils.compete.convert_to_coro_iter: invalid item in {cfs!r}: {i!r}') from None
                continue
        yield A.wrap_in_coro(i)
def enhanced_staggered_race(cfs, delay=None, *, loop=None): return staggered_race(map(lambda c: lambda: c, convert_to_coro_iter(cfs, loop=loop)), delay, loop=loop)
def enhanced_gather(it, return_exceptions=False, *, loop=None, _=I.gather): return _(*convert_to_coro_iter(it, loop=loop), return_exceptions=return_exceptions)
P.patch_function_signatures((first_completed, '*coros, ret_exc=False, timeout=None, loop=None'), (race_with_callback, '*coros, winner=None, loser=None, timeout=None'), (multi_winner_race_with_callback, '*coros, timeout, winner=None, loser=None'), (convert_to_coro_iter, 'cfs, *, loop=None, skip_invalid=None, corocheck={0}, futwrap={0}, handle_aiter=None, handle_iter=None'), (enhanced_gather, 'it, return_exceptions=False, *, loop=None'))
del H, P
