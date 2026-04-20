'''Implementation of an interactive console base class, as well as an :class:`AsyncUtilsConsole` class derived from it.'''
from ._internal.types import ValidExcType
from _collections_abc import Callable, Coroutine, Iterable
from _contextvars import Context
from abc import ABC, abstractmethod
from asyncio.events import AbstractEventLoop
from asyncio.tasks import Task
from code import InteractiveConsole
from collections import ChainMap
from concurrent.futures import Future
from types import CodeType, ModuleType
from typing import Any, ClassVar, Self, TypeGuard, final, overload
__all__ = 'AsyncUtilsConsole', 'ConsoleBase'
class ConsoleBase(InteractiveConsole, ABC):
    '''A base class for async consoles. Derives from :class:`code.InteractiveConsole`, or :class:`_pyrepl.console.InteractiveColoredConsole` if available.
    Inspired by asyncio/__main__.py. Highly adaptable.'''
    BANNER: ClassVar[str]
    '''A %-formattable string representating the template of the banner to be shown when the console starts.'''
    STATEMENT_FAILED: ClassVar[object]
    '''This is present if :class:`_pyrepl.console.InteractiveColoredConsole` is used as the base class.'''
    NAME: ClassVar[str]
    '''The name of the module implementing this console, detected from the class name by default. Corresponds to the keyword argument `name`.'''
    CAN_USE_PYREPL: ClassVar[bool]
    '''Whether _pyrepl enhancements are available and allowed.'''
    LOCALS_HANDLERS: ClassVar[ChainMap[str, Callable[[dict[str, Any]], Any]|None]]
    '''module name -> (locals of console of corresponding type -> Any)
    Add handlers for the module of your own console with `native_handler` and other modules with `other_handlers`.'''
    interrupt_hooks: ClassVar[tuple[Callable[[Self], Any], ...]]
    '''Functions called when :exc:`KeyboardInterrupt` occurs, in that order, besides essential hardcoded logic.
    Add hooks using `additional_interrupt_hooks`.'''
    memerr_hooks: ClassVar[tuple[Callable[[Self], Any], ...]]
    '''Functions called when a :exc:`MemoryError` occurs, in that order, besides essential hardcoded logic.
    Add hooks using `additional_memerr_hooks`.'''
    default_local_exit: ClassVar[bool]
    '''Whether python should continue running after the console exits by default, as opposed to the console raising :exc:`SystemExit` directly.'''
    disallow_subclass_msg: ClassVar[str]
    '''The error message when attempts are made to subclass subclasses of this class. Specified through the `disallow_subclass_msg` argument, which any unsubclassable console should pass.'''
    @property
    def context(self) -> Context: '''The :class:`contextvars.Context` instance passed to methods of the underlying asyncio event loop.'''
    @property
    def retcode(self) -> int: '''The integer return code of the console. If the console has not exited, return 0.'''
    @final
    @property
    def memory_errors(self) -> int: '''The number of :exc:`MemoryError`s that have occurred.'''
    @final
    @property
    def _internal_is_running(self) -> bool: '''Whether the console thinks itself is running. Can be used in `is_running` for state consistency checks.'''
    @property
    def is_running(self) -> bool: '''Whether the console is running. The default implementation uses `_internal_is_running` only.'''
    def __init__(self, loop: AbstractEventLoop, mod: ModuleType=..., modname: str=..., *, context_factory: Callable[[], Context]=...):
        '''`loop`: Event loop used by console interaction.
        `mod` (optional): The module to import within the console, determined by the subclass name by default.
        `modname` (optional): The name of the above module.
        `context_factory` (optional): A function that takes no arguments and returns an instance of contextvars.Context, to be used by the event loop.'''
    def __init_subclass__(cls, *, name: str=..., version: str=..., description: str=..., default_local_exit: bool=..., disallow_subclass_msg: str|None=..., native_handler: Callable[[dict[str, Any]], object]|None=..., other_handlers: dict[str, Callable[[dict[str, Any]], object]|None]=..., additional_interrupt_hooks: Iterable[Callable[[Self], object]]=..., additional_memerr_hooks: Iterable[Callable[[Self], object]]=..., template: str=..., **k: Any) -> None:
        '''`name` (optional): name of the module using the console
        `version` (optional): version of the module using the console
        `description` (optional): description of the module using the console
        `default_local_exit` (optional): see above
        `disallow_subclass_msg` (optional): see above
        `native_handler` (optional): see above
        `other_handlers` (optional): see above
        `additional_interrupt_hooks` (optional): see above
        `additional_memerr_hooks` (optional): see above
        `template` (optional): the console banner to use, with %-placeholders for name, version and description
        Additional keyword arguments are passed to `template.__mod__`.'''
    def __callback(self, fut: Future[Any], code: CodeType, /, *, makef: Callable[[CodeType, dict[str, Any]], Callable[[], Any]]=..., corocheck: Callable[[object], TypeGuard[Coroutine[Any, Any, Any]]]=..., futchain: Callable[[Task[Any], Future[Any]], object]=...) -> None: '''Called by runcode internally. To change its behaviour, override the entire method in a subclass with different default parameters.'''
    def runcode(self, code: CodeType, *, futimpl: Callable[[], Future[Any]]=..., dont_show_traceback: tuple[ValidExcType, ...]=..., threadsafe: bool=...) -> Any|None:
        '''Run `code`, an instance of `types.CodeType`.
        `futimpl` is a function that returns an instance of `concurrent.futures.Future`.
        `dont_show_traceback` is a tuple of types of exceptions for which the traceback should not be shown if they are to occur.
        `threadsafe` dictates whether to run the code in the event loop using `call_soon_threadsafe` instead of `call_soon`.'''
    def interact(self, banner: str|None=..., *, ps1: object=...) -> None: '''In the main thread, the run method is preferred.''' # type: ignore[override]
    def run(self, *, exitmsg: str=..., threadname: str=..., max_memerrs: int=..., always_run_interactive: bool=..., always_install_completer: bool=..., suppress_asyncio_warnings: bool=..., suppress_unawaited_coroutine_warnings: bool=...) -> int:
        '''Run the console and return the integer return code.
        The strings `exitmsg` and `threadname` should support `%`-formatting, the placeholder being the module name.
        Pass a negative value for `max_memerrs` to disable the stop after certain number of MemoryErrors behaviour.
        If `always_install_completer` is True, set the completer on readline as long as readline is available.
        Pass `True` for `suppress_asyncio_warnings` and `suppress_unawaited_coroutine_warnings` to silence asyncio logging and
        warnings for garbage-collected coroutines not being awaited respectively.
        If you wish the console to act like a console even when stdin is piped, pass `always_run_interactive=True` or start
        python with the -i flag.'''
    def showtraceback(self) -> None: '''Display the formatted traceback of the exception being handled. If there was no exception, do nothing (this differs from the superclass behaviour).'''
    @final
    def interrupt(self) -> None: '''Pass `additional_interrupt_hooks` to the subclass constructor to change the behaviour when encountering a `KeyboardInterrupt`, instead of touching this method.'''
    @final
    def memoryerror(self) -> None: '''Pass `additional_memerr_hooks` to the subclass constructor to change the behaviour when encountering a `MemoryError`, instead of touching this method.'''
    def write_special(self, msg: str) -> None: '''Called to write the banner and exit messages. Can have a different implementation than `write`.'''
    def refresh(self) -> None: '''Callback in `interrupt` and `memoryerror`.'''
    @abstractmethod
    def prehook(self, max_memerrs: int) -> None:
        '''Called by `run_console` before beginning the interaction logic. Can raise errors.
        When implementing, call `super().prehook(max_memerrs)` before everything.
        Not really an abstract method, but implementing is highly recommended.'''
    @abstractmethod
    def posthook(self) -> None:
        '''Called by `run_console` after the interaction has ended before writing the exit message. Should not raise errors.
        When implementing, call `super().posthook()` after everything.
        Not really an abstract method, but implementing is highly recommended.'''
    @overload
    def set_return_code(self, exc: SystemExit, /) -> None: '''Set the return code of this console from an instance of `SystemExit` or an integer return code and exit the console.'''
    @overload
    def set_return_code(self, code: int, /) -> None: ...
    def _interact_hook(self, ps1: object, kcolor: str, reset: str, fcolor: str) -> None:
        '''Called to write code with emulated color (such as import statements to represent the namespace) after the banner has been written, with parameters `ps1` representing :data:`sys.ps1`
        and `kcolor`, `reset` and `fcolor` representing the ANSI escape codes for the keyword color, color reset and the function color respectively.'''
@final
class AsyncUtilsConsole(ConsoleBase):
    '''A subclass of :class:`ConsoleBase`, used to implement the asyncutils REPL.'''
    @property
    def is_running(self) -> bool: '''Performs internal state consistency checks and returns whether the console is currently running. Only one :class:`AsyncUtilsConsole` can be running at a time.'''
    def prehook(self, max_memerrs: int) -> None: '''Ensures the console will be the only one running.'''
    def posthook(self) -> None: '''Ensures that the console is not left running after unset.'''
    def _interact_hook(self, ps1: object, kcolor: str, reset: str, fcolor: str) -> None: ...
    def write_special(self, msg: str) -> None: '''Writes msg to stderr only if the quiet flag is not set.'''
    def showtraceback(self) -> None: ...