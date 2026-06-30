from asyncutils.locksmiths import *
from asyncutils import done_fut, locked_lock, wrap_exc
from tests.conftest import mk
import asyncio, pytest
@mk
async def test_force():
    smith, lock = LocksmithBase(), await locked_lock()
    task = smith.wrap_task(done_fut(67))
    assert isinstance(task, asyncio.Task)
    assert await task == 67
    with pytest.raises(RuntimeError, match='test'): await smith.wrap_task(done_fut(wrap_exc(RuntimeError('test'))))
    res = await smith.force(lock)
    assert res == ForceResult.UNFORCEABLE
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
    assert await smith.force(lock) == ForceResult.UNFORCEABLE
