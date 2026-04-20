'''Set up some module-global state and sentinels, and expose some user-specified flags.'''
from ._internal.types import PartialInterface, ValidExcType
from concurrent.futures._base import Executor as _
from random import Random
from types import TracebackType
from typing import Final, Self, overload
__all__ = 'Executor', 'basic_repl', 'debug', 'debugging', 'get_past_logs', 'loaded_all', 'logging_to', 'set_logger_level', 'silent'
class Executor(_, PartialInterface): '''A class that implements the PEP 3148 Executor interface. The exact class is determined at runtime by command-line arguments.'''
class debugging:
    '''A context manager used to enter and exit debug mode, ensuring restoration of the original level if the level has not been modified externally
    within the context (using :func:`set_logger_level`).'''
    @property
    def level(self) -> int: '''The current level of the `asyncutils` logger, as an integer.'''
    @property
    def orig_level(self) -> int|None: '''The original logger level as an integer, before this context was entered, or None if it was not.'''
    @property
    def orig_name(self) -> str|None: '''The original logger level name as a string, before this context was entered, or None if it was not.'''
    @property
    def entered(self) -> bool: '''Whether the context is entered.'''
    def __enter__(self) -> Self: '''Start debugging. More output is produced; where to depends on the user's own configuration, accessible via :data:`logging_to` and :attr:`debug.level`.'''
    @overload
    def __exit__(self, exc_typ: ValidExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> None: ...
    @overload
    def __exit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> None: '''Stop debugging, restoring the output to its previous level if appropriate.'''
def set_logger_level(level: int) -> None: '''Set the level of the module-global logger.'''
def get_past_logs() -> str: '''Returns all stored logs as a string. Logs are only stored if asyncutils was started with -l MEMORY, otherwise an empty string is returned.'''
debug: Final[debugging]
'''A global instance of the :class:`debugging` context manager.'''
silent: Final[bool]
'''Whether the user requested to run the program with no banner and exit message in the REPL.'''
basic_repl: Final[bool]
'''Whether the user specified not to use the functions from :mod:`_pyrepl` to run the console.'''
max_memerrs: Final[int]
'''Maximum number of memory errors that can occur before the console automatically exits. Negative if there is no maximum.'''
loaded_all: Final[bool]
'''Whether all submodules of this module have been loaded.'''
_randinst: Final[Random]
'''The random number generator (instance of :class:`random.Random`) used by this module.'''
logging_to: Final[str]
'''A string indicating where the logging output of the program is going.
It is the name (path; possibly relative) of the log file, with four exceptions:
'NULL': no logging is taking place
'MEMORY': the logs are not going to a physical file but can be retrieved by :func:`get_past_logs`
'STDOUT': logging is going to :data:`sys.stdout`
'STDERR': logging is going to :data:`sys.stderr`'''