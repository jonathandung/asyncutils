import pytest
from asyncutils import event_loop
from asyncutils.context import *
@pytest.fixture
def ctx(): return getcontext()
def test_essential(ctx):
    with pytest.raises(AttributeError): Context().foo = None
    with pytest.raises(TypeError): setcontext(None)
    assert isinstance(ctx, Context)
    assert ctx is getcontext()
    assert ctx.LEAKY_BUCKET_DEFAULT_EXT_CAN_SET_FACTOR
    assert ctx['RWLOCK_DEFAULT_PREFER_WRITERS']
    assert ctx is not Context()
    assert all_contextual_consts == frozenset(Context.__slots__)
    assert eval(str(ctx), d := {'__name__': 'asyncutils.context', 'Context': Context}) == eval(repr(ctx), d) == ctx
    d = ctx.asdict()
    assert 'EVENT_LOOP_BASE_FLAGS' in d
    d['TIMER_DEFAULT_PRECISION'] = 4
    assert ctx.TIMER_DEFAULT_precision == 7
    assert ctx['SOCKET_TRANSPORT_limits'] == (2048, 8192)
    assert len(event_loop.Flags) == 16
    assert len(event_loop.State) == 4
def test_contextual_behaviour(ctx):
    man = ctx.ascurctx(event_loop_base_flags=5)
    assert type(man) is NonReusableLocalContext
    with man as c:
        assert c is not ctx
        assert isinstance(c, Context)
        evl = event_loop(**{event_loop.Flags(1)._name_.lower(): False})
        assert evl._flags == 4
        evl.clear_flags(3)
        assert evl._flags == hash(evl) == 0
        evl.factory_reset()
        assert evl._flags == 5
        evl = evl.copy_flags()
    assert evl._flags == 5
    evl.factory_reset()
    assert evl._flags == 0
    assert ctx.EVENT_LOOP_BASE_FLAGS == 0
    with LocalContext(aItEr_To_GeN_dEfAuLt_StRiCt=True) as c:
        assert getcontext() is c
        assert c.AITER_TO_GEN_DEFAULT_STRICT
    assert not getcontext().AITER_TO_GEN_DEFAULT_STRICT
