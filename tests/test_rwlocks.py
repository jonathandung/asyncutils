import pytest
from asyncio import create_task, sleep
from asyncutils.rwlocks import *
from tests.conftest import mk
@mk
@pytest.mark.parametrize('lockt', (RWLock, ReadPreferredRWLock, WritePreferredRWLock, FairRWLock, PriorityRWLock, FairPriorityRWLock, WritePreferredPriorityRWLock, AgingRWLock))
async def test_rwlock(lockt):
    lock = lockt()
    async with lock.reading():
        async with lock.reading():
            task = create_task((c := lock.writing()).__aenter__())
            await sleep(0.02)
            assert not task.done()
            assert lock.is_reading()
        await sleep(0.02)
        assert lock.is_reading() and not task.done() and lock.locked() and not lock.is_writing()
    await sleep(0.02)
    assert task.done() and lock.is_writing() and lock.locked()
    await c.__aexit__(None, None, None)
    assert not (lock.locked() or lock.is_reading() or lock.is_writing())
