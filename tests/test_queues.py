from pytest import raises, fixture
from asyncutils.config import _randinst
from asyncutils.queues import *
from asyncutils._internal.compat import QueueFull, QueueEmpty, QueueShutDown
from asyncio.tasks import create_task, sleep
@fixture
def pwd(): return _randinst.randbytes(8)
async def test_pwdq(pwd):
    Q = password_queue(pwd, maxsize=2, init_items=[0, 1])
    await sleep(0.1)
    assert Q.full()
    with raises(QueueFull): Q.put_nowait(-1, pwd)
    t = create_task(Q.put(2, pwd))
    assert await Q.get() == 0
    assert Q.get_nowait() == 1
    await sleep(0.1)
    assert t.done() and await Q.get() == 2
    t = create_task(Q.get())
    Q.put_nowait(3, pwd)
    await sleep(0.1)
    assert t.done() and t.result() == 3 and Q.empty()
    with raises(QueueEmpty): Q.get_nowait()
    Q.shutdown()
    with raises(QueueShutDown): Q.put_nowait(-2, pwd)
    with raises(QueueShutDown): await Q.put(-3, pwd)
    with raises(QueueShutDown): Q.get_nowait()
    with raises(QueueShutDown): await Q.get()