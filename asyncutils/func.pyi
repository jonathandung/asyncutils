'''Higher-order functions with asynchronous APIs, containing utilities to retry, time, throttle, run functions periodically and more.'''
from ._internal.types import AsyncLockLike, Exceptable, ExceptionWrapper, SupportsIteration, Timer, BenchmarkResult, DecoratorFactoryRV, EveryRV, EveryMethodRV
from _collections_abc import Awaitable, Callable, Coroutine, Iterable, Mapping
from asyncio.futures import Future
from typing import Any, Literal, Self, overload
__all__ = 'RateLimited', 'areduce', 'benchmark', 'debounce', 'every', 'everymethod', 'measure', 'retry', 'throttle', 'timer'
@overload
async def areduce[T, R](f: Callable[[T, R], Awaitable[T]], it: SupportsIteration[R], initial: T=..., *, await_: Literal[True]=...) -> T: '''Async version of functools.reduce that takes an async function and possibly async iterable. If the function is sync, specify `await_=False`.'''
@overload
async def areduce[T, R](f: Callable[[T, R], T], it: SupportsIteration[R], initial: T=..., *, await_: Literal[False]) -> T: ...
@overload
def every(intvl: float, /, *, count_f: bool=..., verbose: bool=..., stop_on_exc: bool=..., wait_first: bool=..., max_iterations: int=..., timer: Timer=..., supplied_args: Iterable[Any]=..., supplied_kwargs: Mapping[str, Any]=...) -> EveryRV[Any]: ...
@overload
def every[T](intvl: float, /, *, stop_when: Future[T], count_f: bool=..., verbose: bool=..., stop_on_exc: bool=..., wait_first: bool=..., max_iterations: int=..., timer: Timer=..., supplied_args: Iterable[Any]=..., supplied_kwargs: Mapping[str, Any]=...) -> EveryRV[T]: ...
@overload
def every[T](intvl: float, /, *, count_f: bool=..., verbose: bool=..., stop_on_exc: bool=..., wait_first: bool=..., max_iterations: int=..., timer: Timer=..., supplied_args: Iterable[Any]=..., supplied_kwargs: Mapping[str, Any]=..., default: T) -> EveryRV[T]: ...
@overload
def every[T](intvl: float, /, *, stop_when: Future[T], count_f: bool=..., verbose: bool=..., stop_on_exc: bool=..., wait_first: bool=..., max_iterations: int=..., timer: Timer=..., supplied_args: Iterable[Any]=..., supplied_kwargs: Mapping[str, Any]=..., default: T) -> EveryRV[T]:
    '''A decorator factory, useful for periodic monitoring tasks.
    The resultant function will run every `intvl` seconds, as determined by `timer`, at most `max_iterations` times. If `count_f` is True, this time includes the execution time of the function.
    If `wait_first` is True, sleep for `intvl` seconds before the first execution.
    If `stop_on_exc` is True, the function returns once the decorated function throws any exception or `stop_when` is cancelled.
    `verbose` makes the function treat exceptions more severely output-wise.
    Once the result of `stop_when` is set, the function returns that result, which should be None or the same type as the return type of the decorated function after awaiting.
    However, the task is guaranteed to be run at least once.
    When using the supplied_args and supplied_kwargs parameters, maintain a reference to them so that you can edit the args and kwargs fed to the function on the fly.
    Finally, the function returns `default` or None if it was not passed, unless `stop_on_exc` is True or `default` is `constants.RAISE`.'''
@overload
def everymethod(intvl: float, /, *, count_f: bool=..., verbose: bool=..., stop_on_exc: bool=..., wait_first: bool=..., max_iterations: int=..., timer: Timer=..., supplied_args: Iterable[Any]=..., supplied_kwargs: Mapping[str, Any]=...) -> EveryMethodRV[Any, Any]: ...
@overload
def everymethod[T, R](intvl: float, /, *, stop_when_getter: Callable[[T], Future[R]], count_f: bool=..., verbose: bool=..., stop_on_exc: bool=..., wait_first: bool=..., max_iterations: int=..., timer: Timer=..., supplied_args: Iterable[Any]=..., supplied_kwargs: Mapping[str, Any]=...) -> EveryMethodRV[R, T]: ...
@overload
def everymethod[T](intvl: float, /, *, count_f: bool=..., verbose: bool=..., stop_on_exc: bool=..., wait_first: bool=..., max_iterations: int=..., timer: Timer=..., supplied_args: Iterable[Any]=..., supplied_kwargs: Mapping[str, Any]=..., default: T) -> EveryMethodRV[T, Any]: ...
@overload
def everymethod[T, R](intvl: float, /, *, stop_when_getter: Callable[[T], Future[R]], count_f: bool=..., verbose: bool=..., stop_on_exc: bool=..., wait_first: bool=..., max_iterations: int=..., timer: Timer=..., supplied_args: Iterable[Any]=..., supplied_kwargs: Mapping[str, Any]=..., default: R) -> EveryMethodRV[R, T]: '''The method version of `every`. `stop_when_getter`, if passed, should take `self` and returns a suitable future `stop_when`. Other parameters are as in `every`.'''
def timer[T, **P](f: Callable[P, Awaitable[T]], /, *, precision: int=..., expected: Exceptable=..., should_log: bool=..., timer: Timer=..., ns: bool=...) -> Callable[P, Coroutine[Any, Any, tuple[T|ExceptionWrapper, float]]]:
    '''Convert the function that returns an awaitable object into an async function that returns a tuple `(res_or_exc, elapsed)`.
    `timer` is used to count `elapsed`, the time required to execute the function.
    `res_or_exc` is the awaited result of the wrapped function, or the exception thrown as wrapped by `exceptions.wrap_exc`.
    `precision` is the number of digits to keep in the time in logging, and `ns` whether the return value of the timer indicates time in nanoseconds.
    Any exception the wrapped function emits whose type is not in `expected` is propagated directly.'''
def retry(tries: int=..., delay: float=..., *, max_delay: float=..., backoff: float=..., jitter: float=..., exc: Exceptable=..., on_retry: Callable[[int, BaseException], Any]=..., on_success: Callable[[int, float], Any]=..., random: Callable[[], float]=...) -> DecoratorFactoryRV:
    '''A decorator factory that retries the wrapped function with exponential backoff, returning once the function succeeds.
    If the function never succeeds within `tries` attempts, the last exception is propagated.
    `backoff` is the multiplier applied to the delay (initially `delay`) after each failed attempt, which can never exceed `max_delay`.
    `jitter` is the maximum random jitter added to the delay.
    `exc` specifies which exceptions to catch and retry on; if an exception not in `exc` is raised, it is propagated immediately.
    `on_retry` and `on_success` are callbacks called before each retry and after a successful call, with the attempt number (zero-based)
    as the first argument and the exception caught or the time taken for the successful call respectively as the second. `on_success` is
    only called once.'''
def throttle(lim: float, timer: Timer=...) -> DecoratorFactoryRV: ...
def debounce(wait: float) -> DecoratorFactoryRV: ...
async def measure[T](f: Callable[[], Awaitable[T]], timer: Timer=...) -> tuple[T, float]: '''A simple version of `timer` for functions taking no arguments and returning awaitables.'''
def benchmark(f: Callable[[], Awaitable[Any]], /, times: int=..., warmup: int=...) -> BenchmarkResult:
    '''`f` is the function to benchmark, which should take no arguments and return an awaitable.
    `times` is how many times the function should be run, which defaults to 1.
    `warmup` is the number of warmup rounds to call the function for; not included in the benchmark results; default `0`.'''
class RateLimited[T, **P]:
    '''The rate limiter pattern as a decorator (factory). See `locks.AdvancedRateLimit` for the async context manager version.'''
    @overload
    def __new__(cls, calls: int, period: float, *, raise_: bool=..., timer: Timer=..., lock_impl: Callable[[], AsyncLockLike[Any]]=...) -> Callable[[Callable[P, Awaitable[T]]], Self]: ... # type: ignore[misc]
    @overload
    def __new__(cls, f: Callable[P, Awaitable[T]], calls: int, period: float, *, raise_: bool=..., timer: Timer=..., lock_impl: Callable[[], AsyncLockLike[Any]]=...) -> Self: '''Limit the rate of calls of a function `f`, such that only `calls` calls within `period` seconds, as determined by `timer`, are allowed.'''
    async def __call__(self, *a: P.args, **k: P.kwargs) -> T: ...