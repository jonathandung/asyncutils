from ._internal.helpers import copy_and_clear, fullname
from ._internal.submodules import futures_all as __all__
from _contextvars import copy_context
from asyncio.futures import Future, _PyFuture  # type: ignore[import-not-found]
from asyncio.tasks import Task, _PyTask, eager_task_factory  # type: ignore[import-not-found]
from sys import audit
class Base:
    def __init__(self): self._creation_time = self.get_loop().time() # type: ignore[attr-defined]
    def __lt__(self, other, /): return self._creation_time < other._creation_time
class TimeAwareFuture(Base, Future): ...
class TimeAwareTask(Base, Task): ...
class AsyncCallbacksFuture(_PyFuture):
    def __init__(self, *, loop=None): audit(type(self).__qualname__, loop); _PyFuture.__init__(self, loop=loop); self._setup()
    def _setup(self): self._loop.set_task_factory(eager_task_factory); self._async_callbacks, self._noargs_callbacks, self._noargs_async_callbacks = [], [], []
    def add_async_callback(self, fn, *, context=None):
        if self._state == 'PENDING': self._async_callbacks.append((fn, context or copy_context()))
        else: self._loop.create_task(fn(self))
    def add_noargs_callback(self, fn, *, context=None):
        if self._state == 'PENDING': self._noargs_callbacks.append((fn, context or copy_context()))
        else: self._loop.call_soon(fn)
    def add_noargs_async_callback(self, fn, *, context=None):
        if self._state == 'PENDING': self._noargs_async_callbacks.append((fn, context or copy_context()))
        else: self._loop.create_task(fn())
    def remove_async_callback(self, fn, /):
        if r := (len(C := self._async_callbacks)-len(l := [(f, c) for f, c in C if f is not fn])): C[:] = l
        return r
    def __schedule_callbacks(self):
        audit(f'{fullname(self)}/schedule_callbacks', id(self)); a, b = (l := self._loop).create_task, l.call_soon; c, d, e, f = map(copy_and_clear, (self._async_callbacks, self._callbacks, self._noargs_async_callbacks, self._noargs_callbacks))
        for g, _ in c: a(g(self), context=_)
        for g, _ in d: b(g, self, context=_)
        for g, _ in e: a(g(), context=_)
        for g, _ in f: b(g, context=_)
class AsyncCallbacksTask(_PyTask, AsyncCallbacksFuture):
    def __init__(self, coro, **k): audit(type(self).__qualname__, coro, k.get('loop'), k.get('name')); _PyTask.__init__(self, coro, **k); self._setup()
class TimeAwareAsyncCallbacksFuture(Base, AsyncCallbacksFuture): ...
class TimeAwareAsyncCallbacksTask(Base, AsyncCallbacksTask): ...
del Base