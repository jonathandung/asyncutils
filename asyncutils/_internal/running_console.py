# type: ignore
_s = type('info', (), {'__slots__': ('_c', '_s'), '__init__': lambda self: setattr(self, '_c', None) or setattr(self, '_s', False)})()
def __getattr__(name, /): return getattr(_get_(), name)
def _get_(_s=_s): return _s._c
def _set_(c, /, _s=_s): _s._c = c
def _unset_(_s=_s): _s._c, r = None, _s._c; return r
def _request_write_load_all_(_s=_s): _s._s = True
def _should_write_load_all_(_s=_s): return _s._s
del _s