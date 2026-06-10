import asyncutils as A
from asyncutils.constants import _NO_DEFAULT
from asyncutils._internal import helpers as H, patch as P
from asyncutils._internal.submodules import iterclasses_all as __all__
from _collections import defaultdict, deque
from sys import maxsize as INF
@H.subscriptable
class achain:
    __slots__ = '__its',
    @classmethod
    def from_iterable(cls, it_of_its): (self := super().__new__(cls)).__its = A.amap(A.iter_to_agen, it_of_its); return self
    def __new__(cls, *its): return cls.from_iterable(its)
    async def __aiter__(self):
        async for i in self.__its: # ty: ignore[unresolved-attribute]
            async for _ in i: yield _
@H.subscriptable
class apeekable(H.LoopMixinBase):
    __slots__ = '__cache', '__it'
    def __init__(self, it=()): self.__it, self.__cache = A.iter_to_agen(it), deque(); super().__init__()
    def __aiter__(self): return self
    async def can_peek(self):
        try: await self.peek(); return True
        except StopAsyncIteration: return False
    async def peek(self, default=_NO_DEFAULT):
        if not (c := self.__cache):
            try: c.append(await anext(self.__it))
            except StopAsyncIteration:
                if default is _NO_DEFAULT: raise
                return default
        return c[0]
    def prepend(self, /, *i): self.__cache.extendleft(reversed(i))
    async def __anext__(self):
        if (c := self.__cache): return c.popleft()
        return await anext(self.__it)
    async def __getitem__(self, i, /, _=~INF):
        f = (C := self.__cache).append
        if isinstance(i, slice):
            if (c := 1 if (s := i.step) is None else int(s)) > 0: a, b = 0 if (s := i.start) is None else int(s), INF if (s := i.stop) is None else int(s)
            elif c < 0: a, b = -1 if (s := i.start) is None else int(s), _ if (s := i.stop) is None else int(s)
            else: raise ValueError('asyncutils.iterclasses.apeekable: slice step cannot be zero')
            if a < 0 or b < 0:
                async for s in A.iter_to_agen(self.__it): f(s)
            elif (d := min(max(a, b)+1, INF)-len(C)) >= 0:
                async for s in A.take(self.__it, d): f(s)
            return tuple(C)[a:b:c]
        async for s in A.iter_to_agen(self.__it) if (i := i.__index__()) < 0 else A.empty_agen() if i < (l := len(C)) else A.take(self.__it, i-l+1): f(s)
        return C[i]
    P.patch_method_signatures((__getitem__, 'idx, /'))
@H.subscriptable
class abucket:
    __slots__ = '__cache', '__it', '__key', '__validator'
    def __init__(self, it, key, validator=None): super().__init__(); self.__it, self.__key, self.__cache, self.__validator = A.iter_to_agen(it), key, defaultdict(deque), validator or (lambda _: True)
    async def contains(self, k, /):
        if not self.__validator(k): return False
        try: i = await anext(self[k])
        except StopAsyncIteration: return False
        self.__cache[k].append(i); return True
    async def __aiter__(self):
        K, V, C = self.__key, self.__validator, self.__cache
        async for i in self.__it:
            if V(k := K(i)): C[k].append(i)
        for k in C: yield k
    async def __getitem__(self, k, /):
        if not (V := self.__validator)(k): return
        p, I, K = (a := (C := self.__cache)[k]).popleft, self.__it, self.__key
        while True:
            if a: yield p(); continue
            while True:
                try: i = await anext(I)
                except StopAsyncIteration:
                    if not a: del C[k]
                    return
                if (c := K(i)) == k: yield i; break
                elif V(c): C[c].append(i)
del P
