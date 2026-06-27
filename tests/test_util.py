import asyncio, pytest
from asyncutils.iters import acount, vecs_eq
from asyncutils.util import *
from tests.conftest import mk
import itertools
@pytest.fixture
def args(): return b'', '', None
@pytest.fixture
def kwargs(): return {'a': (), 'Z': NotImplemented, 'r': False}
@mk
async def test_basic():
    m = asyncio.get_running_loop().set_task_factory
    m(make_task_factory(asyncio.Task))
    async with anullcontext: ...
    c = wrap_in_coro(asyncio.sleep(0, 0))
    assert not c.cr_running
    assert await c == 0
    assert done_evt().is_set()
    assert await done_fut(42) == 42
    assert [i async for i in aiter_from_f(to_async(itertools.count().__next__), 10)] == list(range(10))
    await safe_cancel(asyncio.create_task(safe_cancel(t := asyncio.create_task(asyncio.sleep(0.03, 3)))))
    assert await t == 3
    f = acount(2).__anext__
    assert await vecs_eq(aiter_from_f(f, 10), range(2, 10))
    assert await vecs_eq(aiter_from_f(f, 20, yield_sentinel=True), range(11, 21))
    m(None)
@mk
async def test_higher_order(args, kwargs):
    assert await avalify(2)(*args, **kwargs) == 2
    assert await discard_retval(asyncio.sleep)(0, 42) is None
    assert await evaluate_and_return(asyncio.sleep, 41)(0, 42) == 41
    c = afcopy(asyncio.create_task)(asyncio.sleep(0, 1))
    assert not c.cr_running
    assert await c == 1
@mk
async def test_stuff(args, kwargs):
    assert await anullify(*args, **kwargs) is None
    assert await atruthify(*args, **kwargs) is True
    assert await afalsify(*args, **kwargs) is False
@mk
async def test_semaphore():
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
