'''Utilities to patch various things, from function signatures to annoying warnings emitted by :mod:`asyncio` and python itself.'''
from .types import SigPatcher
from typing import Final
def patch_asyncio_warnings() -> None: '''Equivalent to `logging.getLogger('asyncio').disabled = True`.'''
def patch_unawaited_coroutine_warnings() -> None: '''Silence instances of :exc:`RuntimeWarning` emitted when an unawaited coroutine is garbage collected.'''
patch_function_signatures: Final[SigPatcher]
'''Hide the original signature of functions defined in the top level of a (sub-)module with new signatures.
Useful when, for example, dependency injection, unrepresentable sentinels, mutable defaults and other arity shenanigans are used.'''
patch_method_signatures: Final[SigPatcher]
''':func:`patch_function_signatures`, but for instance methods.
A `self` parameter (positional-only) is automatically prepended to each of the passed signatures.'''
patch_classmethod_signatures: Final[SigPatcher]
''':func:`patch_function_signatures`, but for class methods. `classmethod` objects, though not callable, are supported.
A `cls` parameter (positional-only) is automatically prepended to each of the passed signatures.'''
xsig: Final[str]
'''The signature of :meth:`__exit__` and :meth:`__aexit__` as a signature-patcher-compatible string.'''