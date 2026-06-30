from concurrent.futures import Executor as _Executor
from asyncutils.config import *
def test_mod():
    assert issubclass(Executor, _Executor)
    assert isinstance(debug, Debugging)
    with debug:
        assert debug.level == 10
        assert debug.orig_level == 30
        assert debug.orig_name == 'WARNING'
        assert not get_past_logs()
        set_logger_level(20)
        assert debug.level == 20
    assert not silent
    assert not loaded_all
    assert not pdb
    assert logging_to == 'STDERR'
