import asyncio, pytest
from asyncutils import done_fut, exc_fut, locked_lock
from asyncutils.locksmiths import *
from tests.conftest import mk
@mk
async def test_force():
    smith, lock = Locksmith(), await locked_lock()
    assert len(smith.currently_recognized) == 1
    assert not smith.handlers
    task = smith.wrap_task(done_fut(4))
    assert isinstance(task, asyncio.Task)
    assert await task == 4
    with pytest.raises(RuntimeError, match='test'): await smith.wrap_task(exc_fut(RuntimeError('test')))
    res = await smith.force(lock)
    assert res == ForceResult.CANNOT_FORCE
    assert not succeeded(res)
    res = await smith.recognize_lock(lock)
    assert succeeded(res)
    assert res == RecognitionResult.SUCCESS
    assert lock.locked()
    res = await smith.force(lock, purge_waiters=True)
    assert not lock.locked()
    assert res == ForceResult.RELEASED
    assert succeeded(res)
    assert lock in smith.currently_recognized
    assert await smith.force(lock) == ForceResult.CANNOT_FORCE
