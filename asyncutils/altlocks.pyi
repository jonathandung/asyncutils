'''Non-conventional asynchronous synchronization primitives that may not adhere to the traditional lock interface.'''
from ._internal.types import AsyncLockLike, Exceptable, SupportsIteration, Timer, ValidExcType
from .mixins import AsyncContextMixin, AwaitableMixin
from _collections_abc import Awaitable, Callable, Coroutine
from asyncio.locks import BoundedSemaphore
from collections import deque
from types import TracebackType
from typing import Any, NoReturn, Self, final, overload
__all__ = 'CircuitBreaker', 'DynamicBoundedSemaphore', 'DynamicThrottle', 'Releasing', 'ResourceGuard', 'StatefulBarrier', 'UniqueResourceGuard'
class DynamicBoundedSemaphore(BoundedSemaphore):
    '''A subclass of :class:`asyncio.BoundedSemaphore` whose bound can be set by the user via the `bound` property.'''
    def __init__(self, value: int=...): '''`value`, the initial value of the semaphore, defaults to :const:`context.DYNAMIC_BOUNDED_SEMAPHORE_DEFAULT_VALUE`.'''
    @property
    def bound(self) -> int: ...
    @bound.setter
    def bound(self, value: int, /) -> None: ...
class ResourceGuard(RuntimeError, AsyncContextMixin[None]):
    '''Reimplementation of :class:`anyio.ResourceGuard`, as a sync- and async-compatible context manager.'''
    @property
    def guarded(self) -> bool: ...
    def __init__(self, action: str=..., rname: object=...): ...
    def __enter__(self) -> None: '''Throw :obj:`self` as an exception (inherits from :exc:`RuntimeError`) if the resource is already being guarded; mark the resource as guarded otherwise.'''
    @overload
    def __exit__(self, exc_typ: ValidExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> None: ...
    @overload
    def __exit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> None: '''Unmark the resource as guarded.'''
    @classmethod
    def guard(cls, obj: object, /, *, action: str=...) -> Self: '''Alternate constructor; determines the name of the resource from the representation of the object.'''
@final
class UniqueResourceGuard(ResourceGuard):
    '''A subclass of :class:`ResourceGuard` that only allows one guard per object. Cannot be further subclassed.
    The object does not have to be hashable, but a strong reference will be held to it for the lifetime of the guard.
    Note that this does not stop the object from having an instance of :class:`ResourceGuard` (or subclass thereof) from guarding it simultaneously.'''
    def __new__(cls, /, *a: Any, **k: Any) -> NoReturn: '''Use the :meth:`guard` class method instead.'''
    @classmethod
    def clear_cache(cls) -> None: '''Clear the internal cache mapping guarded objects to their guards. Call only when you are sure no guards are in use.'''
    @classmethod
    def guard(cls, obj: object, /, *, action: str=...) -> Self:
        '''If the object already has a guard, return that guard, regardless of whether it is held. In that case, the `action` parameter is ignored.
        Otherwise, create and return a new guard for the object, using the `action` parameter in error messages. Note that the guard is not held upon creation.
        The error will be seen by the user only when they actually try to acquire the guard if it is already held.'''
class Releasing:
    '''An async context manager that releases the given lock on entry and re-acquires it on exit.'''
    def __init__(self, lock: AsyncLockLike[Any], /) -> None: ...
    async def __aenter__(self) -> Any: '''Return the return value of the release method of the lock, awaited if it is a coroutine.'''
    @overload
    async def __aexit__(self, exc_typ: ValidExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> None: ...
    @overload
    async def __aexit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> None: '''Re-enter the lock, propagating errors.'''
class CircuitBreaker:
    '''The circuit breaker pattern. Use on async functions that may fail often, such as requests to an unreliable server.
    Instances can be used as decorators, unless instantiated with a function as the first parameter, in which case the decorated function is returned.'''
    @overload
    def __new__(cls, name: str, /, max_fails: int=..., reset: float|None=..., *, exc: Exceptable=..., max_half_open_calls: int|None=...) -> Self: ...
    @overload
    def __new__[T, **P](cls, f: Callable[P, Awaitable[T]], /, max_fails: int=..., reset: float|None=..., *, exc: Exceptable=..., max_half_open_calls: int|None=...) -> Callable[P, Coroutine[Any, Any, T]]: # type: ignore[misc]
        '''Construct a circuit breaker, whose circuit is initially closed.
        If `name` is passed, use it as the name; return a function wrapping `f` otherwise, with the name of the circuit breaker (for debugging) derived from the name of the function.
        Pass exceptions that are expected to happen through the `exc` parameter.
        When the decorated function fails more than `max_fails` times (default :const:`context.CIRCUIT_BREAKER_DEFAULT_MAX_FAILS`), the breaker triggers (opens the circuit) and disallows further
        calls of the wrapped functions by throwing an exception.
        This state persists until the `reset` timeout expires (default :const:`context.CIRCUIT_BREAKER_DEFAULT_RESET`). Then, the breaker enters the half-open state.
        If the function completes successfully when the breaker is half-open under `max_half_open_calls` tries, the circuit closes automatically. Otherwise, the circuit reopens.'''
    def __call__[T, **P](self, f: Callable[P, Awaitable[T]], /, *, timer: Timer=..., default: T=...) -> Callable[P, Coroutine[Any, Any, T]]:
        '''Apply the circuit breaker to a function `f` returning an awaitable, and return a wrapper function with the same signature but strictly returning a coroutine.
        Care should be taken when applying the same circuit breaker to multiple functions, as they will not be able to run concurrently, and the calls counters will be shared.
        `timer` (default :func:`time.monotonic`) is used to get the current time for timeout calculation.
        `default` is returned if an expected exception is raised, also suppressing that exception.'''
    @property
    def fails(self) -> int: '''Current count of conseuctive failures.'''
    @property
    def name(self) -> str: '''The name of the circuit breaker, to be shown in error messages.'''
    @property
    def state(self) -> int: '''The state of the circuit breaker: 0 for closed, 1 for half-open, and 2 for open.'''
class StatefulBarrier[T](AwaitableMixin[tuple[int, deque[T]]]):
    '''An async barrier, that unlike traditional barriers, accumulates state from parties in a deque and makes it available once the barrier is tripped.'''
    def __init__(self, parties: int, name: str=..., initstate: SupportsIteration[T]=[], maxstate: int|None=...):
        '''`parties` (required): number of parties required to break the barrier
        `name`: name of the barrier; to appear in error messages
        `initstate`: an iterable storing the initial state; will be exhausted; preferrably not async
        `maxstate`: maximum length of state to store; older state will be expelled'''
    async def wait(self, state: T=..., *, timeout: float|None=...) -> tuple[int, deque[T]]:
        '''Note that the calling party is waiting for the barrier, optionally adding some state.
        If the barrier has already been aborted or broken, raise :exc:`asyncio.BrokenBarrierError`.
        Once enough parties are waiting, all callers receive a tuple `(pos, states)`, where `states` is the deque of stored state
        and `pos` is the number of parties having arrived before this one.'''
    async def abort(self) -> None: '''Abort the barrier, signalling :exc:`asyncio.BrokenBarrierError` to present waiting parties.'''
    def raise_for_abort(self) -> None: '''Throw :exc:`asyncio.BrokenBarrierError` if the barrier has been aborted.'''
    @property
    def broken(self) -> bool: '''Whether the barrier is broken.'''
    @property
    def parties(self) -> int: '''Total number of parties, arrived or not.'''
    @property
    def remaining_parties(self) -> int: '''Number of parties the waiting parties are waiting for.'''
    @property
    def n_waiting(self) -> int: '''Number of parties currently waiting.'''
class DynamicThrottle:
    '''An async context manager used to limit the rate of a function being called. See also: :class:`func.RateLimited`, :class:`locks.AdvancedRateLimit`'''
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
    async def __aenter__(self) -> None: '''Wait for the time as computed by the throttler, with some jitter applied, to pass, such that the rate is maintained.'''
    @overload
    async def __aexit__(self, exc_typ: ValidExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> None: ...
    @overload
    async def __aexit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> None: '''If an error caused the context manager, increment `fails` and reraise; otherwise, increment `successes`. Also adjust the rate if necessary.'''
    def reset(self) -> None: '''Reset the successes and fails.'''
    @property
    def ctime(self) -> float: '''The current time as returned by `timer`.'''
    @property
    def fails(self) -> int: '''Current number of failed calls. Reset periodically.'''
    @property
    def jitter(self) -> float: '''The current jitter.'''
    @jitter.setter
    def jitter(self, jitter: float, /) -> None: '''Set the jitter to `jitter`.'''
    @property
    def rate(self) -> float: '''The current rate.'''
    @rate.setter
    def rate(self, rate: float, /) -> None: '''Set the rate manually, applying the `min_rate` and `max_rate` bounds.'''
    @property
    def successes(self) -> int: '''Current number of succeeded calls; reset periodically.'''