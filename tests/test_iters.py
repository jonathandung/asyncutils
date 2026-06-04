from asyncutils.base import *
from asyncutils.iterclasses import *
from asyncutils.iters import *
from asyncio import CancelledError, create_task, gather, sleep
from _collections import deque
from operator import is_
from pytest import fail, mark, raises
from tests.conftest import mk
def test_aiter_to_gen(): assert all(i == j for i, j in zip(aiter_to_gen(arange(10)), range(10)))
@mk
async def test_iter_to_agen(): assert await vecs_eq(iter_to_agen(range(10)), arange(10))
@mk
async def test_amap(): assert await vecs_eq(amap(1 .__lshift__, arange(10)), apowers_of_two(), strict=False)
@mk
async def test_drop(): assert await vecs_eq(aprepend(2, drop(arange(1, 8, 2), 1)), asieve(8))
@mk
async def test_take(): assert await vecs_eq(take(atabulate(aisprime, await_=True), 10), (False, False, True, True, False, True, False, True, False, False))
@mk
async def test_collect(): assert [*range(10), 3, 3, 3, 3, 3] == await to_list(achain(arange(10), arepeat(3, 5))) == await collect(arange(10), 15, default=3)
@mk
async def test_aisprime(): assert await vecs_eq(afilter(aisprime, range(1, 1001)), asieve(1000))
@mk
async def test_agives(): assert await aallequal(aenumerate(agives(0)), strict=True)
@mk
async def test_anth(): assert await anth((), 1, default=0) == 0 and await anth(acycle(acount()), 2) == 2
@mk
async def test_azip(): assert await vecs_eq(azip(arange(10), arange(10, 20)), ((0, 10), (1, 11), (2, 12), (3, 13), (4, 14), (5, 15), (6, 16), (7, 17), (8, 18), (9, 19)))
@mk
async def test_sleep_forever():
    task = create_task(c := sleep_forever())
    await sleep(0.2)
    assert not task.done()
    task.cancel('message')
    assert c.cr_suspended and not c.cr_running and c.cr_await
    with raises(CancelledError, match='message'): await task
    with raises(RuntimeError, match='cannot reuse already awaited coroutine'): await c
@mk
async def test_dummies():
    await gather(yield_to_event_loop, dummy_task)
    for i in dummy_task: fail(f'dummy_task should be empty; got {i}')
    async for i in aloops(4): assert i is None
@mk
async def test_adisembowel():
    assert await vecs_eq(aappend(0, adisembowel([1, 2, 3])), areversed(range(4)), is_)
    dq = deque()
    async for i in achain.from_iterable(amap(arange, arange(1, 4))): dq.append(i)
    assert await vecs_eq(adisembowelleft(dq), await agather(amap(sleep.__get__(0), (0, 0, 1, 0, 1, 2))), is_)
@mk
async def test_aaccumulate(): assert await vecs_eq(aaccumulate(range(10)), (0, 1, 3, 6, 10, 15, 21, 28, 36), strict=False)
@mk
async def test_aonline_sorter():
    s = aonline_sorter([-1, -2], key=hash)
    assert await anext(s) == -1
    assert await s.asend(3) == -2
    assert await s.asend(-4) == -4
    assert await s.asend(5) == 3
    assert await vecs_eq(s, (5,))
