from pytest import RaisesGroup
from asyncutils.exceptions import unnest, unnest_reverse
def test_unnest():
    with RaisesGroup(ValueError, TypeError): raise BaseExceptionGroup('', tuple(unnest(BaseExceptionGroup('', (RuntimeError('a'), ValueError('b'), TypeError('c'), SystemExit('d'))), filter_out=RuntimeError, raise_critical=False, keep=Exception)))
def test_unnest_reverse():
    with RaisesGroup(TypeError, ValueError): raise BaseExceptionGroup('', tuple(unnest_reverse(BaseExceptionGroup('', (RuntimeError('a'), ValueError('b'), TypeError('c'), SystemExit('d'))), filter_out=RuntimeError, raise_critical=False, keep=Exception)))