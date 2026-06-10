import math, pytest
from asyncutils.constants import *
from asyncutils.constants import _NO_DEFAULT
def test_misc():
    assert 1/math.e == RECIP_E and math.e == 1/RECIP_E # noqa: RUF069
    assert EXECUTORS_FROZENSET.issuperset(POSSIBLE_EXECUTORS) and EXECUTORS_FROZENSET.issubset(POSSIBLE_EXECUTORS)
    assert RAISE.is_(RAISE)
    assert RAISE.name == RAISE.__reduce__() == str(RAISE) == 'asyncutils.constants.RAISE'
    assert not RAISE.is_private
    assert _NO_DEFAULT.is_private
@pytest.fixture
def ctxmgr(): return pytest.raises(TypeError, match=r"cannot instantiate 'asyncutils\.constants\..*'")
@pytest.mark.parametrize('cls', (sentinel_base, type(RAISE)))
def test_sentinels(cls, ctxmgr):
    with ctxmgr: cls()
    with ctxmgr: cls('foo')
    with ctxmgr: cls('corge.bar')
    with ctxmgr:
        class Foo: __slots__, baz = (), cls()
    with ctxmgr:
        class Bar: __slots__, quux = (), cls('Bar.quux')
    assert not (sentinel_base._can_instantiate or type(RAISE)._can_instantiate)
def test_custom_sentinel():
    class TestSentinel(sentinel_base): __slots__ = ()
    a = TestSentinel()
    assert a.is_(a) and a.bound_to is None
    class qux: __slots__, grault = (), TestSentinel()
    assert f'{qux.grault.bound_to}.{qux.grault.back}'.endswith('qux.grault')
