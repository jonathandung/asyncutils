__lazy_modules__ = frozenset(('_collections', '_functools'))
from asyncutils import LoopBoundMixin, LoopContextMixin, dummy_task, take, iter_to_agen, sync_await
from asyncutils.constants import _NO_DEFAULT
from asyncutils._internal import helpers as H, patch as P
from asyncutils._internal.submodules import iterclasses_all as __all__
from _collections import defaultdict, deque # type: ignore[import-not-found]
from sys import maxsize as INF
@H.subscriptable
class achain:
    __slots__ = '_its',
    @classmethod
    def from_iterable(cls, it_of_its): (self := super().__new__(cls))._its = it_of_its; return self
    def __new__(cls, *its): return cls.from_iterable(its)
    async def __aiter__(self):
        async for i in iter_to_agen(self._its):
            async for _ in iter_to_agen(i): yield _
@H.subscriptable
class apeekable(LoopBoundMixin):
    __slots__ = '_cache', '_it'
    def __init__(self, it=()): self._it, self._cache = iter_to_agen(it), deque(); super().__init__()
    def __aiter__(self): return self
    def __bool__(self):
        try: sync_await(self.peek(), loop=self.loop); return True
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
    async def __getitem__(self, i, /, _=~INF):
        f = (C := self._cache).append
        if isinstance(i, slice):
            if (c := 1 if (s := i.step) is None else int(s)) > 0: a, b = 0 if (s := i.start) is None else int(s), INF if (s := i.stop) is None else int(s)
            elif c < 0: a, b = -1 if (s := i.start) is None else int(s), _ if (s := i.stop) is None else int(s)
            else: raise ValueError('slice step cannot be zero')
            if a < 0 or b < 0:
                async for s in iter_to_agen(self._it): f(s)
            elif (d := min(max(a, b)+1, INF)-len(C)) >= 0:
                async for s in take(self._it, d): f(s)
            return tuple(C)[a:b:c]
        l, i = len(C), int(i)
        if i < 0:
            async for s in iter_to_agen(self._it): f(s)
        elif i >= l:
            async for s in take(self._it, i-l+1): f(s)
        return C[i]
    P.patch_method_signatures((__getitem__, 'idx, /'))
class await_later:
    __slots__ = 'aw',
    def __new__(cls, a, /, _=type(dummy_task)):
        if H.check_methods(a, '__await__') or isinstance(a, _) and a.gi_code.co_flags&0x100: object.__setattr__(_ := super().__new__(cls), 'aw', a); return _ # noqa: RUF021
        raise TypeError(f'{H.fullname(a)} object at {id(a):#x} is not awaitable')
    def __getattr__(self, n, /): return getattr(self.aw, n)
    def __repr__(self): return f'<proxy at {id(self):#x} to awaitable at {id(self.aw):#x}>'
    def __setattr__(self, n, /): raise AttributeError('attribute aw is read-only' if n == 'aw' else f'cannot set attribute {n!r} through proxy')
    def __init_subclass__(cls, /, **_): raise AttributeError('cannot subclass the type of proxies to awaitables')
    P.patch_classmethod_signatures((__new__, 'aw, /'))
@H.subscriptable
class abucket(LoopContextMixin):
    def __init__(self, it, key, validator): super().__init__(); self._it, self._key, self._cache, self._validator = iter_to_agen(it), key, defaultdict(deque), validator or (lambda _: True)
    def __contains__(self, k, /, _=await_later):
        if not self._validator(k): return False
        try: self._cache[k].appendleft(_(anext(self[k]))); return True
        except StopIteration: return False
    async def __aiter__(self):
        K, V, C = self._key, self._validator, self._cache
        async for i in self._it:
            if V(v := K(i)): C[v].append(i)
        for k in C: yield k
    async def __getitem__(self, v, /, _=await_later):
        if not (V := self._validator)(v): return
        C, I, K = self._cache, self._it, self._key
        while True:
            if a := C[v]: yield (await a.aw) if isinstance(a := a.popleft(), _) else a
            else:
                while True:
                    try: i = await anext(I)
                    except StopAsyncIteration: return
                    if (k := K(i)) == v: yield i; break
                    elif V(k): C[k].append(i)
    P.patch_method_signatures((__contains__, _ := 'key, /'), (__getitem__, _)); del _
del P, await_later, dummy_task