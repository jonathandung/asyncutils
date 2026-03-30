from _collections_abc import Callable
from threading import Lock
from typing import Final, NoReturn, Literal, Self, final, type_check_only, overload
__all__ = 'RECIP_E', 'RAISE', 'SYNC_AWAIT', 'sentinel_base'
RECIP_E: Final[float]
class sentinel_base:
    '''Base class for sentinel values.'''
    def __new__(cls, name: str=...) -> NoReturn: '''Remember to override this in stubs (change NoReturn to Self) if and only if your subclass can be instantiated by the user.'''
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def __reduce__(self) -> tuple[type[Self], tuple[str]]: '''Support for pickling.'''
    def __set_name__(self, owner: type, name: str, /) -> None: '''Bind the sentinel to a class and assign its name, if no arguments were passed to the constructor.'''
    def __init_subclass__(cls, lock_impl: Callable[[], Lock]=...) -> None: '''`lock_impl` is a callable that takes no arguments and returns a **synchronous** lock (e.g. `_thread.allocate_lock`).'''
    @property
    def name(self) -> str: '''Fully qualified name of the sentinel, the only thing that identifies it uniquely. May not be present if impropertly instantiated.'''
    @property
    def is_private(self) -> bool: '''Whether the sentinel is private (name begins with underscore).'''
    @property
    def bound_to(self) -> str|None: '''The name of the class the sentinel is bound to, None if there is none.'''
    @overload
    def is_(self, other: Self, /) -> bool: ... # type: ignore[overload-overlap]
    @overload
    def is_(self, other: object, /) -> Literal[False]: ...
@final
@type_check_only
class _sentinel(sentinel_base):
    '''Sentinels for this module, internal or public. Not exported.'''
    def __reduce__(self) -> str: '''These sentinels are accessible in the top level of the asyncutils.config namespace.''' # type: ignore[override]
RAISE: Final[_sentinel]
'''Can be passed to some functions that are documented to support it, so that errors will be raised in the specified cases.'''
SYNC_AWAIT: Final[_sentinel]
'''A possible value to Deadlock.noticer, indicating the deadlock situation was found by the sync_await function.'''
_NO_DEFAULT: Final[_sentinel]
'''Users are not meant to interact with this directly.'''