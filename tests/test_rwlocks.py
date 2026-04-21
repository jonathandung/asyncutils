import pytest
from asyncio import create_task, sleep
from asyncutils.rwlocks import *
@pytest.mark.parametrize('lockt', (RWLock, ReadPreferredRWLock, WritePreferredRWLock, FairRWLock, PriorityRWLock, FairPriorityRWLock, WritePreferredPriorityRWLock))
async def test_rwlock(lockt):
    lock = lockt()
    async with lock.reading():
        async with lock.reading():
            task = create_task((c := lock.writing()).__aenter__())
            await sleep(0.1)
            assert not task.done()
        await sleep(0.1)
        assert not task.done()
    await sleep(0.1)
    assert task.done()
    await c.__aexit__(None, None, None)