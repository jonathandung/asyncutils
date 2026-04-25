__lazy_modules__ = frozenset(('_contextvars', 'asyncutils._internal.helpers'))
from asyncutils._internal.helpers import copy_and_clear, fullname
from asyncutils._internal.submodules import futures_all as __all__
from _contextvars import copy_context
from asyncio.futures import Future, _PyFuture # type: ignore[import-not-found]
from asyncio.tasks import Task, _PyTask, eager_task_factory # type: ignore[import-not-found]
from sys import audit
class FB:
    def __init__(self): self._creation_time = self.get_loop().time() # type: ignore[attr-defined]
    def __lt__(self, other, /): return self._creation_time < other._creation_time
class TimeAwareFuture(FB, Future): ...
class TimeAwareTask(FB, Task): ...
def ff(a):
    def remove_callback(self, fn, /):
        if r := len(C := getattr(self, a))-len(l := [(f, c) for f, c in C if f is not fn]): C[:] = l
        return r
    return remove_callback
class AsyncCallbacksFuture(_PyFuture):
    def __init__(self, *, loop=None): _PyFuture.__init__(self, loop=loop); self._setup()
    def _setup(self): self._async_callbacks, self._noargs_callbacks, self._noargs_async_callbacks = [], [], []
    def add_async_callback(self, fn, /, *, context=None):
        if self._state == 'PENDING': self._async_callbacks.append((fn, context or copy_context()))
        else: self._loop.create_task(fn(self))
    def add_noargs_callback(self, fn, /, *, context=None):
        if self._state == 'PENDING': self._noargs_callbacks.append((fn, context or copy_context()))
        else: self._loop.call_soon(fn)
    def add_noargs_async_callback(self, fn, /, *, context=None):
        if self._state == 'PENDING': self._noargs_async_callbacks.append((fn, context or copy_context()))
        else: self._loop.create_task(fn())
    remove_async_callback, remove_noargs_callback, remove_noargs_async_callback = map(ff, ('_async_callbacks', '_noargs_callbacks', '_noargs_async_callbacks'))
    def __schedule_callbacks(self):
        audit(f'{fullname(self)}/schedule_callbacks', id(self)); a, b = (l := self._loop).create_task, l.call_soon; c, d, e, f = map(copy_and_clear, (self._async_callbacks, self._callbacks, self._noargs_async_callbacks, self._noargs_callbacks))
        for g, _ in c: a(g(self), context=_)
        for g, _ in d: b(g, self, context=_)
        for g, _ in e: a(g(), context=_)
        for g, _ in f: b(g, context=_)
class AsyncCallbacksTask(_PyTask, AsyncCallbacksFuture):
    def __init__(self, coro, **k): _PyTask.__init__(self, coro, **k); self._setup()
class EagerAsyncCallbacksFuture(AsyncCallbacksFuture):
    def _setup(self): self._loop.set_task_factory(eager_task_factory); super()._setup()
class EagerAsyncCallbacksTask(AsyncCallbacksTask, EagerAsyncCallbacksFuture): ...
class TimeAwareAsyncCallbacksFuture(FB, AsyncCallbacksFuture): ...
class TimeAwareAsyncCallbacksTask(FB, AsyncCallbacksTask): ...
class EagerTimeAwareAsyncCallbacksFuture(TimeAwareAsyncCallbacksFuture, EagerAsyncCallbacksFuture): ...
class EagerTimeAwareAsyncCallbacksTask(TimeAwareAsyncCallbacksTask, EagerAsyncCallbacksTask): ...
del FB, ff