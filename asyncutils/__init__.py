# Copyright © 2026 Jonathan Dung. All rights reserved.
# SPDX-License-Identifier: MIT
# ruff: file-ignore[undocumented-public-package]
from sys import implementation as I, modules as M
match I.name:
    case 'cpython':
        if I.version < (3, 12): raise ImportError('asyncutils: CPython 3.12 or above required')
    case 'graalpy':
        if I.version[0] < 25: raise ImportError('asyncutils: GraalPy 25 (Python 3.12) or above required')
    case s: raise ImportError(f'asyncutils is neither tested in {s} nor currently planned to be')
from time import monotonic as T
def time_since_boot(t=T(), T=T): return round(T()-t, 7)*1000 # ruff: ignore[function-call-in-default-argument]
M['asyncutils._internal.log'] = __import__('logging').getLogger('asyncutils') # ty: ignore[invalid-assignment]
def __getattr__(n, /, _=globals()):
    from asyncutils._internal import initialize as I; (s := I.S).sort(); _.update(__getattr__=I.Module, __all__=I.a, submodules_map=I.s, all_symbols=s)
    try: return _[n]
    except KeyError: return I.Module(n)
from asyncutils.version import VersionInfo as V # ruff: ignore[module-import-not-at-top-of-file]
time_since_boot.__text_signature__, __hexversion__, console_preloaded_submodules = '()', int(__version__ := V('1.1.2')), (preloaded_submodules := frozenset(('constants', 'context', 'cli', 'exceptions', 'version'))).union(('base', 'config', 'console')) # ty: ignore[unresolved-attribute]
del V, I, T, M
