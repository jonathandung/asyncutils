import gc, pytest
from asyncio import Lock, gather, sleep, timeout
from asyncutils.altlocks import *
from asyncutils import CircuitOpen, ResourceBusy, locked_lock, timer
from collections import deque
from tests.conftest import mk
@pytest.fixture
def obj(): return object()
def test_rsrc_guard(obj):
    g = ResourceGuard(obj, action='foo')
    assert g.success_ratio == 0
    with g:
        assert g.guarded
        with pytest.raises(ResourceBusy), g: ...
    assert not g.guarded
    G = ResourceGuard(obj, action='bar')
    assert G is not g
    with G, g:
        assert G.guarded
        assert g.guarded
    assert not G.guarded
    assert not g.guarded
    with G.yields_resource() as rsrc:
        assert rsrc is obj
        assert G.guarded
    with g.yields_resource() as rsrc:
        assert rsrc is obj
        assert not G.guarded
    assert g.success_ratio*4 == 3
    assert G.success_ratio == 1
    assert G.action == 'bar'
    assert g.action == 'foo'
def test_unique_rsrc_guard(obj):
    with UniqueResourceGuard(obj), pytest.raises(ResourceBusy), UniqueResourceGuard(obj): ...
    i = id(UniqueResourceGuard(obj))
    with ResourceGuard(obj), UniqueResourceGuard(obj): ...
    gc.collect()
    _, g = object(), UniqueResourceGuard(obj)
    assert id(g) != i
    with pytest.warns(RuntimeWarning, match=r'asyncutils\.altlocks\.UniqueResourceGuard: ignoring keyword arguments in favour of pre-existing guard'): g = UniqueResourceGuard(obj, action='baz')
    assert g is UniqueResourceGuard(obj)
    UniqueResourceGuard.clear_cache()
    G = UniqueResourceGuard(obj, action='spamming')
    assert g is not G
    g = ResourceGuard(obj)
    with pytest.warns(RuntimeWarning, match=r'asyncutils\.altlocks\.UniqueResourceGuard: ignoring keyword arguments in favour of pre-existing guard'): assert UniqueResourceGuard(obj, action='baz') is G
    with UniqueResourceGuard(obj), g:
        assert G.guarded
        with pytest.raises(ResourceBusy), g: ...
        with pytest.raises(ResourceBusy), G: ...
        with pytest.raises(ResourceBusy, match='another task is already spamming resource: <.*>'), UniqueResourceGuard(obj): ...
@mk
async def test_circuit_breaker():
    cb = CircuitBreaker('test', 3, 0.01, exc=TypeError, max_half_open_calls=2)
    @cb
    async def f(): return 1
    assert await f() == 1
    async def g(): raise TypeError
    h = cb(g, default=0)
    for _ in range(3): assert await h() == 0
    with pytest.raises(CircuitOpen): await h()
    assert cb.state == cb.State.OPEN
    await sleep(0.02)
    for _ in range(2):
        assert await h() == 0
        assert cb.state == cb.State.HALF_OPEN
    await f()
    assert cb.state == cb.State.CLOSED
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
    async with t, t, t: raise RuntimeError
@mk
@pytest.mark.skipif('sys.implementation.name == "graalpy"')
async def test_dynamic_throttle():
    t = DynamicThrottle(10, window=6)
    assert 0.16 < (await dts(t))[1] < 0.3
    await dtf(t)
