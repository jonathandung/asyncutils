'''Functions related to asynchronous signal handling.'''
from ._internal.prots import ExcType
from asyncio import AbstractEventLoop
from collections.abc import Awaitable, Callable, Iterable
from logging import Logger
from signal import Signals
from typing import Literal, overload
__all__ = 'wait_for_signal',
@overload
async def wait_for_signal[T](processor: Callable[[Signals], Awaitable[T]], /, *S: int, timeout: float|None=..., raise_on_timeout: Literal[True], loop: AbstractEventLoop|None=..., possible_errors: tuple[ExcType, ...]=..., default_on_processor_failure: T, sigs: Iterable[int]=..., logger: Logger=...) -> T: ...
@overload
async def wait_for_signal[T](processor: Callable[[Signals], Awaitable[T]], /, *S: int, timeout: float|None=..., raise_on_timeout: Literal[True], loop: AbstractEventLoop|None=..., possible_errors: tuple[ExcType, ...]=..., sigs: Iterable[int]=..., logger: Logger=...) -> T|None: ...
@overload
async def wait_for_signal[T](processor: Callable[[Signals], Awaitable[T]], /, *S: int, timeout: float|None=..., raise_on_timeout: Literal[False]=..., loop: AbstractEventLoop|None=..., possible_errors: tuple[ExcType, ...]=..., sigs: Iterable[int]=..., logger: Logger=...) -> T|None: ...
@overload
async def wait_for_signal[T](processor: Callable[[Signals], Awaitable[T]], /, *S: int, timeout: float|None=..., raise_on_timeout: Literal[False]=..., loop: AbstractEventLoop|None=..., possible_errors: tuple[ExcType, ...]=..., default_on_processor_failure: T, sigs: Iterable[int]=..., logger: Logger=...) -> T|None: ...
@overload
async def wait_for_signal[T](processor: Callable[[Signals], T], /, *S: int, timeout: float|None=..., raise_on_timeout: Literal[True], loop: AbstractEventLoop|None=..., possible_errors: tuple[ExcType, ...]=..., default_on_processor_failure: T, sigs: Iterable[int]=..., logger: Logger=...) -> T: ...
@overload
async def wait_for_signal[T](processor: Callable[[Signals], T], /, *S: int, timeout: float|None=..., raise_on_timeout: Literal[True], loop: AbstractEventLoop|None=..., possible_errors: tuple[ExcType, ...]=..., sigs: Iterable[int]=..., logger: Logger=...) -> T|None: ...
@overload
async def wait_for_signal[T](processor: Callable[[Signals], T], /, *S: int, timeout: float|None=..., raise_on_timeout: Literal[False]=..., loop: AbstractEventLoop|None=..., possible_errors: tuple[ExcType, ...]=..., sigs: Iterable[int]=..., logger: Logger=...) -> T|None: ...
@overload
async def wait_for_signal[T](processor: Callable[[Signals], T], /, *S: int, timeout: float|None=..., raise_on_timeout: Literal[False]=..., loop: AbstractEventLoop|None=..., possible_errors: tuple[ExcType, ...]=..., default_on_processor_failure: T, sigs: Iterable[int]=..., logger: Logger=...) -> T|None:
    '''| Wait for an operating system level signal included in ``sigs`` (default :const:`~asyncutils.context.Context.WAIT_FOR_SIGNAL_DEFAULT_SIGNALS`) and the variable positional arguments to be signaled within ``timeout`` and handle it.
    | See the docs for the :mod:`signal` module, :meth:`~asyncio.loop.add_signal_handler`, as well as `the Wikipedia page for signals <https://en.wikipedia.org/wiki/Signal_(IPC)>`__.
    | ``processor`` should be a function that takes the signal occurred, preferrably returning an awaitable object.
    | If ``raise_on_timeout`` is ``True``, throw :exc:`TimeoutError` on timeout. Otherwise, return ``None``.
    | If ``loop`` is passed, its :meth:`~asyncio.loop.add_signal_handler` and :meth:`~asyncio.loop.remove_signal_handler` methods will be used; a loop is created and set otherwise.
    | Errors whose types are included in ``possible_errors`` will cause the logger ``logger`` to emit an error and the function to return ``default_on_processor_failure``, or ``None`` if not passed.
    | Some information related to the progress of the wait also goes to the logger.
    | The return value of the processor is returned through this function.

    .. note::
      :collapsible:

      There is limited support for signals on Windows and this function may not work as expected even with the little signals it provides.
      Therefore, the function emits a warning unless the console is running, in which case it would be much too annoying.
'''
