import asyncio, pytest
from asyncutils.util import *
from tests.conftest import mk
import itertools
@mk
async def test_basic():
    async with anullcontext: ...
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
async def test_non_trivial():
    s = semaphore(True, 2)
    assert s._value == 2
    with pytest.raises(ValueError, match='BoundedSemaphore released too many times'): s.release()
    assert isinstance(semaphore(True), asyncio.Lock)
    s = semaphore(workers=3)
    assert s._value == 3
    s.release()
@dualcontextmanager
def dc(a):
    try: yield 67
    finally: a.append(41)
@mk
async def test_dualcontextmanager():
    a = []
    with dc(a) as x:
        assert not a
        assert x == 67
    assert a.pop() == 41
    async with dc(a=a) as x:
        assert not a
        assert x == 67
    b, = a
    assert b == 41
