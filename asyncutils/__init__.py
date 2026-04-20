from sys import implementation as I
if I.name != 'cpython': __import__('_warnings').warn('asyncutils is not yet tested in this python implementation', ImportWarning)
if I.version < (3, 12): raise ImportError('asyncutils currently only supports python 3.12 or above')
from time import monotonic as T
def time_since_boot(t=T(), T=T): return (T()-t)*1000 # noqa: B008
from .version import VersionInfo as V
__hexversion__, console_preloaded_submodules = int(__version__ := V('0.8.26')), (preloaded_submodules := frozenset(('config', 'constants', 'context', 'exceptions', 'version'))).union(('base', 'cli', 'console'))
def __getattr__(name, /, _=globals()):
    from ._internal import initialize as I; _.update(__getattr__=I.Module, __all__=(a := I.a), __dir__=lambda a=a: a, submodules_map=I.s); del I
    try: return _[name]
    except KeyError: return __getattr__(name)
del V, I, T