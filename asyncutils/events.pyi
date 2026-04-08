'''Classes that extend the functionality of `asyncio.locks.Event` but do not inherit from it.'''
from .mixins import EventMixin
from asyncio.events import AbstractEventLoop
from _collections_abc import Generator
from typing import Literal, overload
__all__ = 'EventWithValue', 'SingleWaiterEventWithValue'
class SingleWaiterEventWithValue[T](EventMixin[T]):
    def __init__(self) -> None: ...
    def set(self, value: T) -> None: '''Set the result of the event, awakening the waiters.'''
    def clear(self) -> None: '''Unset the result of the event.'''
    def is_set(self) -> bool: '''Whether the result is currently set.'''
    async def wait_for_next(self, timeout: float|None=..., *, strict: bool=...) -> T: '''Wait for the next result of the event to be set.''' # type: ignore[override]
    def get(self) -> T: '''Get the result of the event immediately.'''
class EventWithValue[T](EventMixin[T]):
    def __init__(self, *, maxhist: int|None=...) -> None: '''Initialize an EventWithValue, storing a maximum of `maxhist` entries of past results, which defaults to `context.EVENT_WITH_VALUE_DEFAULT_MAXHIST`.'''
    @overload
    def set(self, value: None, strict: Literal[False]=...) -> None: '''Set the result of the event and wake up waiters. If strict is True, throws an error when the value is None.'''
    @overload
    def set(self, value: T, strict: bool=...) -> None: ...
    def remove_done_waiters(self) -> None: '''Should be run periodically to cleanup the internal queue of waiters, removing those having already completed.'''
    def set_once(self, value: T) -> None: '''Set the result to `value`, and then immediately revert it to the original.'''
    def clear(self) -> None: '''Unset the result of the event.'''
    @overload
    def get(self, strict: Literal[False]) -> T|None: '''Return the result set for the event immediately. If strict is False and the result is not set, return None.'''
    @overload
    def get(self, strict: Literal[True]=...) -> T: ...
    async def wait_for_next(self, timeout: float|None=...) -> T: '''Wait for the next result of the event to be set.''' # type: ignore[override]
    def is_set(self) -> bool: '''Whether the result is currently set.'''
    @property
    def history(self) -> list[tuple[float, T]]: '''The past results of the event as a list of tuples (timestamp, value).'''
    @property
    def history_asdict(self) -> dict[float, T]: '''Above, but as a dictionary.'''
    def recent_history(self, duration: float|None=...) -> Generator[tuple[float, T], None, None]: '''Yield recent history entries in order; what qualifies as recent depends on `duration`, defaulting to `context.EVENT_WITH_VALUE_DEFAULT_RECENT`.'''
    async def wait_for_transition(self, old: T, new: T, timeout: float|None=..., *, force_transition: bool=...) -> bool:
        '''Wait until the value is set to `old`, and then `new`. The timeout for which defaults to `context.EVENT_WITH_VALUE_DEFAULT_TIMEOUT`.
        If the timeout expires and force_transition is True, cause the transition to happen manually.
        Return whether the transition occurred naturally.'''
    async def wait_for_transition_unordered(self, a: T, b: T, timeout: float|None=..., *, force_transition: bool=..., loop: AbstractEventLoop|None=...) -> bool:
        '''Wait until either `a` transitions to `b` or `b` transitions to `a`, with the preference being for the former.
        An event loop can be explicitly passed to run the two waits simultaneously.'''