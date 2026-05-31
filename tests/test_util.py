import asyncio, pytest
from asyncutils.util import *
from tests.conftest import mk
import itertools
def test_sync_await(): assert sync_await(asyncio.sleep(0.02, 1), timeout=0.04) == 1
@to_sync
async def g(x): return x<<1
def test_to_sync(): assert g(4) == 8
@mk
async def test_basic():
    async with anullcontext(): ...
    c = wrap_in_coro(asyncio.sleep(0, 0))
    assert not c.cr_running
    assert await c == 0
    assert done_evt().is_set()
    assert await done_fut(42) == 42
    assert [i async for i in aiter_from_f(to_async(itertools.count().__next__), 10)] == list(range(10))
    await safe_cancel(asyncio.create_task(safe_cancel(t := asyncio.create_task(asyncio.sleep(0.03, 3)))))
    c = afcopy(asyncio.create_task)(asyncio.sleep(0, 1))
    assert not c.cr_running
    assert await c == 1
    assert await t == 3
@mk
async def test_nontrivial():
    s = semaphore(True)
    assert s._value == 1
    with pytest.raises(ValueError): s.release()
    s = semaphore(workers=3)
    assert s._value == 3
    s.release()
a = []
@dualcontextmanager
def dc():
    try: yield 67
    finally: a.append(41)
@mk
async def test_dualcontextmanager():
    with dc() as x: assert not a and x == 67
    assert a.pop() == 41
    async with dc() as x: assert not a and x == 67
    assert a.pop() == 41