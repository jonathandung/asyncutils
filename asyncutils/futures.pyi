# ty: ignore[instance-layout-conflict]
'''Various implementations of future and task classes, eager, time-aware and supporting asynchronous and no-argument callbacks.'''
from _collections_abc import Callable, Coroutine
from asyncio.events import AbstractEventLoop
from asyncio.futures import Future
from asyncio.tasks import Task
from contextvars import Context
from typing import Any, Self
__all__ = 'AsyncCallbacksFuture', 'AsyncCallbacksTask', 'EagerAsyncCallbacksFuture', 'EagerAsyncCallbacksTask', 'EagerTimeAwareAsyncCallbacksFuture', 'EagerTimeAwareAsyncCallbacksTask', 'TimeAwareAsyncCallbacksFuture', 'TimeAwareAsyncCallbacksTask', 'TimeAwareFuture', 'TimeAwareTask'
class TimeAwareFuture[T](Future[T]):
    '''A subclass of :class:`~asyncio.futures.Future` that can be compared to other :class:`TimeAwareFuture`'s based on the time they were created.'''
    def __lt__(self, other: Self, /) -> bool: ...
class TimeAwareTask[T](Task[T]):
    '''A subclass of :class:`~asyncio.tasks.Task` that can be compared to other :class:`TimeAwareTask`'s based on the time they were created.'''
    def __lt__(self, other: Self, /) -> bool: ...
class AsyncCallbacksFuture[T](Future[T]):
    '''A subclass of :class:`~asyncio.futures.Future` that supports calling asynchronous callbacks and callbacks with no arguments on completion.

    .. note:: To hook into the callbacks mechanism, subclassing :class:`_asyncio.Future` (the C-accelerated version) is impossible; i.e., using many of them may be noticeably slow.'''
    def __init__(self, *, loop: AbstractEventLoop|None=...): ...
    def add_async_callback(self, fn: Callable[[Self], Coroutine[Any, Any, Any]], /, *, context: Context|None=...) -> None: '''Add an asynchronous callback to be called when the future is done. The callback will be passed the future as an argument.'''
    def add_noargs_callback(self, fn: Callable[[], object], /, *, context: Context|None=...) -> None: '''Add a callback with no arguments to be called when the future is done.'''
    def add_noargs_async_callback(self, fn: Callable[[], Coroutine[Any, Any, Any]], /, *, context: Context|None=...) -> None: '''Add an asynchronous callback with no arguments to be called when the future is done.'''
    def remove_async_callback(self, fn: Callable[[Self], Coroutine[Any, Any, Any]], /) -> int: '''Remove an asynchronous callback. Returns the number of callbacks removed.'''
    def remove_noargs_callback(self, fn: Callable[[], object], /) -> int: '''Remove a callback with no arguments. Returns the number of callbacks removed.'''
    def remove_noargs_async_callback(self, fn: Callable[[], Coroutine[Any, Any, Any]], /) -> int: '''Remove an asynchronous callback with no arguments. Returns the number of callbacks removed.'''
class AsyncCallbacksTask[T](Task[T], AsyncCallbacksFuture[T]): '''The above, but a task.'''
class EagerAsyncCallbacksFuture[T](AsyncCallbacksFuture[T]): '''A subclass of :class:`AsyncCallbacksFuture` that uses an eager task factory.'''
class EagerAsyncCallbacksTask[T](AsyncCallbacksTask[T], EagerAsyncCallbacksFuture[T]): '''A subclass of :class:`AsyncCallbacksTask` that uses an eager task factory.'''
class TimeAwareAsyncCallbacksFuture[T](TimeAwareFuture[T], AsyncCallbacksFuture[T]): '''A subclass of :class:`AsyncCallbacksFuture` that can be compared to other :class:`TimeAwareAsyncCallbacksFuture`'s based on the time they were created.'''
class TimeAwareAsyncCallbacksTask[T](TimeAwareTask[T], AsyncCallbacksTask[T]): '''A subclass of :class:`AsyncCallbacksTask` that can be compared to other :class:`TimeAwareAsyncCallbacksTask`'s based on the time they were created.'''
class EagerTimeAwareAsyncCallbacksFuture[T](TimeAwareAsyncCallbacksFuture[T], EagerAsyncCallbacksFuture[T]): '''A subclass of :class:`TimeAwareAsyncCallbacksFuture` that uses an eager task factory.'''
class EagerTimeAwareAsyncCallbacksTask[T](TimeAwareAsyncCallbacksTask[T], EagerAsyncCallbacksTask[T]): '''A subclass of :class:`TimeAwareAsyncCallbacksTask` that uses an eager task factory.'''