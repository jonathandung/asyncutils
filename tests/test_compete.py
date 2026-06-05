from asyncio import _get_running_loop, gather, sleep
from asyncutils.compete import *
from asyncutils import arange, agives, done_evt, done_fut
from tests.conftest import mk
@mk
async def test_coroit_conv():
    loop = _get_running_loop()
    for i, j in zip(convert_to_coro_iter([arange(2), sleep(0, 2), {3}, done_fut(4)], skip_invalid=False, loop=loop), ([0, 1], 2, [3], 4)): assert await i == j
    assert await enhanced_gather((range(3), 42, agives(3), None, done_evt().wait())) == [[0, 1, 2], [3], True]
