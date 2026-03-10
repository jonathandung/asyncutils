from .version import VersionInfo as V
__hexversion__, preloaded_submodules = int(__version__ := V(0, 8, 4)), frozenset(('config', 'exceptions', 'version'))
def __getattr__(name, /, g=globals()):
    from ._internal import initialize as I; g.update(__getattr__=I.module, __all__=I.a, __dir__=I.g, submodules_map=I.s)
    try: return g[name]
    except KeyError: return __getattr__(name)
del V