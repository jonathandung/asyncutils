from .helpers import subscriptable as s
N = s(type('Namespace', (dict,), {'__getattr__': dict.__getitem__, '__setattr__': dict.__setitem__, '__delattr__': dict.__delitem__}))(log_to='STDERR', executor='thread', Q=0, V=0, quiet=False, basic_repl=False, max_memerrs=3, load_all=False, seed=None, debug=False)
if p := (E := __import__('os').environ).get(k := 'AUTILSCFGPATH', '').strip('"\''):
    import sys as S; S.audit('asyncutils/read_config', p)
    if not p.endswith(('.json', '.jsonl')): S.stderr.write('WARNING: AUTILSCFGPATH should point to a json file; proceeding anyway\n')
    with open(p.strip()) as f:
        if (t := type(f := __import__('json').load(f))) is not dict: raise TypeError(f'incorrent json format for asyncutils configuration; top-level structure should be an object, not {t.__name__!r}')
        if isinstance(v := f.pop('next_config', p), str): S.audit('asyncutils/set_next_config', p, v); E[k] = v
        elif v is None: S.audit('asyncutils/discontinue_config', p); del E[k]
        else: raise TypeError(f'key "next_config" in {p} should point to a string or null, not {v!r}; see format.json5')
        N.update(f)
    del S, f, v, t
del p, E, k, s