from asyncio.tasks import gather, sleep
from asyncutils.channels import Rendezvous
async def test_rdv():
    rdv = Rendezvous()
    assert (await gather(*map(rdv.put, range(5, 10)), rdv.exchange(10), *map(rdv.exchange, range(1, 5)), *(rdv.get() for _ in range(5))))[-10:] == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    task = rdv._loop.create_task(rdv.put(0))
    await sleep(0.1)
    assert tuple(rdv.state_snapshot()) == (0, 1, 1, False)
    assert await rdv.get() == 0
    assert await rdv.get('default') == 'default'
    assert await task