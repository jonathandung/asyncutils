from _collections import defaultdict, deque
from operator import index
from sys import maxsize as I
import asyncutils as A
from asyncutils._internal import helpers as H, patch as P
from asyncutils._internal.submodules import iterclasses_all as __all__
from asyncutils.constants import _NO_DEFAULT
@H.subscriptable
class AChain:
    __slots__ = '__its',
    @classmethod
    async def _flatten_it_of_its(cls, I, /):
        async for i in A.iter_to_agen(I):
            if isinstance(i, cls):
                async for _ in cls._flatten_it_of_its(i.__its): yield _
            else: yield i
    @classmethod
    def from_iterable(cls, it_of_its): (s := super().__new__(cls)).__its = cls._flatten_it_of_its(it_of_its); return s # ty: ignore[unresolved-attribute]
    def __new__(cls, *its): return cls.from_iterable(its)
    async def __aiter__(self):
        async for i in self.__its: # ty: ignore[unresolved-attribute]
            async for _ in i: yield _
@H.subscriptable
class APeekable(H.LoopMixinBase):
    __slots__ = '__ca', '__it'
    def __init__(self, it=()): self.__it, self.__ca = A.iter_to_agen(it), deque(); super().__init__()
    def __aiter__(self): return self
    async def can_peek(self):
        try: await self.peek(); return True
        except StopAsyncIteration: return False
    async def peek(self, default=_NO_DEFAULT):
        if not (c := self.__ca):
            try: c.append(await anext(self.__it))
            except StopAsyncIteration:
                if default is _NO_DEFAULT: raise
                return default
        return c[0]
    def prepend(self, /, *i): self.__ca.extendleft(reversed(i))
    async def __anext__(self):
        if (c := self.__ca): return c.popleft()
        return await anext(self.__it)
    async def __getitem__(self, i, /, _=~I):
        f = (C := self.__ca).append
        if isinstance(i, slice):
            if (c := 1 if (s := i.step) is None else int(s)) > 0: a, b = 0 if (s := i.start) is None else int(s), I if (s := i.stop) is None else int(s)
            elif c < 0: a, b = -1 if (s := i.start) is None else int(s), _ if (s := i.stop) is None else int(s)
            else: raise ValueError('asyncutils.iterclasses.APeekable: slice step cannot be zero')
            if a < 0 or b < 0:
                async for s in A.iter_to_agen(self.__it): f(s)
            elif (d := min(max(a, b)+1, I)-len(C)) >= 0:
                async for s in A.take(self.__it, d): f(s)
            return tuple(C)[a:b:c]
        if (i := index(i)) < (l := len(C)): return C[i]
        async for s in A.iter_to_agen(self.__it) if i < 0 else A.take(self.__it, i-l+1): f(s)
        return C[i]
    P.patch_method_signatures((__getitem__, 'idx, /'), (peek, 'default={}'))
@H.subscriptable
class ABucket:
    __slots__ = '__c', '__i', '__k', '__v'
    def __init__(self, it, key, validator=None): super().__init__(); self.__i, self.__k, self.__c, self.__v = A.iter_to_agen(it), key, defaultdict(deque), validator or (lambda _: True)
    async def contains(self, k, /):
        if not self.__v(k): return False
        try: i = await anext(self[k])
        except StopAsyncIteration: return False
        self.__c[k].append(i); return True
    async def __aiter__(self):
        K, V, C = self.__k, self.__v, self.__c
        async for i in self.__i:
            if V(k := K(i)): C[k].append(i)
        for k in C: yield k
    async def __getitem__(self, k, /):
        if not (V := self.__v)(k): return
        p, I, K = (a := (C := self.__c)[k]).popleft, self.__i, self.__k
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
