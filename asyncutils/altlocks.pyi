'''Non-conventional asynchronous synchronization primitives that may not adhere to the traditional lock interface.'''
from ._internal.prots import AsyncLockLike, DualContextManager, CanExcept, ExcType, SupportsIteration, Timer
from .mixins import AsyncContextMixin, AwaitableMixin
from collections import deque
from collections.abc import Awaitable, Callable, Hashable
from enum import IntEnum
from types import CoroutineType, TracebackType
from typing import Any, Literal, Never, Self, final, overload
__all__ = 'CircuitBreaker', 'DynamicThrottle', 'Releasing', 'ResourceGuard', 'StatefulBarrier', 'UniqueResourceGuard'
class ResourceGuard[T](AsyncContextMixin[None]):
    '''A sync- and async-compatible context manager, inspired by :class:`anyio.ResourceGuard`, which causes contention of a shared resource to fail fast.

    .. tip:: A strong reference to the object will be held for the lifetime of the guard.
    .. note:: The guard is not held upon creation.
    '''
    @property
    def action(self) -> str: '''The action being attempted on the resource, as passed to the constructor.'''
    @property
    def guarded(self) -> bool: '''Whether the resource is currently being guarded.'''
    @property
    def success_ratio(self) -> float: '''The current ratio of successful acquisitions to total acquisition attempts, or 0 if there have been no attempts.'''
    @overload
    def __new__(cls: type[ResourceGuard[Never]], rsrc: Never=..., *, action: str=...) -> ResourceGuard[Never]: ...
    @overload
    def __new__(cls, rsrc: T, *, action: str=...) -> Self:
        '''| ``action`` is used in error messages to describe the action being attempted on the resource, such as ``'access'`` or ``'close'``.
        | ``rsrc`` is used in error messages to describe the resource by calling its :meth:`~object.__repr__`; if not passed, an index is automatically assigned to the resource.
        '''
    def __enter__(self) -> None:
        '''| Throw :exc:`~asyncutils.exceptions.ResourceBusy` if the resource is already being guarded.
        | Otherwise, mark the resource as guarded, such that :attr:`guarded` evaluates to ``True``.
        '''
    def yields_resource(self) -> DualContextManager[T]: '''Return a one-off context manager serving the same purpose as the guard but giving the resource on entry.'''
    @overload
    def __exit__(self, exc_typ: ExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> None: ...
    @overload
    def __exit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> None: '''Mark the resource as no longer guarded.'''
@final
class UniqueResourceGuard[T: Hashable](ResourceGuard[T]):
    '''A subclass of :class:`ResourceGuard` that only allows one guard per object. Cannot be further subclassed.

    .. caution:: This class does not stop the object from having an instance of :class:`ResourceGuard` (or subclass thereof) from guarding it simultaneously.
    .. admonition:: Implementation detail

      Instances are weakly referenceable.
    '''
    def __new__(cls, rsrc: T, *, action: str=...) -> Self:
        '''| If the object already has a guard, return that guard, regardless of whether it is held. In that case, the ``action`` parameter is ignored and a warning is issued.
        | Otherwise, create and return a new guard for the object, using the ``action`` parameter in error messages.

        .. attention:: The error will be seen by the user only when they actually try to acquire the guard if it is already held.
        '''
    @classmethod
    def clear_cache(cls) -> None: '''Clear the internal cache mapping guarded objects to their guards. Call only when you are sure no guards are in use.'''
class Releasing:
    '''Essentially invert the roles of the async enter and exit methods of a lock.'''
    def __init__(self, lock: AsyncLockLike[object], /) -> None: '''Instantiate the async context manager to release ``lock`` on entry and re-acquires it on exit.'''
    async def __aenter__(self) -> None: '''Call the release method of the lock, awaiting if it returns a coroutine.'''
    @overload
    async def __aexit__(self, exc_typ: ExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> None: ...
    @overload
    async def __aexit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> None: '''Re-enter the lock, propagating errors.'''
class CircuitBreaker:
    '''| The circuit breaker pattern. Use on async functions that may fail often, such as requests to an unreliable server.
    | Instances can be used as decorators, unless instantiated with a function as the first parameter, in which case the decorated function is returned.
    '''
    class State(IntEnum):
        CLOSED = 0
        '''The closed state.'''
        HALF_OPEN = 1
        '''The half-open state.'''
        OPEN = 2
        '''The open state.'''
    @overload
    def __new__(cls, name: str, /, max_fails: int=..., reset: float|None=..., *, exc: CanExcept=..., max_half_open_calls: int|None=...) -> Self: ...
    @overload
    def __new__[T, **P](cls, f: Callable[P, Awaitable[T]], /, max_fails: int=..., reset: float|None=..., *, exc: CanExcept=..., max_half_open_calls: int|None=...) -> Callable[P, CoroutineType[Any, Any, T]]:
        '''| Construct a circuit breaker, whose circuit is initially closed.
        | If ``name`` is passed, use it as its name; return a function wrapping ``f`` otherwise, deriving the name of the circuit breaker from the function. This derivation follows exactly one level of ``__wrapped__``-based wrapping after retrieving the :attr:`~method.__func__` attribute if present.
        | Pass exceptions that are expected to happen through the ``exc`` parameter.
        | When the decorated function fails more than ``max_fails`` times (default :const:`~asyncutils.context.Context.CIRCUIT_BREAKER_DEFAULT_MAX_FAILS`), the breaker triggers (opens the circuit, so to say) and disallows further calls of the wrapped functions by throwing an exception.
        | This state persists until the ``reset`` timeout expires (default :const:`~asyncutils.context.Context.CIRCUIT_BREAKER_DEFAULT_RESET`). Then, the breaker enters the half-open state.
        | If the function completes successfully when the breaker is half-open under ``max_half_open_calls`` (default :const:`~asyncutils.context.Context.CIRCUIT_BREAKER_DEFAULT_MAX_HALF_OPEN_CALLS`) tries, the circuit closes automatically. Otherwise, the circuit reopens.
        '''
    def __call__[T, **P](self, f: Callable[P, Awaitable[T]], /, *, timer: Timer=..., default: T=...) -> Callable[P, CoroutineType[Any, Any, T]]:
        '''| Apply the circuit breaker to a function ``f`` returning an awaitable, and return a wrapper function with the same signature that strictly returns coroutines.
        | ``timer`` (default :func:`time.monotonic`) is used to get the current time to calculate the timeout.
        | If passed, ``default`` is returned if an expected exception is raised, also suppressing that exception.

        .. caution:: Care should be taken when applying the same circuit breaker to multiple functions, as the calls counters will be shared.
        '''
    @property
    def fails(self) -> int: '''Current count of consecutive failures.'''
    @property
    def name(self) -> str: '''The name of the circuit breaker, to be shown in error messages.'''
    @property
    def state(self) -> Literal[0, 1, 2]: '''The state of the circuit breaker: 0 for closed, 1 for half-open, and 2 for open.'''
class StatefulBarrier[T](AwaitableMixin[tuple[int, deque[T]]]):
    '''An async barrier, that unlike traditional barriers, accumulates state from parties in a deque and makes it available once the barrier is tripped.'''
    @overload
    def __init__(self, parties: int, name: str=..., *, max_state: int|None=...): ...
    @overload
    def __init__(self, parties: int, *, init_state: SupportsIteration[T], max_state: int|None=...): ...
    @overload
    def __init__(self, parties: int, name: str, init_state: SupportsIteration[T], max_state: int|None=...):
        '''* ``parties`` (required): The number of parties required to break the barrier.
        * ``name``: The name of the barrier, to appear in error messages.
        * ``init_state``: An iterable storing the initial state. The iterable will be exhausted eventually.
        * ``max_state``: Maximum length of state to store. Older state will be expelled.
        '''
    async def wait(self, state: T=..., timeout: float|None=...) -> tuple[int, deque[T]]:
        '''| Note that the calling party is waiting for the barrier, optionally adding some state.
        | If the barrier has already been aborted or broken, raise :exc:`~asyncio.BrokenBarrierError`.
        | Once enough parties are waiting, all callers receive a tuple ``(pos, states)``, where ``states`` is the deque of stored state and ``pos`` the number of parties having arrived before this one.
        '''
    async def abort(self) -> None: '''Abort the barrier, signalling :exc:`~asyncio.BrokenBarrierError` to present waiting parties.'''
    def raise_for_abort(self) -> None: '''Throw :exc:`~asyncio.BrokenBarrierError` if the barrier has been aborted.'''
    @property
    def broken(self) -> bool: '''Whether the barrier is broken.'''
    @property
    def parties(self) -> int: '''Total number of parties, arrived or not.'''
    @property
    def remaining_parties(self) -> int: '''Number of parties the waiting parties are waiting for.'''
    @property
    def n_waiting(self) -> int: '''Number of parties currently waiting.'''
class DynamicThrottle:
    '''Limit the rate of a function being called.

    .. seealso::

      :class:`~asyncutils.func.RateLimited`
        \

      :class:`~asyncutils.locks.AdvancedRateLimit`
        Classes that serve similar rate-limiting functionality.
    '''
    def __init__(self, init_rate: float, min_rate: float=..., max_rate: float=..., window: int|None=..., *, ubound: float|None=..., lbound: float|None=..., ufactor: float|None=..., lfactor: float|None=..., jitter: float|None=..., timer: Timer=..., rand: Callable[[float], float]=...):
        '''* ``init_rate`` (required): The initial rate in calls per second.
        * ``min_rate``: The minimum rate; default :const:`~asyncutils.context.Context.DYNAMIC_THROTTLE_DEFAULT_MIN_RATE`.
        * ``max_rate``: The maximum rate; default :const:`~asyncutils.context.Context.DYNAMIC_THROTTLE_DEFAULT_MAX_RATE`.
        * ``window``: Number of calls, successful or unsuccessful, after which the rate is automatically adjusted; default :const:`~asyncutils.context.Context.DYNAMIC_THROTTLE_DEFAULT_WINDOW`.
        * ``ubound``: Lower bound of the ratio successes: total calls such that the rate is multiplied by ``ufactor`` (default :const:`~asyncutils.context.Context.DYNAMIC_THROTTLE_DEFAULT_UFACTOR`) and clamped to ``min_rate`` and ``max_rate``; default :const:`~asyncutils.context.Context.DYNAMIC_THROTTLE_DEFAULT_UBOUND`.
        * ``lbound``: Upper bound of the above ratio such that the rate is multiplied by ``lfactor`` (default :const:`~asyncutils.context.Context.DYNAMIC_THROTTLE_DEFAULT_LFACTOR`) and clamped similarly; default :const:`~asyncutils.context.Context.DYNAMIC_THROTTLE_DEFAULT_LBOUND`.
        * ``jitter``: The jitter in calculation of the wait time before the context can enter; default :const:`~asyncutils.context.Context.DYNAMIC_THROTTLE_DEFAULT_JITTER`.
        * ``timer``: Function to return current time as a float.
        * ``rand``: Function that takes a float (the jitter) and returns a random number within the interval ``jitter`` and ``-jitter``.
        '''
    async def __aenter__(self) -> None: '''Wait for the time as computed by the throttler, with some jitter applied, to pass, such that the rate is maintained.'''
    @overload
    async def __aexit__(self, exc_typ: ExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> None: ...
    @overload
    async def __aexit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> None: '''If an error caused the context manager, increment ``fails`` and re-raise; otherwise, increment ``successes``. Also adjust the rate if necessary.'''
    def reset(self) -> None: '''Reset the counts of successes and fails.'''
    @property
    def ctime(self) -> float: '''The current time as returned by ``timer``.'''
    @property
    def fails(self) -> int: '''Current number of failed calls. Reset periodically.'''
    @property
    def jitter(self) -> float: '''The current jitter in calculating the wait time.'''
    @jitter.setter
    def jitter(self, jitter: float, /) -> None: '''Set the jitter to ``jitter``.'''
    @property
    def rate(self) -> float: '''The current rate.'''
    @rate.setter
    def rate(self, rate: float, /) -> None: '''Set the rate manually, applying the ``min_rate`` and ``max_rate`` bounds.'''
    @property
    def successes(self) -> int: '''Current number of succeeded calls; reset periodically.'''
