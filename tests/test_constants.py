import math, pytest
from asyncutils.constants import *
from asyncutils.constants import _NO_DEFAULT
def test_misc():
    assert math.isclose(1/RECIP_E, math.e)
    assert EXECUTORS_FROZENSET.issuperset(POSSIBLE_EXECUTORS) and EXECUTORS_FROZENSET.issubset(POSSIBLE_EXECUTORS)
    assert RAISE.is_(RAISE) and not RAISE.is_(SYNC_AWAIT) and SYNC_AWAIT.is_(SYNC_AWAIT)
    assert RAISE.name == RAISE.__reduce__() == str(RAISE) == 'asyncutils.constants.RAISE' and SYNC_AWAIT.name == SYNC_AWAIT.__reduce__() == str(SYNC_AWAIT) == 'asyncutils.constants.SYNC_AWAIT'
    assert not any(_.is_private for _ in (RAISE, SYNC_AWAIT))
    assert _NO_DEFAULT.is_private
    assert tuple(range(3)) == (CLOSED, HALF_OPEN, OPEN)
@pytest.fixture
def ctxmgr(): return pytest.raises(TypeError, match="cannot instantiate '.*'")
@pytest.mark.parametrize('cls', (sentinel_base, type(RAISE)))
def test_sentinels(cls, ctxmgr):
    with ctxmgr: cls()
    with ctxmgr: cls('foo')
    with ctxmgr: cls('corge.bar')
    with ctxmgr:
        class Foo: __slots__, baz = (), cls()
    with ctxmgr:
        class Bar: __slots__, quux = (), cls('Bar.quux')
    assert not (sentinel_base._can_instantiate or type(RAISE)._can_instantiate) # type: ignore[attr-defined]
def test_custom_sentinel():
    class TestSentinel(sentinel_base): __slots__ = ()
    a = TestSentinel()
    assert a.is_(a) and a.bound_to is None
    class qux: __slots__, grault = (), TestSentinel()
    assert f'{qux.grault.bound_to}.{qux.grault.back}'.endswith('qux.grault')
    class garply: __slots__, waldo = (), TestSentinel('garply.waldo')
    assert garply.waldo.is_(TestSentinel('garply.waldo'))