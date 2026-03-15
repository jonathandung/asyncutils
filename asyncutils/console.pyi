'''Implementation of an interactive console base class, as well as an AsyncUtilsConsole class derived from it.'''
from ._internal.protocols import ValidExcType
from typing import ClassVar, Any, Self, TypeGuard, final, overload
from types import ModuleType, CodeType
from collections import ChainMap
from abc import ABCMeta, abstractmethod
from _collections_abc import Callable, Coroutine, Iterable
from _contextvars import Context
from _pyrepl.console import InteractiveColoredConsole
from asyncio.events import AbstractEventLoop
from asyncio.tasks import Task
from concurrent.futures import Future
__all__ = 'ConsoleBase', 'AsyncUtilsConsole'
class ConsoleBase(InteractiveColoredConsole, metaclass=ABCMeta):
    '''Inspired by asyncio/__main__.py. Highly adaptable.'''
    NAME: ClassVar[str]
    '''The name of the module implementing this console, detected from the class name by default. Corresponds to the keyword argument `name`.'''
    CAN_USE_PYREPL: ClassVar[bool]
    '''Whether _pyrepl enhancements are available and allowed.'''
    LOCALS_HANDLERS: ClassVar[ChainMap[str, Callable[[dict]]|None]]
    '''module name -> (locals of console of corresponding type -> Any)
    Add handlers for the module of your own console with `native_handler` and other modules with `other_handlers`.'''
    interrupt_hooks: ClassVar[tuple[Callable[[Self]], ...]]
    '''Functions called when KeyboardInterrupt occurs, in that order, besides essential hardcoded logic.
    Add hooks using `additional_interrupt_hooks`.'''
    memerr_hooks: ClassVar[tuple[Callable[[Self]], ...]]
    '''Functions called when MemoryError occurs, in that order, besides essential hardcoded logic.
    Add hooks using `additional_memerr_hooks`.'''
    default_local_exit: ClassVar[bool]
    '''Whether python should continue running after the console exits by default, as opposed to the console raising SystemExit directly.'''
    disallow_subclass_msg: ClassVar[str]
    '''The error message when attempts are made to subclass subclasses of this class. Specified through the `disallow_subclass_msg` argument, which any unsubclassable console should pass.'''
    _unsubclassable: ClassVar[bool]
    @property
    def context(self) -> Context: ...
    @property
    def local_exit(self) -> bool: ...
    @property
    def retcode(self) -> int: ...
    @final
    @property
    def memory_errors(self) -> int: ...
    @final
    @property
    def _internal_is_running(self) -> bool: '''Whether the console thinks itself is running. Can be used in is_running for state consistency checks.'''
    @property
    def is_running(self) -> bool: '''Whether the console is running. Default implementation uses _internal_is_running only.'''
    def __init__(self, loop: AbstractEventLoop, mod: ModuleType=..., modname: str=..., *, context_factory: Callable[[], Context]=..., importer: Callable[[str], ModuleType]=...): ...
    def __init_subclass__(cls, *, name: str=..., version: str=..., description: str=..., default_local_exit: bool=..., disallow_subclass_msg: str|None=..., native_handler: Callable[[dict[str, Any]]]|None=..., other_handlers: dict[str, Callable[[dict[str, Any]]]|None]=..., additional_interrupt_hooks: Iterable[Callable[[Self]]]=..., additional_memerr_hooks: Iterable[Callable[[Self]]]=..., template: str=..., **k: Any) -> None: ...
    def __callback(self, fut: Future, code: CodeType, /, *, makef: Callable[[CodeType, dict[str, Any]], Callable[[]]]=..., corocheck: Callable[[object], TypeGuard[Coroutine]]=..., futchain: Callable[[Task, Future], None]=...) -> None: '''Called by runcode internally. To change its behaviour, override the entire method in a subclass with different default parameters.'''
    def runcode(self, code: CodeType, *, futimpl: Callable[[], Future]=..., dont_show_traceback: tuple[ValidExcType, ...]=..., threadsafe: bool=...) -> Any|None: ...
    def interact(self, banner: str=..., *, ps1: object=...) -> None: '''In the main thread, the run method is preferred.'''
    def run(self, *, exitmsg: str=..., threadname: str=..., max_memerrs: int=..., always_run_interactive: bool=..., always_install_completer: bool=..., suppress_asyncio_warnings: bool=..., suppress_unawaited_coroutine_warnings: bool=...) -> int: '''Runs the console. The strings exitmsg and threadname should support formatting with %. Pass a negative value for max_memerrs to disable the stop after certain number of MemoryErrors behaviour. Pass always_run_interactive=True or use python -i so that the console acts like a console even when stdin is piped.'''
    def showtraceback(self) -> None: '''Display the formatted traceback of the previous exception.'''
    @final
    def interrupt(self) -> None: '''Pass additional_interrupt_hooks to the subclass constructor to change the behaviour when encountering a KeyboardInterrupt, instead of touching this method.'''
    @final
    def memoryerror(self) -> None: '''Pass additional_memerr_hooks to the subclass constructor to change the behaviour when encountering a MemoryError, instead of touching this method.'''
    def write_special(self, msg: str) -> None: '''Called to write the banner and exit messages. Can have a different implementation than write.'''
    def refresh(self) -> None: '''Callback in interrupt and memoryerror.'''
    @abstractmethod
    def prehook(self, max_memerrs: int) -> None: '''Called by run_console before beginning the interaction logic; can raise errors. When implementing, call super().prehook(max_memerrs) before everything. Not really an abstract method, but implementing is highly recommended.'''
    @abstractmethod
    def posthook(self) -> None: '''Called by run_console after the interaction has ended before writing the exit message; should not raise errors. When implementing, call super().posthook() after everything. Not really an abstract method, but implementing is highly recommended.'''
    @overload
    def set_return_code(self, exc: SystemExit, /) -> None: '''Set the return code of this console from an instance of SystemExit or an integer return code and exit the console.'''
    @overload
    def set_return_code(self, code: int, /) -> None: ...
    def _interact_hook(self, ps1: object, kcolor: str, reset: str, fcolor: str) -> None: '''Called to write code with emulated colour (such as import statements to represent the namespace) after the banner has been written, with parameters ps1 representing sys.ps1, kcolor, reset and fcolor representing the ANSI escape codes for the keyword color, color reset and the function color respectively.'''
    def __repr__(self) -> str: ...
@final
class AsyncUtilsConsole(ConsoleBase):
    '''A derived class of ConsoleBase, used to implement the asyncutils REPL.'''
    @property
    def is_running(self) -> bool: '''Performs internal state consistency checks and returns whether the console is currently running. Only one AsyncUtilsConsole can be running at a time. (*)'''
    def prehook(self, max_memerrs: int) -> None: '''Ensures the console will be the only one running.'''
    def posthook(self) -> None: '''Ensures that the console is not left running after unset.'''
    def _interact_hook(self, ps1: object, kcolor: str, reset: str, fcolor: str) -> None: ...
    def write_special(self, msg: str) -> None: '''Writes msg to stderr only if the quiet flag is not set.'''
    def showtraceback(self) -> None: ...
    def __repr__(self) -> str: ...