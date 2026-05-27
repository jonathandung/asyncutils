import asyncio, pytest
from asyncutils.util import *
from tests.conftest import mk
def test_sync_await(): assert sync_await(asyncio.sleep(0.05, 1), timeout=0.1) == 1
@to_sync
async def g(x): return x<<1
def test_to_sync(): assert g(4) == 8
@mk
async def test_basic():
    async with anullcontext(): ...
    c = wrap_in_coro(asyncio.sleep(0, 0))
    assert not c.cr_running
    assert await c == 0