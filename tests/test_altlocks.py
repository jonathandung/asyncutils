import pytest
from asyncio import Lock, gather, sleep, timeout
from asyncutils.altlocks import *
from asyncutils import CircuitOpen, ResourceBusy, locked_lock, timer
from collections import deque
from tests.conftest import mk
@pytest.fixture
def obj(): return object()
def test_rsrc_guard(obj):
    g = ResourceGuard(obj)
    with g:
        assert g.guarded
        with pytest.raises(ResourceBusy), g: ...
    assert not g.guarded
    G = ResourceGuard(obj)
    assert G is not g
    with G, g:
        assert G.guarded
        assert g.guarded
    assert not G.guarded
    assert not g.guarded
def test_unique_rsrc_guard(obj):
    with UniqueResourceGuard(obj), pytest.raises(ResourceBusy), UniqueResourceGuard(obj): ...
    with ResourceGuard(obj), UniqueResourceGuard(obj): ...
@mk
async def test_circuit_breaker():
    cb = CircuitBreaker('test', 3, reset=0.05, exc=ZeroDivisionError, max_half_open_calls=2)
    @cb
    async def f(): return 1
    assert await f() == 1
    async def g(): return 1/0
    g = cb(g, default=0)
    for _ in range(3): assert await g() == 0
    with pytest.raises(CircuitOpen): await g()
    await sleep(0.07)
    for _ in range(2): assert await g() == 0
    await f()
@mk
async def test_stateful_barrier():
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
    rel = Releasing(lock := await locked_lock())
    async with rel, lock, rel: ...
    assert lock.locked()
@timer
async def dts(t):
    async with t, t, t: ...
@timer
async def dtf(t):
    async with t, t, t: 1/0
@mk
async def test_dynamic_throttle():
    t = DynamicThrottle(10, window=6)
    assert 0.16 < (await dts(t))[1] < 0.35
    await dtf(t)
