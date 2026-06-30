import pytest
from asyncio import create_task, sleep
from asyncutils.rwlocks import *
from tests.conftest import mk
@mk
@pytest.mark.parametrize('lt', (RWLock, ReadPreferredRWLock, WritePreferredRWLock, FairRWLock, PriorityRWLock, FairPriorityRWLock, WritePreferredPriorityRWLock, AgingRWLock))
async def test_rwlocks(lt):
    lock = lt()
    async with lock.reading():
        async with lock.reading():
            task = create_task((c := lock.writing()).__aenter__()) # noqa: PLC2801
            await sleep(0.01)
            assert not task.done()
            assert lock.is_reading()
        await sleep(0.01)
        assert lock.is_reading()
        assert not task.done()
        assert lock.locked()
        assert not lock.is_writing()
    await sleep(0.01)
    assert task.done()
    assert lock.is_writing()
    assert lock.locked()
    await c.__aexit__(None, None, None)
    assert not lock.locked()
    assert not lock.is_reading()
    assert not lock.is_writing()
