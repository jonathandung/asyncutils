import math, pickle, sys, pytest
from asyncutils.constants import *
from asyncutils.constants import _NO_DEFAULT
t = type(NO_COALESCE)
def test_misc():
    assert 1/math.e == RECIPROCAL_E
    assert math.e == 1/RECIPROCAL_E
    assert EXECUTORS_FROZENSET.issuperset(POSSIBLE_EXECUTORS)
    assert EXECUTORS_FROZENSET.issubset(POSSIBLE_EXECUTORS)
    assert _NO_DEFAULT.is_private
    assert type(_NO_DEFAULT) is type(RAISE) is t
    with pytest.raises(TypeError, match='cannot subclass the type of asyncutils-internal sentinels'): type('', (t,), {}) # ty: ignore[unsupported-dynamic-base]
@pytest.mark.parametrize('s', (RAISE, NO_COALESCE))
def test_public(s):
    assert s.name == str(s) == 'asyncutils.constants.'+s.back
    assert pickle.loads(pickle.dumps(s)) is s
    assert not s.is_private
@pytest.mark.parametrize('cls', (SentinelBase, t))
def test_sentinels(cls):
    c = pytest.raises(TypeError, match=r"cannot instantiate 'asyncutils\.constants\..*'")
    with c: cls()
    with c: cls('foo')
    with c: cls('spam.bar')
    with c:
        class Foo: __slots__, baz = (), cls()
    with c:
        class Bar: __slots__, quux = (), cls('Bar.quux')
    assert not SentinelBase._can_instantiate # ty: ignore[unresolved-attribute]
    assert not t._can_instantiate # ty: ignore[unresolved-attribute]
def test_custom_sentinel():
    class TestSentinel(SentinelBase): __slots__ = ()
    a = TestSentinel()
    assert a.bound_to is None
    class qux: __slots__, ham = (), TestSentinel()
    assert f'{qux.ham.bound_to}.{qux.ham.back}'.endswith('qux.ham')
    with pytest.raises(AttributeError) if sys.version_info < (3, 13) or sys.implementation.name == 'graalpy' else pytest.raises(pickle.PicklingError, match="Can't pickle local object .*"): pickle.dumps(qux.ham)
