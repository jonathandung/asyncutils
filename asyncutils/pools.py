import asyncutils as A, asyncio as I
from asyncutils._internal.py312 import PriorityQueue
from asyncutils._internal.helpers import LoopMixinBase, fullname, subscriptable
from asyncutils._internal.submodules import pools_all as __all__
from _functools import partial
from itertools import count, repeat
from threading import Thread, Lock as TLock
from time import monotonic
class AdvancedPool(A.LoopContextMixin):
    __slots__ = '__cnt', '__cur', '__fs', '__kae', '__max', '__min', '__pending', '__q', '__scaling', '__sde', '__shutdown', '__start', '__tl', '__workers', 'completed'
    @property
    def __tiebreak(self): return next(self.__cnt)
    def __init__(self, max_workers=None, min_workers=None, qsize=0, scaling=True, kill_at_exit=False): super().__init__(); C = A.getcontext(); self.__cnt, self.__tl, self.__max, self.__scaling, self.__q, self.__workers, self.__fs, self.__pending, self.__sde, self.__shutdown, self.__start, self.completed, self.__kae = count(), TLock(), C.ADVANCED_POOL_DEFAULT_MAX_WORKERS if max_workers is None else max_workers, scaling, PriorityQueue(qsize), set(), set(), 0, I.Event(), False, monotonic(), 0, kill_at_exit; self.__cur = self.__min = C.ADVANCED_POOL_DEFAULT_MIN_WORKERS if min_workers is None else min_workers
    def __repr__(self): return f'{fullname(self)}({self.__max}, {self.__min}, {self.__q.maxsize}, {self.__scaling}, {self.__kae})'
    async def __ts_get(self):
        with self.__tl: return await self.__q.get()
    def __ts_task_done(self):
        with self.__tl: self.__q.task_done()
    def __wl(self, _):
        x, g, G = 0, (L := self.loop).call_soon_threadsafe, self.__ts_get
        try: # noqa: PLW0717
            while not self.__shutdown:
                if (F := A.sync_await(G(), loop=L)[2]) is None: self.__ts_task_done(); break
                f, a, k, F = F
                try: F.set_result(f(*a, **k))
                except BaseException as e: F.set_exception(e) # noqa: BLE001
                finally:
                    self.__ts_task_done(); x += 1
                    with self.__tl: self.completed += 1; self.__pending -= 1
        except BaseException as e: g(_.set_exception, A.Critical(e) if isinstance(e, A.CRITICAL) else e) # noqa: BLE001
        else: g(_.set_result, x)
    def __scale_to(self, new):
        if (d := new-self.__cur) > 0:
            a, b, f, g = self.__workers.add, self.__fs.add, self.__wl, self.make_fut
            for _ in repeat(None, d): (T := Thread(target=f, args=(F := g(),))).start(); a(T); b(F)
        elif d < 0:
            f = self.__q.put_nowait
            for _ in repeat(None, -d): f((0, self.__tiebreak, None))
        self.__cur = new
    def __set_adjuster(self):
        if not self.__scaling: return
        C = A.getcontext()
        if (l := self.__pending/((c := self.__cur) or 1)) > C.ADVANCED_POOL_THRESHOLD_HI and c < (M := self.__max): self.__scale_to(min(M, c+max(1, c>>1)))
        elif l < C.ADVANCED_POOL_THRESHOLD_LO and c > (m := self.__min): self.__scale_to(max(m, c-max(1, int(c*C.ADVANCED_POOL_FACTOR))))
    async def wait_for_shutdown(self): return await self.__sde.wait()
    def raise_for_shutdown(self):
        if self.__shutdown: raise A.PoolShutDown(f'{fullname(self)} is shutting down')
    def submit_nowait(self, f, *a, _priority_=0, **k):
        self.raise_for_shutdown()
        if self.full: raise A.PoolFull('asyncutils.pool.AdvancedPool.submit_nowait: task queue full')
        with self.__tl: self.__pending += 1
        self.__q.put_nowait((_priority_, self.__tiebreak, (f, a, k, F := self.make_fut()))); self.__set_adjuster(); return F
    async def _kill_helper(self):
        f, g = (q := self.__q).get_nowait, q.task_done
        with self.__tl, A.ignore_qempty:
            while True:
                if (F := f()[2]) is not None: await A.safe_cancel(F[-1])
                g()
    async def complete(self, *a, **k): return await (await self.submit(*a, **k))
    async def submit(self, f, *a, _priority_=0, **k):
        self.raise_for_shutdown()
        with self.__tl: self.__pending += 1
        await self.__q.put((_priority_, self.__tiebreak, (f, a, k, F := self.make_fut()))); self.__set_adjuster(); return F
    async def shutdown(self, cancel_pending=False, idle_timeout=None):
        if self.__shutdown: return await self.wait_for_shutdown()
        if cancel_pending: await self._kill_helper()
        else:
            try: await self.wait_for_slot(idle_timeout)
            except A.PoolFull: await self._kill_helper()
        p = (q := self.__q).put
        with A.ignore_qshutdown:
            for _ in repeat(None, self.__cur): await p((0, self.__tiebreak, None))
        with self.__tl: q.shutdown(True)
        await self.join(); self.__sde.set(); return self.uptime
    async def join(self): return await I.gather(*self.__fs, return_exceptions=True)
    async def map(self, f, /, *its, priority=0, strict=False): return await A.agather(A.amap(partial(self.complete, f, _priority_=priority), *its, strict=strict))
    async def starmap(self, f, it, /, priority=0): return await A.agather(A.astarmap(partial(self.complete, f, _priority_=priority), it))
    async def double_starmap(self, f, it, /, priority=0): return await A.agather(A.adouble_starmap(partial(self.complete, f, _priority_=priority), it))
    async def starmap_with_kwds(self, f, it, /, priority=0): return await A.agather(A.astarmap_with_kwds(partial(self.complete, f, _priority_=priority), it))
    async def resize(self, min_workers, max_workers): M = max(max_workers, m := max(1, min_workers)); self.__scale_to(min(max(self.__cur, m), M)); self.__min, self.__max = m, M
    def drain(self): return self.__q.join()
    async def wait_for_slot(self, timeout=None):
        self.raise_for_shutdown()
        if not self.full: return 0.0
        try: t = monotonic(); await I.wait_for(self.drain(), timeout); return monotonic()-t
        except TimeoutError: raise A.PoolFull('asyncutils.pools.AdvancedPool: timeout waiting for queue space') from None
    async def __cleanup__(self): await self.shutdown(self.__kae)
    def __del__(self):
        if self.loop.is_running(): self.make(self.shutdown(True, 0.03))
    @property
    def full(self): return self.__q.full()
    @property
    def empty(self): return self.__q.empty()
    @property
    def qsize(self): return self.__q.qsize()
    @property
    def idle(self): return self.empty and not self.__pending
    @property
    def uptime(self): return monotonic()-self.__start
@subscriptable
class ConnectionPool(LoopMixinBase):
    __slots__ = '_available', '_cleaner', '_creation_times', '_factory', '_healthchecker', '_in_use', '_lock', '_maintainer', '_pool', 'maxlife', 'maxsize', 'minsize'
    def __init__(self, factory, maxsize=None, minsize=None, maxlife=None, healthchecker=None, cleaner=None): C = A.getcontext(); self._factory, self.maxsize, self.minsize, self.maxlife, self._healthchecker, self._cleaner, self._pool, self._in_use, self._creation_times, self._lock, self._available, self._maintainer = factory, C.CONNECTION_POOL_DEFAULT_MAX_SIZE if maxsize is None else maxsize, C.CONNECTION_POOL_DEFAULT_MIN_SIZE if minsize is None else minsize, C.CONNECTION_POOL_DEFAULT_MAX_LIFE if maxlife is None else maxlife, healthchecker or (lambda _: True), cleaner or (lambda _: None), [], set(), {}, I.Lock(), I.Event(), None
    def _is_healthy(self, conn, /): return self._healthchecker(conn) and not ((t := self._creation_times.get(id(conn))) and monotonic()-t > self.maxlife)
    async def create_connection(self, *a, _executor_=None, **k): self._creation_times[id(c := await self.loop.run_in_executor(_executor_, partial(self._factory, *a, **k)))] = monotonic(); return c
    async def acquire(self, *a, **k):
        p = self._pool
        async with self._lock:
            while p:
                if self._is_healthy(c := p.pop()): self._in_use.add(c); return c
                self._cleaner(c)
            if self.cursize < self.maxsize: self._in_use.add(c := await self.create_connection(*a, **k)); return c
        await self._available.wait(); return await self.acquire(*a, **k)
    def release(self, c, /, *a, **k):
        self._in_use.discard(c)
        if self._is_healthy(c) and len(self._pool) < self.maxsize: self._pool.append(c); self._available.set(); self._available.clear()
        else:
            self._cleaner(c)
            if self.cursize < self.minsize: self.make(self.create_connection(*a, **k))
    async def _maintain(self):
        f = I.sleep.__get__(A.getcontext().CONNECTION_POOL_MAINTENANCE_INTERVAL)
        while True:
            await f(); n, g = [], self.create_connection
            for c in self._pool: (n.append if self._healthchecker(c) else self._cleaner)(c)
            async with self._lock: n.extend(await I.gather(*(g() for _ in repeat(None, self.minsize-self.cursize)))); self._pool = n
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
    def cursize(self): return self.available+self.in_use
    @property
    def available(self): return len(self._pool)
    @property
    def in_use(self): return len(self._in_use)
