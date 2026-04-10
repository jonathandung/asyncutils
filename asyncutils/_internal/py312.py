from .. import __version__
if __version__.major >= 3: __import__('warnings').warn(DeprecationWarning, 'this module for python 3.12 compatibility is deprecated; you are strongly advised to upgrade to 3.15')
from .helpers import subscriptable
from ..mixins import LoopBoundMixin
import heapq as H
from _collections import deque  # type: ignore[import-not-found]
from asyncio.locks import Event
__all__ = 'LifoQueue', 'PriorityQueue', 'Queue', 'QueueEmpty', 'QueueFull', 'QueueShutDown'
class QueueEmpty(Exception): ...
class QueueFull(Exception): ...
class QueueShutDown(Exception): ...
@subscriptable
class Queue(LoopBoundMixin):
    def __init__(self, maxsize=0):
        self.maxsize, self._getters, self._putters, self._unfinished_tasks, self._is_shutdown = maxsize, deque(), deque(), 0, False
        self._finished = e = Event(); e.set(); self._init(maxsize)
    @staticmethod
    def _wakeup_next(W, /, w=None):
        while W and (w := W.popleft()).done(): ...
        if w: w.set_result(None)
    def __repr__(self): return f'<{type(self).__qualname__} at {id(self):#x} {self._format()}>'
    def __str__(self): return f'<{type(self).__qualname__} {self._format()}>'
    def _format(self):
        f = (p := [f'maxsize={self.maxsize!r}']).append
        if l := self._getters: f(f'_getters[{len(l)}]')
        if l := self._putters: f(f'_putters[{len(l)}]')
        if l := self._unfinished_tasks: f(f'tasks={l}')
        if self._is_shutdown: f('shutdown')
        return ' '.join(p)
    def _init(self, maxsize): self._queue = deque(maxsize)
    def _get(self): return self._queue.popleft()
    def _put(self, i, /): self._queue.append(i)
    def qsize(self): return len(self._queue)
    def empty(self): return not self._queue
    def full(self): return 0 < self.maxsize <= self.qsize()
    async def put(self, item):
        f, a = self.full, (P := self._putters).append
        while f():
            if self._is_shutdown: raise QueueShutDown
            a(p := self.make_fut())
            try: await p
            except:
                p.cancel()
                try: P.remove(p)
                except ValueError: ...
                if not (f() or p.cancelled()): self._wakeup_next(P)
                raise
        return self.put_nowait(item)
    def put_nowait(self, item):
        if self._is_shutdown: raise QueueShutDown
        if self.full(): raise QueueFull
        self._put(item); self._unfinished_tasks += 1; self._finished.clear(); self._wakeup_next(self._getters)
    async def get(self):
        A, e = (G := self._getters).append, self.empty
        while e():
            if self._is_shutdown: raise QueueShutDown
            A(g := self.make_fut())
            try: await g
            except:
                g.cancel()
                try: G.remove(g)
                except ValueError: ...
                if not (e() or g.cancelled()): self._wakeup_next(G)
                raise
        return self.get_nowait()
    def get_nowait(self):
        if self.empty(): raise QueueShutDown if self._is_shutdown else QueueEmpty
        r = self._get(); self._wakeup_next(self._putters); return r
    def task_done(self):
        if (U := self._unfinished_tasks) <= 0: raise ValueError('task_done() called too many times')
        self._unfinished_tasks = U-1
        if U == 1: self._finished.set()
    async def join(self):
        if self._unfinished_tasks > 0: await self._finished.wait()
    def shutdown(self, immediate=False):
        self._is_shutdown = True
        if immediate:
            g = self._get
            while not self.empty():
                g()
                if (U := self._unfinished_tasks) > 0: self._unfinished_tasks = U-1
            if U == 1: self._finished.set()
        for D in (self._getters, self._putters):
            f = D.popleft
            while D:
                if not (F := f()).done(): F.set_result(None)
class LifoQueue(Queue):
    def _init(self, maxsize): self._queue = [] # noqa: ARG002
    def _get(self): return self._queue.pop()
    def _put(self, i, /): self._queue.append(i)
class PriorityQueue(Queue):
    def _init(self, maxsize): self._queue = [] # noqa: ARG002
    def _get(self, _=H.heappop): return _(self._queue)
    def _put(self, i, /, _=H.heappush): _(self._queue, i)
del H