from .mixins import LoopContextMixin
from .base import event_loop, iter_to_aiter, safe_cancel_batch, dummy_task, yield_to_event_loop
from .util import safe_cancel, sync_await, to_async, to_sync, semaphore, _ignore_cancellation
from .exceptions import IgnoreErrors, BusShutDown, BusStatsError, BusPublishingError, BusTimeout, Critical, potent_derive, CRITICAL
from .config import Executor, _NO_DEFAULT
from ._internal.helpers import _filter_out, _get_loop_no_exit, copy_and_clear, stop_and_closer, subscriptable
from ._internal.patch import patch_method_signatures, patch_classmethod_signatures
from . import constants
from _weakrefset import WeakSet
from collections import defaultdict, deque, namedtuple
from sys import addaudithook
from contextlib import contextmanager
from functools import partial, cached_property
from asyncio.locks import Lock, Event
from asyncio.queues import Queue, QueueEmpty, QueueShutDown
from asyncio.coroutines import iscoroutine
from asyncio.tasks import wait_for, gather, sleep, shield
from asyncio.timeouts import timeout as _timeout
from ._internal.submodules import channels_all as __all__
from ._internal import log
@subscriptable
class Observable(LoopContextMixin):
    __slots__ = '_data', '_lock', '_to_remove', '_queue', '_event'
    @property
    def idle(self): return self._event.is_set()
    @property
    def notifying(self): return not self.idle
    async def notify(self, *a, _ret_exc_=True, **k):
        if not self: return
        async with self._lock:
            if self.notifying: return None if (q := self._queue) is None else await q.put((_ret_exc_, a, k))
            self._event.clear()
        try: await self._notify_helper(_ret_exc_, a, k); await self.handle_notifications()
        finally: self._event.set(); await self.handle_unsubscriptions()
    async def notify_sequential(self, *a, _silent_=False, _persistent_=False, **k):
        for observer in self._data.copy():
            try: yield await observer(*a, **k)
            except Exception as e:
                if _silent_:
                    if _persistent_: continue
                    break
                elif _persistent_: log.error(f'{type(e).__qualname__} in observer', exc_info=True)
                else: raise
    async def wait_for_next(self, timeout=None, strict=False):
        async def one_time(*a, **k): F.set_result((a, k))
        F, u = self.make_fut(), self.subscribe_nowait(one_time)
        try: return await wait_for(F, timeout)
        finally: u(strict)
    async def wait_until_idle(self, timeout=None): await wait_for(self._event.wait(), timeout)
    async def subscribe(self, observer): await self.wait_until_idle(); return self.subscribe_nowait(observer)
    async def unsubscribe(self, observer, strict=False): await self.wait_until_idle(); self.unsubscribe_nowait(observer, strict)
    async def handle_notifications(self):
        while (q := self._queue) is not None:
            try: await self._notify_helper(*q.get_nowait())
            except QueueEmpty: break
    async def handle_unsubscriptions(self):
        async with self._lock: self._data -= (s := self._to_remove); s.clear()
    async def _notify_helper(self, r, a, k): await gather(*self.make_multiple(obs(*a, **k) for obs in self._data.copy()), return_exceptions=r)
    def __init__(self, init_observers=(), maxsize=0): self._data, self._lock, self._to_remove, self._queue, self._event = set(init_observers), Lock(), set(), None if maxsize is None else Queue(maxsize), Event()
    def __iter__(self): return self._data.__iter__()
    def __aiter__(self): return iter_to_aiter(self)
    async def __setup__(self): LoopContextMixin.__init__(self)
    async def __cleanup__(self): await gather(self.handle_notifications(), self.handle_unsubscriptions()); (l := self.loop).call_soon(stop_and_closer(l))
    def start_accumulation(self): return self.restart_accumulation() or True if self._queue is None else False
    def restart_accumulation(self, flush=False):
        if flush: self.flush_notifications()
        self._queue = Queue()
    def flush_notifications(self, timeout=None): sync_await(self.handle_notifications(), timeout=timeout, loop=self.loop)
    def flush_unsubscriptions(self, timeout=None): sync_await(self.handle_unsubscriptions(), timeout=timeout, loop=self.loop)
    def subscribe_nowait(self, observer): self._data.add(observer); return partial(self.unsubscribe_nowait, observer)
    def unsubscribe_eventually(self, observer, asap=True):
        if asap and self._event.is_set(): self.unsubscribe_nowait(observer)
        else: self._to_remove.add(observer)
    def unsubscribe_nowait(self, observer, strict=False): (self._data.remove if strict else self._data.discard)(observer)
    def subscribe_syncf(self, observer): self._data.add(_ := to_async(observer, self.loop)[0]); return partial(self.unsubscribe_nowait, _)
    def ntimes(self, observer, n=1):
        if n <= 0: raise ValueError('n must be positive')
        async def wrapper(*a, **k):
            nonlocal n; await observer(*a, **k); n -= 1
            if not n: await self.unsubscribe(wrapper)
        self.subscribe_nowait(wrapper); return partial(self.unsubscribe_nowait, wrapper)
    def filter(self, pred, ret_exc=True):
        f = partial((_ := type(self)()).notify, _ret_exc_=ret_exc)
        async def filtered(*a, **k):
            if pred(*a, **k): await f(*a, **k)
        self.subscribe_nowait(filtered); return _
    def map(self, transform, ret_exc=True):
        f = partial((_ := Observable()).notify, _ret_exc_=ret_exc)
        async def mapped(*a, **k):
            A, K = transform(*a, **k)
            await f(*A, **K)
        self.subscribe_nowait(mapped); return _
    def debounce(self, delay, ret_exc=True):
        f = partial((_ := type(self)()).notify, _ret_exc_=ret_exc); t = None
        async def debounced(*a, **k):
            nonlocal t
            if not (t is None or not t.done()): t.cancel()
            async def _notifier():
                with _ignore_cancellation: await sleep(delay); await f(*a, **k)
            t = self.make(_notifier())
        self.subscribe_nowait(debounced); return _
    def throttle(self, interval, ret_exc=True):
        f, t = partial((_ := type(self)()).notify, _ret_exc_=ret_exc), 0
        async def throttled(*a, **k):
            nonlocal t
            with event_loop.from_flags(0) as l:
                if (c := l.time())-t >= interval: t = c; await f(*a, **k)
        self.subscribe_nowait(throttled); return _
    def buffer(self, count, ret_exc=True):
        f, b, c = (_ := type(self)()).notify, [], max(1, count)
        async def buffered(*a, **k):
            b.append((a, k))
            if len(b) >= c: await gather(*(f(*A, **K) for A, K in copy_and_clear(b)), return_exceptions=ret_exc)
        self.subscribe_nowait(buffered); return _
    def at_change(self, key=None, ret_exc=True):
        f, l = partial((_ := type(self)()).notify, _ret_exc_=ret_exc), object()
        if key is None: key = lambda *a, **k: (a, k)
        async def distinct(*a, **k):
            nonlocal l
            if (c := key(*a, **k)) != l: l = c; await f(*a, **k)
        self.subscribe_nowait(distinct); return _
    def fork(self, ret_exc=True): self.subscribe_nowait(partial((_ := type(self)()).notify, _ret_exc_=ret_exc)); return _
    def merge(*obs, ret_exc=True):
        p = partial((_ := type(obs[0])()).notify, _ret_exc_=ret_exc)
        for o in obs: o._data.add(p)
        return _
class EventBus(LoopContextMixin):
    def __init__(self, name=None, *, handler=None, max_concurrent=128, bounded=False, tracking_stats=False, __fmt='{} {}'.format): self._subscribers = s = defaultdict(WeakSet); self.name, self._lock, self._auditing, self._handler, self._sem, self._is_shutdown, self._tracking, self._publisher, s[None] = __fmt((t := type(self)).__qualname__, name or t._inc_cnt()), Lock(), False, handler or (lambda _: None), semaphore(bounded, max_concurrent), False, tracking_stats, None, WeakSet()
    def raise_for_shutdown(self):
        if self._is_shutdown: raise BusShutDown(f'{self.name} is shutting down')
    def get_event_stats(self):
        if self._tracking: return self._published.copy()
        raise BusStatsError(f'{self.name} is not tracking event stats')
    def subscribers_for(self, event_type): return self._subscribers[event_type].copy()
    def event_names(self): (s := set(self._subscribers.keys())).discard(None); return s
    def has_subscribers(self, event_type): return bool(self._subscribers[event_type])
    @staticmethod
    def is_valid_event_type(event_type): return event_type is None or isinstance(event_type, str)
    def is_subscribed(self, callback, event_type=_NO_DEFAULT): return any(callback in i for i in self._subscribers.values()) if event_type is _NO_DEFAULT else callback in self._subscribers.get(event_type, ())
    @property
    def total_subscribers(self): return sum(map(len, self._subscribers.values()))
    @property
    def wildcards(self): return self.subscribers_for(None).copy()
    @property
    def wildcard_count(self): return len(self.wildcards)
    @property
    def active_tasks(self): return self._sem._value
    @property
    def stream_queue(self):
        if (r := getattr(self, '_stream_queue', None)) is None: self._stream_queue = r = Queue()
        return r
    @stream_queue.setter
    def stream_queue(self, val, /): self._stream_queue = val
    @property
    def dummy_task(self): return self.make(dummy_task)
    def is_auditing(self): return self._auditing
    auditing = property(is_auditing, lambda self, val, /: (self.start_audit if val else self.stop_audit)())
    @cached_property
    def auditor(self):
        def F(e, a, p=to_sync(self.publish, loop=self.loop), f=self.is_auditing, /):
            if f(): p(e, a, wait=False)
        F.added = False; return F
    @cached_property
    def _published(self): return defaultdict(int)
    def start_audit(self):
        if not (self._auditing or (a := self.auditor).added): addaudithook(a); self._auditing = a.added = True
    def stop_audit(self): self._auditing = False
    @cached_property
    def _middlewares(self): return {}
    def add_middleware(self, middleware): self._middlewares[middleware] = None
    def remove_middleware(self, middleware, *, result=None, strict=False):
        if (F := self._middlewares.pop(middleware, *(() if strict else (None,)))) is not None:
            if F.done(): return F.result()
            F.set_result(result)
        return result
    def add_middleware_once(self, middleware, until): self._middlewares[middleware] = until
    @contextmanager
    def audit_context(self):
        try:
            if o := not self._auditing: self.start_audit()
            yield
        finally:
            if o: self.stop_audit()
    @contextmanager
    def tracking_context(self, stats_receiver=None):
        try:
            if o := not self._tracking: self.start_tracking()
            yield
        finally:
            if o:
                if stats_receiver is None: self.stop_tracking()
                else: stats_receiver.set_result(self.stop_tracking(True))
    def start_tracking(self): self._tracking = True
    def stop_tracking(self, ret_stats=False):
        self._tracking = False
        if ret_stats: return copy_and_clear(self._published)
        else: self._published.clear()
    async def subscribe(self, callback, /, event_type=None):
        self.raise_for_shutdown()
        async with self._lock: self._subscribers[event_type].add(callback)
        return callback
    async def unsubscribe(self, callback, /, event_type=None):
        async with self._lock:
            try: self._subscribers[event_type].remove(callback); return True
            except KeyError: return False
    def subscribe_to(self, event_type): return to_sync(partial(self.subscribe, event_type=event_type))
    def subscriber_count(self, event_type): return len(self._subscribers[event_type])
    async def _publish_helper(self, d, s, I, *_):
        await gather(*((self._safe_callback(i, d, *_) for i in I) if s else (i(d, *_) for i in I)))
    async def publish(self, event_type, data=None, *, wait=True, safe=False, timeout=None, chaperone=None):
        self.raise_for_shutdown(); f = []
        if chaperone is None: chaperone = f.append
        async def g():
            nonlocal data
            for m, F in self._middlewares.items():
                try:
                    if F is not None and F.done(): continue
                    if iscoroutine(data := m(event_type, data)): data = await data
                except CRITICAL: raise Critical
                except (ExceptionGroup, Exception) as e: chaperone(e)
                except BaseExceptionGroup as e: raise potent_derive(e, BusPublishingError(self, m), ordered=False)
                except BaseException as e: raise BusPublishingError(self, m) from e
            async with self._lock:
                if self._tracking: self._published[event_type] += 1
                s, w = map(lambda _: self._subscribers[_].copy(), (event_type, None))
            await gather((f := partial(type(self)._publish_helper, self, data, safe))(s), f(w, event_type))
        self._publisher = self.make(p := wait_for(g(), timeout))
        try:
            if wait: await p
            if f: raise ExceptionGroup(f'errors occurred in publishing middlewares of {self.name}', f) from None
            log.info(f'{self.name}: publishing succeeded')
        except TimeoutError: raise BusTimeout(f'publishing in {self.name} took too long') from None
        finally:
            if p := self._publisher: self._publisher = None; await safe_cancel(p)
    async def wait_for_event(self, event_type, *, timeout=None, condition=lambda _: True):
        def handler(d):
            if not F.done() and condition(d): F.set_result(d)
        return await self.make(self.subscribe_until(F := self.loop.create_future(), lambda _: self._runner(handler, _), event_type, timeout))
    async def subscribe_until(self, fut, callback, event_type=None, till_permanent=None, _h=_ignore_cancellation.combined(IgnoreErrors(TimeoutError))):
        async def f(h=_h):
            with h: r = await wait_for(fut, till_permanent); await self.unsubscribe(callback, *_filter_out(event_type)); return r
        await self.subscribe(callback, *_filter_out(event_type)); return self.make(f())
    async def feed_event(self, *d, timeout=None):
        if (q := self.stream_queue).full(): log.warning('event stream buffer full')
        try: await wait_for(q.put(d[0] if len(d) == 1 else d), timeout)
        except QueueShutDown: log.info('event stream is closing')
        except TimeoutError:
            if q.full(): log.warning('event stream data lost'); q.get_nowait(); q.put_nowait(d)
    async def event_stream(self, event_type=None, *, timeout=_NO_DEFAULT, item_timeout=_NO_DEFAULT, bufsize=None):
        self.raise_for_shutdown(); t = await self.subscribe_until(F := self.loop.create_future(), partial(self.feed_event, timeout=constants.EVENT_BUS_STREAM_DEFAULT_TIMEOUT if timeout is _NO_DEFAULT else timeout), event_type); self.stream_queue = q = Queue(constants.EVENT_BUS_STREAM_DEFAULT_BUFFER_SIZE if bufsize is None else bufsize)
        if item_timeout is _NO_DEFAULT: item_timeout = constants.EVENT_BUS_STREAM_DEFAULT_ITEM_TIMEOUT
        try:
            while True: yield await wait_for(q.get(), item_timeout)
        except QueueShutDown: log.info(f'event stream of {self.name} has been shut down', exc_info=True)
        except TimeoutError: log.error(f'event stream of {self.name} is stopping because of timeout in waiting for item', exc_info=True)
        finally: F.set_result(None); await t
    async def shutdown(self, immediate=False, timeout=None, preserve_stats=False):
        if self._is_shutdown: return
        self._is_shutdown, f = True, self._sem.acquire; self.stop_audit(); self._middlewares.clear()
        if not preserve_stats: self.clear_stats()
        try:
            async with _timeout(timeout):
                self.stream_queue.shutdown(immediate)
                for _ in range(self.active_tasks): await f()
        except TimeoutError: log.error(f'{self.name} shutdown timed out, some tasks may be incomplete', exc_info=True)
        finally:
            if p := self._publisher: await safe_cancel(p)
            del self._lock, self._handler, self._sem, self._publisher
    @cached_property
    def _runner(self): return partial(self.loop.run_in_executor, Executor())
    async def handle_exception(self, e): await self._runner(self._handler, e)
    def clear(self, event_type=_NO_DEFAULT): return self.clear_all() if event_type is _NO_DEFAULT else self._subscribers.pop(event_type, None)
    def clear_all(self): self._subscribers.clear(); self.clear_stats()
    def clear_wildcards(self): return self.clear(None)
    def clear_stats(self): self._published.clear()
    async def _safe_callback(self, callback, data, event_type=None, timeout=None):
        try:
            async with self._sem:
                if iscoroutine(r := callback(*_filter_out(event_type, s=_NO_DEFAULT), data)): await wait_for(r, timeout)
        except TimeoutError: log.warning(f'callback {callback.__qualname__} timed out')
        except CRITICAL: self.exiter(); raise Critical
        except BaseException as e: await self.handle_exception(e)
    async def __setup__(self): super().__init__()
    patch_classmethod_signatures((_ := lambda _, /, f='#%d', c=__import__('itertools').count(1).__next__: f%c(), '')); patch_method_signatures((__init__, 'name=None, *, handler=None, max_concurrent=128, bounded=False, tracking_stats=False')); WILDCARD, __cleanup__, _inc_cnt = None, shutdown, classmethod(_); del _
@subscriptable
class Rendezvous:
    __slots__ = '_getters', '_putters', '_loop', '_lock', '_task'
    def __init__(self, *, loop=None, lock=None):
        if loop is None: loop = _get_loop_no_exit()
        if lock is None: lock = Lock()
        self._getters, self._putters, self._loop, self._lock = deque(), deque(), loop, lock; self._make_task()
    async def _maintainer(self, f=sleep.__get__(60)):
        while True: await f(); await self.cleanup()
    async def put(self, v, /, *, timeout=None):
        try: await self.raising_put(v, timeout=timeout); return True
        except TimeoutError: return False
    async def raising_put(self, v, /, *, timeout): await wait_for(await shield(self._put_helper(v)), timeout)
    async def get(self, default=_NO_DEFAULT, *, timeout=None):
        p, f = self._putters, timeout is None and default is not _NO_DEFAULT
        try:
            async with _timeout(timeout):
                async with self._lock:
                    while p:
                        v, F = p.popleft()
                        if not F.done(): F.set_result(None); return v
                    if f: return default
                    else: self._getters.append(F := self._loop.create_future())
                return await F
        except TimeoutError:
            if default is _NO_DEFAULT: raise
            return default
    def __length_hint__(self): return len(self._getters)+len(self._putters)
    async def state_snapshot(self, _f=namedtuple('StateSnapshot', 'num_getters num_putters num_ops idle', module='asyncutils.channels')):
        await self.cleanup()
        async with self._lock: t = len(self._getters), len(self._putters)
        return _f(*t, sum(t), not any(t))
    async def cleanup(self):
        async with self._lock: self._getters, self._putters = deque(F for F in self._getters if not F.done()), deque(t for t in self._putters if not t[1].done())
    async def exchange(self, v, /, *, timeout=None, asap=False):
        g, f = self._getters, True
        async with _timeout(timeout):
            async with self._lock:
                while g:
                    if not (F := g.popleft()).done(): break
                else: g.append(F := self._loop.create_future()); f = False
            if f: F.set_result(v); return await self.get()
            else: await (self._put_helper if asap else self.put)(v); g.appendleft(F); return await F
    async def _put_helper(self, v, /):
        g = self._getters
        async with self._lock:
            while g:
                if not (F := g.popleft()).done(): F.set_result(v); break
            else: self._putters.append((v, F := self._loop.create_future()))
        return F
    async def reset(self, _=partial(safe_cancel_batch, disembowel=True)):
        async with self._lock: await gather(*map(_, (self._getters, self._putters)))
        self._task.cancel(); self._make_task()
    def _make_task(self): self._task = self._loop.create_task(self._maintainer())
    patch_method_signatures((reset, ''), (state_snapshot, ''), (_maintainer, ''))