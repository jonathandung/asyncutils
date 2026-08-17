_ = [None, False]
def get(_=_): return _[0]
def run(c, /, _=_): _[0] = c
def unset(_=_): _[0], r = None, _[0]; return r
def request_write_load_all(_=_): _[1] = True
def should_write_load_all(_=_): return _[1]
del _
