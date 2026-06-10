'''Exports sentinels and public constants.'''
from ._internal.prots import Executor, RaiseType
from collections.abc import Callable
from threading import Lock
from typing import Final, Self
__all__ = 'EXECUTORS_FROZENSET', 'POSSIBLE_EXECUTORS', 'RAISE', 'RECIP_E', 'sentinel_base'
RECIP_E: Final[float]
'''The reciprocal of Euler's number, used by :func:`~asyncutils.iters.aguessmin` and :func:`~asyncutils.iters.aguessmax`.'''
POSSIBLE_EXECUTORS: Final[tuple[Executor, ...]]
'''A tuple of all possible executor names that can be passed to -e, in rough order of preference and popularity. Also the order in which the executor options appear in the CLI help.'''
EXECUTORS_FROZENSET: Final[frozenset[Executor]]
'''Equivalent to ``frozenset(POSSIBLE_EXECUTORS)``, so that there can be faster membership testing.'''
class sentinel_base:
    '''Base class for sentinel values. To support versions below Python 3.15, we cannot make use of the :pep:`661` built-in ``sentinel`` type, and this class offers extra methods anyway.'''
    def __new__(cls, name: str=...) -> Self: ...
    def __reduce__(self) -> tuple[type[Self], tuple[str]]: '''Support for pickling.'''
    def __set_name__(self, owner: type, name: str, /) -> None: '''Bind the sentinel to a class and assign its name, if no arguments were passed to the constructor.'''
    def __init_subclass__(cls, *, lock_impl: Callable[[], Lock]=...) -> None: '''``lock_impl`` is a callable that takes no arguments and returns a _synchronous_ lock (e.g. :func:`_thread.allocate_lock`).'''
    @property
    def name(self) -> str: '''Fully qualified name of the sentinel, the only thing that identifies it uniquely. May not be present if impropertly instantiated.'''
    @property
    def is_private(self) -> bool: '''Whether the sentinel is private; that is, the name begins with underscore.'''
    @property
    def bound_to(self) -> str|None: '''The name of the class the sentinel is bound to, or ``None`` if there is none.'''
    @property
    def back(self) -> str|None: '''The unqualified name of the sentinel, or ``None`` if there is none.'''
    @property
    def module(self) -> str: '''The name of the module the sentinel is defined in.'''
    def is_(self, other: object, /) -> bool: ''':func:`operator.is_` for sentinels.'''
RAISE: Final[RaiseType]
'''Can be passed to some functions that are documented to support it, so that errors will be raised in the specified cases.'''
