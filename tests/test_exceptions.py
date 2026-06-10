from pytest import RaisesGroup
from asyncutils.exceptions import unnest, unnest_reverse, wrap_exc, unwrap_exc, exception_occurred
def test_unnest():
    with RaisesGroup(ValueError, TypeError): raise BaseExceptionGroup('', tuple(unnest(BaseExceptionGroup('', (RuntimeError('a'), ValueError('b'), TypeError('c'), SystemExit('d'))), filter_out=RuntimeError, raise_critical=False, keep=Exception)))
def test_runnest():
    with RaisesGroup(TypeError, ValueError): raise BaseExceptionGroup('', tuple(unnest_reverse(BaseExceptionGroup('', (RuntimeError('a'), ValueError('b'), TypeError('c'), SystemExit('d'))), filter_out=RuntimeError, raise_critical=False, keep=Exception)))
def test_ewrap():
    wrapper = wrap_exc(e := IndexError('a'))
    assert unwrap_exc(wrapper) is e
    assert exception_occurred(wrapper)
