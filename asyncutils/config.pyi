'''Set up some module-global state and sentinels, and expose some user-specified flags.'''
from ._internal.prots import PartialInterface, Mark1, Mark2, ExcType
from concurrent.futures import Executor as _
from types import TracebackType
from typing import Final, Self, overload
__all__ = 'Debugging', 'Executor', 'basic_repl', 'debug', 'get_past_logs', 'loaded_all', 'logging_to', 'max_memory_errors', 'pdb', 'set_logger_level', 'silent'
class FaultyConfig(BaseException):
    '''Raised when the user specifies a configuration value that is of the wrong type or otherwise invalid. This is basically impossible to catch, since it is only raised during the import of this module.'''
    @overload
    def __init__(self: Mark1, key: str, wrong: str, correct: tuple[str, ...], /) -> None: ...
    @overload
    def __init__(self: Mark2, key: str, wrong: object, correct: type|tuple[type, ...], /) -> None: ...
    @property
    def key(self) -> str: ...
    @property
    @overload
    def wrong(self: Mark1) -> str: ...
    @property
    @overload
    def wrong(self: Mark2) -> object: ...
    @property
    @overload
    def correct(self: Mark1) -> tuple[str, ...]: ...
    @property
    @overload
    def correct(self: Mark2) -> type|tuple[type, ...]: ...
class Executor(_, PartialInterface):
    '''A class that implements the :pep:`3148` executor interface.

    .. note:: The exact class is determined at runtime by command-line arguments.
    .. tip:: Since instances of this class are only ever passed into :meth:`~asyncio.loop.run_in_executor`, nothing stops you from monkey-patching the event loop itself or policy thereof, and using a custom class that does not follow the interface, but that may be too hacky and fragile.
    .. tip:: If you know your application only uses a specific executor, import this symbol at runtime and import the actual class in the stub or in an ``if TYPE_CHECKING:`` block where applicable to help type checkers.
    '''
class Debugging:
    '''A context manager used to enter and exit debug mode, ensuring restoration of the original level if the level has not been modified externally within the context using :func:`set_logger_level`.'''
    @property
    def level(self) -> int: '''The current level of the :mod:`asyncutils` logger, as an integer.'''
    @property
    def orig_level(self) -> int|None: '''The original logger level as an integer, before this context was entered, or ``None`` if it was not.'''
    @property
    def orig_name(self) -> str|None: '''The original logger level name as a string, before this context was entered, or ``None`` if it was not.'''
    @property
    def entered(self) -> bool: '''Whether the context is entered.'''
    def __enter__(self) -> Self: '''Start debugging. More output is produced; where to depends on the user's own configuration, accessible via :data:`logging_to` and ``debug.level``.'''
    @overload
    def __exit__(self, exc_typ: ExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> None: ...
    @overload
    def __exit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> None: '''Stop debugging, restoring the output to its previous level if appropriate.'''
def set_logger_level(level: int) -> None: '''Set the level of the module-global logger to ``level``.'''
def get_past_logs() -> str: '''Return all stored logs as a string. Logs are stored iff :mod:`asyncutils` was started with ``-l MEMORY``, otherwise an empty string is returned.'''
debug: Final[Debugging]
'''A global instance of the :class:`Debugging` context manager. Initially entered iff the user specified ``-d`` or ``--debug`` when starting the program.'''
silent: Final[bool]
'''Whether the user requested to run the program with no banner and exit message in the REPL.'''
basic_repl: Final[bool]
'''Whether the user specified not to use the functions from ``_pyrepl`` to run the console.'''
max_memory_errors: Final[int]
'''Maximum number of memory errors that can occur before the console automatically exits. Negative iff there is no maximum.'''
loaded_all: Final[bool]
'''Whether all submodules of this module have been loaded.'''
pdb: Final[bool]
'''Whether the user specified to drop into the debugger on an unhandled exception in the REPL console.'''
logging_to: Final[str]
'''The name of (i.e. possibly relative path to) the log file currently used by this library as a string, with four exceptions:

* ``'NULL'``: no logging is taking place
* ``'MEMORY'``: the logs are not going to a physical file but can be retrieved by :func:`get_past_logs`
* ``'STDOUT'``: logging is going to :data:`sys.stdout`
* ``'STDERR'``: logging is going to :data:`sys.stderr` (following the default and fallback behaviour of :mod:`logging`)'''
