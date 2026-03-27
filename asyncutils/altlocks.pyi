'''Non-conventional asynchronous synchronization primitives.'''
from .mixins import AsyncContextMixin, AwaitableMixin
from ._internal.protocols import Exceptable, SupportsIteration, Timer, ValidExcType
from asyncio.locks import BoundedSemaphore
from collections import deque
from _collections_abc import Awaitable, Coroutine, Callable
from types import TracebackType
from typing import Any, Self, overload
__all__ = 'CircuitBreaker', 'DynamicBoundedSemaphore', 'DynamicThrottle', 'ResourceGuard', 'StatefulBarrier', 'UniqueResourceGuard'
class DynamicBoundedSemaphore(BoundedSemaphore):
    '''A subclass of BoundedSemaphore whose bound can be set by the user via the `bound` property.'''
    def __init__(self, value: int=...): ...
    @property
    def bound(self) -> int: ...
    @bound.setter
    def bound(self, value: int, /) -> None: ...
class ResourceGuard(RuntimeError, AsyncContextMixin):
    '''Reimplementation of anyio.ResourceGuard, as a sync or async context manager.'''
    @property
    def guarded(self) -> bool: ...
    def __init__(self, action: str=..., rname: Any=...): ...
    def __enter__(self) -> None: ...
    @overload
    def __exit__(self, exc_typ: ValidExcType, exc_val: BaseException, exc_tb: TracebackType|None, /) -> None: ...
    @overload
    def __exit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> None: ...
    @classmethod
    def guard(cls, obj: Any, /, *, action: str=...) -> Self: ...
class UniqueResourceGuard(ResourceGuard):
    '''A subclass of anyio.ResourceGuard that only allows one guard per object.
    Note that this does not stop the object from having an instance of ResourceGuard (or subclass thereof) from guarding it simultaneously.'''
class CircuitBreaker:
    '''The circuit breaker pattern. Use on async functions that may fail often, such as requests to an unreliable server.
    Instances can be used as decorators, unless instantiated with a function as the first parameter, in which case the decorated function is returned.'''
    @property
    def name(self) -> str: '''The name of the circuit breaker, shown in error messages.'''
    @property
    def fails(self) -> int: '''Current count of conseuctive failures.'''
    @overload
    def __new__(cls, name: str, /, max_fails: int=..., reset: float|None=..., exc: Exceptable=..., max_half_open_calls: int|None=...) -> Self:
        '''Construct a circuit breaker, whose circuit is initially closed.
        If `name` is passed, use it as the name; return a function wrapping `f` otherwise, with the name of the circuit breaker (for debugging) derived from the name of the function.
        Pass exceptions that are expected to happen through the `exc` parameter.
        When the decorated function fails more than `max_fails` times, the breaker triggers (opens the circuit) and disallow further calls of the same function by throwing an exception.
        This state persists until the `reset` timeout expires, the default of which can be changed in the context submodule. Then, the breaker enters the half-open state.
        If the function completes successfully when the breaker is half-open under `max_half_open_calls` tries, the circuit closes automatically. Otherwise, the circuit reopens.'''
    @overload
    def __new__[T, **P](cls, f: Callable[P, Awaitable[T]], /, max_fails: int=..., reset: float|None=..., exc: Exceptable=..., max_half_open_calls: int|None=...) -> Callable[P, Coroutine[Any, Any, T]]: ...
    def __call__[T, **P](self, f: Callable[P, Awaitable[T]], /, timer: Timer=..., default: T=...) -> Callable[P, Coroutine[Any, Any, T]]: ...
class StatefulBarrier[T](AwaitableMixin):
    '''A barrier, that unlike traditional barriers, accumulates state from parties in a deque and makes it available once the barrier is tripped.'''
    def __init__(self, parties: int, name: str=..., initstate: SupportsIteration[T]=[], maxstate: int|None=...):
        '''`parties`: number of parties required to break the barrier
        `name` (optional): name of the barrier; to appear in error messages
        `initstate` (optional): an iterable storing the initial state; will be exhausted; preferrably not async
        `maxstate` (optional): maximum length of state to store; older state will be expelled'''
    async def wait(self, state: T=..., timeout: float|None=...) -> tuple[int, deque[T]]:
        '''Note that the calling party is waiting for the barrier, optionally adding some state.
        If the barrier has already been aborted or broken, raise an asyncio.BrokenBarrierError.
        If the timeout expires, raise a TimeoutError and abort the barrier.
        Once enough parties are waiting, all callers receive a tuple (pos, states).
        Here states is the deque of stored state and pos is the number of parties having arrived before this one.'''
    def _reset(self) -> None: ...
    def abort(self) -> None: '''Abort the barrier, throwing asyncio.BrokenBarrierError to present waiting parties.'''
    def raise_for_abort(self) -> None: '''Throw asyncio.BrokenBarrierError if the barrier has been aborted.'''
    @property
    def parties(self) -> int: '''Total number of parties, arrived or not.'''
    @property
    def broken(self) -> bool: '''Whether the barrier is broken.'''
    @property
    def remaining_parties(self) -> int: '''Number of parties the waiting parties are waiting for.'''
class DynamicThrottle:
    '''An async context manager used to limit the rate of a function being called. See also: `func.RateLimited`, `locks.AdvancedRateLimit`'''
    def __init__(self, init_rate: float, min_rate: float=..., max_rate: float=..., window: int|None=..., *, ubound: float|None=..., lbound: float|None=..., ufactor: float|None=..., lfactor: float|None=..., jitter: float|None=..., timer: Timer=..., rand: Callable[[float], float]=...):
        '''`init_rate` (required): The initial rate in calls per second.
        `min_rate`: The minimum rate.
        `max_rate`: The maximum rate.
        `window`: Number of calls, successful or unsuccessful, after which the rate is automatically adjusted.
        `ubound`: Lower bound of the ratio (successes: total calls) such that the rate is multiplied by `ufactor` and clamped to `min_rate` and `max_rate`.
        `lbound`: Upper bound of the above ratio such that the rate is multiplied by `lfactor` and clamped similarly.
        `jitter`: The jitter in calculation of the wait time before the context can enter.
        `timer`: Function to return current time as a float.
        `rand`: Function that takes a float (the jitter) and returns a random number within the interval `jitter` and `-jitter`.'''
    @property
    def rate(self) -> float: '''The current rate.'''
    @rate.setter
    def rate(self, rate: float, /) -> None: '''Set the rate manually, applying `min_rate` and `max_rate` bounds.'''
    @property
    def jitter(self) -> float: '''The current jitter.'''
    @jitter.setter
    def jitter(self, jitter: float, /) -> None: '''Set the jitter.'''
    @property
    def ctime(self) -> float: '''The current time as returned by `timer`.'''
    @property
    def successes(self) -> int: '''Current number of succeeded calls. Reset periodically.'''
    @property
    def fails(self) -> int: '''Current number of failed calls. Reset periodically.'''
    async def __aenter__(self) -> None: '''Wait for the time as computed by the throttler, with some jitter applied, to pass, such that the rate is maintained.'''
    @overload
    async def __aexit__(self, exc_typ: ValidExcType, exc_val: BaseException, exc_tb: TracebackType|None, /) -> None: '''If an error caused the context manager, increment `fails` and reraise; otherwise, increment `successes`. Also adjust the rate if necessary.'''
    @overload
    async def __aexit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> None: ...
    def reset(self) -> None: '''Reset the successes and fails.'''