from .version import VersionInfo as V
__hexversion__ = int(__version__ := V(0, 8, 2))
def __getattr__(name, /, g=globals()):
    if name == '__git_version__':
        try: g[name] = r = __import__('subprocess').check_output(('git', 'rev-parse', 'HEAD'), text=True).strip(); return r
        except: raise RuntimeError('failed to get git commit hash') from None
    from ._internal import initialize as I; g.update(__getattr__=I.module, __all__=I.a, __dir__=I.g, submodules_map=I.s)
    try: return g[name]
    except KeyError: return __getattr__(name)
del V