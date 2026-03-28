from pytest import raises, fixture, mark
from asyncutils.config import _randinst
from asyncutils.queues import *
from asyncutils._internal.compat import QueueFull, QueueEmpty
from asyncio.tasks import create_task, sleep
@fixture
def pwd(): return _randinst.randbytes(8)
@mark.asyncio
async def test_pwdq(pwd):
    Q = password_queue(pwd, maxsize=2, init_items=[0, 1])
    await sleep(0.1)
    assert Q.full()
    with raises(QueueFull): Q.put_nowait(-1, pwd)
    t = create_task(Q.put(2, pwd))
    assert 0 == await Q.get()
    assert 1 == Q.get_nowait()
    await sleep(0.1)
    assert t.done() and 2 == await Q.get()
    t = create_task(Q.get())
    Q.put_nowait(3, pwd)
    await sleep(0.1)
    assert t.done() and Q.empty()
    with raises(QueueEmpty): Q.get_nowait()
    Q.shutdown()