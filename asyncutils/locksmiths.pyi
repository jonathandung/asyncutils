# ruff: noqa: D401
'''Implementation of a base class for locksmiths, magical entities that can compel not intentionally uncooperative locks to be released while limiting collateral damage and hindrance of the control flow of the program as much as possible and allowing customization of behaviour in different steps regarding some locks.'''
from ._internal.prots import AsyncLockLike
from asyncio import AbstractEventLoop, Task
from collections.abc import Awaitable, Callable
from enum import IntEnum
from typing import Any, ClassVar, Literal, TypeGuard, final
__all__ = 'ForceResult', 'LocksmithBase', 'RecognitionResult', 'succeeded'
def succeeded(result: object, /) -> TypeGuard[Literal[ForceResult.SUCCESS, ForceResult.RELEASED, RecognitionResult.ALREADY_RECOGNIZED, RecognitionResult.SUCCESS]]: '''Return whether the given result is a successful one.'''
class ForceResult(IntEnum):
    '''The possible results of a force attempt.'''
    UNFORCEABLE = 1
    NO_CURRENT_TASK = 2
    OWNER_COMPLETED = 3
    ALREADY_BEING_FORCED = 4
    FAILURE = 5
    RELEASED_WITH_FALSE = 6
    SUCCESS = 7
    RELEASED = 8
class RecognitionResult(IntEnum):
    '''The possible results of a recognition attempt.'''
    FAILED_PRELIM = 1
    FAILED_ACK = 2
    ALREADY_RECOGNIZED = 3
    SUCCESS = 4
class LocksmithBase:
    '''Instances can attempt to force specific locks asynchronously, and run cleanup or emergency tasks under it as soon as possible; this is especially useful in deadlock scenarios.'''
    handlers: ClassVar[dict[type[AsyncLockLike[Any]], Callable[[AsyncLockLike[Any]], Any]]]
    '''A mapping of lock types to handler functions, which are callables that take a lock of the corresponding type and perform any lock-specific logic necessary for forcing it.'''
    def __init__(self, loop: AbstractEventLoop|None=..., lcls: type[AsyncLockLike[Any]]=...): '''Initialize the locksmith. ``loop`` is the event loop to use, defaulting to the current running loop. ``lcls`` is the type of locks that this locksmith will attempt to force, defaulting to :class:`asyncio.Lock`.'''
    @property
    def currently_recognized(self) -> frozenset[AsyncLockLike[Any]]: '''A :class:`frozenset` of locks that this locksmith currently recognizes.'''
    @classmethod
    def register_handler[T: AsyncLockLike[Any]](cls, h: Callable[[T], object], /, *, shadow: bool=...) -> Callable[[type[T]], type[T]]: '''Return a decorator for async lock classes, taking a handler function and returning an identity decorator.'''
    async def _wait_on[T](self, task: Awaitable[T], lock: AsyncLockLike[Any], /) -> T: '''Wait on the task and release the lock. Only called by :meth:`host` when it successfully acquires the lock; not for public use.'''
    async def recognize_lock(self, lock: AsyncLockLike[Any], /) -> RecognitionResult: '''Recognize the given lock as one that this locksmith can handle.'''
    @final
    async def force(self, lock: AsyncLockLike[Any], /, info: object=..., *, purge_waiters: bool=...) -> ForceResult:
        '''| The main feature of the locksmith; that is, to try to force the lock ``lock``.
        | This method cannot be overridden, because it already delegates lock-specific behaviour to overridable methods and handlers in its core logic.
        | ``info``, if passed, should be an object representing the context of the force attempt, and will be passed to the exception thrown to the
        | task asking to release the lock.
        '''
    async def host[T](self, task: Awaitable[T], lock: AsyncLockLike[Any], /, *, timeout1: float|None=..., timeout2: float|None=..., timeout3: float|None=...) -> T: '''Run ``task`` holding ``lock`` immediately after forcing it. The default values of the timeouts are taken from :const:`~asyncutils.context.Context.LOCKSMITH_BASE_DEFAULT_TIMEOUTS`.'''
    async def get_info(self, lock: AsyncLockLike[Any], /) -> Any: '''Return information about the lock that will be passed to the forcing request.''' # noqa: ANN401
    async def lock_busy(self, lock: AsyncLockLike[Any], requester: LocksmithBase, context: dict[str, Any], /) -> None: '''Called when a :class:`~asyncutils.exceptions.LockForceRequest` by a different locksmith propagates, meaning that another locksmith is trying to do the same thing. The ``context`` parameter is a dictionary that can be passed to ``extra`` of a log record, for example. The implementation is allowed to call :meth:`lock_busy` on the requester in this method with a modified ``context``, but care should be taken to avoid infinite recursion.'''
    async def purge_waiters(self, lock: AsyncLockLike[Any], /) -> None: '''Clear all waiters on the lock after a force attempt, if necessary. The default implementation assumes this data is attached to the lock as its ``_waiters`` attribute, which is a data structure that evaluates to whether it still has any items in a boolean context, with a :meth:`~list.pop` method.'''
    async def task_reraised_request(self, lock: AsyncLockLike[Any], /) -> None: '''Called when a task that was forced to release the lock does not handle or re-raises the exception.'''
    async def throw_fallback(self, lock: AsyncLockLike[Any], /) -> ForceResult: '''Called when the locksmith attempts to force a lock but there is no current task that owns it or it could not be found, and no task appears to be running. Its return value is returned by :meth:`force`.'''
    async def eager_fallback(self, lock: AsyncLockLike[Any], /) -> ForceResult: '''Called when the locksmith attempts to force a lock but the owner task appears to have completed, since it has no coroutine. Its return value is returned by :meth:`force`.'''
    async def release_returned_false(self, lock: AsyncLockLike[Any], /) -> ForceResult: '''Called when the locksmith attempts to force a lock and its release method returns ``False``, which is a common convention for indicating that the lock was not actually released. Its return value is returned by :meth:`force`.'''
    async def already_forcing(self, lock: AsyncLockLike[Any], /) -> ForceResult: '''Called when the locksmith attempts to force a lock but it is already being forced by another locksmith, which is detected when the task that owns the lock raises the exception thrown by :meth:`force` instead of handling it. Its return value is returned by :meth:`force`.'''
    async def answer_received(self, lock: AsyncLockLike[Any], answer: object, /) -> None: '''Called when a task that was forced to release the lock responds to the exception thrown by :meth:`force` by setting a value on it, which is detected by :meth:`host`. ``answer`` is the value that the task set on the exception.'''
    async def task_raised_other(self, lock: AsyncLockLike[Any], exc: BaseException, /) -> None: '''Called when a task raises a non-critical exception in response to a force request. The default implementation logs the exception if it is not a :class:`RuntimeError`, since those are commonly raised when a task is cancelled.'''
    def wrap_task[T](self, aw: Awaitable[T], /) -> Task[T]: '''Wrap the given awaitable in a task using the locksmith's event loop.'''
    def find_owner(self, lock: AsyncLockLike[Any], /) -> Task[Any]|None: '''Return the owner of the lock, if it can be found. The default implementation assumes that the ``_owner`` attribute of the lock, if present, points to the task that owns it or ``None``.'''
    def preliminary_check_lock(self, lock: AsyncLockLike[Any], /) -> bool: '''Return whether the lock passes preliminary checks for recognition. The default implementation checks whether the lock has the :meth:`~asyncio.Lock.acquire`, :meth:`~asyncio.Lock.release`, and :meth:`~asyncio.Lock.locked` methods.'''
    def can_force_lock_held(self, lock: AsyncLockLike[Any], /) -> bool: '''Return whether the locksmith can force the lock, given that the internal lock is held. The default implementation allows forcing if the lock is recognized and not currently locked.'''
    def patch_owner(self, task: Task[Any], lock: AsyncLockLike[Any], /) -> None: '''Change the owner of the lock to the given task. The default implementation sets the ``_owner`` attribute of the lock to the task, if it exists.'''
    def task_raised_critical(self, lock: AsyncLockLike[Any], exc: BaseException, /) -> Literal[ForceResult.FAILURE]: '''Called when a task raises a critical exception in response to a force request. The default implementation throws the exception wrapped in :exc:`~asyncutils.exceptions.Critical`, rather than returning any value to :meth:`force`. This is not async because it is imperative that the exception be dealt with quickly. Subclasses can choose to return :const:`ForceResult.FAILURE` after some handling as well.'''
