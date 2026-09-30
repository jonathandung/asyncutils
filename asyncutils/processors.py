import asyncio as I, asyncutils as A, asyncutils._internal.helpers as H
from _functools import partial
from time import monotonic
from asyncutils._internal.py312 import Queue, QueueShutDown
from asyncutils._internal.submodules import processors_all as __all__
@H.subscriptable
class BoundedBatchProcessor:
    __slots__ = '__b', '__p', '__s'
    def __init__(self, processor, batch=None, max_concurrent=None): C = A.getcontext(); self.__p, self.__b, self.__s = processor, C.BOUNDED_BATCH_PROCESSOR_DEFAULT_BATCH_SIZE if batch is None else batch, I.Semaphore(C.BOUNDED_BATCH_PROCESSOR_DEFAULT_MAX_CONCURRENT if max_concurrent is None else max_concurrent)
    async def process(self, items):
        f, p, s = partial(A.collect, A.iter_to_agen(items), self.__b), self.__p, self.__s
        while b := await f():
            async with s: x = await p(b)
            yield x # ruff: ignore[unnecessary-assign-before-yield]
@H.subscriptable
class BatchProcessor(H.LoopMixinBase):
    __slots__ = '__b', '__lo', '__lp', '__ms', '__p', '__s', '__ta', '__ti'
    def __init__(self, processor, *, maxsize=None, maxtime=None, timer=monotonic): C = A.getcontext(); self.__p, self.__ms, self.__s, self.__b, self.__lp, self.__lo, self.__ti = processor, C.BATCH_PROCESSOR_DEFAULT_MAX_SIZE if maxsize is None else maxsize, I.sleep.__get__(C.BATCH_PROCESSOR_DEFAULT_MAX_TIME if maxtime is None else maxtime), [], timer(), I.Lock(), timer
    async def add(self, item):
        async with self.__lo:
            (b := self.__b).append(item)
            if len(b) >= self.__ms: return await self._process()
    async def _flush_periodic(self):
        while True: await self.__s(); await self.flush()
    async def _process(self):
        if not (b := self.__b): return
        b, self.__lp = H.copy_and_clear(b), self.__ti()
        await self.__p(b)
    async def flush(self):
        async with self.__lo:
            if self.__b: await self._process()
    @property
    def time_since_last_process(self): return self.__ti()-self.__lp
    async def __aenter__(self): self.__ta = self.make(self._flush_periodic()); return self
    async def __aexit__(self, /, *_): await I.gather(self.flush(), A.safe_cancel(self.__ta)); del self.__ta
class Bulkhead(H.LoopMixinBase):
    __slots__ = '__exc', '__iv', '__mr', '__mt', '__p', '__q', '__r', '__sd', '__sem'
    def __init__(self, max_concurrent, *, max_queue=None, max_rej=None, exc=Exception, processor=None):
        if max_concurrent <= 0: raise ValueError('asyncutils.processors.Bulkhead: max_concurrent must be positive')
        C = A.getcontext()
        if max_queue is None: max_queue = C.BULKHEAD_DEFAULT_MAX_QUEUE
        if max_queue <= 0: raise ValueError('asyncutils.processors.Bulkhead: max_queue must be positive')
        if max_rej is None: max_rej = C.BULKHEAD_DEFAULT_MAX_REJ
        super().__init__(); self.__sem, self.__q, self.__r, self.__iv, self.__exc, self.__p, self.__sd, self.__mt, self.__mr = I.Semaphore(max_concurrent), Queue(max_queue), 0, max_concurrent, exc, processor, self.loop.create_future(), I.Event(), max_rej
    async def execute(self, coro):
        try: self.__q.put_nowait(coro)
        except I.QueueFull as e:
            if (x := self.__r) == self.__mr: await self.shutdown(); raise A.BulkheadShutDown(f'{H.fullname(self)} has been shutdown because too many tasks were rejected') from e
            self.__r = x+1; raise A.BulkheadFull(f'{H.fullname(self)} queue full') from None
        if self.is_shutdown: raise A.BulkheadShutDown(f'{H.fullname(self)} is shutting down')
        async with self.__sem:
            try: await (await self.__q.get())
            except (I.QueueEmpty, QueueShutDown, I.CancelledError): raise A.BulkheadShutDown(f'{H.fullname(self)} is shutting down') from None
            except self.__exc as e:
                if p := self.__p: await p(e)
        getattr(self.__mt, 'clear' if self.active_tasks else 'set')()
    async def __aenter__(self): return self
    async def __aexit__(self, /, *_): await self.shutdown()
    @property
    def available_slots(self): return self.__sem._value
    @property
    def active_tasks(self): return self.__iv-self.available_slots
    @property
    def curr_qsize(self): return self.__q.qsize()
    @property
    def max_qsize(self): return self.__q.maxsize
    @property
    def available_queue_slots(self): return m-self.curr_qsize if (m := self.max_qsize) > 0 else float('inf')
    @property
    def is_shutdown(self): return self.__sd.done()
    @property
    def rejected(self): return self.__r
    async def wait_until_idle(self, timeout=None): await I.wait_for(self.__mt.wait(), timeout)
    def wait_for_shutdown(self, timeout=None): return I.wait_for(self.__sd, timeout)
    async def shutdown(self, timeout=None):
        self.__sd.set_result(None); (h := (q := self.__q).shutdown)(); r = []
        try:
            async with I.timeout(timeout):
                await self.__mt.wait(); a = (s := self.__sem).acquire
                while s._value: await a()
        except TimeoutError:
            f, g = r.append, q.get_nowait
            while True:
                try: f(g())
                except: h(True); break # ruff: ignore[bare-except]
        return r
