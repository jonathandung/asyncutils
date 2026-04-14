from concurrent.futures._base import Executor as _Executor
from asyncutils.config import *
def test_mod():
    assert issubclass(Executor, _Executor)
    assert isinstance(debug, debugging)
    assert debug.level == 10
    assert debug.orig_level == 30
    assert debug.orig_name == 'WARNING'
    assert logging_to == 'STDERR'
    assert not get_past_logs()