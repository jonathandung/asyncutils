from asyncutils.func import *
from asyncutils.config import _randinst
from tests.conftest import mk
from asyncio import create_task, sleep
from asyncutils.iters import acount, vecs_eq
from itertools import count
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
