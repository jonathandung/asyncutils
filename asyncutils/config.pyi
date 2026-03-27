'''Set up some module-global state and sentinels, and expose some user-specified flags.'''
from ._internal.protocols import ValidExcType, PartialInterface
from concurrent.futures._base import Executor as _
from random import Random
from types import TracebackType
from typing import Final, Self, overload
__all__ = 'debugging', 'debug', 'silent', 'Executor', 'set_logger_level', 'basic_repl', 'loaded_all', 'get_past_logs', 'logging_to'
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
def set_logger_level(level: int) -> None: '''Set the level of the module-global logger.'''
def get_past_logs() -> str: '''Returns all stored logs as a string. Logs are only stored if asyncutils was started with -l MEMORY, otherwise an empty string is returned.'''
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