import math, sys, pickle, pytest
from asyncutils.constants import *
from asyncutils.constants import _NO_DEFAULT
def test_misc():
    assert 1/math.e == RECIPROCAL_E # noqa: RUF069
    assert math.e == 1/RECIPROCAL_E # noqa: RUF069
    assert EXECUTORS_FROZENSET.issuperset(POSSIBLE_EXECUTORS)
    assert EXECUTORS_FROZENSET.issubset(POSSIBLE_EXECUTORS)
    assert RAISE.is_(RAISE)
    assert RAISE.name == str(RAISE) == 'asyncutils.constants.RAISE'
    assert pickle.loads(pickle.dumps(RAISE)) is RAISE
    assert not RAISE.is_private
    assert _NO_DEFAULT.is_private
@pytest.fixture
def ctxmgr(): return pytest.raises(TypeError, match=r"cannot instantiate 'asyncutils\.constants\..*'")
@pytest.mark.parametrize('cls', (SentinelBase, type(RAISE)))
def test_sentinels(cls, ctxmgr):
    with ctxmgr: cls()
    with ctxmgr: cls('foo')
    with ctxmgr: cls('spam.bar')
    with ctxmgr:
        class Foo: __slots__, baz = (), cls()
    with ctxmgr:
        class Bar: __slots__, quux = (), cls('Bar.quux')
    assert not SentinelBase._can_instantiate
    assert not type(RAISE)._can_instantiate
def test_custom_sentinel():
    class TestSentinel(SentinelBase): __slots__ = ()
    a = TestSentinel()
    assert a.is_(a)
    assert a.bound_to is None
    class qux: __slots__, ham = (), TestSentinel()
    assert f'{qux.ham.bound_to}.{qux.ham.back}'.endswith('qux.ham')
    with pytest.raises(AttributeError, match="Can't get local object .*") if sys.version_info < (3, 13) else pytest.raises(pickle.PicklingError, match="Can't pickle local object .*"): pickle.dumps(qux.ham)
