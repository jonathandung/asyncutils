'''Higher-order functions with asynchronous APIs, containing utilities to retry, time, throttle, run functions periodically and more.'''
from ._internal.protocols import Exceptable, Timer, SupportsIteration
from .exceptions import _ExceptionWrapper
from asyncio.futures import Future
from _collections_abc import Callable, Iterable, Mapping, Coroutine, Awaitable
from typing import Any, Literal, Protocol, Self, overload, type_check_only
__all__ = 'areduce', 'every', 'everymethod', 'timer', 'retry', 'throttle', 'debounce', 'measure', 'benchmark', 'RateLimited'
@overload
async def areduce[T, R](f: Callable[[T, R], Awaitable[T]], it: SupportsIteration[R], initial: T=..., *, await_: Literal[True]=...) -> T: '''Async version of functools.reduce that takes an async function and possibly async iterable. If the function is sync, specify `await_=False`.'''
@overload
async def areduce[T, R](f: Callable[[T, R], T], it: SupportsIteration[R], initial: T=..., *, await_: Literal[False]) -> T: ...
@overload
def every(intvl: float, /, *, count_f: bool=..., verbose: bool=..., stop_on_exc: bool=..., wait_first: bool=..., max_iterations: int=..., timer: Timer=..., supplied_args: Iterable[Any]=..., supplied_kwargs: Mapping[str, Any]=...) -> _everyrv:
    '''A decorator factory, useful for periodic monitoring tasks.
    The resultant function will run every `intvl` seconds, as determined by `timer`, at most `max_iterations` times. If `count_f` is True, this time includes the execution time of the function.
    If `wait_first` is True, sleep for `intvl` seconds before the first execution.
    If `stop_on_exc` is True, the function returns once the decorated function throws any exception or `stop_when` is cancelled.
    `verbose` makes the function treat exceptions more severely output-wise.
    Once the result of `stop_when` is set, the function returns that result, which should be None or the same type as the return type of the decorated function after awaiting.
    However, the task is guaranteed to be run at least once.
    When using the supplied_args and supplied_kwargs parameters, maintain a reference to them so that you can edit the args and kwargs fed to the function on the fly.
    Finally, the function returns `default` or None if it was not passed, unless `stop_on_exc` is True or `default` is `RAISE`.'''
@overload
def every[T](intvl: float, /, *, stop_when: Future[T], count_f: bool=..., verbose: bool=..., stop_on_exc: bool=..., wait_first: bool=..., max_iterations: int=..., timer: Timer=..., supplied_args: Iterable[Any]=..., supplied_kwargs: Mapping[str, Any]=...) -> _everyrv[T]: ...
@overload
def every[T](intvl: float, /, *, count_f: bool=..., verbose: bool=..., stop_on_exc: bool=..., wait_first: bool=..., max_iterations: int=..., timer: Timer=..., supplied_args: Iterable[Any]=..., supplied_kwargs: Mapping[str, Any]=..., default: T) -> _everyrv[T]: ...
@overload
def every[T](intvl: float, /, *, stop_when: Future[T], count_f: bool=..., verbose: bool=..., stop_on_exc: bool=..., wait_first: bool=..., max_iterations: int=..., timer: Timer=..., supplied_args: Iterable[Any]=..., supplied_kwargs: Mapping[str, Any]=..., default: T) -> _everyrv[T]: ...
@overload
def everymethod(intvl: float, /, *, count_f: bool=..., verbose: bool=..., stop_on_exc: bool=..., wait_first: bool=..., max_iterations: int=..., timer: Timer=..., supplied_args: Iterable[Any]=..., supplied_kwargs: Mapping[str, Any]=...) -> _everymethodrv[Any, Any]: '''The method version of `every`. `stop_when_getter`, if passed, should take `self` and returns a suitable future `stop_when`. Other parameters are as in `every`.'''
@overload
def everymethod[T, R](intvl: float, /, *, stop_when_getter: Callable[[T], Future[R]], count_f: bool=..., verbose: bool=..., stop_on_exc: bool=..., wait_first: bool=..., max_iterations: int=..., timer: Timer=..., supplied_args: Iterable[Any]=..., supplied_kwargs: Mapping[str, Any]=...) -> _everymethodrv[R, T]: ...
@overload
def everymethod[T, R](intvl: float, /, *, count_f: bool=..., verbose: bool=..., stop_on_exc: bool=..., wait_first: bool=..., max_iterations: int=..., timer: Timer=..., supplied_args: Iterable[Any]=..., supplied_kwargs: Mapping[str, Any]=..., default: R) -> _everymethodrv[R, Any]: ...
@overload
def everymethod[T, R](intvl: float, /, *, stop_when_getter: Callable[[T], Future[R]], count_f: bool=..., verbose: bool=..., stop_on_exc: bool=..., wait_first: bool=..., max_iterations: int=..., timer: Timer=..., supplied_args: Iterable[Any]=..., supplied_kwargs: Mapping[str, Any]=..., default: R) -> _everymethodrv[R, T]: ...
def timer[T, **P](f: Callable[P, Awaitable[T]], /, *, precision: int=..., expected: Exceptable=..., should_log: bool=..., timer: Timer=..., ns: bool=...) -> Callable[P, Coroutine[Any, Any, tuple[T|_ExceptionWrapper, float]]]:
    '''Convert the function that returns an awaitable object into an async function that returns a tuple `(res_or_exc, elapsed)`.
    `timer` is used to count `elapsed`, the time required to execute the function.
    `res_or_exc` is the awaited result of the wrapped function, or the exception thrown as wrapped by `exceptions.wrap_exc`.
    `precision` is the number of digits to keep in the time in logging, and `ns` whether the return value of the timer indicates time in nanoseconds.
    Any exception the wrapped function emits whose type is not in `expected` is propagated directly.'''
def retry(tries: int=..., delay: float=..., max_delay: float=..., backoff: float=..., jitter: float=..., exc: Exceptable=..., on_retry: Callable[[int, BaseException], Any]=..., on_success: Callable[[int, float], Any]=..., random: Callable[[], float]=...) -> _frv: ...
def throttle(lim: float, timer: Timer=...) -> _frv: ...
def debounce(wait: float) -> _frv: ...
async def measure[T](f: Callable[[], Awaitable[T]], timer: Timer=...) -> tuple[T, float]: '''A simple version of `timer` for functions taking no arguments and returning awaitables.'''
class benchmark(tuple[float, float, float, float, int]):
    '''Actually a function at runtime.'''
    def __new__(cls, f: Callable[[], Awaitable], /, times: int=..., warmup: int=...) -> Self:
        '''`f` is the function to benchmark, which should take no arguments and return an awaitable.
        `times` is how many times the function should be run, which defaults to 1.
        `warmup` is the number of warmup rounds to call the function for; not included in the benchmark results. Default 0.'''
    @property
    def min(self) -> float: '''The minimum execution time among all non-warmup calls.'''
    @property
    def max(self) -> float: '''The maximum execution time among all non-warmup calls.'''
    @property
    def total(self) -> float: '''The total execution time.'''
    @property
    def avg(self) -> float: '''`total/iterations`.'''
    @property
    def iterations(self) -> int: '''The `times` constructor parameter.'''
class RateLimited[T, **P]:
    '''The rate limiter pattern as a decorator (factory). See `locks.AdvancedRateLimit` for the async context manager version.'''
    @overload
    def __new__(cls, calls: int, period: float, *, raise_: bool=..., timer: Timer=...) -> Callable[[Callable[P, Awaitable[T]]], Self]: ... # type: ignore[misc]
    @overload
    def __new__(cls, f: Callable[P, Awaitable[T]], calls: int, period: float, *, raise_: bool=..., timer: Timer=...) -> Self: '''Limit the rate of calls of a function `f`, such that only `calls` calls within `period` seconds, as determined by `timer`, are allowed.'''
    async def __call__(self, *a: P.args, **k: P.kwargs) -> T: ...
    def __repr__(self) -> str: ...
@type_check_only
class _everymethodrvrv[T, R](Protocol):
    '''Not exported.'''
    async def __call__(self, _: T, /, *a: Any, **k: Any) -> R|None: ...
@type_check_only
class _everymethodft[T, R](Protocol):
    '''Not exported.'''
    def __call__(self, _: T, /, *a: Any, **k: Any) -> Awaitable[R]: ...
@type_check_only
class _frv(Protocol):
    '''Not exported.'''
    def __call__[T, **P](self, f: Callable[P, Awaitable[T]], /) -> Callable[P, Coroutine[Any, Any, T]]: ...
@type_check_only
class _everyrv[T](Protocol):
    '''Not exported.'''
    def __call__[**P](self, f: Callable[P, Awaitable[T]], /) -> Callable[P, Coroutine[Any, Any, T|None]]: ...
type _everymethodrv[R, T] = Callable[[_everymethodft[T, R]], _everymethodrvrv[T, R]]