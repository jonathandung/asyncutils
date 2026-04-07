from sys import implementation as I
if I.name != 'cpython': raise ImportError('asyncutils only supports cpython')
if I.version < (3, 12): raise ImportError('asyncutils currently only supports python 3.12 or above')
from time import monotonic as T
def time_since_boot(t=T(), T=T): return (T()-t)*1000
from .version import VersionInfo as V
__hexversion__, preloaded_submodules = int(__version__ := V('0.8.22')), frozenset(('config', 'constants', 'exceptions', 'version'))
def __getattr__(name, /, g=globals()):
    from ._internal import initialize as I; g.update(__getattr__=I.module, __all__=(a := I.a), __dir__=lambda a=a: a, submodules_map=I.s); del I
    try: return g[name]
    except KeyError: return __getattr__(name)
del V, I, T