from .mixins import LoopContextMixin
from ._internal.protocols import Middleware, WildcardType
from asyncio.events import AbstractEventLoop
from asyncio.futures import Future
from asyncio.locks import Lock
from asyncio.queues import Queue
from asyncio.tasks import Task
from collections import defaultdict
from _collections_abc import Callable, Generator, AsyncGenerator, Mapping, Awaitable, Iterable
from contextlib import _GeneratorContextManager
from typing import Protocol, TypeGuard, Self, Any, Concatenate, Literal, NoReturn, type_check_only, overload
from _weakrefset import WeakSet
__all__ = 'EventBus', 'Observable', 'Rendezvous'
class Observable[**P](LoopContextMixin):
    type _Observer = Callable[Concatenate[Any, P], Awaitable[Any]]
    @type_check_only
    class _SubscriptionReturnType(Protocol):
        '''Not exposed.'''
        def __call__(self, strict: bool=...) -> None: ...
    @property
    def idle(self) -> bool: ...
    @property
    def notifying(self) -> bool: ...
    @overload
    async def notify(self, *a: P.args, **k: P.kwargs) -> None: ...
    @overload
    async def notify(self, *a: Any, _ret_exc_: bool=..., **k: Any) -> None: ...
    @overload
    def notify_sequential(self, *a: P.args, **k: P.kwargs) -> AsyncGenerator[Any]: ...
    @overload
    def notify_sequential(self, *a: Any, _silent_: bool=..., _persistent_: bool=..., **k: Any) -> AsyncGenerator[Any]: ...
    async def wait_for_next(self, timeout: float|None=..., strict: bool=...) -> tuple[tuple[Any, ...], dict[str, Any]]: ...
    async def wait_until_idle(self, timeout: float|None=...) -> None: ...
    async def subscribe(self, observer: _Observer) -> _SubscriptionReturnType: ...
    async def unsubscribe(self, observer: _Observer, strict: bool=...) -> None: ...
    async def handle_notifications(self) -> None: ...
    async def handle_unsubscriptions(self) -> None: ...
    def __init__(self, init_observers: Iterable[_Observer]=..., maxsize: int|None=...): ...
    def __iter__(self) -> Generator[_Observer]: ...
    def __aiter__(self) -> AsyncGenerator[_Observer]: ...
    async def __setup__(self) -> None: ...
    async def __cleanup__(self) -> None: ...
    def start_accumulation(self) -> bool: ...
    def restart_accumulation(self, flush: bool=...) -> None: ...
    def flush_notifications(self, timeout: float|None=...) -> None: ...
    def flush_unsubscriptions(self, timeout: float|None=...) -> None: ...
    def subscribe_nowait(self, observer: _Observer) -> _SubscriptionReturnType: ...
    def unsubscribe_eventually(self, observer: _Observer, asap: bool=...) -> None: ...
    def unsubscribe_nowait(self, observer: _Observer, strict: bool=...) -> None: ...
    def subscribe_syncf(self, observer: _Observer) -> _SubscriptionReturnType: ...
    def ntimes(self, observer: _Observer, n: int=...) -> _SubscriptionReturnType: ...
    def filter(self, pred: Callable[P, bool], ret_exc: bool=...) -> Self: ...
    def map(self, transform: Callable[P, tuple[Iterable[Any], Mapping[str, Any]]], ret_exc: bool=...) -> Observable[...]: ...
    def debounce(self, delay: float, ret_exc: bool=...) -> Self: ...
    def throttle(self, interval: float, ret_exc: bool=...) -> Self: ...
    def buffer(self, count: int, ret_exc: bool=...) -> Self: ...
    def at_change(self, key: Callable[P, object]=..., ret_exc: bool=...) -> Self: ...
    def fork(self, ret_exc: bool=...) -> Self: ...
    def merge(*obs: Self, ret_exc: bool=...) -> Self: ...
class EventBus(LoopContextMixin):
    '''A class abstracting the communication between notable events and asynchronous callbacks (an async auditing system), that can optionally be hooked up to sys.audit.
    Has extensive telemetry and middleware support, allowing data to be processed in a pipeline and eventually passed to subscribers. Subscribers must be hashable!
    A subscriber is a function that will be called every time data is published, with the corresponding data passed in. Publishing is thus the action of triggering these subscribers.
    Wildcard subscribers should take the event type as the first argument, and the event data as the next; while specific subscribers should take the event data as the only argument.
    Use instances as context managers only for proper setup and shutdown.'''
    WILDCARD: WildcardType
    '''Sentinel representing the event type of subscribers that accept any event name.'''
    def __init__(self, name: str=..., *, handler: Callable[[BaseException], None]=..., max_concurrent: int=..., tracking_stats: bool=...):
        '''name: The name of this event bus, which will appear in error messages.
        handler: A function that takes an exception having occurred in a subscribers and handles it.
        max_concurrent: The maximum number of concurrent callbacks; default 128.
        tracking_stats: Whether to remember the amount of published data to subscribers of each event type.'''
    def raise_for_shutdown(self) -> None: '''Throw an exception if the event bus is shutting down.'''
    def get_event_stats(self) -> defaultdict[str, int]: '''Return a copy of the stats, mapping event type to number of published events.'''
    @overload
    def subscribers_for(self, event_type: str) -> WeakSet[Callable[[Any], Awaitable[object]]]: ...
    @overload
    def subscribers_for(self, event_type: WildcardType) -> WeakSet[Callable[[str, Any], Awaitable[object]]]: '''A WeakSet of subscribers for the event type.'''
    def event_names(self) -> set[str]: '''A set of the current event types.'''
    def has_subscribers(self, event_type: str|WildcardType) -> bool: '''Whether the event type has any subscribers.'''
    @staticmethod
    def is_valid_event_type(event_type: object) -> TypeGuard[str|WildcardType]: '''Whether the object is a valid event type (i.e. a string or wildcard).'''
    @overload
    def is_subscribed(self, subscriber: Callable[[Any], Awaitable[object]], event_type: str=...) -> bool: ... # type: ignore[overload-overlap]
    @overload
    def is_subscribed(self, subscriber: Callable[[str, Any], Awaitable[object]], event_type: WildcardType=...) -> bool: ... # type: ignore[overload-overlap]
    @overload
    def is_subscribed(self, subscriber: object, event_type: object=...) -> Literal[False]: '''Whether the callback is subscribed for the event type, or subscribed for any event type if event_type is not passed.'''
    @property
    def total_subscribers(self) -> int: '''The total number of subscribers for any event type.'''
    @property
    def name(self) -> str: '''The name of the event bus.'''
    @property
    def wildcards(self) -> WeakSet[Callable[[str, Any], Awaitable[object]]]: '''All the wildcard subscribers for this event bus.'''
    @property
    def wildcard_count(self) -> int: '''The number of wildcard subscribers under this event bus.'''
    @property
    def active_tasks(self) -> int: '''The number of callbacks occurring at this moment.'''
    @property
    def stream_queue(self) -> Queue[tuple[str, Any]]|Queue[Any]:
        '''The asynchronous queue to which events are output by the event_stream method.
        The items in the queue are tuples (event_type, data) if the event type was not specified in the creation of the event stream, otherwise just the data attached to each event of that type.'''
    @stream_queue.setter
    def stream_queue(self, val: Queue[tuple[str, Any]|Any], /) -> None: ...
    def is_auditing(self) -> bool: '''Whether the event bus is connected to `sys.audit`.'''
    @property
    def auditing(self) -> bool: '''Get/set property for `is_auditing`. When changed, connect or disconnect the underlying audit hook accordingly.'''
    @auditing.setter
    def auditing(self, val: bool, /) -> None: ...
    def auditor(self, event: str, args: tuple[Any, ...], /) -> None: '''The auditor of the event bus. I can't think of a use case where you would call this directly. Not an instance method at runtime, just a function attached to the instance.'''
    def start_audit(self) -> None: '''Connect the bus' audit hook to sys.audit, creating if necessary. Incurs overhead. Use with caution.'''
    def stop_audit(self) -> None: '''Disconnect the bus' audit hook. Note that it is currently impossible to actually remove an audit hook, so this function just deactivates it.'''
    def add_middleware(self, middleware: Middleware) -> None:
        '''Append a middleware to the back of the pipe of middlewares. The middleware must be a hashable callable taking the event type as the first argument and the associated data as the second.
        If the middleware does not recognize the event type, it should simply return the data immediately. There is no protection in place against malicious malware besides the user's abstraction.
        It is preferred that the middleware be a coroutine function. Each middleware should be extremely optimized, for example through C extensions, to avoid hindrance of the publishing.
        When publishing occurs, the following is done asynchronously.
        The first middleware takes the initial data, does some processing, and passes the modified data to the second middleware, and so on.
        The output of the final middleware is passed to each subscriber concurrently. They cannot see the initial data.'''
    def remove_middleware(self, middleware: Middleware, *, result: Any=..., strict: bool=...) -> Any:
        '''Remove a previously added middleware, via `add_middleware` or `add_middleware_once`, and return its result. Runs in O(1) time.
        If `strict` is True and the middleware was never added, throw a KeyError.
        If the middleware has an associated future `add_middleware_once` and it is done, return its result. Otherwise, set its result to `result` and return it.'''
    def add_middleware_once(self, middleware: Middleware, until: Future[Any]) -> bool:
        '''Add a middleware that should take effect until the future `until` is done, after which the result of the future will be treated as the result of the middleware.
        If the middleware has already been associated with another future, do nothing and return False.'''
    def audit_context(self) -> _GeneratorContextManager[None, None, None]:
        '''Start receiving publications from sys.audit upon entry and stop on exit. Use as a context manager.
        Note that publish does not trigger sys.audit; it is the other way around to avoid infinite recursion.'''
    def tracking_context(self, stats_receiver: Future[Mapping[str, int]]|None=...) -> _GeneratorContextManager[None, None, None]: '''Context manager, under which stats are tracked and finally sent to the stats_receiver future.'''
    def start_tracking(self) -> None: '''Start tracking event publication statistics (number of publications under each event type).'''
    @overload
    def stop_tracking(self, ret_stats: Literal[False]=...) -> None: '''Stop tracking event publication statistics.'''
    @overload
    def stop_tracking(self, ret_stats: Literal[True]) -> defaultdict[str, int]: ...
    @overload
    async def subscribe[C: Callable[[Any], Awaitable[object]]](self, subscriber: C, /, event_type: str) -> C: '''Add a subscriber to the event bus under the specified event type (if unspecified, add as wildcard). Return the subscriber to allow usage as a decorator.'''
    @overload
    async def subscribe[C: Callable[[str, Any], Awaitable[object]]](self, subscriber: C, /, event_type: WildcardType=...) -> C: ...
    @overload
    async def unsubscribe(self, subscriber: Callable[[Any], Awaitable[object]], /, event_type: str) -> bool: '''Remove a subscriber from the event bus under the event type (if unspecified, remove from wildcards) and return whether the removal occurred.'''
    @overload
    async def unsubscribe(self, subscriber: Callable[[str, Any], Awaitable[object]], /, event_type: WildcardType=...) -> bool: ...
    @overload
    def subscribe_to[C: Callable[[Any], Awaitable[object]]](self, event_type: str) -> Callable[[C], C]: '''A decorator factory for functions to subscribe to this event bus under the specified event type.'''
    @overload
    def subscribe_to[C: Callable[[str, Any], Awaitable[object]]](self, event_type: WildcardType) -> Callable[[C], C]: ...
    def sync_start_publish(self, event_type: str, data: Any=..., *, safe: bool=..., timeout: float|None=..., chaperone: Callable[[ExceptionGroup|Exception], object]|None=...) -> None: '''Begin a publication synchronously. Parameters are as in `publish`, below.'''
    async def publish(self, event_type: str, data: Any=..., *, wait: bool=..., safe: bool=..., timeout: float|None=..., chaperone: Callable[[ExceptionGroup|Exception], object]|None=...) -> None:
        '''Publish an event, that is, some data attached to an event type, to the subscribers involved, with timeout `timeout`.
        Each subscriber for that event type and wildcard subscribers will be triggered by the publication, receiving the data after processing by the middlewares in order.
        If `wait` is False (default True), don't wait for the publication to complete.
        If `safe` is False (default True), don't wrap callbacks with proper error handling.
        `chaperone`, if passed, should be a function processing non-severe exceptions (instances of Exception and ExceptionGroup) in the callbacks. Otherwise, these
        exception( group)s are flattened and collected into an ExceptionGroup and finally thrown, which the caller should be prepared to handle.'''
    async def wait_for_event(self, event_type: str, *, timeout: bool|None=..., condition: Callable[[Any], object]=...) -> Task[Any]:
        '''Wait for an event of the specified event type that satisfies the condition to occur.
        Note that the function completes once the subscription has registered and returns a task, which will be cancelled on timeout.'''
    @overload
    async def subscribe_until[T](self, fut: Future[T], subscriber: Callable[[str], Awaitable[object]], event_type: str, till_permanent: float|None=...) -> Task[T]:
        '''Add the subscriber under the event type (as a wildcard without event_type) and return a task.
        The subscriber is removed once `fut` completes, and its result returned through the returned task.
        After `till_permanent` seconds elapse (if passed), the task errors and the subscriber is left under that event type.'''
    @overload
    async def subscribe_until[T](self, fut: Future[T], subscriber: Callable[[str, Any], Awaitable[object]], event_type: WildcardType=..., till_permanent: float|None=...) -> Task[T]: ...
    @overload
    async def feed_event(self, data: Any, *, timeout: float|None=...) -> None: '''Feed the data for an event into the event stream, the queue for which is created if necessary, such that the event stream needs not be active.'''
    @overload
    async def feed_event(self, event_type: str, data: Any, *, timeout: float|None=...) -> None: ...
    @overload
    def event_stream(self, event_type: str, *, timeout: float|None=..., item_timeout: float|None=..., bufsize: int=...) -> AsyncGenerator[Any]: ...
    @overload
    def event_stream(self, *, timeout: float|None=..., item_timeout: float|None=..., bufsize: int=...) -> AsyncGenerator[tuple[str, Any], None]: '''Open an event stream for the event type.'''
    async def shutdown(self, immediate: bool=..., timeout: float|None=..., preserve_stats: bool=...) -> None:
        '''Gracefully shut down the event bus, within `timeout` if specified.
        After the shutdown, publications fail fast and middlewares are cleared.
        This waits for as many subscriber callbacks to complete as possible.
        If immediate is True, getters for the queue for the event stream will error immediately.
        If preserve_stats is True, the event publication statistics will be saved. Access using get_event_stats.'''
    async def handle_exception(self, e: BaseException) -> None: '''Asynchronously handle an exception according to the `handler` initialization parameter, which can be a sync or async function.'''
    @overload
    def clear(self, event_type: str) -> WeakSet[Callable[[Any], Awaitable[object]]]|None: ...
    @overload
    def clear(self, event_type: WildcardType) -> WeakSet[Callable[[str, Any], Awaitable[object]]]|None: ...
    @overload
    def clear(self) -> None: '''Remove all subscribers for the event type, or all subscribers if not passed.'''
    def clear_all(self) -> None: '''Remove all subscribers and clear statistics.'''
    def subscriber_count(self, event_type: str|WildcardType) -> int: '''The number of subscribers for that event type.'''
    def clear_wildcards(self) -> WeakSet[Callable[[str, Any], Awaitable[object]]]|None: '''Equivalent to bus.clear(EventBus.WILDCARD).'''
    def clear_stats(self) -> None: '''Clear the event publication statistics.'''
    async def __setup__(self) -> None: ...
    async def __cleanup__(self) -> None: ...
class Rendezvous[T]:
    '''A rendezvous object, emulating Golang's unbuffered channels. Usage:
    >>> rdv = Rendezvous()
    >>> (await asyncio.gather(*map(rdv.put, range(5, 10)), rdv.exchange(10), *map(rdv.exchange, range(1, 5)), *(rdv.get() for _ in range(5))))[-10:]
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    >>> task = rdv._loop.create_task(rdv.put(0))
    >>> await rdv.state_snapshot()
    StateSnapshot(num_getters=0, num_putters=1, num_ops=1, idle=False)
    >>> await rdv.get()
    0
    >>> await rdv.get('default')
    'default'
    >>> await task
    True
    >>> task = rdv._loop.create_task(rdv.get())
    >>> await rdv.reset()
    >>> task.cancelled()
    True'''
    def __init__(self, *, loop: AbstractEventLoop=..., lock: Lock=...): '''If loop is not passed, the running event loop is used. If there is no running event loop, one is created and set.'''
    async def raising_put(self, value: T, /, *, timeout: float) -> None:
        '''Put in a value to the rendezvous, blocking until it is gotten or timeout is reached, at which point TimeoutError is raised and the put cancelled.
        Also be prepared to intercept or reraise CancelledError resulting from reset.'''
    async def put(self, value: T, /, *, timeout: float|None=...) -> bool:
        '''Like raising_put, but returns a boolean representing if the put succeeded. The recommended interface.
        May still raise CancelledError when the Rendezvous is reset, which should be allowed to propagate.'''
    async def get(self, default: T|None=..., *, timeout: float|None=...) -> T:
        '''Get a value from the rendezvous, blocking until available unless default is passed and timeout is not, in which case the default is returned if a value is not immediately available.
        If default is not passed and the timeout is reached, the TimeoutError is propagated. In any case, the get is cancelled at timeout.'''
    async def cleanup(self) -> None: '''Clean up the internal getter and putter stacks.'''
    async def reset(self) -> None:
        '''Reset the Rendezvous. Call from a monitoring task when a deadlock appears to have occurred.
        This cancels all pending gets, puts and exchanges; their callers will see CancelledError.'''
    @type_check_only
    class StateSnapshot(tuple[int, int, int, bool]):
        '''Does not exist at runtime.'''
        @property
        def num_getters(self) -> int: '''Current number of slots waiting for values.'''
        @property
        def num_putters(self) -> int: '''Current number of values waiting for slots.'''
        @property
        def num_ops(self) -> int: '''num_getters+num_putters'''
        @property
        def idle(self) -> bool: '''num_getters == num_putters == 0'''
    def __length_hint__(self) -> int: '''Approximate number of operations pending; for operator.length_hint.'''
    async def state_snapshot(self) -> StateSnapshot: '''Trigger a cleanup and return a snapshot of the current state of the object.'''
    async def exchange(self, put_val: T, /, *, timeout: float|None=..., asap: bool=...) -> T:
        '''Put in a value to the rendezvous and get a different one back, not necessarily in that order.
        If asap is True, don't wait for the put to complete.'''
    async def _put_helper(self, value: T, /) -> Future[None]: '''Request a value be put into the rendezvous, returning an asyncio.Future. When cancelled, the put is cancelled as well. When done, the value has been handed off to a getter.'''
    async def _maintainer(self) -> NoReturn: '''Periodically clean up done getters and putters.'''