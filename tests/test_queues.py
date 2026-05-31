from asyncio.tasks import create_task, sleep
from pytest import fixture, mark, raises
from asyncutils._internal.compat import QueueEmpty, QueueFull, QueueShutDown
from asyncutils.config import _randinst
from asyncutils.queues import *
from asyncutils import exceptions
from tests.conftest import mk
@fixture
def pwd(): return _randinst.randbytes(8)
@mk
async def test_pwdq(pwd):
    Q = password_queue(pwd, maxsize=2, init_items=[0, 1], can_change_put=True, puttyp=bytes)
    await sleep(0.02)
    assert Q.full() and not Q.cancel_extend(41)
    with raises(QueueFull): Q.put_nowait(-1, pwd)
    assert Q.change_put_password(pwd, pwd := pwd[::-1]) and not Q.change_get_password(pwd, pwd)
    t = create_task(Q.put(2, pwd))
    assert await Q.get() == 0
    assert Q.get_nowait() == 1
    await sleep(0)
    assert t.done() and await Q.get() == 2
    t = create_task(Q.get())
    Q.put_nowait(3, pwd)
    Q.task_done()
    await sleep(0)
    assert t.done() and t.result() == 3 and Q.empty()
    with raises(exceptions.PutPasswordMissing): await Q.put(-4)
    with raises(exceptions.WrongPassword): Q.put_nowait(-5, b'')
    with raises(exceptions.WrongPasswordType): await Q.put(-6, 123)
    with raises(QueueEmpty): Q.get_nowait()
    Q.shutdown()
    with raises(QueueShutDown): Q.put_nowait(-2, pwd)
    with raises(QueueShutDown): await Q.put(-3, pwd)
    with raises(QueueShutDown): Q.get_nowait()
    with raises(QueueShutDown): await Q.get()
    t = create_task(Q.join())
    Q.task_done()
    await sleep(0)
    assert not t.done()
    Q.task_done()
    Q.shutdown(True)
    Q.task_done()
    await sleep(0)
    assert t.done()
    with raises(ValueError, match=r'task_done\(\) called too many times'): Q.task_done()
    assert not (Q.cancel_extend() or Q.change_put_password(pwd, pwd) or Q.change_get_password(pwd, pwd))