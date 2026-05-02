from sys import implementation as I, modules as M
if I.name != 'cpython': __import__('_warnings').warn('asyncutils is not yet tested in this python implementation', ImportWarning)
if I.version < (3, 12): raise ImportError('asyncutils currently only supports python 3.12 or above')
from time import monotonic as T
def time_since_boot(t=T(), T=T): return round(T()-t, 7)*1000 # noqa: B008
from asyncutils.version import VersionInfo as V
time_since_boot.__text_signature__, __hexversion__, console_preloaded_submodules = '()', int(__version__ := V('0.9.1')), (preloaded_submodules := frozenset(('config', 'constants', 'context', 'cli', 'exceptions', 'version'))).union(('base', 'console'))
def __getattr__(n, /, _=globals()):
    from asyncutils._internal import initialize as I; _.update(__getattr__=I.Module, __all__=I.a, submodules_map=I.s, __dir__=lambda _=I.S: _); del I
    try: return _[n]
    except KeyError: return __getattr__(n)
del V, I, T, M