'''Bridges between asynchronous consumers/subscribers and producers/publishers.'''
from ._internal.prots import DualContextManager, Middleware, Observer, SpecificSubscriber, SubscriptionRV, StateSnapshot, WildcardSubscriber, WildcardType
from .mixins import LoopContextMixin
from asyncio import AbstractEventLoop, Future, Lock, Queue, Task
from collections import defaultdict
from collections.abc import AsyncGenerator, Callable, Iterable, Iterator, Mapping
from typing import Any, Literal, Self, TypeGuard, overload
from weakref import WeakSet
__all__ = 'EventBus', 'Observable', 'Rendezvous'
class Observable[**P](LoopContextMixin):
    '''A class representing an observable stream of data, that observers can subscribe to and receive notifications from. Observers must be hashable!

    .. caution:: Use instances of this class as context managers only.'''
    @property
    def idle(self) -> bool: '''Whether the observable is idle, that is, not currently notifying observers.'''
    @property
    def notifying(self) -> bool: '''The opposite of :attr:`idle`.'''
    @overload
    async def notify(self, *a: P.args, **k: P.kwargs) -> None: ...
    @overload
    async def notify(self, *a: object, _ret_exc_: bool=..., **k: object) -> None: '''Notify the observers with the parameters passed in. If another notification is in progress, it will be queued to be completed by that notification. If ``_ret_exc_`` is ``True`` (default ``False``), exceptions occurring in any observer is not propagated.'''
    @overload
    def notify_sequential(self, *a: P.args, **k: P.kwargs) -> AsyncGenerator[Any]: ...
    @overload
    def notify_sequential(self, *a: object, _silent_: bool=..., _persistent_: bool=..., **k: object) -> AsyncGenerator[Any]: '''Version of :meth:`notify` that doesn't attempt to trigger the observers in parallel.'''
    async def wait_for_next(self, timeout: float|None=..., strict: bool=...) -> tuple[tuple[Any, ...], dict[str, Any]]: '''Wait for the next notification to occur by adding a temporary subscriber and return its parameters as a tuple ``(args, kwargs)``. If ``strict`` is ``True``, assert that another operation did not remove the subscriber prematurely.'''
    async def wait_until_idle(self, timeout: float|None=...) -> None: '''Wait until the observable is idle, that is, until all notifications have completed.'''
    async def subscribe(self, observer: Observer[P]) -> SubscriptionRV: '''Call :meth:`wait_until_idle`, then add an observer and return a subscription object that can be used to remove it.'''
    async def unsubscribe(self, observer: Observer[P], strict: bool=...) -> None: '''Call :meth:`wait_until_idle`, then remove the observer. If ``strict`` is ``True``, assert that the observer was indeed subscribed.'''
    async def handle_notifications(self) -> None: '''Execute the queued notifications one by one and wait for each to complete.'''
    async def handle_unsubscriptions(self) -> None: '''Perform the unsubscriptions as requested by :meth:`unsubscribe_eventually`.'''
    @overload
    def __init__(self, init_observers: Iterable[Observer[P]], maxsize: int|None=...): ...
    @overload
    def __init__(self, *, maxsize: int|None=...): '''Instantiate the observable with the initial observers taken from the iterable ``init_observers``. If ``maxsize`` is ``None``, accumulation of notifications is disabled; otherwise, it is the maximum size of the queue of notifications (default is no maximum).'''
    def __iter__(self) -> Iterator[Observer[P]]: '''Iterate over the current observers. When this iterator is active, no subscriptions or unsubscriptions can be done.'''
    def __aiter__(self) -> AsyncGenerator[Observer[P]]: '''Return an async generator over the observers.'''
    async def __setup__(self) -> None: ...
    async def __cleanup__(self) -> None: ...
    def start_accumulation(self) -> bool: '''Begin accumulation of notifications and return ``True``, or return ``False`` if accumulation is already occurring.'''
    async def restart_accumulation(self, flush: bool=...) -> None: '''Complete all notifications if ``flush`` is ``True``, then restart notification accumulation.'''
    def subscribe_nowait(self, observer: Observer[P]) -> SubscriptionRV: '''Add an observer without waiting for the observable to be idle.'''
    def unsubscribe_eventually(self, observer: Observer[P], asap: bool=...) -> None: '''Note that the observer is to be removed at some point in the future. If ``asap`` is ``True`` and there is no notification running, the observer is removed immediately.'''
    def unsubscribe_nowait(self, observer: Observer[P], strict: bool=...) -> None: '''Remove the observer immediately even if a notification is occurring. If ``strict`` is ``True``, assert that the observer was indeed subscribed.'''
    def subscribe_syncf(self, observer: Observer[P]) -> SubscriptionRV: '''Subscribe a synchronous observer by converting it to async in an executor.'''
    def ntimes(self, observer: Observer[P], n: int=...) -> SubscriptionRV: '''Add an observer immediately and automatically have it removed after ``n`` notifications. ``n`` defaults to :const:`~asyncutils.context.Context.OBSERVABLE_DEFAULT_NTIMES_N`.'''
    def filter(self, pred: Callable[P, bool], ret_exc: bool=...) -> Self: '''Return a new observable emitting the notifications of this observable to its observers only when the parameters, starred and passed to ``pred``, evaluate to a true value.'''
    def map(self, transform: Callable[P, tuple[Iterable[object], Mapping[str, object]]], ret_exc: bool=...) -> Observable[...]: '''Return a new observable transforming the parameters of notifications from this observable by ``transform``.'''
    def debounce(self, delay: float, ret_exc: bool=...) -> Self: '''Return a new observable that will only emit the latest notification after ``delay`` seconds have passed since the last notification.'''
    def throttle(self, interval: float, ret_exc: bool=...) -> Self: '''Return a new observable that will emit notifications at most once every ``interval`` seconds.'''
    def buffer(self, count: int, ret_exc: bool=...) -> Self: '''Return a new observable that will buffer notifications and emit them concurrently in batches of size ``count``.'''
    def at_change(self, key: Callable[P, object]=..., ret_exc: bool=...) -> Self: '''Return a new observable that will only emit notifications when the value returned by ``key`` changes.'''
    def fork(self, ret_exc: bool=...) -> Self: '''Return a new observable that will emit all notifications to its observers.'''
    def merge(*obs: Self, ret_exc: bool=...) -> Self: '''Return a new observable that will emit notifications from all the observables in ``obs``.'''
class EventBus(LoopContextMixin):
    '''| A class abstracting the communication between notable events and asynchronous callbacks (an async auditing system), that can optionally be hooked up to sys.audit.
    | Has extensive telemetry and middleware support, allowing data to be processed in a pipeline and eventually passed to subscribers. Subscribers must be hashable!
    | A subscriber is a function that will be called every time data is published, with the corresponding data passed in. Publishing is thus the action of triggering these subscribers.
    | Wildcard subscribers should take the event type as the first argument, and the event data as the next; while specific subscribers should take the event data as the only argument.

    .. caution:: Use instances as context managers only for proper setup and shutdown.
    .. version-changed:: 0.9.5
      Support for repeated, unhashable middlewares and removal using an opaque cookie was added.'''
    WILDCARD: WildcardType
    '''Sentinel representing the event type of subscribers that accept any event name.'''
    def __init__(self, name: str=..., *, handler: Callable[[BaseException], None]=..., max_concurrent: int=..., tracking_stats: bool=...):
        '''All arguments are optional:

        * ``name``: The name of this event bus, which will appear in error messages.
        * ``handler``: A function that takes an exception having occurred in a subscribers and handles it.
        * ``max_concurrent``: The maximum number of concurrent callbacks; default :const:`~asyncutils.context.Context.EVENT_BUS_DEFAULT_MAX_CONCURRENT`.
        * ``tracking_stats``: Whether to remember the amount of published data to subscribers of each event type.'''
    def raise_for_shutdown(self) -> None: '''Throw an exception if the event bus is shutting down.'''
    def get_event_stats(self) -> defaultdict[str, int]: '''Return a copy of the stats, mapping event type to number of published events.'''
    @overload
    def subscribers_for(self, event_type: str) -> WeakSet[SpecificSubscriber]: ...
    @overload
    def subscribers_for(self, event_type: WildcardType) -> WeakSet[WildcardSubscriber]: '''A :class:`weakref.WeakSet` of subscribers for the event type.'''
    def event_names(self) -> set[str]: '''A set of the current event types.'''
    def has_subscribers(self, event_type: str|WildcardType) -> bool: '''Whether the event type has any subscribers.'''
    @staticmethod
    def is_valid_event_type(event_type: object) -> TypeGuard[str|WildcardType]: '''Whether the object is a valid event type (i.e. a string or wildcard).'''
    @overload
    def is_subscribed(self, subscriber: SpecificSubscriber, event_type: str=...) -> bool: ...
    @overload
    def is_subscribed(self, subscriber: WildcardSubscriber, event_type: WildcardType=...) -> bool: '''Whether the callback is subscribed for the event type, or subscribed for any event type if event_type is not passed.'''
    @property
    def total_subscribers(self) -> int: '''The total number of subscribers for any event type.'''
    @property
    def name(self) -> str: '''The name of the event bus.'''
    @property
    def wildcards(self) -> WeakSet[WildcardSubscriber]: '''All the wildcard subscribers for this event bus.'''
    @property
    def wildcard_count(self) -> int: '''The number of wildcard subscribers under this event bus.'''
    @property
    def active_tasks(self) -> int: '''The number of callbacks occurring at this moment.'''
    @property
    def stream_queue(self) -> Queue[tuple[str, Any]]|Queue[Any]:
        '''| The asynchronous queue to which events are output by :meth:`event_stream`.
        | The items in the queue are tuples ``(event_type, data)`` if the event type was not specified in the creation of the event stream,
        | otherwise just the data attached to each event of that type.'''
    @stream_queue.setter
    def stream_queue(self, val: Queue[tuple[str, Any]|Any], /) -> None: ...
    def is_auditing(self) -> bool: '''Whether the event bus is connected to :func:`sys.audit`.'''
    @property
    def auditing(self) -> bool: '''Get-set property for :meth:`is_auditing`. When changed, connect or disconnect the underlying audit hook accordingly.'''
    @auditing.setter
    def auditing(self, val: bool, /) -> None: ...
    def auditor(self, event: str, args: tuple[object, ...], /) -> None:
        '''| The auditor of the event bus. You probably don't want to call this directly.
        | Not an instance method at runtime, just a function as an attribute of the instance.'''
    def start_audit(self) -> None: '''Connect the audit hook of the bus to :func:`sys.audit`, creating if necessary. Incurs overhead. Use with caution.'''
    def stop_audit(self) -> None: '''Disconnect the audit hook of the bus. Note that it is currently impossible to actually remove an audit hook, so this function just deactivates it.'''
    def add_middleware(self, middleware: Middleware) -> int:
        '''| Append a middleware to the back of the pipe of middlewares, and return a permanent cookie that can be passed to :meth:`remove_middleware` to invalidate it. O(1) time.
        | The middleware must take the event type as the first argument and the associated data as the second.
        | If the middleware does not recognize the event type, it should simply return the data immediately.
        | There is no protection in place against malicious middlewares but the user's abstraction.
        | It is preferred that the middleware be a coroutine function.
        | Each middleware should be extremely optimized, such as through C extensions, to avoid hindrance of the publishing.
        | When publishing occurs, the first middleware takes the initial data, does some processing asynchronously, and passes the modified data to the second middleware, and so forth. Insertion order is maintained. This may be different from the typical meaning of a 'middleware'.
        | The output of the final middleware is broadcast to each subscriber concurrently. Subscribers cannot see the initial data.'''
    @overload
    def remove_middleware[T](self, cookie: int, *, result: T, strict: bool=...) -> T: ...
    @overload
    def remove_middleware(self, cookie: int, *, result: object=..., strict: bool=...) -> Any: # noqa: ANN401
        '''| Remove a previously added middleware, via :meth:`add_middleware` or :meth:`add_temp_middleware`, and return its result. O(1) time.
        | If ``strict`` is ``True`` and the middleware was never added, throw :exc:`ValueError`.
        | If the middleware has an associated future :meth:`add_temp_middleware` and it is done, return its result. If an exception was set, reraise it.
        | Otherwise, set its result to ``result`` and return it.'''
    def add_temp_middleware(self, middleware: Middleware, until: Future[Any]) -> None: '''Add a middleware that should take effect until the future ``until`` is done, after which the result of the future will be treated as the result of the middleware on removal. No cookie is returned in this case.'''
    def audit_context(self) -> DualContextManager[None]: '''Start receiving publications from and sending publications to :func:`sys.audit` upon entry and stop on exit. Use as a context manager.'''
    def tracking_context(self, stats_receiver: Future[Mapping[str, int]]|None=...) -> DualContextManager[None]: '''Context manager, under which stats are tracked and finally sent to the stats_receiver future.'''
    def start_tracking(self) -> None: '''Start tracking event publication statistics (number of publications under each event type).'''
    @overload
    def stop_tracking(self, ret_stats: Literal[False]=...) -> None: ...
    @overload
    def stop_tracking(self, ret_stats: Literal[True]) -> defaultdict[str, int]: '''Stop tracking event publication statistics. If ``ret_stats`` is ``True``, return a dictionary of the stats up to that point, with keys corresponding to event types and values the number of publications.'''
    @overload
    def subscribe[T: SpecificSubscriber](self, subscriber: T, /, event_type: str) -> T: ...
    @overload
    def subscribe[T: WildcardSubscriber](self, subscriber: T, /, event_type: WildcardType=...) -> T: '''Add a subscriber to the event bus under the specified event type (if unspecified, add as wildcard). Return the subscriber to allow usage as a decorator.'''
    @overload
    def unsubscribe(self, subscriber: SpecificSubscriber, /, event_type: str) -> bool: ...
    @overload
    def unsubscribe(self, subscriber: WildcardSubscriber, /, event_type: WildcardType=...) -> bool: '''Remove a subscriber from the event bus under the event type (if unspecified, remove from wildcards) and return whether the removal occurred (i.e. the subscriber was initially present).'''
    @overload
    def subscribe_to[T: SpecificSubscriber](self, event_type: str) -> Callable[[T], T]: ...
    @overload
    def subscribe_to[T: WildcardSubscriber](self, event_type: WildcardType) -> Callable[[T], T]: '''A decorator factory for functions to subscribe to this event bus under the specified event type.'''
    def sync_start_publish(self, event_type: str, data: object=..., *, safe: bool=..., timeout: float|None=..., chaperone: Callable[[ExceptionGroup|Exception], object]|None=...) -> None: '''Begin a publication synchronously. Parameters are as in :meth:`publish`, below.'''
    async def publish(self, event_type: str, data: object=..., *, wait: bool=..., safe: bool=..., timeout: float|None=..., chaperone: Callable[[ExceptionGroup|Exception], object]|None=...) -> None:
        '''| Publish an event, that is, some data attached to an event type, to the subscribers involved, with timeout ``timeout``.
        | Each subscriber for that event type and wildcard subscribers will be triggered by the publication, receiving the data after processing by the middlewares in order.
        | If ``wait`` is ``False`` (default ``True``), don't wait for the publication to complete.
        | If ``safe`` is ``False`` (default ``True``), don't wrap callbacks with proper error handling.
        | ``chaperone``, if passed, should be a function processing non-severe exceptions (instances of :exc:`Exception` and :exc:`ExceptionGroup`) in the callbacks. Otherwise, these
        | exception( group)s are flattened and collected into an :exc:`ExceptionGroup` and propagated; the caller should be prepared to handle that case.'''
    async def wait_for_event(self, event_type: str, *, timeout: bool|None=..., condition: Callable[[Any], object]=...) -> Task[Any]:
        '''Wait for an event of the specified event type that satisfies the condition to occur.

        .. note:: The function completes once the subscription has registered and returns a task, which will be cancelled on timeout.'''
    @overload
    async def subscribe_until[T](self, fut: Future[T], subscriber: SpecificSubscriber, event_type: str, *, till_permanent: float|None=...) -> Task[T]: ...
    @overload
    async def subscribe_until[T](self, fut: Future[T], subscriber: WildcardSubscriber, event_type: WildcardType=..., *, till_permanent: float|None=...) -> Task[T]:
        '''| Add the subscriber under the event type (as a wildcard if ``event_type`` is :const:`WILDCARD` or not passed) and return a task.
        | The subscriber is removed once ``fut`` completes, and its result returned through the returned task.
        | After ``till_permanent`` seconds elapse (if passed), the task errors and the subscriber is left under that event type.'''
    @overload
    async def feed_event(self, data: object, /, *, timeout: float|None=...) -> None: ...
    @overload
    async def feed_event(self, event_type: str, data: object, /, *, timeout: float|None=...) -> None: '''Feed the data for an event into the event stream, the queue for which is created if necessary, such that the event stream needs not be active.'''
    @overload
    def event_stream(self, event_type: str, *, timeout: float|None=..., item_timeout: float|None=..., bufsize: int=...) -> AsyncGenerator[Any]: ...
    @overload
    def event_stream(self, *, timeout: float|None=..., item_timeout: float|None=..., bufsize: int=...) -> AsyncGenerator[tuple[str, Any]]:
        '''| Open an event stream for the specified event type, that is, an async generator from which consumers can receive events and the corresponding data as they occur.
        | If ``event_type`` is not passed, the stream will include the event type in the output.
        | ``timeout``, ``item_timeout`` and ``bufsize`` default to :const:`~asyncutils.context.Context.EVENT_BUS_STREAM_DEFAULT_TIMEOUT`, :const:`~asyncutils.context.Context.EVENT_BUS_STREAM_DEFAULT_ITEM_TIMEOUT` and :const:`~asyncutils.context.Context.EVENT_BUS_STREAM_DEFAULT_BUFFER_SIZE` respectively.'''
    async def shutdown(self, immediate: bool=..., *, timeout: float|None=..., preserve_stats: bool=...) -> None:
        '''| Gracefully shut down the event bus.
        | After the shutdown, publications fail fast and middlewares are cleared.
        | This waits for as many subscriber callbacks to complete as possible, within ``timeout`` seconds if specified.
        | If ``immediate`` is ``True``, getters for the queue for the event stream will error immediately.
        | If ``preserve_stats`` is ``True``, the event publication statistics will be saved and accessible with :meth:`get_event_stats`.'''
    async def handle_exception(self, e: BaseException) -> None: '''Asynchronously handle an exception according to the ``handler`` initialization parameter, which can be a sync or async function.'''
    @overload
    def clear(self, event_type: str) -> WeakSet[SpecificSubscriber]|None: ...
    @overload
    def clear(self, event_type: WildcardType) -> WeakSet[WildcardSubscriber]|None: ...
    @overload
    def clear(self) -> None: '''Remove all subscribers for the event type and return them. If not passed, clear all subscribers but persist statistics unlike :meth:`clear_all`.'''
    def clear_all(self) -> None: '''Remove all subscribers and clear statistics.'''
    def subscriber_count(self, event_type: str|WildcardType) -> int: '''The number of subscribers for that event type.'''
    def clear_wildcards(self) -> WeakSet[WildcardSubscriber]|None: '''Equivalent to ``bus.clear(EventBus.WILDCARD)``.'''
    def clear_stats(self) -> None: '''Clear the event publication statistics.'''
    async def __setup__(self) -> None: ...
    async def __cleanup__(self) -> None: ...
class Rendezvous[T]:
    '''A rendezvous object, emulating Golang's unbuffered channels.'''
    def __init__(self, *, loop: AbstractEventLoop=..., lock: Lock=...):
        '''| Instantiate a rendezvous object, which will be maintained by a background task cleaning up its done getters and putters periodically,
        | according to :const:`~asyncutils.context.Context.RENDEZVOUS_MAINTENANCE_INTERVAL`. If ``loop`` is not passed, the running event loop is used. If there is no
        | running event loop, one is created and set.'''
    async def raising_put(self, value: T, /, *, timeout: float) -> None:
        '''| Put in ``value`` to the rendezvous, blocking until it is gotten or timeout is reached, at which point :exc:`TimeoutError` is raised and the put cancelled.
        | Also be prepared to intercept or reraise :exc:`~asyncio.CancelledError` resulting from reset.'''
    async def put(self, value: T, /, *, timeout: float|None=...) -> bool: '''Like :meth:`raising_put`, but returns a boolean representing if the put succeeded. The recommended interface.'''
    async def get(self, default: T|None=..., *, timeout: float|None=...) -> T:
        '''| Get a value from the rendezvous, blocking until available unless default is passed and timeout is not, in which case the default is returned if a value is not immediately available.
        | If ``default`` is not passed and ``timeout`` is reached, the :exc:`TimeoutError` is propagated. In any case, the get is cancelled at timeout.'''
    def cleanup(self) -> None: '''Clean up the internal getter and putter stacks.'''
    async def reset(self) -> None:
        '''| Hard reset the rendezvous. Call from a monitoring task when a deadlock appears to have occurred.
        | This cancels all pending gets, puts and exchanges; their callers will see :exc:`~asyncio.CancelledError`.'''
    def __length_hint__(self) -> int: '''Approximate number of operations pending. Implemented for :func:`operator.length_hint`.'''
    def state_snapshot(self) -> StateSnapshot: '''Trigger a cleanup and return a snapshot of the current state of the object.'''
    async def exchange(self, put_val: T, /, *, timeout: float|None=..., asap: bool=...) -> T:
        '''| Put in a value to the rendezvous and get and return a different value gotten from it.
        | If ``asap`` is ``True``, return once a value is available, without necessarily having completed the put.'''
