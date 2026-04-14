from asyncio.tasks import gather, sleep
from asyncutils.compete import *
async def agen(): yield 3
async def test_coroit_conv():
    t = await gather(*convert_to_coro_iter((range(3), agen(), None, sleep(0, 4))))
    assert t == [[0, 1, 2], [3], 4]