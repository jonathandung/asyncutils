from asyncutils import EventValueError
from asyncutils.events import *
from tests.conftest import mk
from asyncio import create_task, sleep
from pytest import raises
@mk
async def test_swe():
    e = SingleWaiterEventWithValue()
    with raises(EventValueError): e.get()
    assert e.get(1) == 1
    t = create_task(e.wait_for_next())
    await sleep(0)
    assert not t.done()
    e.set(0)
    assert e.is_set()
    await sleep(0)
    assert t.result() == 0
@mk
async def test_ewv():
    e = EventWithValue()
    with raises(EventValueError): e.get()
    assert e.get(1) == 1
    e.set(1)
    await e.wait_for_value(1)
    e.set(2)
    assert e.is_set()
    e.set(3)
    assert e.get(5) == 3
