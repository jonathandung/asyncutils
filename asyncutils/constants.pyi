'''Miscellaneous public constants.'''
from ._internal.types import Executor, RaiseType, SyncAwaitType, NoDefaultType
from _collections_abc import Callable
from threading import Lock
from typing import Final, Literal, NoReturn, Self, overload
__all__ = 'CLOSED', 'EXECUTORS_FROZENSET', 'HALF_OPEN', 'OPEN', 'POSSIBLE_EXECUTORS', 'RAISE', 'RECIP_E', 'SYNC_AWAIT', 'sentinel_base'
RECIP_E: Final[float]
'''The reciprocal of Euler's number, used by :func:`iters.aguessmin` and :func:`iters.aguessmax`.'''
POSSIBLE_EXECUTORS: Final[tuple[Executor, ...]]
'''A tuple of all possible executor names that can be passed to -e, in rough order of preference and popularity, which is also the order
in which the executor options appear in the CLI help.'''
EXECUTORS_FROZENSET: Final[frozenset[Executor]]
'''Equivalent to `frozenset(POSSIBLE_EXECUTORS)` to allow faster membership testing.'''
class sentinel_base:
    '''Base class for sentinel values.'''
    def __new__(cls, name: str=...) -> NoReturn: '''Remember to override this in stubs (change `NoReturn` to `Self`) if and only if your subclass can be instantiated by the user.'''
    def __reduce__(self) -> tuple[type[Self], tuple[str]]: '''Support for pickling.'''
    def __set_name__(self, owner: type, name: str, /) -> None: '''Bind the sentinel to a class and assign its name, if no arguments were passed to the constructor.'''
    def __init_subclass__(cls, lock_impl: Callable[[], Lock]=...) -> None: '''`lock_impl` is a callable that takes no arguments and returns a **synchronous** lock (e.g. :func:`_thread.allocate_lock`).'''
    @property
    def name(self) -> str: '''Fully qualified name of the sentinel, the only thing that identifies it uniquely. May not be present if impropertly instantiated.'''
    @property
    def is_private(self) -> bool: '''Whether the sentinel is private (name begins with underscore).'''
    @property
    def bound_to(self) -> str|None: '''The name of the class the sentinel is bound to, or `None` if there is none.'''
    @property
    def back(self) -> str|None: '''The unqualified name of the sentinel, or `None` if there is none.'''
    @overload
    def is_(self, other: Self, /) -> bool: ... # type: ignore[overload-overlap]
    @overload
    def is_(self, other: object, /) -> Literal[False]: ''':func:`operator.is_` for sentinels.'''
RAISE: Final[RaiseType]
'''Can be passed to some functions that are documented to support it, so that errors will be raised in the specified cases.'''
SYNC_AWAIT: Final[SyncAwaitType]
'''A possible value to :attr:`exceptions.Deadlock.noticer`, indicating the deadlock situation was found by :func:`util.sync_await`.'''
_NO_DEFAULT: Final[NoDefaultType]
'''Users are not meant to interact with this directly; only here for completeness.'''
CLOSED: Final[int]
'''The closed state of a circuit breaker.'''
HALF_OPEN: Final[int]
'''The half-open state of a circuit breaker.'''
OPEN: Final[int]
'''The open state of a circuit breaker.'''