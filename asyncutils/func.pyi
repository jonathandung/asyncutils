from ._internal.protocols import Exceptable, Timer, SupportsIteration
from .exceptions import _ExceptionWrapper
from _collections_abc import Callable, Iterable, Mapping, Coroutine, Awaitable
from typing import Any, Literal, Protocol, Self, overload, type_check_only
from asyncio.futures import Future
__all__ = 'areduce', 'every', 'everymethod', 'timer', 'retry', 'throttle', 'debounce', 'rate_limit', 'measure', 'benchmark'
@overload
async def areduce[T, R](f: Callable[[T, R], Awaitable[T]], it: SupportsIteration[R], initial: T=..., *, await_: Literal[True]=...) -> T: '''Async version of functools.reduce that takes an async function and possibly async iterable. If the function is sync, specify await_=False.'''
@overload
async def areduce[T, R](f: Callable[[T, R], T], it: SupportsIteration[R], initial: T=..., *, await_: Literal[False]) -> T: ...
def every[T](intvl: float, /, *, stop_when: Future[T]|None=..., count_f: bool=..., verbose: bool=..., stop_on_exc: bool=..., wait_first: bool=..., max_iterations: int=..., timer: Timer=..., supplied_args: Iterable[Any]=..., supplied_kwargs: Mapping[str, Any]=..., default: T=...) -> Callable[[Callable[..., Awaitable[T]]], Callable[..., Coroutine[Any, Any, T|None]]]:
    '''A decorator factory, useful for periodic monitoring tasks.
    The resultant function will run every `intvl` seconds, as determined by `timer`, at most `max_iterations` times. If `count_f` is True, this time includes the execution time of the function.
    If `wait_first` is True, sleep for `intvl` seconds before the first execution.
    If `stop_on_exc` is True, the function returns once the decorated function throws any exception or `stop_when` is cancelled.
    `verbose` makes the function treat exceptions more severely output-wise.
    Once the result of `stop_when` is set, the function returns that result, which should be None or the same type as the return type of the decorated function after awaiting.
    However, the task is guaranteed to be run at least once.
    When using the supplied_args and supplied_kwargs parameters, maintain a reference to them so that you can edit the args and kwargs fed to the function on the fly.
    Finally, the function returns `default` or None if it was not passed, unless `stop_on_exc` is True or `default` is `RAISE`.'''
def everymethod[T, R](intvl: float, /, *, stop_when_getter: Callable[[T], Future[R]]|None=..., count_f: bool=..., verbose: bool=..., stop_on_exc: bool=..., wait_first: bool=..., max_iterations: int=..., timer: Timer=..., supplied_args: Iterable[Any]=..., supplied_kwargs: Mapping[str, Any]=..., default: R=...) -> Callable[[_everymethodft[T, R]], _everymethodrvrv[T, R]]: '''The method version of `every`. `stop_when_getter`, if passed, should take `self` and returns a suitable future `stop_when`. Other parameters are as in `every`.'''
def timer[T, **P](f: Callable[P, Awaitable[T]], /, *, precision: int=..., expected: Exceptable=..., log: bool=..., timer: Timer=..., ns: bool=...) -> Callable[P, Coroutine[Any, Any, tuple[T|_ExceptionWrapper, float]]]:
    '''Convert the function that returns an awaitable object into an async function that returns a tuple `(res_or_exc, elapsed)`.
    `timer` is used to count `elapsed`, the time required to execute the function.
    `res_or_exc` is the awaited result of the wrapped function or the exception thrown wrapped by `exceptions.wrap_exc`.'''
def retry(tries: int=..., delay: float=..., max_delay: float=..., backoff: float=..., jitter: float=..., exc: Exceptable=..., on_retry: Callable[[int, BaseException], Any]=..., on_success: Callable[[int, float], Any]=..., random: Callable[[], float]=...) -> _frv: ...
def throttle(lim: float, timer: Timer=...) -> _frv: ...
def debounce(wait: float) -> _frv: ...
def rate_limit(calls: int, period: float, timer: Timer=...) -> _frv: ...
async def measure[T](f: Callable[[], Awaitable[T]], timer: Timer=...) -> tuple[T, float]: ...
class benchmark(tuple[float, float, float, float, int]):
    '''Actually a function at runtime.'''
    def __new__(cls, f: Callable[[], Awaitable], /, times: int=..., warmup: int=...) -> Self: ...
    @property
    def min(self) -> float: ...
    @property
    def max(self) -> float: ...
    @property
    def total(self) -> float: ...
    @property
    def avg(self) -> float: ...
    @property
    def iterations(self) -> int: ...
@type_check_only
class _everymethodrvrv[T, R](Protocol):
    async def __call__(_, self: T, /, *a: Any, **k: Any) -> R|None: ...
@type_check_only
class _everymethodft[T, R](Protocol):
    def __call__(_, self: T, /, *a: Any, **k: Any) -> Awaitable[R]: ...
@type_check_only
class _frv(Protocol):
    def __call__[T, **P](self, f: Callable[P, Awaitable[T]], /) -> Callable[P, Coroutine[Any, Any, T]]: ...