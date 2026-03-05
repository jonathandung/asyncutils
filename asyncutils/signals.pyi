from ._internal.protocols import ValidExcType
from _collections_abc import Callable, Awaitable
from signal import Signals
from typing import Literal, overload
from asyncio.events import AbstractEventLoop
from logging import Logger
__all__ = 'wait_for_signal',
@overload
async def wait_for_signal[T](processor: Callable[[Signals], Awaitable[T]], *S: int, timeout: float|None=..., raise_on_timeout: Literal[True], loop: AbstractEventLoop|None=..., possible_errors: tuple[ValidExcType, ...]=..., default_on_processor_failure: T=..., logger: Logger=...) -> T: ...
@overload
async def wait_for_signal[T](processor: Callable[[Signals], Awaitable[T]], *S: int, timeout: float|None=..., raise_on_timeout: Literal[False]=..., loop: AbstractEventLoop|None=..., possible_errors: tuple[ValidExcType, ...]=..., default_on_processor_failure: T=..., logger: Logger=...) -> T|None: ...
@overload
async def wait_for_signal[T](processor: Callable[[Signals], T], *S: int, timeout: float|None=..., raise_on_timeout: Literal[True], loop: AbstractEventLoop|None=..., possible_errors: tuple[ValidExcType, ...]=..., default_on_processor_failure: T=..., logger: Logger=...) -> T: ...
@overload
async def wait_for_signal[T](processor: Callable[[Signals], T], *S: int, timeout: float|None=..., raise_on_timeout: Literal[False]=..., loop: AbstractEventLoop|None=..., possible_errors: tuple[ValidExcType, ...]=..., default_on_processor_failure: T=..., logger: Logger=...) -> T|None: ...