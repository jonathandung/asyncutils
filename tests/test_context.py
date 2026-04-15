# type: ignore
import pytest
from asyncutils import context
def test_mod():
    with pytest.raises(TypeError): context.Context(0.0)
    with pytest.raises(AttributeError): context.Context().foo = None
    with pytest.raises(TypeError): context.setcontext(None)
    ctx = context.getcontext()
    assert isinstance(ctx, context.Context)
    assert ctx is context.getcontext()
    assert ctx.LEAKY_BUCKET_DEFAULT_EXT_CAN_SET_FACTOR and ctx.RWLOCK_DEFAULT_PREFER_WRITERS
    assert ctx is not context.Context()