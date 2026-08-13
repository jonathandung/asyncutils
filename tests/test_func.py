from asyncutils.func import *
from asyncutils.config import _randinst
from tests.conftest import mk
from asyncio import create_task, sleep
from asyncutils import acount, amap, arange, vecs_eq
from itertools import count
from pytest import raises
async def func(a, b=3, /, c=24, *, d, e=7): return a+b-c/d*e # ruff: ignore[unused-async]
@mk
async def test_areduce():
    assert await areduce(int.__add__, range(10), await_=False) == 45
    assert await areduce(max, l := _randinst.choices(range(100), k=30), await_=False) == max(l)
    assert await areduce(lambda *_: True, (), None, await_=False) is None
@mk
async def test_aiter_from_f():
    assert [i async for i in aiter_from_f(to_async(count().__next__), 10)] == list(range(10))
    f = acount(2, 2).__anext__
    assert await vecs_eq(aiter_from_f(f, 10), range(2, 9, 2))
    assert await vecs_eq(aiter_from_f(f, 20, yield_sentinel=True), range(12, 21, 2))
@mk
async def test_easy():
    assert await discard_retval(sleep)(0, 42) is None
    assert await evaluate_and_return(sleep, 41)(0, 42) == 41
    c = afcopy(create_task)(sleep(0, 1))
    assert not c.cr_running
    assert await c == 1
@mk
async def test_acompose():
    assert await vecs_eq(amap(acompose(1 .__lshift__, 8 .__rshift__, wrap_last=False), range(4), await_=True), (256, 16, 4, 2), strict=True)
    assert await vecs_eq(amap(acompose(2 .__add__, 3 .__mul__, wrap_last=True), range(5), await_=True), (2, 5, 8, 11, 14), strict=True)
@mk
async def test_star():
    f = star(func)
    with raises(TypeError): await f()
    assert await f((1,), {'c': 16, 'd': 2}) == -52
    assert await f(arange(16, 25, 4), {'e': 6, 'd': 8}) == 18
    g = unstar(f)
    assert await g(5, d=7) == -16
