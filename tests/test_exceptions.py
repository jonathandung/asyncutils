from pytest import raises, RaisesGroup
from asyncutils.exceptions import *
def test_unnest():
    with RaisesGroup(ValueError, TypeError): raise BaseExceptionGroup('', tuple(unnest(BaseExceptionGroup('', (RuntimeError('a'), ValueError('b'), TypeError('c'), SystemExit('d'))), filter_out=RuntimeError, raise_critical=False, keep=Exception)))
    with RaisesGroup(TypeError, ValueError): raise BaseExceptionGroup('', tuple(unnest_reverse(BaseExceptionGroup('', (RuntimeError('a'), ValueError('b'), TypeError('c'), SystemExit('d'))), filter_out=RuntimeError, raise_critical=False, keep=Exception)))
def test_wrap_exc():
    wrapper = wrap_exc(e := IndexError('a'))
    assert unwrap_exc(wrapper) is e
    assert exception_occurred(wrapper)
def test_critical():
    with raises(Critical, match='critical error occurred or user attempted to terminate the program', check=lambda e: e.__cause__ is None and e.exc is e.__context__ and isinstance(e.exc, KeyboardInterrupt) and e.exc.args == ('a',) and isinstance(e.exc, CRITICAL)): # noqa: PT012
        try: raise KeyboardInterrupt('a')
        except: raise Critical # noqa: E722
