import asyncio, pytest
from asyncutils.util import *
from tests.conftest import mk
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
    await safe_cancel(asyncio.create_task(safe_cancel(t := asyncio.create_task(asyncio.sleep(0.03, 3)))))
    assert await t == 3
    m(None)
@mk
async def test_stuff():
    args = b'', set(), '', None, {}
    kwargs = {'a': (), 'Z': NotImplemented, 'r': False, '_': 0.0, 'q1': []}
    assert await avalify(2)(*args, **kwargs) == 2
    assert await anullify(*args, **kwargs) is None
    assert await atruthify(*args, **kwargs) is True
    assert await afalsify(*args, **kwargs) is False
def test_semaphore():
    s = semaphore(True, 2)
    assert s._value == 2
    with pytest.raises(ValueError, match='BoundedSemaphore released too many times'): s.release()
    assert type(semaphore(True)) is asyncio.Lock
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
