'''Various implementations of future and task classes, eager, time-aware and supporting asynchronous and no-argument callbacks.'''
from asyncio import AbstractEventLoop, Future, Task
from collections.abc import Awaitable, Callable
from contextvars import Context
from typing import Any, Literal, Self
__all__ = 'AsyncCallbacksFuture', 'AsyncCallbacksTask', 'TimeAwareAsyncCallbacksFuture', 'TimeAwareAsyncCallbacksTask', 'TimeAwareFuture', 'TimeAwareTask', 'TimeAwareUniqueCallbacksFuture', 'TimeAwareUniqueCallbacksTask', 'UniqueCallbacksFuture', 'UniqueCallbacksTask'
class TimeAwareFuture[T](Future[T]):
    '''A subclass of :class:`~asyncio.Future` that can be compared to other :class:`TimeAwareFuture`'s based on the time they were created.'''
    def __lt__(self, other: TimeAwareFuture[Any], /) -> bool: ...
class TimeAwareTask[T](Task[T]):
    '''A subclass of :class:`~asyncio.Task` that can be compared to other :class:`TimeAwareTask`'s based on the time they were created.'''
    def __lt__(self, other: TimeAwareFuture[Any], /) -> bool: ...
class AsyncCallbacksFuture[T](Future[T]):
    '''A subclass of :class:`~asyncio.Future` that supports calling asynchronous callbacks and callbacks with no arguments on completion.

    .. note:: To hook into the callbacks mechanism, subclassing the C-accelerated implementation of :class:`~asyncio.Future` is impossible; i.e., using many of them, for example when implementing a queue, may be slower.
    '''
    def __init__(self, *, loop: AbstractEventLoop|None=...): ...
    def add_async_callback(self, fn: Callable[[Self], Awaitable[object]], /, *, context: Context|None=...) -> None: '''Add an asynchronous callback to be called when the future is done. The callback will be passed the future as an argument.'''
    def add_noargs_callback(self, fn: Callable[[], object], /, *, context: Context|None=...) -> None: '''Add a callback with no arguments to be called when the future is done.'''
    def add_noargs_async_callback(self, fn: Callable[[], Awaitable[object]], /, *, context: Context|None=...) -> None: '''Add an asynchronous callback with no arguments to be called when the future is done.'''
    def remove_done_callback(self, fn: Callable[[Self], object], /) -> int: '''Remove a callback. Returns the number of callbacks removed.'''
    def remove_async_callback(self, fn: Callable[[Self], Awaitable[object]], /) -> int: '''Remove an asynchronous callback. Returns the number of callbacks removed.'''
    def remove_noargs_callback(self, fn: Callable[[], object], /) -> int: '''Remove a callback with no arguments. Returns the number of callbacks removed.'''
    def remove_noargs_async_callback(self, fn: Callable[[], Awaitable[object]], /) -> int: '''Remove an asynchronous callback with no arguments. Returns the number of callbacks removed.'''
class AsyncCallbacksTask[T](Task[T], AsyncCallbacksFuture[T]): '''Self-explanatory.'''
class TimeAwareAsyncCallbacksFuture[T](TimeAwareFuture[T], AsyncCallbacksFuture[T]): '''A subclass of :class:`AsyncCallbacksFuture` that can be compared to other :class:`TimeAwareAsyncCallbacksFuture`'s based on the time they were created.'''
class TimeAwareAsyncCallbacksTask[T](TimeAwareTask[T], AsyncCallbacksTask[T]): '''A subclass of :class:`AsyncCallbacksTask` that can be compared to other :class:`TimeAwareAsyncCallbacksTask`'s based on the time they were created.'''
class UniqueCallbacksFuture[T](Future[T]):
    '''Like :class:`AsyncCallbacksFuture`, but disallow the same callback from being added twice. Removal is faster and more intuitive to use.'''
    def __init__(self, *, loop: AbstractEventLoop|None=...): ...
    def add_done_callback(self, fn: Callable[[Self], object], /, *, context: Context|None=...) -> None: '''Add a callback to be called when the future is done. The callback will be passed the future as an argument.'''
    def add_async_callback(self, fn: Callable[[Self], Awaitable[object]], /, *, context: Context|None=...) -> None: '''Add an asynchronous callback to be called when the future is done. The callback will be passed the future as an argument.'''
    def add_noargs_callback(self, fn: Callable[[], object], /, *, context: Context|None=...) -> None: '''Add a callback with no arguments to be called when the future is done.'''
    def add_noargs_async_callback(self, fn: Callable[[], Awaitable[object]], /, *, context: Context|None=...) -> None: '''Add an asynchronous callback with no arguments to be called when the future is done.'''
    def remove_done_callback(self, fn: Callable[[Self], object], /) -> Literal[0, 1]: '''Remove a callback. Returns the number of callbacks removed.'''
    def remove_async_callback(self, fn: Callable[[Self], Awaitable[object]], /) -> Literal[0, 1]: '''Remove an asynchronous callback. Returns the number of callbacks removed.'''
    def remove_noargs_callback(self, fn: Callable[[], object], /) -> Literal[0, 1]: '''Remove a callback with no arguments. Returns the number of callbacks removed.'''
    def remove_noargs_async_callback(self, fn: Callable[[], Awaitable[object]], /) -> Literal[0, 1]: '''Remove an asynchronous callback with no arguments. Returns the number of callbacks removed.'''
class UniqueCallbacksTask[T](Task[T], UniqueCallbacksFuture[T]): '''Self-explanatory.'''
class TimeAwareUniqueCallbacksFuture[T](TimeAwareFuture[T], UniqueCallbacksFuture[T]): '''A subclass of :class:`UniqueCallbacksFuture` that can be compared to other :class:`TimeAwareUniqueCallbacksFuture`'s based on the time they were created.'''
class TimeAwareUniqueCallbacksTask[T](TimeAwareTask[T], UniqueCallbacksTask[T]): '''A subclass of :class:`UniqueCallbacksTask` that can be compared to other :class:`TimeAwareUniqueCallbacksTask`'s based on the time they were created.'''
