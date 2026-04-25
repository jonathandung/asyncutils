from asyncutils.base import *
from asyncutils.iterclasses import *
from asyncutils.iters import *
def test_aiter_to_gen(): assert all(i == j for i, j in zip(aiter_to_gen(arange(10)), range(10)))
async def test_iter_to_agen(): assert await vecs_eq(iter_to_agen(range(10)), arange(10))
async def test_amap(): assert await vecs_eq(amap(1 .__lshift__, arange(10)), apowersoftwo(), strict=False)
async def test_drop(): assert await vecs_eq(aprepend(2, drop(arange(1, 8, 2), 1)), asieve(8))
async def test_take(): assert await vecs_eq(take(atabulate(aisprime, await_=True), 10), (False, False, True, True, False, True, False, True, False, False))
async def test_collect(): assert [*range(10), 3, 3, 3, 3, 3] == await to_list(achain(arange(10), arepeat(3, 5))) == await collect(arange(10), 15, default=3)
async def test_aisprime(): assert await vecs_eq(afilter(aisprime, range(1, 1001)), asieve(1000))