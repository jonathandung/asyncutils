from .. import __version__
if __version__.major >= 3: __import__('warnings').warn(DeprecationWarning, 'this module for python 3.12 compatibility is deprecated; you are strongly advised to upgrade to 3.15')
from .helpers import subscriptable
from collections import deque
from asyncio.locks import Event
from ..mixins import LoopBoundMixin
__all__ = 'Queue', 'QueueEmpty', 'QueueFull', 'QueueShutDown'
class QueueEmpty(Exception): ...
class QueueFull(Exception): ...
class QueueShutDown(Exception): ...
@subscriptable
class Queue(LoopBoundMixin):
    def __init__(self, maxsize=0):
        self.maxsize, self._getters, self._putters, self._unfinished_tasks, self._finished, self._is_shutdown = maxsize, deque(), deque(), 0, Event(), False
        self._finished.set(); self._init(maxsize)
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
    def full(self): return not 0 < self.qsize() < self.maxsize
    async def put(self, item):
        while self.full():
            if self._is_shutdown: raise QueueShutDown
            self._putters.append(putter := self.make_fut())
            try: await putter
            except:
                putter.cancel()
                try: self._putters.remove(putter)
                except ValueError: ...
                if not self.full() and not putter.cancelled(): self._wakeup_next(self._putters)
                raise
        return self.put_nowait(item)
    def put_nowait(self, item):
        if self._is_shutdown: raise QueueShutDown
        if self.full(): raise QueueFull
        self._put(item)
        self._unfinished_tasks += 1
        self._finished.clear()
        self._wakeup_next(self._getters)
    async def get(self):
        while self.empty():
            if self._is_shutdown and self.empty(): raise QueueShutDown
            getter = self.make_fut()
            self._getters.append(getter)
            try:
                await getter
            except:
                getter.cancel()
                try: self._getters.remove(getter)
                except ValueError: ...
                if not (self.empty() or getter.cancelled()): self._wakeup_next(self._getters)
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
            while not self.empty():
                self._get()
                if (U := self._unfinished_tasks) > 0: self._unfinished_tasks = U-1
            if U == 1: self._finished.set()
        f = (D := self._getters).popleft
        for D in (self._getters, self._putters):
            f = D.popleft
            while D:
                if not (F := f()).done(): F.set_result(None)
class LifoQueue(Queue):
    def _init(self, maxsize): self._queue = []
    def _get(self): return self._queue.pop()
    def _put(self, i, /): self._queue.append(i)