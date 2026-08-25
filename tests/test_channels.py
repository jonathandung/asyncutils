from asyncio import create_task, gather, sleep, wait_for
from asyncutils.channels import *
from tests.conftest import mk
import pytest
@mk
async def test_rdv():
    rdv = Rendezvous()
    assert (await gather(*map(rdv.put, range(5, 10)), rdv.exchange(10), *map(rdv.exchange, range(1, 5)), *(rdv.get() for _ in range(5))))[-10:] == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    t = create_task(rdv.put(0))
    await sleep(0.01)
    assert tuple(rdv.state_snapshot()) == (0, 1, 1, False)
    assert await rdv.get() == 0
    assert await rdv.get('default') == 'default'
    assert await t
    await rdv.reset()
    with pytest.raises(TimeoutError): await rdv.raising_put(-1, timeout=0.01)
    t = create_task(rdv.put(0))
    await sleep(0.01)
    assert await rdv.get(-1) == 0
    assert await wait_for(t, 0.01)
@mk
async def test_evt_bus():
    bus = EventBus('bus', tracking_stats=True)
    r = []
    bus.add_middleware(lambda t, d: r.append((t, d-1)) or d+1)
    @bus.on('a')
    async def sub(d): # ruff: ignore[unused-async]
        r.append(d)
    await bus.publish('a', 1, timeout=0.1)
    await bus.publish('a', 4, safe=False, timeout=0.05)
    assert r == [('a', 0), 2, ('a', 3), 5]
    assert bus.get_event_stats() == {'a': 2}
