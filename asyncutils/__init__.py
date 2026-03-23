from sys import implementation as I
if I.name != 'cpython': raise ImportError('asyncutils only supports cpython')
if I.version < (3, 14): raise ImportError('asyncutils currently only supports python 3.14 or above')
from .version import VersionInfo as V
__hexversion__, preloaded_submodules = int(__version__ := V(0, 8, 16)), frozenset(('config', 'exceptions', 'version'))
def __getattr__(name, /, g=globals()):
    from ._internal import initialize as I; g.update(__getattr__=I.module, __all__=I.a, __dir__=lambda: __all__, submodules_map=I.s); del I # noqa: F821 # type: ignore
    try: return g[name]
    except KeyError: return __getattr__(name)
del V, I
