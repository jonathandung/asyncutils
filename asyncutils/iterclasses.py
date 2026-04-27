__lazy_modules__ = frozenset(('_collections', '_functools'))
from asyncutils import LoopBoundMixin, LoopContextMixin, iter_to_agen, sync_await
from asyncutils.constants import _NO_DEFAULT
from asyncutils._internal import helpers as H
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
    async def __getitem__(self, idx, /, i=~INF):
        f = (C := self._cache).append
        if isinstance(idx, slice):
            if (c := 1 if (_ := idx.step) is None else int(_)) > 0: a, b = 0 if (_ := idx.start) is None else int(_), INF if (_ := idx.stop) is None else int(_)
            elif c < 0: a, b = -1 if (_ := idx.start) is None else int(_), i if (_ := idx.stop) is None else int(_)
            else: raise ValueError('slice step cannot be zero')
            if a < 0 or b < 0:
                async for _ in iter_to_agen(self._it): f(_)
            elif (d := min(max(a, b)+1, INF)-len(C)) >= 0:
                from asyncutils import aislice as g
                async for _ in g(self._it, d): f(_)
            return tuple(C)[a:b:c]
        l, idx = len(C), int(idx)
        if idx < 0:
            async for _ in iter_to_agen(self._it): f(_)
        elif idx >= l:
            from asyncutils import aislice as s
            async for _ in s(self._it, idx-l+1): f(_)
        return C[idx]
class await_later:
    __slots__ = 'aw',
    def __new__(cls, aw, /, _=type((lambda: (yield))())): # noqa: B008,PLC3002
        if H.check_methods(aw, '__await__') or isinstance(aw, _) and aw.gi_code.co_flags&0x100: object.__setattr__(_ := super().__new__(cls), 'aw', aw); return _ # noqa: RUF021
        raise TypeError(f'{H.fullname(type(aw))} object at {id(aw):#x} is not awaitable')
    def __getattr__(self, name, /): return getattr(self.aw, name)
    def __repr__(self): return f'<proxy at {id(self):#x} to awaitable at {id(self.aw):#x}>'
    def __setattr__(self, name, /): raise AttributeError('attribute aw is read-only' if name == 'aw' else f'cannot set attribute {name!r} through proxy')
    def __init_subclass__(cls, /, **_): raise AttributeError('cannot subclass the type of proxies to awaitables')
@H.subscriptable
class abucket(LoopContextMixin):
    def __init__(self, it, key, validator): super().__init__(); self._it, self._key, self._cache, self._validator = iter_to_agen(it), key, defaultdict(deque), validator or (lambda _: True)
    def __contains__(self, v, /, _=await_later):
        if not self._validator(v): return False
        try: self._cache[v].appendleft(_(anext(self[v]))); return True
        except StopIteration: return False
    async def __aiter__(self):
        K, V, C = self._key, self._validator, self._cache
        async for i in self._it:
            if V(v := K(i)): C[v].append(i)
        for k in C: yield k
    async def __getitem__(self, v, /, a=await_later):
        if not (V := self._validator)(v): return
        C, I, K = self._cache, self._it, self._key
        while True:
            if _ := C[v]: yield (await _.aw) if isinstance(_ := _.popleft(), a) else _
            else:
                while True:
                    try: i = await anext(I)
                    except StopAsyncIteration: return
                    if (k := K(i)) == v: yield i; break
                    elif V(k): C[k].append(i)