_ = [None, False]
def __getattr__(name, /): return getattr(_get_(), name)
def _get_(_=_): return _[0]
def _set_(c, /, _=_): _[0] = c
def _unset_(_=_): _[0], r = None, _[0]; return r
def _request_write_load_all_(_=_): _[1] = True
def _should_write_load_all_(_=_): return _[1]
del _