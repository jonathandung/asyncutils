from collections import deque
from asyncio.locks import Lock
from asyncio.tasks import sleep, gather
from asyncio.timeouts import timeout
import pytest
from tests.conftest import mk
from asyncutils.altlocks import *
from asyncutils import CircuitOpen, timer
@pytest.fixture
def obj(): return object()
def test_rguard(obj):
    g = ResourceGuard.guard(obj)
    with g:
        assert g.guarded
        with pytest.raises(ResourceGuard, check=lambda e: e is g and str(e) == f'another task is already using resource: {obj!r}'), g: ...
    assert not g.guarded
    G = ResourceGuard.guard(obj)
    assert G is not g
    with G, g: assert G.guarded and g.guarded
    assert not (G.guarded or g.guarded)
def test_urguard(obj):
    with UniqueResourceGuard.guard(obj), pytest.raises(UniqueResourceGuard), UniqueResourceGuard.guard(obj): ...
    with ResourceGuard.guard(obj), UniqueResourceGuard.guard(obj): ...
@mk
async def test_cbreaker():
    cb = CircuitBreaker('test', 3, reset=0.2, exc=ZeroDivisionError, max_half_open_calls=2)
    @cb
    async def f(): return 1
    assert await f() == 1
    async def g(): return 1/0
    g = cb(g, default=0)
    for _ in range(3): assert await g() == 0
    with pytest.raises(CircuitOpen): await g()
    await sleep(0.25)
    for _ in range(2): assert await g() == 0
    await f()
@mk
async def test_sbarrier():
    b = StatefulBarrier[int](3)
    assert not b.broken
    (u, x), (v, y), (w, z) = await gather(*map(b.wait, range(1, 6, 2)))
    assert (u, v, w) == (0, 1, 2)
    assert x == y == z == deque((1, 3, 5))
@mk
async def test_releasing():
    rel = Releasing(lock := Lock())
    with pytest.raises(RuntimeError, match=r'asyncutils\.altlocks\.Releasing: lock is not acquired'):
        async with rel: ...
    async with lock:
        async with rel: assert not lock.locked()
        assert lock.locked()
@timer
async def dts(t):
    async with t, t, t: ...
@timer
async def dtf(t):
    async with t, t, t: 1/0
@mk
async def test_dthrottle():
    t = DynamicThrottle(3, window=6)
    assert 0.5 < (await dts(t))[1] < 0.8
    await dtf(t)