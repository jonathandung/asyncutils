from sys import implementation as I, modules as M
if I.version < (3, 12): raise ImportError('asyncutils: Python 3.12 or above required')
from time import monotonic as T
def time_since_boot(t=T(), T=T): return round(T()-t, 7)*1000 # noqa: B008
if I.name != 'cpython': __import__('_warnings').warn('asyncutils is neither tested in this Python implementation nor currently planned to be', ImportWarning)
M['asyncutils._internal.log'] = __import__('logging').getLogger('asyncutils') # ty: ignore[invalid-assignment]
def __getattr__(n, /, _=globals()):
    from asyncutils._internal import initialize as I; _.update(__getattr__=I.Module, __all__=I.a, submodules_map=I.s, __dir__=lambda _=I.S: _)
    try: return _[n]
    except KeyError: return I.Module(n) # pragma: no cover
from asyncutils.version import VersionInfo as V
time_since_boot.__text_signature__, __hexversion__, console_preloaded_submodules = '()', int(__version__ := V('0.9.11')), (preloaded_submodules := frozenset(('constants', 'context', 'cli', 'exceptions', 'version'))).union(('base', 'config', 'console')) # ty: ignore[unresolved-attribute]
del V, I, T, M