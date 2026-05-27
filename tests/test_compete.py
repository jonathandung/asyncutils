from asyncio.tasks import gather, sleep
from asyncutils.compete import *
from asyncutils import agives
from tests.conftest import mk
@mk
async def test_coroit_conv():
    t = await gather(*convert_to_coro_iter((range(3), agives(3), None, sleep(0, 4))))
    assert t == [[0, 1, 2], [3], 4]