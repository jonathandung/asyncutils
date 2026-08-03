def __getattr__(n, /, g=globals(), s=frozenset(__all__ := ('compat', 'helpers', 'log', 'patch', 'running_console', 'submodules')).union(('parsed', 'initialize', 'py312', 'py313', 'unparsed')), t='from asyncutils._internal.%s import __class__', m=__import__('sys').modules, p='asyncutils._internal.'): # ruff: ignore[function-call-in-default-argument]
    if n not in s: raise AttributeError(f'module {__name__!r} has no attribute {n!r}')
    exec(t%n, g); return m[p+n] # ruff: ignore[exec-builtin]
