import asyncio, pytest
from asyncutils import event_loop, safe_cancel
from asyncutils.futures import *
from functools import partial
from tests.conftest import mk
async def dummy(): return 42
async def dummy2(fut): fut.set_exception(ValueError('foo'))
@mk
async def test_time_aware():
    t1 = TimeAwareTask(dummy())
    t2 = TimeAwareTask(dummy())
    assert t1 < t2
    assert await t1 == 42
    assert await t2 == 42
    assert TimeAwareAsyncCallbacksFuture() < TimeAwareFuture() < TimeAwareUniqueCallbacksFuture()
    t1 = TimeAwareAsyncCallbacksTask(dummy())
    t2 = TimeAwareAsyncCallbacksTask(dummy())
    assert t1 < t2
    assert await t1 == 42
    assert await t2 == 42
@mk
async def test_task_usage():
    fut = AsyncCallbacksFuture()
    fut2 = UniqueCallbacksFuture()
    fut3 = TimeAwareFuture()
    fut4 = asyncio.Future()
    fut.add_noargs_callback(partial(fut2.set_result, None))
    fut.add_noargs_async_callback(partial(dummy2, fut3))
    await safe_cancel(fut)
    assert fut2.done()
    assert fut2.result() is None
    with pytest.raises(ValueError, match='foo'): fut3.result()
    fut2.add_noargs_callback(partial(fut4.set_result, 67))
    assert await fut4 == 67
