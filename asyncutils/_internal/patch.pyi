'''Utilities to patch various things, from function signatures to annoying warnings emitted by asyncio and python itself.'''
from typing import Final
from .protocols import SigPatcher
def patch_asyncio_warnings() -> None: '''Equivalent to `logging.getLogger('asyncio').disabled = True`.'''
def patch_unawaited_coroutine_warnings() -> None: '''Silence the `RuntimeWarning`s emitted when an unawaited coroutine is garbage collected.'''
def patch_properties[T: type](cls: T, /) -> T: '''Utility function for `version.VersionInfo` and `version.VersionDelta`; adds `major`, `minor` and `patch` properties.'''
patch_function_signatures: Final[SigPatcher]
'''Hide the original signature of functions defined in the top level of a (sub-)module with new signatures.
Useful when, for example, dependency injection, unrepresentable sentinels, mutable defaults and other arity shenanigans are used.'''
patch_method_signatures: Final[SigPatcher]
'''`patch_function_signatures`, but for instance methods.
A `self` parameter (positional-only) is automatically prepended to each of the passed signatures.'''
patch_classmethod_signatures: Final[SigPatcher]
'''`patch_function_signatures`, but for class methods.
A `cls` parameter (positional-only) is automatically prepended to each of the passed signatures.'''