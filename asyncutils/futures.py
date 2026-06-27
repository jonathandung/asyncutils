# ty: ignore[unresolved-attribute]
from asyncutils._internal.helpers import copy_and_clear, fullname, simple_wrap
from asyncutils._internal.submodules import futures_all as __all__
from contextvars import copy_context
from asyncio.futures import Future, _PyFuture # ty: ignore[unresolved-import]
from asyncio.tasks import Task, _PyTask # ty: ignore[unresolved-import]
from sys import audit
from time import monotonic_ns
t = '_callbacks', '_async_callbacks', '_noargs_callbacks', '_noargs_async_callbacks'
def f(a, /):
    def remove_callback(self, f, /):
        if r := len(C := getattr(self, a))-len(l := tuple(t for t in C if t[0] is not f)): C[:] = l
        return r
    return remove_callback
class A:
    def __init__(self, *a, **k): super().__init__(*a, **k); self._async_callbacks, self._noargs_callbacks, self._noargs_async_callbacks = (c := self._mcb)(), c(), c()
    def add_async_callback(self, f, /, *, context=None):
        if self._state == 'PENDING': self._acb(self._async_callbacks, f, context)
        else: self._loop.create_task(simple_wrap(f(self)), context=context)
    def add_noargs_callback(self, f, /, *, context=None):
        if self._state == 'PENDING': self._acb(self._noargs_callbacks, f, context)
        else: self._loop.call_soon(f, context=context)
    def add_noargs_async_callback(self, f, /, *, context=None):
        if self._state == 'PENDING': self._acb(self._noargs_async_callbacks, f, context)
        else: self._loop.create_task(simple_wrap(f()), context=context)
    def _Future__schedule_callbacks(self): # noqa: N802
        audit(f'{fullname(self)}/schedule_callbacks', id(self)); a, b = (l := self._loop).create_task, l.call_soon; c, d, e, f = map(self._icb, (self._async_callbacks, self._callbacks, self._noargs_async_callbacks, self._noargs_callbacks))
        for g, _ in c: a(g(self), context=_)
        for g, _ in d: b(g, self, context=_)
        for g, _ in e: a(g(), context=_)
        for g, _ in f: b(g, context=_)
class B:
    def __init__(self, *a, **k): self._creation_time = monotonic_ns(); super().__init__(*a, **k)
    def __lt__(self, o, /): return self._creation_time < o._creation_time
class C(A):
    _icb, _mcb = staticmethod(copy_and_clear), list; remove_done_callback, remove_async_callback, remove_noargs_callback, remove_noargs_async_callback = map(f, t)
    @staticmethod
    def _acb(a, f, c, /): a.append((f, c or copy_context()))
class D(A):
    _mcb = dict; remove_done_callback, remove_async_callback, remove_noargs_callback, remove_noargs_async_callback = map(lambda a, /: lambda self, f, a=a, /: 0 if getattr(self, a).pop(f, None) is None else 1, t)
    @staticmethod
    def _acb(a, f, c, /): a[f] = c or copy_context()
    @staticmethod
    def _icb(d, /): return tuple(d.items())
    def __init__(self, *a, **k): super().__init__(*a, **k); self._callbacks = {}
    def add_done_callback(self, f, /, *, context=None):
        if self._state == 'PENDING': self._acb(self._callbacks, f, context)
        else: self._loop.call_soon(f, self, context=context)
class TimeAwareFuture(B, Future): ...
class TimeAwareTask(B, Task): ...
class AsyncCallbacksFuture(C, _PyFuture): ...
class AsyncCallbacksTask(C, _PyTask): ...
class TimeAwareAsyncCallbacksFuture(C, B, _PyFuture): ...
class TimeAwareAsyncCallbacksTask(C, B, _PyTask): ...
class UniqueCallbacksFuture(D, _PyFuture): ...
class UniqueCallbacksTask(D, _PyTask): ...
class TimeAwareUniqueCallbacksFuture(D, B, _PyFuture): ...
class TimeAwareUniqueCallbacksTask(D, B, _PyTask): ...
del f, t, A, B, C, D
