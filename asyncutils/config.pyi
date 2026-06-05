'''Set up some module-global state and sentinels, and expose some user-specified flags.'''
from ._internal.types import PartialInterface, ExcType
from concurrent.futures._base import Executor as _
from types import TracebackType
from typing import Final, Self, overload
__all__ = 'Executor', 'basic_repl', 'debug', 'debugging', 'get_past_logs', 'loaded_all', 'logging_to', 'max_memerrs', 'pdb', 'set_logger_level', 'silent'
class Executor(_, PartialInterface):
    '''A class that implements the :pep:`3148` executor interface.

    .. note:: The exact class is determined at runtime by command-line arguments.
    .. tip::
      Since instances of this class are only ever passed into :meth:`~asyncio.loop.run_in_executor`, nothing stops you from monkey-patching the event loop itself
      or policy thereof, and using a custom class that does not follow the interface, but that may be too hacky and fragile.
    .. tip::
      If you know your application only uses a specific executor, import this symbol at runtime and import the actual class in the stub or in an
      `if TYPE_CHECKING:` block where applicable to help type checkers.'''
class debugging:
    '''A context manager used to enter and exit debug mode, ensuring restoration of the original level if the level has not been modified externally within the context using :func:`set_logger_level`.'''
    @property
    def level(self) -> int: '''The current level of the :mod:`asyncutils` logger, as an integer.'''
    @property
    def orig_level(self) -> int|None: '''The original logger level as an integer, before this context was entered, or ``None`` if it was not.'''
    @property
    def orig_name(self) -> str|None: '''The original logger level name as a string, before this context was entered, or ``None`` if it was not.'''
    @property
    def entered(self) -> bool: '''Whether the context is entered.'''
    def __enter__(self) -> Self: '''Start debugging. More output is produced; where to depends on the user's own configuration, accessible via :data:`logging_to` and :attr:`debug.level`.'''
    @overload
    def __exit__(self, exc_typ: ExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> None: ...
    @overload
    def __exit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> None: '''Stop debugging, restoring the output to its previous level if appropriate.'''
def set_logger_level(level: int) -> None: '''Set the level of the module-global logger to ``level``.'''
def get_past_logs() -> str: '''Return all stored logs as a string. Logs are only stored if asyncutils was started with ``-l MEMORY``, otherwise an empty string is returned.'''
debug: Final[debugging]
'''A global instance of the :class:`debugging` context manager. Initially entered if and only if the user specified ``-d`` or ``--debug`` when starting the program.'''
silent: Final[bool]
'''Whether the user requested to run the program with no banner and exit message in the REPL.'''
basic_repl: Final[bool]
'''Whether the user specified not to use the functions from :mod:`_pyrepl` to run the console.'''
max_memerrs: Final[int]
'''Maximum number of memory errors that can occur before the console automatically exits. Negative if and only if there is no maximum.'''
loaded_all: Final[bool]
'''Whether all submodules of this module have been loaded.'''
pdb: Final[bool]
'''Whether the user specified to drop into the debugger on an unhandled exception in the REPL console.'''
logging_to: Final[str]
'''The name (path; possibly relative) of the log file currently used by this library as a string, with four exceptions:

* `'NULL'`: no logging is taking place
* `'MEMORY'`: the logs are not going to a physical file but can be retrieved by :func:`get_past_logs`
* `'STDOUT'`: logging is going to :data:`sys.stdout`
* `'STDERR'`: logging is going to :data:`sys.stderr` (following the default and fallback behaviour of :mod:`logging`)'''
