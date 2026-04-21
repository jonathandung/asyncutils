from ._internal.compat import Queue, QueueEmpty, QueueFull, QueueShutDown
from ._internal.helpers import copy_and_clear, fullname, subscriptable
from ._internal.submodules import processors_all as __all__
from .base import collect, iter_to_aiter, safe_cancel_batch
from .context import getcontext
from .exceptions import BulkheadFull, BulkheadShutDown
from .mixins import LoopContextMixin
from .util import safe_cancel
from _functools import partial # type: ignore[import-not-found]
from asyncio.exceptions import CancelledError
from asyncio.locks import Event, Lock, Semaphore
from asyncio.tasks import sleep, wait_for
from asyncio.timeouts import timeout as _timeout
from time import monotonic
@subscriptable
class BoundedBatchProcessor:
    __slots__ = '_batch', '_processor', '_sem'
    def __init__(self, processor, batch=None, max_concurrent=None): C = getcontext(); self._processor, self._batch, self._sem = processor, C.BOUNDED_BATCH_PROCESSOR_DEFAULT_BATCH_SIZE if batch is None else batch, Semaphore(C.BOUNDED_BATCH_PROCESSOR_DEFAULT_MAX_CONCURRENT if max_concurrent is None else max_concurrent)
    async def process(self, items):
        f, p, s = partial(collect, iter_to_aiter(items), self._batch), self._processor, self._sem
        while b := await f():
            async with s: yield await p(b)
@subscriptable
class BatchProcessor(LoopContextMixin):
    __slots__ = '_batch', '_flusher', '_last_process', '_lock', '_maxsize', '_processor', '_sleep', '_timer'
    def __init__(self, processor, *, maxsize=None, maxtime=None, timer=monotonic): C = getcontext(); self._processor, self._maxsize, self._sleep, self._batch, self._last_process, self._lock, self._timer = processor, C.BATCH_PROCESSOR_DEFAULT_MAX_SIZE if maxsize is None else maxsize, sleep.__get__(C.BATCH_PROCESSOR_DEFAULT_MAX_TIME if maxtime is None else maxtime), [], timer(), Lock(), timer; self._flusher = None
    async def add(self, item):
        async with self._lock:
            (b := self._batch).append(item)
            if len(b) >= self._maxsize: return await self._process()
            if self._flusher is None: self._flusher = self.make(self._schedule_flush())
    async def _schedule_flush(self): await self._sleep(); await self.flush(); self._flusher = None
    async def _process(self):
        if not (b := self._batch): return
        b, self._last_process = copy_and_clear(b), self._timer()
        await self._processor(b)
    async def flush(self):
        async with self._lock:
            if self._batch: await self._process()
    @property
    def time_since_last_process(self): return self._timer()-self._last_process
    async def __setup__(self): super().__init__()
    async def __cleanup__(self):
        if (f := self._flusher) is not None: await safe_cancel(f)
class Bulkhead(LoopContextMixin):
    __slots__ = '_exc', '_init_val', '_max_rej', '_mtevt', '_processor', '_queue', '_rejected', '_sdevt', '_sem'
    def __init__(self, max_concurrent, *, max_queue=None, max_rej=None, exc=Exception, processor=None): super().__init__(); C = getcontext(); self._sem, self._queue, self._rejected, self._init_val, self._exc, self._processor, self._sdevt, self._mtevt, self._max_rej = Semaphore(max_concurrent), Queue(C.BULKHEAD_DEFAULT_MAX_QUEUE if max_queue is None else max_queue), 0, max_concurrent, exc, processor, Event(), Event(), C.BULKHEAD_DEFAULT_MAX_REJ if max_rej is None else max_rej
    async def execute(self, coro):
        try: self._queue.put_nowait(coro)
        except QueueFull as e:
            if (x := self._rejected) == self._max_rej: await self.shutdown(); raise BulkheadShutDown(f'{fullname(self)} has been shutdown because too many tasks were rejected') from e
            self._rejected = x+1; raise BulkheadFull(f'{fullname(self)} queue full') from None
        if self.is_shutdown: raise BulkheadShutDown(f'{fullname(self)} is shutting down')
        async with self._sem:
            try: return await self.make(await self._queue.get())
            except (QueueEmpty, QueueShutDown, CancelledError): raise BulkheadShutDown(f'{fullname(self)} is shutting down') from None
            except self._exc as e:
                if p := self._processor: await p(e)
        getattr(self._mtevt, 'clear' if self.active_tasks else 'set')()
    async def __cleanup__(self): await self.shutdown()
    @property
    def available_slots(self): return self._sem._value
    @property
    def active_tasks(self): return self._init_val-self.available_slots
    @property
    def curr_qsize(self): return self._queue.qsize()
    @property
    def max_qsize(self): return self._queue.maxsize
    @property
    def available_qslots(self): return m-self.curr_qsize if (m := self.max_qsize) > 0 else float('inf')
    @property
    def is_available(self): return bool(self.available_slots and self.available_qslots)
    @property
    def is_shutdown(self): return self._sdevt.is_set()
    @property
    def rejected(self): return self._rejected
    def wait_until_idle(self, timeout=None): return wait_for(self._mtevt.wait(), timeout)
    async def shutdown(self, timeout=None):
        self._sdevt.set(); f, g, h = (r := []).append, (q := self._queue).get_nowait, q.shutdown; h()
        try:
            async with _timeout(timeout): await self._mtevt.wait(); await safe_cancel_batch(self.running_tasks, disembowel=True)
        except TimeoutError:
            while True:
                try: f(g())
                except: h(True); break # noqa: E722
        return r