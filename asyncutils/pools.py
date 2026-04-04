from .base import aiter_to_iter, take, event_loop, dummy_task
from .constants import _NO_DEFAULT
from .exceptions import exception_occurred, wrap_exc, unwrap_exc, CRITICAL, Critical, PoolError, PoolShutDown, PoolFull
from ._internal.helpers import filter_out, check_methods, subscriptable
from .mixins import LoopContextMixin, AsyncContextMixin
from .util import semaphore, safe_cancel, sync_lock_from_binder, _ignore_cancellation
from asyncio.locks import Event, Lock
from asyncio.queues import Queue, PriorityQueue
from asyncio.tasks import gather, wait_for, sleep
from asyncio.timeouts import timeout
from _functools import partial # type: ignore[import-not-found]
from itertools import count
from sys import exc_info
from time import monotonic
from ._internal.submodules import pools_all as __all__
@subscriptable
class Pool(LoopContextMixin):
    __slots__ = '_func', '_it', '_sem', '_queue', '_task', '_event'
    def __init__(self, func, it, workers=4, bounded=False): self._func, self._it, self._sem, self._queue, self._task, self._event = func, it, semaphore(bounded, workers), Queue(1), None, Event()
    async def process(self, item):
        async with self._sem: await self._queue.put(await self._func(item))
    def __aiter__(self):
        async def consumer():
            try:
                if check_methods(I := self._it, '__aiter__'):
                    async for _ in I: await self.process(_)
                else:
                    for _ in I: await self.process(_)
            finally: await self._queue.put(wrap_exc(StopAsyncIteration('pool ran out of items'))); self._event.set()
        import asyncio.events as E; self._task = (E._get_running_loop() or E.new_event_loop()).create_task(consumer()); return self
    async def __anext__(self):
        if self._event.is_set() and self._queue.empty(): raise StopAsyncIteration('pool ran out of items')
        try:
            if exception_occurred(i := await self._queue.get()) and isinstance(e := unwrap_exc(i), StopAsyncIteration): raise e
            return i
        finally:
            if self._task: self._task.cancel()
    async def __setup__(self): super().__init__()
    async def aclose(self):
        if t := self._task: await safe_cancel(t)
    __cleanup__ = aclose
class AdvancedPool(LoopContextMixin):
    __slots__ = '__cnt', '_max', 'completed', '_max', '_min', '_scaling', '_kill_at_exit', '_queue', '_workers', '_pending', '_shutdown', '_lock', '_adjustment', '_start', '_current'
    @property
    def _tiebreak(self): return self.__cnt.__next__()
    def __init__(self, max_workers=5, min_workers=1, qsize=0, scaling=True, kill_at_exit=False): super().__init__(); self.__cnt, self._max, self._scaling, self._queue, self._workers, self._pending, self._shutdown, self._lock, self._adjustment, self._start, self.completed, self._kill_at_exit = count(), max_workers, scaling, PriorityQueue(qsize), set(), 0, False, Lock(), None, monotonic(), 0, kill_at_exit; self._current = self._min = min_workers
    def __repr__(self): return f'{type(self).__qualname__}({self._max}, {self._min}, {self._queue.maxsize}, {self._scaling}, {self._kill_at_exit})'
    async def _worker_loop(self):
        with _ignore_cancellation:
            while not self._shutdown:
                if (F := (await self._queue.get())[2]) is None: self._queue.task_done(); break
                f, a, k, F = F
                try: F.set_result(await f(*a, **k))
                except CRITICAL: raise Critical
                except BaseException as e: F.set_exception(e)
                finally: self._queue.task_done(); self.completed += 1; self._pending -= 1
    async def _adjust_workers(self):
        if not self._scaling: return
        async with self._lock:
            if (l := self._pending/(self._current or 1)) > 1.5 and self._current < self._max: self._scale_to(min(self._max, self._current+max(1, int(self._current/2))))
            elif l < 0.5 and self._current > self._min: self._scale_to(max(self._min, self._current-max(1, int(self._current*0.3))))
    def _scale_to(self, new):
        if (d := new-self._current) > 0:
            f, g, h, j = (w := self._workers).add, w.discard, self.make, self._worker_loop
            for _ in range(d): f(w := h(j())); w.add_done_callback(g)
        elif d < 0:
            f = self._put_nowait_priority
            for _ in range(-d): f(0, None)
        self._current = new
    def _put_nowait_priority(self, priority, item): self._queue.put_nowait((priority, self._tiebreak, item))
    def set_adjuster(self, raising=False):
        if self._scaling: self._adjustment = self.make(self._adjust_workers())
        elif raising: raise PoolError(f'{type(self).__qualname__} is non-scaling')
    def raise_for_shutdown(self):
        if self._shutdown: raise PoolShutDown(f'{type(self).__qualname__} is shutting down')
    def submit_nowait(self, f, *a, _priority_=0, **k):
        self.raise_for_shutdown()
        if self.full: raise PoolFull('task queue full')
        self._pending += 1; self._put_nowait_priority(_priority_, (f, a, k, F := self.make_fut())); self.set_adjuster(); return F
    def dead(self, worker): return worker in self._workers and worker.done() and not worker.cancelled()
    def revive(self): self.__init__(self._max, self._min, self._queue.maxsize, self._scaling, self._kill_at_exit)
    async def _kill_helper(self):
        from .queues import ignore_qempty as C; f, g = (q := self._queue).get_nowait, q.task_done
        with C:
            while True:
                if (F := f()[2]) is not None: await safe_cancel(F[3])
                g()
    async def submit(self, f, *a, _priority_=0, **k): self.raise_for_shutdown(); self._pending += 1; await self._queue.put((_priority_, self._tiebreak, (f, a, k, F := self.make_fut()))); self.set_adjuster(); return F
    async def shutdown(self, cancel_pending=False, idle_timeout=None, total_timeout=None):
        self._shutdown = True
        try:
            async with timeout(total_timeout):
                if a := self._adjustment: await safe_cancel(a)
                if cancel_pending: await self._kill_helper()
                else:
                    try: await self.wait_for_slot(idle_timeout)
                    except PoolFull: await self._kill_helper()
                for _ in range(self._current): await self._queue.put((0, self._tiebreak, None))
                self._queue.shutdown(True); await self.gather(True); await self.drain(); return self.uptime
        except TimeoutError: self.exiter(); raise TimeoutError('kill exceeded timeout, forced shutdown') from None
    async def gather(self, ret_exc=False): return await gather(*self._workers, return_exceptions=ret_exc)
    async def map(self, f, it, priority=0): return await gather(*[await self.submit(f, i, _priority_=priority) for i in it])
    async def starmap(self, f, it, priority=0): return await gather(*[await self.submit(f, *a, _priority_=priority) for a in it])
    async def doublestarmap(self, f, it, priority=0): return await gather(*[await self.submit(f, _priority_=priority, **k) for k in it])
    async def starmap_withkwds(self, f, it, priority=0): return await gather(*[await self.submit(f, *a, _priority_=priority, **k) for a, k in it])
    async def resize(self, _min, _max):
        async with self._lock: M = max(_max, m := max(1, _min)); self._scale_to(min(max(self._current, m), M)); self._min, self._max = m, M
    async def drain(self): await self._queue.join()
    async def restart_worker(self, worker): self._workers.discard(worker); self._workers.add(t := self.make(self._worker_loop())); t.add_done_callback(self._workers.discard); return t
    async def health_check(self):
        if self._shutdown: return False
        for w in filter(self.dead, self._workers): await self.restart_worker(w)
        t = self.make(dummy_task)
        for _ in range(self._min-len(self._workers)): await self.restart_worker(t)
        self._current = len(self._workers); return True
    async def wait_for_slot(self, timeout=None):
        self.raise_for_shutdown()
        if not self.full: return 0.0
        try: t = monotonic(); await wait_for(self._queue.join(), timeout); return monotonic()-t
        except TimeoutError: raise PoolFull('timeout waiting for queue space') from None
    async def __cleanup__(self): await self.shutdown(self._kill_at_exit)
    @property
    def full(self): return self._queue.full()
    @property
    def empty(self): return self._queue.empty()
    @property
    def qsize(self): return self._queue.qsize()
    @property
    def idle(self): return self.empty and not self._pending
    @property
    def uptime(self): return monotonic()-self._start
@subscriptable
class ConnectionPool:
    __slots__ = '_healthchecker', '_creation_times', '_loop', '_factory', '_pool', 'maxsize', 'minsize', '_in_use', 'maxlife', '_cleaner', '_lock', '_available', '_exiter', '_maintainer'
    def __init__(self, factory, maxsize=10, minsize=10, maxlife=3600, healthchecker=None, cleaner=None): self._factory, self.maxsize, self.minsize, self.maxlife, self._healthchecker, self._cleaner, self._pool, self._in_use, self._creation_times, self._lock, self._available, self._exiter = factory, maxsize, minsize, maxlife, healthchecker or (lambda _: True), cleaner or (lambda _: None), [], set(), {}, Lock(), Event(), CallbackAccumulator('__exit__'); self._maintainer = self._loop = None
    def _is_healthy(self, conn, /): return self._healthchecker(conn) and not ((t := self._creation_times.get(id(conn))) and monotonic()-t > self.maxlife)
    async def create_connection(self, *a, _executor_=None, **k): self._creation_times[id(c := self.loop.run_in_executor(_executor_, partial(self._factory, *a, **k)))] = monotonic(); return await c
    async def acquire(self, *a, **k):
        p = self._pool
        async with self._lock:
            while p:
                if self._is_healthy(c := p.pop()): self._in_use.add(c); return c
                self._cleaner(c)
            if self.currsize < self.maxsize: self._in_use.add(c := await self.create_connection(*a, **k)); return c
        await self._available.wait(); return await self.acquire(*a, **k)
    async def release(self, conn, /, *a, **k):
        async with self._lock:
            self._in_use.discard(conn)
            if self._is_healthy(conn) and len(self._pool) < self.maxsize: self._pool.append(conn); self._available.set(); self._available.clear()
            else:
                self._cleaner(conn)
                if self.currsize < self.minsize: self.loop.create_task(self.create_connection(*a, **k))
    async def _maintain(self, intvl=30.0):
        while True:
            await sleep(intvl); n = []
            async with self._lock:
                for c in self._pool: (n.append if self._healthchecker(c) else self._cleaner)(c)
                self._pool = n
                while self.currsize < self.minsize: n.append(await self.create_connection())
    async def start(self, akgen=None, executor=None):
        f = self.create_connection
        if akgen is None:
            for _ in range(self.minsize): await f(_executor_=executor)
        else:
            async for a, k in take(akgen, self.minsize, default=((), {})): await f(*a, _executor_=executor, **k)
        self._maintainer = self.loop.create_task(self._maintain())
    async def stop(self):
        if (m := self._maintainer): await safe_cancel(m)
        async with self._lock:
            while self._pool: self._cleaner(self._pool.pop())
            for _ in self._in_use: self._cleaner(_)
            self._in_use.clear()
        self._exiter(*exc_info()); self._loop = None
    async def __aenter__(self): await self.start(); return self
    async def __aexit__(self, /, *_): await self.stop()
    @property
    @(_locker := sync_lock_from_binder(lambda self: self._lock)) # type: ignore
    def loop(self): # type: ignore
        if self._loop is None: self._loop = (_ := event_loop.from_flags(0)).__enter__(); self._exiter.add(_)
        return self._loop
    @loop.setter
    @_locker
    def loop(self, val, /): # type: ignore
        if (l := self._loop) is not None: l.call_soon(l.stop)
        self._loop = val
    @loop.deleter
    @_locker
    def loop(self): self._loop = None
    @property
    def currsize(self): return self.available+self.in_use
    @property
    def available(self): return len(self._pool)
    @property
    def in_use(self): return len(self._in_use)
    del _locker
class CallbackAccumulator(__import__('_collections').deque, AsyncContextMixin):
    def __init__(self, name, it=(), maxlen=None, default=_NO_DEFAULT, call_once=True, default_getter=None): super().__init__(aiter_to_iter(it), maxlen); self.t, self.call_once, self.default_getter = tuple(filter_out(name, default, s=_NO_DEFAULT)), call_once, (lambda: (exc_info(), {}) if name == '__exit__' else ((), {})) if default_getter is None else default_getter
    def __call__(self, *a, **k):
        for f in self: f(*a, **k)
    def __exit__(self, /, *_): a, k = self.default_getter(); self(*a, **k)
    def add(self, o, /): self.append(getattr(o, *self.t))
    def offer_last(self, o, /):
        if (x := self.maxlen) is None or x > len(self): self.add(o)
    @property
    def callbacks(self): return self.copy()
    def __iter__(self):
        if self.call_once:
            while self: yield self.pop()
        else: yield from self.callbacks