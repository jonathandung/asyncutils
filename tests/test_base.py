from asyncutils.base import *
from asyncutils.iters import *
from asyncutils.iterclasses import *
aio_mark = __import__('pytest').mark.asyncio
def test_aiter_to_iter(): assert all(i == j for i, j in zip(aiter_to_iter(arange(10)), range(10)))
@aio_mark
async def test_iter_to_aiter(): assert await vecs_eq(iter_to_aiter(range(10)), arange(10))
@aio_mark
async def test_amap(): assert await vecs_eq(amap(1 .__lshift__, arange(10)), apowersoftwo(), strict=False)
@aio_mark
async def test_aenum(): assert await vecs_eq(aenumerate(range(2, 13, 2), 1, step=2), amap(tuple, batch(range(1, 13), 2, strict=True)), strict=False)
@aio_mark
async def test_drop(): assert await vecs_eq(aprepend(2, drop(arange(1, 8, 2), 1)), asieve(8))
@aio_mark
async def test_take(): assert await vecs_eq(take(atabulate(atotient, await_=True), 10), (0, 1, 1, 2, 2, 4, 2, 6, 4, 6))
@aio_mark
async def test_collect(): assert [*range(10), 3, 3, 3, 3, 3] == await to_list(achain(arange(10), arepeat(3, 5))) == await collect(arange(10), 15, 3)
@aio_mark
async def test_aisprime():
    assert await vecs_eq(afilter(aisprime, range(1, 101)), asieve(100))
    print(*await to_tuple(asieve(29)))