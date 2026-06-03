'''| Classes that extend the functionality of :class:`~asyncio.locks.Event` with the interface it specifies, without inheriting from it.
| Not at all related to the :mod:`asyncio.events` submodule, which manages the event loop, despite the common name.'''
from .mixins import EventMixin
from collections.abc import Generator
from ty_extensions import Not
from typing import Literal, overload
__all__ = 'EventWithValue', 'SingleWaiterEventWithValue'
class SingleWaiterEventWithValue[T](EventMixin[T]):
    '''Essentially wraps a future in the event interface.'''
    def set(self, value: T) -> None: '''Set the result of the event to ``value``, awakening the sole waiter.'''
    def clear(self) -> None: '''Unset the result of the event.'''
    def is_set(self) -> bool: '''Whether the result is currently set.'''
    async def wait(self, timeout: float|None=..., *, strict: bool=...) -> T: ...
    async def wait_for_next(self, timeout: float|None=..., *, strict: bool=...) -> T: '''Wait for the next result of the event to be set.'''
    def get(self, default: T=...) -> T: '''Get the result of the event immediately if set, otherwise returning ``default`` if passed or throw :exc:`RuntimeError`.'''
class EventWithValue[T: Not[None]](EventMixin[T]):
    '''An event class that can store a value and maintains a history of past values.'''
    def __init__(self, *, maxhist: int|None=...) -> None: '''A maximum of ``maxhist`` entries, which defaults to :const:`context.EVENT_WITH_VALUE_DEFAULT_MAX_HIST`, of past results, are stored.'''
    @overload
    def set(self, value: None, *, strict: Literal[False]) -> None: ...
    @overload
    def set(self, value: T, *, strict: bool=...) -> None: '''Set the result of the event and wake up waiters. If ``strict`` is ``True``, throws an error when the value is ``None``, since it is more idiomatic to call :meth:`clear` instead.'''
    def remove_done_waiters(self) -> None: '''Should be run periodically to cleanup the internal queue of waiters, removing those having already completed.'''
    def set_once(self, value: T) -> None: '''Set the result to ``value``, and then immediately revert it to the original. Waiters are triggered twice.'''
    def clear(self) -> None: '''Unset the result of the event.'''
    def get(self, default: T=...) -> T: '''Get the result of the event immediately if set, otherwise returning ``default`` if passed or throw :exc:`RuntimeError`.'''
    async def wait_for_next(self, timeout: float|None=...) -> T: '''Wait for the next result of the event to be set.'''
    def is_set(self) -> bool: '''Whether the result is currently set.'''
    @property
    def history(self) -> list[tuple[float, T]]: '''The past results of the event as a list of tuples ``(timestamp, value)``.'''
    @property
    def history_asdict(self) -> dict[float, T]: '''Above, but as a dictionary.'''
    def recent_history(self, duration: float|None=...) -> Generator[tuple[float, T]]: '''Yield recent history entries in order; what qualifies as recent depends on ``duration``, defaulting to :const:`context.EVENT_WITH_VALUE_DEFAULT_RECENT`.'''
    async def wait_for_transition(self, old: T, new: T, timeout: float|None=..., *, force_transition: bool=..., legacy: bool=...) -> bool:
        '''| Wait until the value is set to ``old``, and then ``new``, in that order.
        | ``timeout`` defaults to :const:`context.EVENT_WITH_VALUE_DEFAULT_TIMEOUT`
        | On timeout, if ``force_transition`` is ``True``, cause the transition to happen manually.
        | Return whether the transition occurred naturally.

        .. version-changed:: 0.9.6
          Fixed a bug where overlapping potential transitions are not considered. The old behaviour can be achieved by passing ``legacy=True``.'''
    async def wait_for_transition_unordered(self, a: T, b: T, timeout: float|None=..., *, force_transition: bool=..., legacy: bool=...) -> bool: '''Wait until either ``a`` transitions to ``b`` or ``b`` transitions to ``a``, with the preference being for the former.'''