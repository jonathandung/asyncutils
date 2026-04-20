'''Functions related to asynchronous signal handling.'''
from ._internal.types import ValidExcType
from _collections_abc import Awaitable, Callable, Iterable
from asyncio.events import AbstractEventLoop
from logging import Logger
from signal import Signals
from typing import Literal, overload
__all__ = 'wait_for_signal',
@overload
async def wait_for_signal[T](processor: Callable[[Signals], Awaitable[T]], /, *S: int, timeout: float|None=..., raise_on_timeout: Literal[True], loop: AbstractEventLoop|None=..., possible_errors: tuple[ValidExcType, ...]=..., default_on_processor_failure: T, sigs: Iterable[int]=..., logger: Logger=...) -> T: ...
@overload
async def wait_for_signal[T](processor: Callable[[Signals], Awaitable[T]], /, *S: int, timeout: float|None=..., raise_on_timeout: Literal[True], loop: AbstractEventLoop|None=..., possible_errors: tuple[ValidExcType, ...]=..., sigs: Iterable[int]=..., logger: Logger=...) -> T|None: ...
@overload
async def wait_for_signal[T](processor: Callable[[Signals], Awaitable[T]], /, *S: int, timeout: float|None=..., raise_on_timeout: Literal[False]=..., loop: AbstractEventLoop|None=..., possible_errors: tuple[ValidExcType, ...]=..., sigs: Iterable[int]=..., logger: Logger=...) -> T|None: ...
@overload
async def wait_for_signal[T](processor: Callable[[Signals], Awaitable[T]], /, *S: int, timeout: float|None=..., raise_on_timeout: Literal[False]=..., loop: AbstractEventLoop|None=..., possible_errors: tuple[ValidExcType, ...]=..., default_on_processor_failure: T, sigs: Iterable[int]=..., logger: Logger=...) -> T|None: ...
@overload
async def wait_for_signal[T](processor: Callable[[Signals], T], /, *S: int, timeout: float|None=..., raise_on_timeout: Literal[True], loop: AbstractEventLoop|None=..., possible_errors: tuple[ValidExcType, ...]=..., default_on_processor_failure: T, sigs: Iterable[int]=..., logger: Logger=...) -> T: ...
@overload
async def wait_for_signal[T](processor: Callable[[Signals], T], /, *S: int, timeout: float|None=..., raise_on_timeout: Literal[True], loop: AbstractEventLoop|None=..., possible_errors: tuple[ValidExcType, ...]=..., sigs: Iterable[int]=..., logger: Logger=...) -> T|None: ...
@overload
async def wait_for_signal[T](processor: Callable[[Signals], T], /, *S: int, timeout: float|None=..., raise_on_timeout: Literal[False]=..., loop: AbstractEventLoop|None=..., possible_errors: tuple[ValidExcType, ...]=..., sigs: Iterable[int]=..., logger: Logger=...) -> T|None: ...
@overload
async def wait_for_signal[T](processor: Callable[[Signals], T], /, *S: int, timeout: float|None=..., raise_on_timeout: Literal[False]=..., loop: AbstractEventLoop|None=..., possible_errors: tuple[ValidExcType, ...]=..., default_on_processor_failure: T, sigs: Iterable[int]=..., logger: Logger=...) -> T|None:
    '''Wait for an operating system level signal included in `sigs` and the variable positional arguments to be signaled within `timeout` and handle it.
    See the docs for the [:mod:`signal`](https://docs.python.org/library/signal.html) and [:mod:`asyncio`](https://docs.python.org/library/asyncio-eventloop.html#loop-add-signal-handler) libraries, as well as [the Wikipedia page for signals](https://en.wikipedia.org/wiki/Signal_(IPC)).
    `processor` should be a function that takes the signal occurred, preferrably returning an awaitable object.
    If `raise_on_timeout` is True, throw :exc:`TimeoutError` on timeout. Otherwise, return `None`.
    If `loop` was passed, its :meth:`add_signal_handler` and :meth:`remove_signal_handler` methods will be used.
    Errors whose types are included in `possible_errors` will cause the logger :const:`logger` to emit an error and the function to return `default_on_processor_failure` (or `None` if not passed).
    Some info related to the progress of the wait also goes to the logger.
    The return value of the processor is returned through this function.
    Note that since there is very limited support for signals on Windows, this function may not work as expected even with the little signals it provides.'''