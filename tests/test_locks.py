import pytest
from asyncio import create_task, gather, sleep, timeout
from asyncutils.locks import *
@pytest.mark.parametrize('lockt', (RWLock, ReadPreferredRWLock, WritePreferredRWLock, FairRWLock, PriorityRWLock))
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
async def test_kcond():
    cond = KeyedCondition[str]()
    async with cond:
        task = create_task(cond.wait('a'))
        await sleep(0.1)
        assert not task.done()
        cond.notify('a', 2)
        await sleep(0.1)
        assert task.done()
        task = gather(cond.wait('b'), cond.wait('b'))
        await sleep(0.1)
        cond.notify('b', 3)
        assert await task == [None, None]
        cond.notify('c')
        with pytest.raises(ValueError, match=r"asyncutils\.locks\.KeyedCondition: no parties waiting for key 'd'"): cond.notify('d', strict=True)
        with pytest.raises(ValueError, match=r"asyncutils\.locks\.KeyedCondition: n must be positive"): cond.notify('e', -1, strict=True)
        await cond.wait_all()
async def test_mcdlatch():
    async with timeout(1):
        latch = MultiCountDownLatch[str]({'a': 1, 'b': 2, 'c': 3})
        await latch.count_down('c', strict=True)
        await latch.count_down('a')
        await latch.wait('a')
        await latch.count_down_all()
        await latch.count_down('d')
        with pytest.raises(KeyError, match=r"asyncutils\.locks\.MultiCountDownLatch: cannot count down key 'e' further"): await latch.count_down('e', True)
        with pytest.raises(KeyError, match=r"asyncutils\.locks\.MultiCountDownLatch: no count for key 'f'"): await latch.wait('f', strict=True)
        await latch.count_down('b')
        await latch.wait('b')
        await latch.count_down('c')
        await latch.wait_all()
        assert latch.broken