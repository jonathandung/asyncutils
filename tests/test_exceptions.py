from pytest import raises, RaisesGroup
from asyncutils import empty_agen
from asyncutils.exceptions import *
from tests.conftest import mk
from warnings import catch_warnings, warn
def test_unnest():
    with RaisesGroup(ValueError, TypeError, match='msg'): raise BaseExceptionGroup('msg', tuple(unnest(BaseExceptionGroup('', (RuntimeError('a'), ValueError('b'), TypeError('c'), SystemExit('d'))), filter_out=RuntimeError, raise_critical=False, keep=Exception)))
    with RaisesGroup(TypeError, ValueError, match='msg'): raise BaseExceptionGroup('msg', tuple(unnest_reverse(BaseExceptionGroup('', (RuntimeError('a'), ValueError('b'), TypeError('c'), SystemExit('d'))), filter_out=RuntimeError, raise_critical=False, keep=Exception)))
def test_wrap_exc():
    wrapper = wrap_exc(e := IndexError('a'))
    assert unwrap_exc(wrapper) is e
    assert exception_occurred(wrapper)
def test_critical():
    with raises(Critical, match='critical error occurred or user attempted to terminate the program', check=lambda e: e.__cause__ is None and e.exc is e.__context__ and isinstance(e.exc, KeyboardInterrupt) and e.exc.args == ('a',) and isinstance(e.exc, CRITICAL)): # noqa: PT012
        try: raise KeyboardInterrupt('a')
        except: raise Critical # noqa: E722
def test_raise_exc():
    def check(e):
        n, = e.__notes__
        assert n == 'note'
        with raises(KeyboardInterrupt, match='cause'): raise e.__cause__
        return True
    with raises(ValueError, match='message', check=check): raise_exc(ValueError, 'message', cause=KeyboardInterrupt('cause'), notes='note')
@mk
async def test_ignore_errors():
    with ignore_valerrs: raise ValueError('foo')
    async with ignore_typeerrs: raise type('TypeError', (TypeError,), {})('bar')
    with ignore_all: raise SystemError('baz')
    async with ignore_typical: 1/0
    with ignore_stop_iteration.excluding(BytesWarning): next(iter(int, 0))
    async with ignore_warnings.combined(ignore_stop_async_iteration): await anext(empty_agen())
    with raises(KeyboardInterrupt, match='qux'), ignore_noncritical: raise KeyboardInterrupt('qux')
@mk
async def test_warning_to_error():
    with raises(UserWarning, match='foo'):
        async with WarningToError(UserWarning): warn('foo', stacklevel=2)
    with raises(DeprecationWarning, match='bar'), WarningToError(): warn('bar', type('DeprecationWarning', (DeprecationWarning,), {}), 2)
    with WarningToError(), catch_warnings(action='ignore', category=PendingDeprecationWarning): warn('baz', PendingDeprecationWarning, 2)
