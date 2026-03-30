import pytest
from asyncutils.base import *
from asyncutils.iters import *
async def agen():
    for i in range(10): yield i
def test_aiter_to_iter():
    assert all(i == j for i, j in zip(aiter_to_iter(agen()), range(10)))
@pytest.mark.asyncio
async def test_iter_to_aiter(): assert await aall(i == j async for i, j in azip(iter_to_aiter(range(10)), agen()))