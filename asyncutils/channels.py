from asyncutils.constants import _NO_DEFAULT
from asyncutils._internal import py312 as C, helpers as H, log as L, patch as P
from asyncutils._internal.submodules import channels_all as __all__
from _functools import partial
from _weakrefset import WeakSet
import asyncio as I, asyncutils as A
from collections import defaultdict, deque, namedtuple
from itertools import count, repeat, starmap
from sys import addaudithook, audit
from time import monotonic
@H.subscriptable
class Observable(H.LoopMixinBase):
    __slots__ = '__d', '__e', '__l', '__q', '__r'
    @property
    def idle(self): return self.__e.is_set()
    @property
    def notifying(self): return not self.idle
    async def notify(self, *a, _ret_exc_=False, **k):
        if not self.__d: return
        async with self.__l:
            if self.notifying:
                if (q := self.__q) is not None: await q.put((_ret_exc_, a, k)); return
                await self.wait_until_idle()
            self.__e.clear()
        try: await self._notify_helper(_ret_exc_, a, k); await self.handle_notifications()
        finally: self.__e.set(); await self.handle_unsubscriptions()
    async def notify_sequential(self, *a, _silent_=False, _persistent_=False, **k):
        for o in self.__d.copy():
            try: yield await o(*a, **k)
            except A.CRITICAL: raise
            except: # ruff: ignore[bare-except]
                if _silent_:
                    if _persistent_: continue
                    break
                if not _persistent_: raise
                L.exception('asyncutils.channels.Observable: error in observer')
    async def wait_for_next(self, timeout=None, strict=False):
        async def f(*a, **k): F.set_result((a, k)) # ruff: ignore[unused-async]
        F, u = self.make_fut(), self.subscribe_nowait(f)
        try: return await I.wait_for(F, timeout)
        finally: u(strict)
    async def wait_until_idle(self, timeout=None): await I.wait_for(self.__e.wait(), timeout)
    async def subscribe(self, observer): await self.wait_until_idle(); return self.subscribe_nowait(observer)
    async def unsubscribe(self, observer, strict=False): await self.wait_until_idle(); self.unsubscribe_nowait(observer, strict)
    async def handle_notifications(self):
        if self.__q is None: return
        while True:
            try: await self._notify_helper(*self.__q.get_nowait())
            except (I.QueueEmpty, C.QueueShutDown): break
    async def handle_unsubscriptions(self):
        async with self.__l: self.__d -= (s := self.__r); s.clear()
    async def _notify_helper(self, r, a, k): await I.gather(*(self.make(obs(*a, **k)) for obs in self.__d.copy()), return_exceptions=r)
    def __init__(self, init_observers=(), maxsize=0): audit('asyncutils.channels.Observable', maxsize); self.__d, self.__l, self.__r, self.__q, self.__e = set(init_observers), I.Lock(), set(), None if maxsize is None else C.Queue(maxsize), I.Event()
    def __iter__(self): yield from self.__d
    async def __aenter__(self): self.__e.set(); return self
    async def __aexit__(self, /, *_): await I.gather(self.handle_notifications(), self.handle_unsubscriptions())
    def start_accumulation(self): return self.restart_accumulation() or True if self.__q is None else False
    async def restart_accumulation(self, flush=True):
        if flush: await self.handle_notifications()
        self.__q = C.Queue()
    def subscribe_nowait(self, observer): self.__d.add(observer); return partial(self.unsubscribe_nowait, observer)
    def unsubscribe_eventually(self, observer, asap=True):
        if asap and self.__e.is_set(): self.unsubscribe_nowait(observer)
        else: self.__r.add(observer)
    def unsubscribe_nowait(self, observer, strict=False): getattr(self.__d, 'remove' if strict else 'discard')(observer)
    def subscribe_sync_observer(self, observer): return self.subscribe_nowait(A.to_async(observer))
    def ntimes(self, observer, n=None):
        if n is None: n = A.getcontext().OBSERVABLE_DEFAULT_NTIMES_N
        if n <= 0: raise ValueError('asyncutils.channels.Observable.ntimes: n must be positive')
        async def wrapper(*a, **k):
            nonlocal n; await observer(*a, **k); n -= 1 # ty: ignore[unsupported-operator]
            if n == 0: await self.unsubscribe(wrapper)
        self.subscribe_nowait(wrapper); return partial(self.unsubscribe_nowait, wrapper)
    def filter(self, pred, ret_exc=False):
        f = partial((_ := type(self)())._notify_helper, ret_exc)
        async def filtered(*a, **k):
            if pred(*a, **k): await f(a, k)
        self.subscribe_nowait(filtered); return _
    def map(self, transform, ret_exc=False):
        f = partial((_ := Observable())._notify_helper, ret_exc)
        async def mapped(*a, **k): await f(*transform(*a, **k))
        self.subscribe_nowait(mapped); return _
    def debounce(self, delay, ret_exc=False):
        f = partial((_ := type(self)())._notify_helper, ret_exc); t = None
        async def debounced(*a, **k):
            nonlocal t
            if t is not None: await A.safe_cancel(t)
            async def notifier():
                with A.ignore_cancellation: await I.sleep(delay); await f(a, k)
            t = self.make(notifier())
        self.subscribe_nowait(debounced); return _
    def throttle(self, interval, ret_exc=False):
        f, t = partial((_ := type(self)())._notify_helper, ret_exc), 0
        async def throttled(*a, **k):
            nonlocal t
            if (c := monotonic())-t >= interval: t = c; await f(a, k)
        self.subscribe_nowait(throttled); return _
    def buffer(self, count, ret_exc=False):
        f, b, c = (_ := type(self)())._notify_helper, [], max(1, count)
        async def buffered(*a, **k):
            b.append((a, k))
            if len(b) >= c: await I.gather(*starmap(f, H.copy_and_clear(b)), return_exceptions=ret_exc)
        self.subscribe_nowait(buffered); return _
    def at_change(self, key=lambda *a, **k: (a, frozenset(k.items())), ret_exc=False):
        f, l = partial((_ := type(self)())._notify_helper, ret_exc), object()
        async def distinct(*a, **k):
            nonlocal l
            if (c := key(*a, **k)) != l: l = c; await f(a, k)
        self.subscribe_nowait(distinct); return _
    def fork(self, ret_exc=False): self.subscribe_nowait(partial((_ := type(self)()).notify, _ret_exc_=ret_exc)); return _
    def merge(*O, ret_exc=False):
        p = partial((_ := type(O[0])()).notify, _ret_exc_=ret_exc)
        for o in O: o.__d.add(p)
        return _
class EventBus(H.LoopMixinBase): # ruff: ignore[too-many-public-methods]
    __slots__ = '_auditing', '_handler', '_is_shutdown', '_lock', '_middlewares', '_published', '_publishers', '_sem', '_subscribers', '_tracking', 'auditor', 'name'
    def __init__(self, name=None, *, handler=None, max_concurrent=None, tracking_stats=False, evs_bufsize=None):
        if max_concurrent is None: max_concurrent = A.getcontext().EVENT_BUS_DEFAULT_MAX_CONCURRENT
        def auditor(*a, f=self.is_auditing, _=self.sync_start_publish):
            if f(): _(*a)
        audit('asyncutils.channels.EventBus', name, id(self)); self.auditor, self._subscribers, self._published, self._middlewares, self._publishers, self.name, self._lock, self._auditing, self._handler, self._sem, self._is_shutdown, self._tracking, self.stream_queue, s[None] = auditor, (s := defaultdict(WeakSet)), defaultdict(int), [], set(), f'{H.fullname(self)} {name or f'#{__class__.__inc_cnt()}'}', I.Lock(), False, handler or (lambda _: None), I.Semaphore(max_concurrent), False, tracking_stats, C.Queue(A.getcontext().EVENT_BUS_STREAM_DEFAULT_BUFFER_SIZE if evs_bufsize is None else evs_bufsize), WeakSet()
    def raise_for_shutdown(self):
        if self._is_shutdown: raise A.BusShutDown(f'{self.name} is shutting down')
    def get_event_stats(self):
        if self._tracking: return self._published.copy()
        raise A.BusStatsError(f'{self.name} is not tracking event stats')
    def subscribers_for(self, event_type): return self._subscribers[event_type].copy()
    def events(self): (s := set(self._subscribers)).discard(None); return s
    def has_subscribers(self, event_type): return bool(self._subscribers[event_type])
    def is_subscribed(self, s, /, event_type=_NO_DEFAULT): return any(s in i for i in self._subscribers.values()) if event_type is _NO_DEFAULT else s in self._subscribers.get(event_type, ())
    @property
    def total_subscribers(self): return sum(map(len, self._subscribers.values()))
    @property
    def wildcards(self): return self.subscribers_for(None)
    @property
    def wildcard_count(self): return len(self._subscribers[None])
    @property
    def active_tasks(self): return self._sem._value
    def is_auditing(self): return self._auditing
    auditing = property(is_auditing, lambda self, v, /: (self.start_audit if v else self.stop_audit)())
    def start_audit(self):
        if not (self._auditing or getattr(a := self.auditor, 'added', False)): audit('asyncutils.channels.EventBus.start_audit', id(self)); addaudithook(a); self._auditing = a.added = True # ty: ignore[unresolved-attribute]
    def stop_audit(self): audit('asyncutils.channels.EventBus.stop_audit', id(self)); self._auditing = False
    def add_middleware(self, middleware): r = len(m := self._middlewares); m.append((middleware, None)); return r
    def remove_middleware(self, cookie, *, result=None, strict=False):
        r, m[cookie] = (m := self._middlewares)[cookie], None
        if r:
            if (F := r[1]).done(): return F.result()
            F.set_result(result)
        elif strict: raise ValueError(cookie)
        return result
    def add_temp_middleware(self, middleware, until): self._middlewares.append((middleware, until))
    @(c := A.dualcontextmanager(use_existing_executor=False, create_executor=False, strict=False))
    def audit_context(self):
        if self._auditing: yield; return
        try: self.start_audit(); yield
        finally: self.stop_audit()
    @c
    def tracking_context(self, stats_receiver=None):
        if self._tracking: yield; return
        try: self.start_tracking(); yield
        finally: self.stop_tracking() if stats_receiver is None else stats_receiver.set_result(self.stop_tracking(True))
    def start_tracking(self): self._tracking = True
    def stop_tracking(self, ret_stats=False): self._tracking = False; return H.copy_and_clear(self._published) if ret_stats else self._published.clear()
    def subscribe(self, s, /, event_type=None): self.raise_for_shutdown(); self._subscribers[event_type].add(s); return s
    def unsubscribe(self, s, /, event_type=None):
        self.raise_for_shutdown()
        try: self._subscribers[event_type].remove(s); return True
        except KeyError: return False
    def on(self, event_type): return partial(self.subscribe, event_type=event_type)
    def subscriber_count(self, event_type): return len(self._subscribers[event_type])
    async def _publish_helper(self, d, s, I, *_, f=I.gather): await f(*((self._safe_callback(i, d, *_) for i in I) if s else (i(d, *_) for i in I)))
    async def publish(self, event_type, data=None, *, wait=True, **k):
        p, f = self.sync_start_publish(event_type, data, **k)
        if not wait: return
        try:
            await p
            if f: raise ExceptionGroup(f'errors occurred in publishing middlewares of {self.name}', f) from None
            L.info('%s: publishing of event %r succeeded', self.name, event_type); L.debug('final data: %r', data)
        except TimeoutError: raise A.BusTimeout(f'{self.name}: publishing of event {event_type!r} took too long') from None
        finally: await A.safe_cancel(p)
    def sync_start_publish(self, event_type, data=None, *, safe=None, timeout=None, chaperone=None):
        self.raise_for_shutdown(); f = []
        if safe is None: safe = A.getcontext().EVENT_BUS_PUBLISH_DEFAULT_SAFE
        async def g(C=(lambda e, /, a=f.extend, b=f.append: a(e.exceptions) if isinstance(e, BaseExceptionGroup) else b(e)) if chaperone is None else chaperone, D=data):
            for t in self._middlewares:
                if t is None: continue
                m, F = t
                if F is not None and F.done(): continue
                try:
                    if I.iscoroutine(D := m(event_type, D)): D = await D
                except A.CRITICAL: raise A.Critical
                except (ExceptionGroup, Exception) as e: C(e) # ruff: ignore[blind-except]
                except BaseException as e: raise A.BusPublishingError(self, m) from e # ty: ignore[invalid-argument-type]
            U = self._subscribers
            if self._tracking: self._published[event_type] += 1
            s, w = (U[_].copy() for _ in (event_type, None))
            await I.gather((f := partial(self._publish_helper, D, safe))(s), f(w, event_type))
        (P := self._publishers).add(p := self.make(I.wait_for(g(), timeout))); p.add_done_callback(lambda p, d=P.discard: d(p)); return p, f
    async def wait_for_event(self, event_type, *, timeout=None, condition=lambda _: True):
        async def handler(d):
            if F.done(): return
            if I.iscoroutine(c := condition(d)): c = await c
            if c: F.set_result(d)
        return self.make(I.wait_for(await self.subscribe_until(F := self.loop.create_future(), handler, event_type), timeout))
    def subscribe_until(self, f, s, /, event_type=None, *, till_permanent=None, _=A.ignore_cancellation.combined(TimeoutError)): # ruff: ignore[function-call-in-default-argument]
        if f.done(): raise RuntimeError('asyncutils.channels.EventBus.subscribe_until: future is already done')
        async def g():
            with _: r = await I.wait_for(f, till_permanent); self.unsubscribe(s, event_type); return r
        self.subscribe(s, event_type); return self.make(g())
    async def feed_event(self, *d, timeout=None):
        if (q := self.stream_queue).full(): L.warning('%s: event stream buffer full', self.name)
        try: await I.wait_for(q.put(d[0] if len(d) == 1 else d), timeout)
        except C.QueueShutDown: L.info('%s: event stream is closing', self.name, exc_info=True)
        except TimeoutError:
            if q.full(): L.warning('%s: event stream data lost', self.name, exc_info=True); q.get_nowait(); q.put_nowait(d)
    async def event_stream(self, event_type=None, *, timeout=_NO_DEFAULT, item_timeout=_NO_DEFAULT):
        self.raise_for_shutdown()
        if not self._auditing: audit('asyncutils.channels.EventBus.event_stream', id(self), event_type)
        t, g = await self.subscribe_until(F := self.loop.create_future(), partial(self.feed_event, timeout=A.getcontext().EVENT_BUS_STREAM_DEFAULT_TIMEOUT if timeout is _NO_DEFAULT else timeout), event_type), self.stream_queue.get
        if _NO_DEFAULT is item_timeout: item_timeout = A.getcontext().EVENT_BUS_STREAM_DEFAULT_ITEM_TIMEOUT
        try:
            while True: yield await I.wait_for(g(), item_timeout)
        except C.QueueShutDown: L.info('%s: event stream has been shut down', self.name, exc_info=True)
        except TimeoutError: L.exception('%s: event stream is stopping because of timeout in waiting for item', self.name)
        finally: F.set_result(None); await t
    async def shutdown(self, immediate=False, *, timeout=None, preserve_stats=False):
        if self._is_shutdown: return
        self._is_shutdown, f = True, self._sem.acquire; self.stop_audit(); self._middlewares.clear()
        self.clear()
        if not preserve_stats: self.clear_stats()
        try:
            async with I.timeout(timeout):
                self.stream_queue.shutdown(immediate)
                for _ in repeat(None, self.active_tasks): await f()
        except TimeoutError: L.exception('%s: shutdown timed out, some tasks may be incomplete', self.name)
        finally:
            if p := self._publishers: await A.safe_cancel_batch(p)
            del self._lock, self._handler, self._sem, self._publishers
    async def handle_exception(self, e):
        if I.iscoroutine(e := self._handler(e)): await e
    def clear(self, event_type=_NO_DEFAULT): return self._subscribers.clear() if event_type is _NO_DEFAULT else self._subscribers.pop(event_type, None)
    def clear_all(self): self.clear(); self.clear_stats()
    def clear_wildcards(self): return self.clear(None)
    def clear_stats(self): self._published.clear()
    async def _safe_callback(self, c, d, t=None, i=None):
        try:
            async with self._sem:
                if I.iscoroutine(r := c(*H.filter_out(t, s=_NO_DEFAULT), d)): await I.wait_for(r, i)
        except TimeoutError: L.warning('%s: callback %s timed out', self.name, H.fullname(c), exc_info=True)
        except A.CRITICAL: raise A.Critical
        except BaseException as e: await self.handle_exception(e) # ruff: ignore[blind-except]
    async def __aenter__(self): return self
    def __aexit__(self, *_): return self.shutdown(True)
    __inc_cnt = count(1).__next__
    P.patch_classmethod_signatures((_ := lambda _, /, f='#%d', c=count(1).__next__: f%c(), '')); P.patch_method_signatures((__init__, 'name=None, *, handler=None, max_concurrent=128, tracking_stats=False'), (subscribe_until, 'fut, subscriber, /, event_type=None, *, till_permanent=None')); WILDCARD, _inc_cnt = None, classmethod(_); del _, c # ruff: ignore[function-call-in-default-argument]
@H.subscriptable
class Rendezvous:
    __slots__ = '_getters', '_lock', '_loop', '_putters', '_task'
    def __init__(self, *, lock=None): self._getters, self._putters, self._loop, self._lock = deque(), deque(), H.get_loop_and_set(), I.Lock() if lock is None else lock; self._make_task()
    async def _maintainer(self):
        f, g = I.sleep.__get__(A.getcontext().RENDEZVOUS_MAINTENANCE_INTERVAL), self.cleanup
        while True: await f(); g()
    async def put(self, v, /, *, timeout=None):
        try: await self.raising_put(v, timeout=timeout); return True
        except (I.CancelledError, TimeoutError): return False
    async def raising_put(self, v, /, *, timeout): await I.wait_for(await I.shield(self._put_helper(v)), timeout)
    async def get(self, default=_NO_DEFAULT, *, timeout=None, _=100):
        f = (p := self._putters).popleft
        while p:
            v, F = f()
            if not F.done(): F.set_result(None); return v
        if timeout is None and default is not _NO_DEFAULT: return default
        self._getters.append(F := self._loop.create_future())
        try: return await I.wait_for(F, timeout)
        except TimeoutError:
            if default is _NO_DEFAULT: raise
            return default
    def __length_hint__(self): return len(self._getters)+len(self._putters)
    def state_snapshot(self, _=namedtuple('StateSnapshot', 'num_getters num_putters num_ops idle', module='asyncutils.channels')): self.cleanup(); t = len(self._getters), len(self._putters); return _(*t, sum(t), not any(t))
    def cleanup(self): self._getters, self._putters = deque(F for F in self._getters if not F.done()), deque(t for t in self._putters if not t[1].done())
    async def exchange(self, v, /, *, asap=False):
        g, f = self._getters, True
        async with self._lock:
            while g:
                if not (F := g.popleft()).done(): break
            else: g.append(F := self._loop.create_future()); f = False
        if f: F.set_result(v); return await self.get()
        await (self._put_helper if asap else self.put)(v); g.appendleft(F); return await F
    async def _put_helper(self, v, /):
        g = self._getters
        async with self._lock:
            while g:
                if not (F := g.popleft()).done(): F.set_result(v); break
            else: self._putters.append((v, F := self._loop.create_future()))
        return F
    async def reset(self, _=partial(A.safe_cancel_batch, disembowel=True)):
        async with self._lock: await I.gather(A.safe_cancel_batch(self._getters, disembowel=True), A.safe_cancel_batch(F async for _, F in A.adisembowel(self._putters)))
        await A.safe_cancel(self._task); self._make_task()
    def _make_task(self): self._task = self._loop.create_task(self._maintainer())
    P.patch_method_signatures((reset, ''), (state_snapshot, ''), (_maintainer, ''))
del P
