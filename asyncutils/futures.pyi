'''Various implementations of future and task classes, eager, time-aware and supporting asynchronous and no-argument callbacks.'''
from _collections_abc import Callable, Coroutine
from asyncio.events import AbstractEventLoop
from asyncio.futures import Future
from asyncio.tasks import Task
from contextvars import Context
from typing import Any, Self
__all__ = 'AsyncCallbacksFuture', 'AsyncCallbacksTask', 'EagerAsyncCallbacksFuture', 'EagerAsyncCallbacksTask', 'EagerTimeAwareAsyncCallbacksFuture', 'EagerTimeAwareAsyncCallbacksTask', 'TimeAwareAsyncCallbacksFuture', 'TimeAwareAsyncCallbacksTask', 'TimeAwareFuture', 'TimeAwareTask'
class TimeAwareFuture[T](Future[T]):
    '''A subclass of `asyncio.Future` that can be compared to other `TimeAwareFuture`s based on the time they were created.'''
    def __lt__(self, other: Self, /) -> bool: ...
class TimeAwareTask[T](Task[T]):
    '''A subclass of `asyncio.Task` that can be compared to other `TimeAwareTask`s based on the time they were created.'''
    def __lt__(self, other: Self, /) -> bool: ...
class AsyncCallbacksFuture[T](Future[T]):
    '''A subclass of asyncio.Future that supports calling asynchronous callbacks and callbacks with no arguments on completion.
    To hook into the callbacks mechanism, subclassing `_asyncio.Future` is infeasible; i.e., this future is noticeably slower than the C-accelerated version.'''
    def __init__(self, *, loop: AbstractEventLoop|None=...): ...
    def add_async_callback(self, fn: Callable[[Self], Coroutine[Any, Any, Any]], /, *, context: Context|None=...) -> None: ...
    def add_noargs_callback(self, fn: Callable[[], object], /, *, context: Context|None=...) -> None: ...
    def add_noargs_async_callback(self, fn: Callable[[], Coroutine[Any, Any, Any]], /, *, context: Context|None=...) -> None: ...
    def remove_async_callback(self, fn: Callable[[Self], Coroutine[Any, Any, Any]], /) -> int: ...
    def remove_noargs_callback(self, fn: Callable[[], object], /) -> int: ...
    def remove_noargs_async_callback(self, fn: Callable[[], Coroutine[Any, Any, Any]], /) -> int: ...
class AsyncCallbacksTask[T](Task[T], AsyncCallbacksFuture[T]): '''The above, but a task.'''
class EagerAsyncCallbacksFuture[T](AsyncCallbacksFuture[T]): '''A subclass of `AsyncCallbacksFuture` that uses an eager task factory.'''
class EagerAsyncCallbacksTask[T](AsyncCallbacksTask[T], EagerAsyncCallbacksFuture[T]): '''A subclass of `AsyncCallbacksTask` that uses an eager task factory.'''
class TimeAwareAsyncCallbacksFuture[T](TimeAwareFuture[T], AsyncCallbacksFuture[T]): '''A subclass of `AsyncCallbacksFuture` that can be compared to other `TimeAwareAsyncCallbacksFuture`s based on the time they were created.'''
class TimeAwareAsyncCallbacksTask[T](TimeAwareTask[T], AsyncCallbacksTask[T]): '''A subclass of `AsyncCallbacksTask` that can be compared to other `TimeAwareAsyncCallbacksTask`s based on the time they were created.'''
class EagerTimeAwareAsyncCallbacksFuture[T](TimeAwareAsyncCallbacksFuture[T], EagerAsyncCallbacksFuture[T]): '''A subclass of `TimeAwareAsyncCallbacksFuture` that uses an eager task factory.'''
class EagerTimeAwareAsyncCallbacksTask[T](TimeAwareAsyncCallbacksTask[T], EagerAsyncCallbacksTask[T]): '''A subclass of `TimeAwareAsyncCallbacksTask` that uses an eager task factory.'''