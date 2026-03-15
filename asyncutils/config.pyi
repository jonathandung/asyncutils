'''Set up some module-global state and sentinels, and expose some user-specified flags.'''
from ._internal.protocols import ValidExcType, PartialInterface
from _collections_abc import Callable
from concurrent.futures._base import Executor as _
from typing import Final, Self, NoReturn, Final, final, type_check_only, overload
from types import TracebackType
from random import Random
from threading import Lock
__all__ = 'debugging', 'debug', 'sentinel_base', 'RAISE', 'SYNC_AWAIT', 'silent', 'Executor', 'set_logger_level', 'basic_repl', 'loaded_all', 'get_past_logs', 'logging_to'
class Executor(_, PartialInterface): '''A class that implements the PEP 3148 Executor interface. The exact class is determined at runtime by command-line arguments.'''
class debugging:
    '''A context manager used to enter and exit debug mode, ensuring restoration of the original level if the level has not been modified externally
    (using `set_logger_level`) within the context.'''
    @property
    def level(self) -> int: '''The current level of the asyncutils logger, as an integer.'''
    @property
    def orig_level(self) -> int|None: '''The original logger level as an integer, before this context was entered, or None if it was not.'''
    @property
    def orig_name(self) -> str|None: '''The original logger level name as a string, before this context was entered, or None if it was not.'''
    def __enter__(self) -> Self: '''Start debugging. More output is produced; where to depends on the user's own configuration, accessible via `logging_to` and `debug.level`.'''
    @overload
    def __exit__(self, exc_typ: ValidExcType, exc_val: BaseException, exc_tb: TracebackType|None, /) -> None: '''Stop debugging, restoring the output to its previous level if appropriate.'''
    @overload
    def __exit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> None: ...
class sentinel_base:
    '''Base class for sentinel values.'''
    def __new__(cls, name: str=...) -> NoReturn: '''Remember to override this in stubs (change NoReturn to Self) if your subclass can be instantiated by the user.'''
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def __reduce__(self) -> tuple[type[Self], tuple[str]]: ...
    def __set_name__(self, owner: type, name: str, /) -> None: '''Bind the sentinel to a class and assign its name, if no arguments were passed to the constructor.'''
    def __init_subclass__(cls, lock_impl: Callable[[], Lock]=...) -> None: ...
    @property
    def name(self) -> str: '''Fully qualified name of the sentinel, the only thing that identifies it uniquely. May not be present if impropertly instantiated.'''
    @property
    def is_private(self) -> bool: '''Whether the sentinel is private (name begins with underscore).'''
    @property
    def bound_to(self) -> str|None: '''The name of the class the sentinel is bound to, None if there is none.'''
@final
@type_check_only
class _sentinel(sentinel_base):
    '''Sentinels for this module, internal or public.'''
    def __reduce__(self) -> str: '''These sentinels are accessible in the top level of the asyncutils.config namespace.'''
def set_logger_level(level: int) -> None: '''Set the level of the module-global logger.'''
def get_past_logs() -> str: '''Returns all stored logs as a string. Logs are only stored if asyncutils was started with -l MEMORY, otherwise an empty string is returned.'''
RAISE: Final[_sentinel]
'''Can be passed to some functions that are documented to support it, so that errors will be raised in the specified cases.'''
SYNC_AWAIT: Final[_sentinel]
'''A possible value to Deadlock.noticer, indicating the deadlock situation was found by the sync_await function.'''
_NO_DEFAULT: Final[_sentinel]
'''Users are not meant to interact with this directly.'''
debug: Final[debugging]
'''A global instance of the debugging context manager.'''
silent: Final[bool]
'''Whether the user requested to run the program with no banner and exit message in the REPL.'''
basic_repl: Final[bool]
'''Whether the user specified not to use the functions from _pyrepl to run the console.'''
max_memerrs: Final[int]
'''Maximum number of memory errors that can occur before the console automatically exits. Negative if there is no maximum.'''
loaded_all: Final[bool]
'''Whether all submodules of this module have been loaded.'''
_randinst: Final[Random]
'''The random number generator (instance of random.Random) used by this module.'''
logging_to: Final[str]
'''A string indicating where the logging output of the program is going. 'NULL' means no logging is taking place, 'MEMORY' means the logs are
not going to a file but can be retrieved from get_past_logs, 'STDOUT' means logging is going to stdout and 'STDERR' means it is going to stderr.
Otherwise, it is the filename, which may be an integer (file descriptor) or bytestring in extremely rare cases the caller need not prepare for.'''