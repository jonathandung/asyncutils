from _collections import deque
from asyncio import CancelledError, create_task, gather, sleep
from enum import IntEnum
from operator import is_
from random import choice, shuffle
from pytest import fail, fixture, raises
from asyncutils import iterf
from asyncutils.base import *
from asyncutils.iterclasses import *
from asyncutils.iters import *
from tests.conftest import mk
@fixture
def bucket(): return ABucket((10, 20, 30, 11, 21, 31, 12, 22, 23, 33), 10 .__rfloordiv__)
Set = IntEnum('Set', 'A B C D E F G H I J')
l = list(Set)
shuffle(l)
d = dict(zip(Set, l, strict=True))
async def next_node(x): return d[x]  # ruff: ignore[unused-async]
def test_aiter_to_gen(): assert all(i == j for i, j in zip(aiter_to_gen(arange(10)), range(10), strict=True))
@mk
async def test_iter_to_agen(): assert await vecs_eq(iter_to_agen(range(10)), arange(10))
@mk
async def test_amap(): assert await vecs_eq(amap(1 .__lshift__, arange(10)), apowers_of_two(), strict=False)
@mk
async def test_drop():
    assert await vecs_eq(aprepend(2, drop(arange(1, 8, 2), 1)), asieve(8))
    assert await vecs_eq(drop(arange(10), 0), arange(10))
    assert await vecs_eq(drop(arange(10), 15), ())
@mk
async def test_take():
    assert await vecs_eq(take(atabulate(aisprime, await_=True), 10), (False, False, True, True, False, True, False, True, False, False))
    assert await vecs_eq(take(arange(10), 0), ())
    assert await vecs_eq(take(arange(10), 15), arange(10))
    assert await vecs_eq(take(arange(3), 5, 0), (0, 1, 2, 0, 0))
@mk
async def test_collect(): assert [*range(10), 3, 3, 3, 3, 3] == await to_list(AChain(arange(10), arepeat(3, 5))) == await collect(arange(10), 15, 3)
@mk
async def test_aisprime(): assert await vecs_eq(afilter(aisprime, range(1, 501), await_=True), asieve(500))
@mk
async def test_agives(): assert await aall_equal(aenumerate(agives(0)), strict=True)
@mk
async def test_anth():
    assert await anth((), 1, default=0) == 0
    assert await anth(acycle(acount()), 2) == 2
@mk
async def test_azip(): assert await vecs_eq(azip(arange(10), arange(10, 20)), ((0, 10), (1, 11), (2, 12), (3, 13), (4, 14), (5, 15), (6, 16), (7, 17), (8, 18), (9, 19)))
@mk
async def test_sleep_forever():
    task = create_task(c := sleep_forever())
    await sleep(0.2)
    assert not task.done()
    task.cancel('message')
    assert c.cr_suspended
    assert not c.cr_running
    assert c.cr_await
    with raises(CancelledError, match='message'): await task
    with raises(RuntimeError, match='cannot reuse already awaited coroutine'): await c
@mk
async def test_dummies():
    await gather(yield_to_event_loop, dummy_task)
    for i in dummy_task: fail(f'dummy_task should be empty; got {i}')
    async for i in aloops(0x1000): assert i is None
@mk
async def test_adisembowel():
    assert await vecs_eq(aappend(0, adisembowel([1, 2, 3])), areversed(range(4)), is_)
    dq = deque()
    async for i in AChain.from_iterable(amap(arange, arange(1, 4))): dq.append(i)
    assert await vecs_eq(adisembowel_left(dq), await agather(amap(sleep.__get__(0), (0, 0, 1, 0, 1, 2))), is_)
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
@mk
async def test_bucket(bucket):
    assert await bucket.contains(1)
    assert not await bucket.contains(4)
    assert await bucket.contains(2)
    assert await anext(bucket[1]) == 10
@mk
async def test_bucket2(bucket):
    assert await collect(bucket[1]) == [10, 11, 12]
    assert await basic_collect(bucket[3]) == [30, 31, 33]
    assert await to_list(bucket[2]) == [20, 21, 22, 23]
    assert await to_tuple(bucket[0]) == ()
    assert await to_set(bucket) == set()
@mk
async def test_abrent():
    cur = choice(l)
    node, la, mu = await abrent(next_node, cur)
    assert type(node) is Set
    assert await iterf(mu)(next_node)(cur) is node
    s = {cur}
    for _ in range(la-1):
        cur = d[cur]
        assert cur not in s
        s.add(cur)
    assert d[cur] is node
@mk
async def test_tee():
    x, y, z = tee(arange(5), 3)
    assert await anext(x) == 0
    assert await gather(anext(y), anext(z), anext(y), anext(x), anext(x)) == [0, 0, 1, 1, 2]
    assert await anext(y) == 2
    assert await gather(anext(x), anext(z), anext(y), anext(z)) == [3, 1, 3, 2]
    assert await anext(z) == 3
    async for i in AChain(x, y, z): assert i == 4
@mk
async def test_aunzip():
    x, y, z = await aunzip(tuple(range(i, i+3)) for i in range(1, 8, 3))
    assert await vecs_eq(x, (1, 4, 7), strict=True)
    assert await anext(z) == 3
    assert await gather(anext(y), anext(z)) == [2, 6]
    assert await gather(anext(z), anext(y), anext(y)) == [9, 5, 8]
    assert await aisempty(y)
    assert await aisempty(z)
    assert await aisempty(x)
