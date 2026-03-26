from .mixins import EventualLoopMixin, LoopContextMixin
lazy from .base import iter_to_aiter
lazy from .config import Executor
from .constants import _NO_DEFAULT
from ._internal import helpers as H
from sys import maxsize as INF, audit
lazy from _functools import partial # type: ignore[import-not-found]
lazy from _collections import deque, defaultdict # type: ignore[import-not-found]
lazy import heapq as Q
from ._internal.submodules import iterclasses_all as __all__
class anullcontext:
    async def __aenter__(self): ...
    async def __aexit__(*_): ...
@H.subscriptable
class achain:
    __slots__ = 'its'
    @classmethod
    def from_iterable(cls, it_of_its): (self := super().__new__(cls)).its = it_of_its; return self
    def __new__(cls, *its): return cls.from_iterable(its)
    async def __aiter__(self):
        async for i in iter_to_aiter(self.its):
            async for _ in iter_to_aiter(i): yield _
@H.subscriptable
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
    async def __getitem__(self, idx, /, i=~INF):
        f = (C := self._cache).append
        if isinstance(idx, slice):
            if (c := 1 if (_ := idx.step) is None else int(_)) > 0: a, b = 0 if (_ := idx.start) is None else int(_), INF if (_ := idx.stop) is None else int(_)
            elif c < 0: a, b = -1 if (_ := idx.start) is None else int(_), i if (_ := idx.stop) is None else int(_)
            else: raise ValueError('slice step cannot be zero')
            if a < 0 or b < 0:
                async for _ in iter_to_aiter(self._it): f(_)
            elif (d := min(max(a, b)+1, INF)-len(C)) >= 0:
                from .iters import aislice as g
                async for _ in g(self._it, d): f(_)
            return tuple(C)[a:b:c]
        l, idx = len(C), int(idx)
        if idx < 0:
            async for _ in iter_to_aiter(self._it): f(_)
        elif idx >= l:
            from .iters import aislice as s
            async for _ in s(self._it, idx-l+1): f(_)
        return C[idx]
class _await_later:
    __slots__ = 'aw'
    def __new__(cls, aw, /, _=type((lambda: (yield))())):
        if H.check_methods(aw, '__await__') or isinstance(aw, _) and aw.gi_code.co_flags&0x100: object.__setattr__(_ := super().__new__(cls), 'aw', aw); return _
        raise TypeError(f'{type(aw).__qualname__!r} object at {id(aw):#x} is not awaitable')
    def __getattr__(self, name, /): return getattr(self.aw, name)
    def __repr__(self): return f'<proxy at {id(self):#x} for awaitable at {id(self.aw):#x}>'
    def __setattr__(self, name, /): raise AttributeError('attribute aw is read-only' if name == 'aw' else f'cannot set attribute {name!r} through proxy')
    def __init_subclass__(cls, /, **_): raise AttributeError('cannot subclass type of awaitable proxy')
@H.subscriptable
class abucket(LoopContextMixin):
    def __init__(self, it, key, validator): super().__init__(); self._it, self._key, self._cache, self._validator = iter_to_aiter(it), key, defaultdict(deque), validator or (lambda _: True)
    def __contains__(self, v):
        if not self._validator(v): return False
        try: self._cache[v].appendleft(_await_later(anext(self[v]))); return True
        except StopIteration: return False
    async def __aiter__(self):
        async for i in self._it:
            if self._validator(v := self._key(i)): self._cache[v].append(i)
        for k in self._cache: yield k
    async def __getitem__(self, val, /):
        if not self._validator(val): return
        while True:
            if (_ := self._cache[val]): yield (await _.aw) if isinstance(_ := _.popleft(), _await_later) else _
            else:
                while True:
                    try: i = await anext(self._it)
                    except StopAsyncIteration: return
                    if (v := self._key(i)) == val: yield i; break
                    elif self._validator(v): self._cache[v].append(i)
@H.subscriptable
class OnlineSorter:
    __slots__ = '_it', '_runner', '_popper', '_pusher', '_loop'
    def __init__(self, it): audit('asyncutils/create_executor', 'iterclasses.OnlineSorter'); self._it, self._runner, self._loop = it, partial(type(l := H.get_loop_and_set()).run_in_executor, l, Executor()), l
    def __aiter__(self):
        from .iters import to_list
        if not hasattr(self, '_popper'): h = self._loop.run_until_complete(to_list(self._it)); Q.heapify(h); self._popper, self._pusher = partial(Q.heappop, h), partial(Q.heappushpop, h)
        return self
    async def __anext__(self): return await self._runner(self._popper)
    async def asend(self, item): return await self._runner(self._pusher, item)
    async def athrow(self, typ, val=None, tb=None): return await self._runner(self._it.throw, typ, val, tb)
    async def aclose(self): r = self._runner(self._it.close); del self._it, self._runner, self._popper, self._pusher, self._loop; return await r