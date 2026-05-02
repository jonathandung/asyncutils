'''Exception handling utilties and exception classes used by this module.'''
from ._internal.types import AsyncLockLike, Exceptable, ExceptionWrapper, Middleware, ExcType, Q
from .channels import EventBus
from .locks import LocksmithBase
from .version import VersionInfo
from _collections_abc import Callable, Generator, Iterable
from types import TracebackType
from typing import Any, Literal, NoReturn, Self, TypeGuard, overload
from weakref import ref
__all__ = 'CRITICAL', 'BulkheadError', 'BulkheadFull', 'BulkheadShutDown', 'BusError', 'BusPublishingError', 'BusShutDown', 'BusStatsError', 'BusTimeout', 'CircuitBreakerError', 'CircuitHalfOpen', 'CircuitOpen', 'Critical', 'Deadlock', 'EventValueError', 'FaultyConfig', 'ForbiddenOperation', 'FutureCorrupted', 'GetPasswordMissing', 'GetPasswordRetrievalError', 'IgnoreErrors', 'ItemsExhausted', 'LockForceRequest', 'MaxIterationsError', 'PasswordError', 'PasswordMissing', 'PasswordQueueError', 'PasswordRetrievalError', 'PoolError', 'PoolFull', 'PoolShutDown', 'PutPasswordMissing', 'PutPasswordRetrievalError', 'RateLimitExceeded', 'StateCorrupted', 'VersionConversionError', 'VersionCorrupted', 'VersionError', 'VersionNormalizerFault', 'VersionNormalizerMissing', 'VersionNormalizerTypeError', 'VersionValueError', 'WarningToError', 'WrongPassword', 'WrongPasswordType', 'exception_occurred', 'ignore_all', 'ignore_noncritical', 'ignore_typical', 'potent_derive', 'prepare_exception', 'raise_exc', 'ref', 'unnest', 'unnest_reverse', 'unwrap_exc', 'wrap_exc'
CRITICAL: tuple[ExcType, ...]
'''The tuple (:exc:`SystemExit`, :exc:`SystemError`, :exc:`KeyboardInterrupt`), representing exceptions that should be allowed to propagate under most error handling mechanisms.'''
def unnest(group: BaseException, /, *more: BaseException, raise_critical: bool=..., keep: Exceptable=..., filter_out: Exceptable=..., predicate: Callable[[BaseException], bool]=..., ack1: Callable[[BaseException], object]|None=..., ack2: Callable[[BaseException], object]|None=..., ack3: Callable[[BaseException], object]|None=...) -> Generator[BaseException, BaseException]:
    '''Flatten exceptions that may be nested in :class:`BaseExceptionGroup`'s, with priority for those just sent in. Use this when you must preserve the order.
    Keyword arguments are as in `potent_derive`.'''
def unnest_reverse(group: BaseException, /, *more: BaseException, raise_critical: bool=..., keep: Exceptable=..., filter_out: Exceptable=..., predicate: Callable[[BaseException], bool]=..., ack1: Callable[[BaseException], object]|None=..., ack2: Callable[[BaseException], object]|None=..., ack3: Callable[[BaseException], object]|None=...) -> Generator[BaseException, BaseException]: '''Basically the above but in reverse order, with rare edge cases. More memory- and time-efficient than unnest.'''
@overload
def potent_derive(group: BaseExceptionGroup, /, *more: BaseException, ordered: bool=..., predicate: Callable[[BaseException], bool]=..., raise_critical: bool=..., keep: Exceptable=..., filter_out: Exceptable=..., ack1: Callable[[BaseException], object]|None=..., ack2: Callable[[BaseException], object]|None=..., ack3: Callable[[BaseException], object]|None=..., notes: Iterable[str]|None=...) -> BaseExceptionGroup: ...
@overload
def potent_derive(exc: BaseException, /, *more: BaseException, message: str, ordered: bool=..., predicate: Callable[[BaseException], bool]=..., raise_critical: bool=..., keep: Exceptable=..., filter_out: Exceptable=..., ack1: Callable[[BaseException], object]|None=..., ack2: Callable[[BaseException], object]|None=..., ack3: Callable[[BaseException], object]|None=..., notes: Iterable[str]|None=..., traceback: TracebackType|None=..., context: BaseException, cause: None=..., suppress: bool=...) -> BaseExceptionGroup: ...
@overload
def potent_derive(exc: BaseException, /, *more: BaseException, message: str, ordered: bool=..., predicate: Callable[[BaseException], bool]=..., raise_critical: bool=..., keep: Exceptable=..., filter_out: Exceptable=..., ack1: Callable[[BaseException], object]|None=..., ack2: Callable[[BaseException], object]|None=..., ack3: Callable[[BaseException], object]|None=..., notes: Iterable[str]|None=..., traceback: TracebackType|None=..., context: None=..., cause: BaseException, suppress: bool=...) -> BaseExceptionGroup: ...
@overload
def potent_derive(exc: BaseException, /, *more: BaseException, message: str, ordered: bool=..., predicate: Callable[[BaseException], bool]=..., raise_critical: bool=..., keep: Exceptable=..., filter_out: Exceptable=..., ack1: Callable[[BaseException], object]|None=..., ack2: Callable[[BaseException], object]|None=..., ack3: Callable[[BaseException], object]|None=..., notes: Iterable[str]|None=..., traceback: TracebackType|None=..., context: None=..., cause: None=..., suppress: bool=...) -> BaseExceptionGroup:
    '''Return an instance of :exc:`BaseExceptionGroup`, applying the specified filtering and combining the exceptions from other groups, flattening when necessary.
    The intersection of `filter_out` and `keep`, which are exception types (or tuples thereof), should be non-empty; they are redundant otherwise.
    The acknowledgement parameters `ack1`, `ack2` and `ack3` are called on exceptions in the above intersection, exceptions that don't pass the predicate
    and exceptions that are not in `keep` respectively. They must be callables that return fast (e.g. collecting into a list) to avoid slowing down the function.
    If `raise_critical` is `True`, exit early once a critical exception (type of which is a member of :const:`CRITICAL`) is encountered and propagate it.
    `notes` is attached to the group using :meth:`~BaseException.add_note`.
    The `suppress`, `context`, `cause` and `traceback` parameters are used to add metadata to the result group; see :func:`prepare_exception`.
    They only have an effect when the first argument is not a group.'''
def prepare_exception[E: BaseException](exc: E, /, *, traceback: TracebackType|None=..., cause: BaseException|None=..., context: BaseException|None=..., suppress: bool=..., notes: Iterable[str]=...) -> E:
    '''Attach some info to the exception `exc` and return it.
    `notes` is an iterable of strings that are added to the exception using :meth:`~BaseException.add_note`. If a single string, it is treated as one note; to avoid this for some reason, convert the string to a tuple beforehand.
    The parameter `traceback` corresponds to the attribute :attr:`~BaseException.__traceback__`, `cause` to :attr:`~BaseException.__cause__`, `context` to :attr:`~BaseException.__context__` and `suppress` to :attr:`~BaseException.__suppress_context__`.'''
@overload
def raise_exc(exc_typ: ExcType, /, *args: Any, traceback: TracebackType|None=..., cause: BaseException|None=..., context: BaseException|None=..., suppress: bool=..., notes: Iterable[str]=..., **kwargs: Any) -> NoReturn: ...
@overload
def raise_exc(exc_val: BaseException, /, *, traceback: TracebackType|None=..., cause: BaseException|None=..., context: BaseException|None=..., suppress: bool=..., notes: Iterable[str]=...) -> NoReturn: '''Programmatically raise an exception. `args` and `kwargs` are passed to the constructor of `exc_typ` in the first overload. Remaining args are as in `potent_derive`.'''
def wrap_exc(exc: BaseException, /) -> ExceptionWrapper: '''Wrap an exception in a special proxy `wrapper`, such that `exception_occurred(wrapper)` returns `True`.'''
def unwrap_exc(instance: ExceptionWrapper, /) -> BaseException: '''Recover the exception wrapped by :func:`wrap_exc`.'''
def exception_occurred(instance: Any, /) -> TypeGuard[ExceptionWrapper]: '''Whether the object is actually a sentinel for an exception, described above.'''
class Deadlock(BaseException):
    '''Raised when a potential async deadlock situation is noticed by this module.'''
    def __init__(self, /, *args: str, noticer: Any=...): ...
    @property
    def noticer(self) -> Any: ...
class StateCorrupted(BaseException):
    '''Raised when the module-internal state is corrupted, usually by a slip-up of some abstraction layer outside of this library, and an exception can be thrown. Should not be caught by users.'''
    def __init__(self, adjective: str, details: str, /): ...
    @property
    def adjective(self) -> str: ...
    @property
    def details(self) -> str: ...
class FaultyConfig(BaseException):
    '''Raised when the configuration json has values of incorrect types; should not be caught.'''
    def __init__(self, key: str, wrong: type, correct: type|tuple[type, ...], /): ...
    @property
    def key(self) -> str: ...
    @property
    def wrong(self) -> type: ...
    @property
    def correct(self) -> type|tuple[type, ...]: ...
class Critical[E: (SystemExit, SystemError, KeyboardInterrupt)](BaseException):
    '''Raised when a critical error is encountered by exception-handling middleware.'''
    @overload
    def __new__(cls, exc: E) -> Self: ...
    @overload
    def __new__(cls, exc: None=...) -> Self: '''Construct the critical exception with the exception being wrapped, or the currently handled exception if not passed.'''
    @property
    def exc(self) -> E: '''The exception that occurred, determined by the raising scope by default.'''
    @property
    def __suppress_context__(self) -> Literal[False]: ... # type: ignore[override]
class VersionError(Exception): '''Base class for all version-related errors.'''
class VersionConversionError(VersionError): '''Base class for errors thrown when attempting to normalize an object to a version.'''
class VersionValueError(VersionConversionError, ValueError): '''Raised when an argument passed to the :class:`~version.VersionInfo` constructor is negative, for instance.'''
class VersionNormalizerMissing[T](VersionConversionError, TypeError):
    '''Raised when no normalizer is registered for an unrecognized object.'''
    def __init__(self, obj: T, /): ...
    @property
    def obj(self) -> T|None: '''The unrecognized object. `None` if garbage collected.'''
class VersionNormalizerTypeError[T](VersionConversionError, TypeError):
    '''Raised when a custom normalizer returns anything but an iterable of integers.'''
    def __init__(self, normalizer: Callable[[T], object], obj: T, /): ...
    @property
    def normalizer(self) -> Callable[[T], Any]|None: '''The normalizer at fault. `None` if garbage collected.'''
    @property
    def obj(self) -> T|None: '''The object being normalized by the normalizer, for which a value of incorrect type was returned. `None` if garbage collected.'''
class VersionNormalizerFault[T](VersionConversionError):
    '''Wraps any errors thrown by a custom normalizer, intentionally or otherwise.'''
    def __init__(self, normalizer: Callable[[T], Iterable[int]], obj: T, exc: BaseException, /): ...
    @property
    def normalizer(self) -> Callable[[T], Iterable[int]]|None: '''The normalizer at fault. `None` if garbage collected.'''
    @property
    def obj(self) -> T|None: '''The handled object. `None` if garbage collected.'''
    @property
    def exc(self) -> BaseException|None: '''The exception thrown. `None` if garbage collected.'''
class VersionCorrupted(VersionError, RuntimeError):
    '''Raised when internal state consistency checks of a version fail, indicating modification by the user and intrusion of the unstable API.'''
    def __init__(self, obj: VersionInfo, /): ...
    def __getattr__(self, name: str, /) -> Any: ...
    @property
    def obj(self) -> VersionInfo|None: '''The instance of :class:`~version.VersionInfo` having been corrupted. `None` if garbage collected.'''
class BulkheadError(RuntimeError): '''Raised when there is an error in bulkhead processing.'''
class BulkheadFull(BulkheadError): '''Raised when a bulkhead is full and a party requests it to execute a coroutine.'''
class BulkheadShutDown(BulkheadError): '''Raised when a bulkhead is being shut down and a party requests it to execute a coroutine.'''
class PoolError(RuntimeError): '''Raised when a task pool encounters a miscellaneous error.'''
class PoolFull(PoolError): '''Raised when the task queue in a task pool is filled.'''
class PoolShutDown(PoolError): '''Raised when submissions are sent to a shutting down pool.'''
class BusError(RuntimeError): '''Raised when an operation on an :class:`~channels.EventBus` fails.'''
class BusTimeout(BusError): '''Raised when an :class:`~channels.EventBus` takes too long to publish an event.'''
class BusShutDown(BusError): '''Raised when subscription or publishing operations are called on an :class:`~channels.EventBus` that is closing down.'''
class BusStatsError(BusError): '''Raised when attempting to access publishing statistics on an :class:`~channels.EventBus` whose statistics are not tracked.'''
class CircuitBreakerError(RuntimeError): '''Base class for circuit breaker errors.'''
class CircuitHalfOpen(CircuitBreakerError): '''Raised when a circuit exceeds its maximum calls in the half-open state.'''
class CircuitOpen(CircuitBreakerError): '''Raised when a circuit is open in a :class:`~altlocks.CircuitBreaker` (but shouldn't be).'''
class EventValueError(ValueError): '''Raised when a party attempts to get the value an event of which the value is not set.'''
class FutureCorrupted(RuntimeError): '''Raised after an internal party discovers an external party has set the result of a future whose result is for it to set only.'''
class MaxIterationsError(RuntimeError): '''Raised when a function has reached the specified maximum iterations.'''
class ItemsExhausted(ValueError): '''Raised when an asynchronous iterable runs out of items to take or collect.'''
class RateLimitExceeded(RuntimeError):
    '''Raised when a call to a function exceeds its rate limit and waiting is not allowed.
    The initialization signature is considered an implementation detail, may change without notice, and is therefore not documented here.'''
    async def repeat_call(self) -> Any: '''Repeat the call to the function that exceeded the rate limit without the rate limiter.'''
class BusPublishingError(BusError):
    '''Raised when an event bus fails to publish an event.'''
    def __init__(self, bus: EventBus, mw: Middleware, /): ...
    @property
    def bus(self) -> EventBus|None: '''May be None if the event bus was garbage-collected.'''
    @property
    def middleware(self) -> Middleware|None: '''May be None if the middleware was garbage-collected.'''
class LockForceRequest[T](BaseException):
    '''Thrown to coroutines that acquire locks when a locksmith (inheriting from :class:`locks.LocksmithBase`) necessitates the lock be released.'''
    def __init__(self, requester: LocksmithBase, fulfill: Callable[[Any], None], lock: AsyncLockLike[Any], info: T, /): ...
    @property
    def requester(self) -> LocksmithBase: '''The locksmith that sent this error.'''
    @property
    def lock(self) -> AsyncLockLike[Any]: '''The lock involved.'''
    def fulfill(self, answer: Any, /) -> None: '''Answer the request with `answer`, after presumably releasing the lock and performing error handling.'''
    @property
    def args(self) -> tuple[str, T]: '''The tuple `(error_message, additional_info)`.''' # type: ignore[override]
class PasswordQueueError(Exception): '''Base class for all errors related to password-protected queues, as returned by :func:`~queues.password_queue`.'''
class PasswordRetrievalError(PasswordQueueError):
    '''Raised when the `password_queue` function cannot find the password from the closure variables.'''
    @property
    def from_(self) -> str: '''The specified name of the closure variable.'''
    def __init__(self, from_: str): ...
class GetPasswordRetrievalError(PasswordRetrievalError): '''Raised when :func:`~queues.password_queue` cannot find the get password from the closure variables.'''
class PutPasswordRetrievalError(PasswordRetrievalError): '''Raised when :func:`~queues.password_queue` cannot find the put password from the closure variables.'''
class ForbiddenOperation(PasswordQueueError, TypeError):
    '''A forbidden operation was attempted on a password-protected queue.'''
    @property
    def op(self) -> str: '''A string representing the operation type.'''
    def __init__(self, op: str, *a: Any): '''Substitute in the arguments to the string (if any) to derive the name of the forbidden operation.'''
class PasswordError(PasswordQueueError):
    '''Raised when the wrong password is provided to the get or put methods of a password-protected queue.'''
    @property
    def wrongpass(self) -> Any: '''The wrong password associated with the exception. May be `None` if the wrong password has been garbage collected.'''
    @property
    def queue(self) -> Q[Any, Any]|None: '''The queue associated with the exception. May be `None` if the queue has been garbage collected.'''
class WrongPassword(PasswordError, ValueError):
    '''Raised when the wrong password of the correct type is provided to the get or put methods of a password-protected queue.'''
    def __init__(self, queue: Q[Any, Any], pwd: Any, /): ...
class WrongPasswordType[T, R: type](PasswordError, TypeError):
    '''Raised when the password provided to the get or put methods of a password-protected queue is of the incorrect type.'''
    def __init__(self, pwd: T, wrongtyp: type[T], queue: Q[Any, Any]|None, correcttyp: R, /): ...
    @property
    def wrongtype(self) -> type[T]|None: '''The wrong password type associated with the exception. May be `None` if the wrong password type has been garbage collected.'''
    @property
    def correcttype(self) -> R|None: '''The correct password type associated with the exception. May be `None` if the wrong password type has been garbage collected.'''
class PasswordMissing(PasswordQueueError, TypeError):
    '''Base class of :exc:`GetPasswordMissing` and :exc:`PutPasswordMissing`.'''
    def __init__(self) -> None: ...
    def __init_subclass__(cls, *, m: str=...) -> None: ...
class GetPasswordMissing(PasswordMissing): '''The get password was not passed to the get methods of a get-protected queue.'''
class PutPasswordMissing(PasswordMissing): '''The put password was not passed to the put methods of a put-protected queue.'''
class IgnoreErrors:
    '''Context manager to suppress errors of the specified types and exit once they occur; works in both sync and async.'''
    @property
    def exc(self) -> tuple[ExcType, ...]: '''The exception types that are ignored.'''
    @property
    def but(self) -> tuple[ExcType, ...]: '''The subclasses of exception types in :attr:`exc` that are not ignored.'''
    def __init__(self, /, *exc: ExcType, exclude: Iterable[ExcType]=...): '''The positional arguments are the exception classes to suppress within the context, and the iterable `exclude` will be consumed to build up :attr:`but`. All overlap is discarded.'''
    def __enter__(self) -> Self: '''Start suppressing the exceptions with types in `exc`, except those in :attr:`but`, and return the context manager instance.'''
    @overload
    def __exit__(self, exc_typ: ExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> bool: ...
    @overload
    def __exit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> Literal[False]: '''Stop suppressing the specified exceptions.'''
    async def __aenter__(self) -> Self: '''Async context support.'''
    @overload
    async def __aexit__(self, exc_typ: ExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> bool: ...
    @overload
    async def __aexit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> Literal[False]: '''Async context support.'''
    def excluding(self, *others: ExcType) -> Self: '''Return a new :class:`IgnoreErrors` instance that ignores the error types from itself except those from the others.'''
    def combined(self, *others: Self|ExcType|Iterable[Self]|Iterable[ExcType]) -> Self: '''Return a combined :class:`IgnoreErrors` instance that ignores all the error types from itself and the others and respects their exclusions.'''
class WarningToError:
    '''Async context manager to convert specific warnings to errors.'''
    def __init__(self, /, *typs: type[Warning]): '''Positional arguments represent warning types to convert to their corresponding error types if they are to occur within the context.'''
    def __enter__(self) -> Self: '''Note that an error is to be raised once one of the warning types is encountered within the context and return the context manager instance.'''
    @overload
    def __exit__(self, exc_typ: ExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> None: ...
    @overload
    def __exit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> None: '''Stop raising errors for the warning types specified.'''
    async def __aenter__(self) -> None: '''Async context support.'''
    @overload
    async def __aexit__(self, exc_typ: ExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> None: ...
    @overload
    async def __aexit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> None: '''Async context support.'''
ignore_all: IgnoreErrors
'''Instance of :class:`IgnoreErrors` that ignores all errors; that is, `IgnoreErrors(BaseException)`. Use with caution!'''
ignore_noncritical: IgnoreErrors
'''Instance of :class:`IgnoreErrors` that ignores all errors besides :exc:`SystemExit`, :exc:`SystemError` and :exc:`KeyboardInterrupt`. Equivalent to `ignore_all.excluding(CRITICAL)`.'''
ignore_typical: IgnoreErrors
'''Instance of :class:`IgnoreErrors` that ignores :exc:`Exception` and subclasses thereof. Equivalent to `IgnoreErrors()`.'''