lazy from ._internal.helpers import copy_and_clear
from sys import audit
from asyncio.tasks import eager_task_factory, _PyTask # type: ignore[import-not-found]
from asyncio.futures import _PyFuture # type: ignore
lazy from _contextvars import copy_context
from ._internal.submodules import futures_all as __all__
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
        audit(f'asyncutils.futures.{(n := type(self).__name__)}._{n}__schedule_callbacks', self); a, b = (l := self._loop).create_task, l.call_soon; c, d, e, f = map(copy_and_clear, (self._async_callbacks, self._callbacks, self._noargs_async_callbacks, self._noargs_callbacks))
        for g, _ in c: a(g(self), context=_)
        for g, _ in d: b(g, self, context=_)
        for g, _ in e: a(g(), context=_)
        for g, _ in f: b(g, context=_)
class AsyncCallbacksTask(_PyTask, AsyncCallbacksFuture):
    def __init__(self, coro, **k): audit(type(self).__qualname__, coro, k.get('loop'), k.get('name')); _PyTask.__init__(self, coro, **k); self._setup()