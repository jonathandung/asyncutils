import asyncutils as A, asyncio as I
from asyncutils.constants import _NO_DEFAULT
from asyncutils._internal.compat import PriorityQueue
from asyncutils._internal.helpers import filter_out, fullname, subscriptable
from asyncutils._internal.submodules import pools_all as __all__
from _functools import partial
from itertools import count, repeat
from sys import exc_info
from threading import Thread, Lock as TLock
from time import monotonic
class AdvancedPool(A.LoopContextMixin):
    __slots__ = '__cnt', '_current', '_kill_at_exit', '_max', '_min', '_pending', '_queue', '_scaling', '_shutdown', '_start', '_workers', 'completed'
    @property
    def _tiebreak(self): return self.__cnt.__next__()
    def __init__(self, max_workers=None, min_workers=None, qsize=0, scaling=True, kill_at_exit=False): super().__init__(); C = A.getcontext(); self.__cnt, self._tlock, self._max, self._scaling, self._queue, self._workers, self._futures, self._pending, self._shutdown, self._start, self.completed, self._kill_at_exit = count(), TLock(), C.ADVANCED_POOL_DEFAULT_MAX_WORKERS if max_workers is None else max_workers, scaling, PriorityQueue(qsize), set(), set(), 0, False, monotonic(), 0, kill_at_exit; self._current = self._min = C.ADVANCED_POOL_DEFAULT_MIN_WORKERS if min_workers is None else min_workers
    def __repr__(self): return f'{fullname(self)}({self._max}, {self._min}, {self._queue.maxsize}, {self._scaling}, {self._kill_at_exit})'
    async def _threadsafe_get(self):
        with self._tlock: return await self._queue.get()
    def _threadsafe_task_done(self):
        with self._tlock: self._queue.task_done()
    def _worker_loop(self, _):
        x, g, G = 0, (L := self.loop).call_soon_threadsafe, self._threadsafe_get
        try:
            while not self._shutdown:
                if (F := A.sync_await(G(), loop=L)[2]) is None: self._threadsafe_task_done(); break
                f, a, k, F = F
                try: F.set_result(f(*a, **k))
                except BaseException as e: F.set_exception(e) # noqa: BLE001
                finally:
                    self._threadsafe_task_done(); x += 1
                    with self._tlock: self.completed += 1; self._pending -= 1
        except A.CRITICAL as e: g(_.set_exception, A.Critical(e))
        else: g(_.set_result, x)
    def _scale_to(self, new):
        if (d := new-self._current) > 0:
            a, b, f, g = self._workers.add, self._futures.add, self._worker_loop, self.make_fut
            for _ in repeat(None, d): (T := Thread(target=f, args=(F := g(),))).start(); a(T); b(F)
        elif d < 0:
            f = self._put_nowait_priority
            for _ in repeat(None, -d): f(0, None)
        self._current = new
    def _put_nowait_priority(self, priority, item): self._queue.put_nowait((priority, self._tiebreak, item))
    def _set_adjuster(self):
        if not self._scaling: return
        C = A.getcontext()
        if (l := self._pending/((c := self._current) or 1)) > C.ADVANCED_POOL_THRESHOLD_HI and c < (M := self._max): self._scale_to(min(M, c+max(1, c>>1)))
        elif l < C.ADVANCED_POOL_THRESHOLD_LO and c > (m := self._min): self._scale_to(max(m, c-max(1, int(c*C.ADVANCED_POOL_FACTOR))))
    def raise_for_shutdown(self):
        if self._shutdown: raise A.PoolShutDown(f'{fullname(self)} is shutting down')
    def submit_nowait(self, f, *a, _priority_=0, **k):
        self.raise_for_shutdown()
        if self.full: raise A.PoolFull('asyncutils.pool.AdvancedPool.submit_nowait: task queue full')
        with self._tlock: self._pending += 1
        self._put_nowait_priority(_priority_, (f, a, k, F := self.make_fut())); self._set_adjuster(); return F
    async def _kill_helper(self):
        f, g = (q := self._queue).get_nowait, q.task_done
        with self._tlock, A.ignore_qempty:
            while True:
                if (F := f()[2]) is not None: await A.safe_cancel(F[-1])
                g()
    async def complete(self, *a, **k): return await (await self.submit(*a, **k))
    async def submit(self, f, *a, _priority_=0, **k):
        self.raise_for_shutdown()
        with self._tlock: self._pending += 1
        await self._queue.put((_priority_, self._tiebreak, (f, a, k, F := self.make_fut()))); self._set_adjuster(); return F
    async def shutdown(self, cancel_pending=False, idle_timeout=None):
        self._shutdown, p = True, (q := self._queue).put
        if cancel_pending: await self._kill_helper()
        else:
            try: await self.wait_for_slot(idle_timeout)
            except A.PoolFull: await self._kill_helper()
        for _ in repeat(None, self._current): await p((0, self._tiebreak, None))
        with self._tlock: q.shutdown(True)
        await self.join(); return self.uptime
    async def join(self): return await I.gather(*self._futures, return_exceptions=True)
    async def map(self, f, /, *its, priority=0, strict=False): return await A.agather(A.amap(partial(self.complete, f, _priority_=priority), *its, strict=strict))
    async def starmap(self, f, it, /, priority=0): return await A.agather(A.astarmap(partial(self.complete, f, _priority_=priority), it))
    async def doublestarmap(self, f, it, /, priority=0): return await A.agather(A.adoublestarmap(partial(self.complete, f, _priority_=priority), it))
    async def starmap_withkwds(self, f, it, /, priority=0): return await A.agather(A.astarmap_withkwds(partial(self.complete, f, _priority_=priority), it))
    async def resize(self, min_workers, max_workers): M = max(max_workers, m := max(1, min_workers)); self._scale_to(min(max(self._current, m), M)); self._min, self._max = m, M
    def drain(self): return self._queue.join()
    async def wait_for_slot(self, timeout=None):
        self.raise_for_shutdown()
        if not self.full: return 0.0
        try: t = monotonic(); await I.wait_for(self.drain(), timeout); return monotonic()-t
        except TimeoutError: raise A.PoolFull('asyncutils.pools.AdvancedPool: timeout waiting for queue space') from None
    async def __cleanup__(self): await self.shutdown(self._kill_at_exit)
    def __del__(self):
        try:
            if (l := self.loop).is_running(): l.call_soon_threadsafe(self.shutdown, True, 0.2)
        except (AttributeError, RuntimeError): ...
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
class ConnectionPool(A.LoopBoundMixin):
    __slots__ = '_available', '_cleaner', '_creation_times', '_factory', '_healthchecker', '_in_use', '_lock', '_maintainer', '_pool', 'maxlife', 'maxsize', 'minsize'
    def __init__(self, factory, maxsize=None, minsize=None, maxlife=None, healthchecker=None, cleaner=None): C = A.getcontext(); self._factory, self.maxsize, self.minsize, self.maxlife, self._healthchecker, self._cleaner, self._pool, self._in_use, self._creation_times, self._lock, self._available, self._maintainer = factory, C.CONNECTION_POOL_DEFAULT_MAX_SIZE if maxsize is None else maxsize, C.CONNECTION_POOL_DEFAULT_MIN_SIZE if minsize is None else minsize, C.CONNECTION_POOL_DEFAULT_MAX_LIFE if maxlife is None else maxlife, healthchecker or (lambda _: True), cleaner or (lambda _: None), [], set(), {}, I.Lock(), I.Event(), None
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
    def release(self, c, /, *a, **k):
        self._in_use.discard(c)
        if self._is_healthy(c) and len(self._pool) < self.maxsize: self._pool.append(c); self._available.set(); self._available.clear()
        else:
            self._cleaner(c)
            if self.currsize < self.minsize: self.make(self.create_connection(*a, **k))
    async def _maintain(self):
        f = I.sleep.__get__(A.getcontext().CONNECTION_POOL_MAINTENANCE_INTERVAL)
        while True:
            await f(); n, g = [], self.create_connection
            for c in self._pool: (n.append if self._healthchecker(c) else self._cleaner)(c)
            async with self._lock: n.extend(await I.gather(*(g() for _ in repeat(None, self.minsize-self.currsize)))); self._pool = n
    async def start(self, akgen=None, executor=None):
        f = self.create_connection
        if akgen is None:
            for _ in repeat(None, self.minsize): await f(_executor_=executor)
        else:
            async for a, k in A.take(akgen, self.minsize, default=((), {})): await f(*a, _executor_=executor, **k)
        self._maintainer = self.make(self._maintain())
    async def stop(self):
        if m := self._maintainer: await A.safe_cancel(m)
        p, c, f = (P := self._pool).pop, self._cleaner, (u := self._in_use).pop
        while P: c(p())
        while u: c(f())
    async def __aenter__(self): await self.start(); return self
    async def __aexit__(self, /, *_): await self.stop()
    @property
    def currsize(self): return self.available+self.in_use
    @property
    def available(self): return len(self._pool)
    @property
    def in_use(self): return len(self._in_use)
class CallbackAccumulator(__import__('_collections').deque, A.ExecutorRequiredAsyncContextMixin):
    __slots__ = 'call_once', 'default_getter', 't'
    def __init__(self, name, it=(), maxlen=None, default=_NO_DEFAULT, call_once=True, default_getter=None): super().__init__(A.aiter_to_gen(it), maxlen); self.t, self.call_once, self.default_getter = tuple(filter_out(name, default, s=_NO_DEFAULT)), call_once, (lambda: (exc_info(), {}) if name == '__exit__' else ((), {})) if default_getter is None else default_getter
    def __call__(self, *a, **k):
        for f in self: f(*a, **k)
    def __enter__(self): return self
    def __exit__(self, /, *_): a, k = self.default_getter(); self(*a, **k)
    def add(self, o, /): self.append(getattr(o, *self.t))
    def offer_last(self, o, /):
        if (x := self.maxlen) is None or x > len(self): self.add(o); return True
        return False
    @property
    def callbacks(self): return self.copy()
    def __iter__(self):
        if self.call_once:
            p = self.popleft
            while self: yield p()
        else: yield from self.callbacks