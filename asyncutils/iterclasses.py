from .base import aiter_to_iter, iter_to_aiter
from .mixins import EventualLoopMixin, LoopContextMixin
from .config import Executor, _NO_DEFAULT
from ._internal.helpers import _get_loop_no_exit, subscriptable
from sys import maxsize as INF, audit
from functools import partial, singledispatchmethod
from _collections import deque, defaultdict
from heapq import heapify, heappop, heappushpop
from ._internal.submodules import iterclasses_all as __all__
class anullcontext:
    async def __aenter__(self): ...
    async def __aexit__(*_): ...
@subscriptable
class achain:
    __slots__ = 'its'
    @classmethod
    def from_iterable(cls, it): return cls(*aiter_to_iter(it))
    def __init__(self, *its): self.its = its
    async def __aiter__(self):
        for i in self.its:
            async for _ in iter_to_aiter(i): yield _
@subscriptable
class apeekable(EventualLoopMixin):
    def __init__(self, it): self._it, self._cache = iter_to_aiter(it), deque(); super().__init__()
    def __aiter__(self): return self
    def __bool__(self):
        try: self.loop.run_until_complete(self.peek()); return True
        except StopAsyncIteration: return False
    async def peek(self, default=_NO_DEFAULT):
        if not (c := self._cache):
            try: c.append(await anext(self._it))
            except StopAsyncIteration:
                if default is _NO_DEFAULT: raise
                return default
        return c[0]
    def prepend(self, /, *i): self._cache.extendleft(reversed(i))
    async def __anext__(self):
        if (c := self._cache): return c.popleft()
        return await anext(self._it)
    @singledispatchmethod
    def __getitem__(self, idx, /): raise TypeError(f'cannot get item from {type(self).__qualname__} for index {idx!r}')
    @__getitem__.register(slice)
    def _(self, s, /, i=~INF):
        if (c := 1 if (_ := s.step) is None else _) > 0: a, b = 0 if (_ := s.start) is None else _, INF if (_ := s.stop) is None else _
        elif c < 0: a, b = -1 if (_ := s.start) is None else _, i if (_ := s.stop) is None else _
        else: raise ValueError('slice step cannot be zero')
        C = self._cache
        if a < 0 or b < 0: C.extend(aiter_to_iter(self._it))
        elif (d := min(max(a, b)+1, INF)-len(C)) >= 0: from .iters import aislice as s; C.extend(aiter_to_iter(s(self._it, d)))
        return tuple(C)[s]
    @__getitem__.register(int)
    def _(self, i, /):
        l = len(c := self._cache)
        if i < 0: c.extend(aiter_to_iter(self._it))
        elif i >= l: from .iters import aislice as s; c.extend(aiter_to_iter(s(self._it, i-l+1)))
        return c[i]
@subscriptable
class abucket(LoopContextMixin):
    def __init__(self, it, key, validator): super().__init__(); self._it, self._key, self._cache, self._validator = iter_to_aiter(it), key, defaultdict(deque), validator or (lambda _: True)
    def __contains__(self, v):
        if not self._validator(v): return False
        try: self._cache[v].appendleft(self.loop.run_until_complete(anext(self[v]))); return True
        except StopIteration: return False
    async def __aiter__(self):
        async for i in self._it:
            if self._validator(v := self._key(i)): self._cache[v].append(i)
        for k in self._cache: yield k
    async def __getitem__(self, val, /):
        if not self._validator(val): return
        while True:
            if (_ := self._cache[val]): yield _.popleft()
            else:
                while True:
                    try: i = await anext(self._it)
                    except StopAsyncIteration: return
                    if (v := self._key(i)) == val: yield i; break
                    elif self._validator(v): self._cache[v].append(i)
@subscriptable
class OnlineSorter:
    __slots__ = '_it', '_runner', '_popper', '_pusher'
    def __init__(self, it): audit('asyncutils/create_executor', 'iterclasses.OnlineSorter'); self._it, self._runner = aiter_to_iter(it), partial(type(l := _get_loop_no_exit()).run_in_executor, l, Executor())
    def __aiter__(self):
        if not hasattr(self, '_popper'): h = list(self._it); heapify(h); self._popper, self._pusher = partial(heappop, h), partial(heappushpop, h)
        return self
    def __anext__(self): return self._runner(self._popper)
    def asend(self, item): return self._runner(self._pusher, item)
    def athrow(self, typ, val=None, tb=None): return self._runner(self._it.throw, typ, val, tb)
    def aclose(self): r = self._runner(self._it.close); del self._it, self._runner, self._popper, self._pusher; return r