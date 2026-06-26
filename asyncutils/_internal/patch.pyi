'''Utilities to patch various things, from function signatures to annoying warnings emitted by :mod:`asyncio` and python itself.'''
from .prots import SigPatcherArg
from typing import Final
def patch_aio_logs() -> None: '''Equivalent to ``logging.getLogger('asyncio').disabled = True``.'''
def patch_unawaited_coroutine_warnings() -> None: '''Silence instances of :exc:`RuntimeWarning` emitted when an unawaited coroutine is garbage collected.'''
def patch_function_signatures(*to_patch: SigPatcherArg, follow_wrapped: bool=...) -> None:
    '''| Hide the original signature of functions defined in the top level of a (sub-)module with new signatures.
    | Each positional argument is a tuple of the form ``(target_func, signature)``, where ``signature`` looks like the portion of a function declaration within the parentheses opening to the right of the function name.
    | If ``follow_wrapped`` is ``True``, the original signature is taken from the first wrapped function with a ``__text_signature__`` attribute or the innermost function instead of the wrapper, if applicable.
    | Wrapped functions are found using :attr:`~method.__func__` and ``__wrapped__``, and it is assumed in the implementation that every level only has one of these, otherwise unpredictable behaviour may arise.
    | Useful when, for example, dependency injection, unrepresentable sentinels, mutable defaults and other arity shenanigans are used.
    '''
def patch_method_signatures(*to_patch: SigPatcherArg, follow_wrapped: bool=...) -> None:
    '''| :func:`patch_function_signatures`, but for instance methods.
    | A ``self`` parameter (positional-only) is automatically prepended to each of the passed signatures.
    '''
def patch_classmethod_signatures(*to_patch: SigPatcherArg, follow_wrapped: bool=...) -> None:
    '''| :func:`patch_function_signatures`, but for class methods.
    | :class:`classmethod` objects, though not callable, are supported.
    | A ``cls`` parameter (positional-only) is automatically prepended to each of the passed signatures.
    '''
exit_sig: Final[str]
'''The signature of :meth:`~object.__exit__` and :meth:`~object.__aexit__` as a signature-patcher-compatible string. You would usually only pass this to :func:`patch_method_signatures`.'''
