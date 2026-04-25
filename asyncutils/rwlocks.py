# type: ignore
from asyncutils import coercedmethod, getcontext, ignore_valerrs
from asyncutils._internal.submodules import rwlocks_all as __all__
from _collections import deque
from asyncio.locks import Condition, Lock
from contextlib import asynccontextmanager
from _heapq import heappush, heappop
def _rwlock_sub_new(cls, /): (_ := object.__new__(cls)).setup(); return _
class Base:
    __slots__ = '__wrapped__', 'reader', 'reading', 'writer', 'writing'
    def __init__(self, l, f, /, _=__slots__[1:]):
        for s in _: setattr(self, s, getattr(l, s))
        self.__wrapped__ = f
    def __init_subclass__(cls, /, **_):
        if getattr(cls, '__slots__', True): raise TypeError('__slots__ should be empty tuple')
    def __getattr__(self, n, /): return getattr(self.__wrapped__, n)
class RWLock:
    __slots__ = '_wa',
    def __new__(cls, /, prefer_writers=None): return _rwlock_sub_new(WritePreferredRWLock if (getcontext().RWLOCK_DEFAULT_PREFER_WRITERS if prefer_writers is None else prefer_writers) else ReadPreferredRWLock)
    @coercedmethod
    class reader(Base):
        __slots__ = ()
        async def __call__(self, *a, **k):
            async with self.reading(): return await self.__wrapped__(*a, **k)
    @coercedmethod
    class writer(Base):
        __slots__ = ()
        async def __call__(self, *a, **k):
            async with self.writing(): return await self.__wrapped__(*a, **k)
    def locked(self): return self._wa
    def __init_subclass__(cls, /, **_):
        if not isinstance(getattr(cls, '__slots__', None), tuple): raise TypeError('__slots__ must be a tuple')
        if cls.__new__ is __class__.__new__: cls.__new__ = _rwlock_sub_new
        super().__init_subclass__(**_)
class ReadPreferredRWLock(RWLock):
    __slots__ = '_cm', '_readers'
    def setup(self): self._readers, self._cm, self._wa = 0, Lock(), Lock()
    @asynccontextmanager
    async def reading(self):
        async with self._cm:
            if (r := self._readers+1) == 1: await self._wa.acquire()
            self._readers = r
        try: yield
        finally:
            async with self._cm:
                if (r := self._readers-1) == 0: self._wa.release()
                self._readers = r
    @asynccontextmanager
    async def writing(self):
        async with self._wa: yield
    def locked(self): return self._wa.locked()
class WritePreferredRWLock(RWLock):
    __slots__ = '_cond', '_nr', '_nw'
    def setup(self): self._cond, self._wa = Condition(), False; self._nr = self._nw = 0
    @asynccontextmanager
    async def reading(self):
        async with (C := self._cond):
            w = C.wait
            while self._wa or self._nw > 0: await w()
            self._nr += 1
        try: yield
        finally:
            async with C:
                if (r := self._nr-1) == 0: C.notify_all()
                self._nr = r
    @asynccontextmanager
    async def writing(self):
        async with (C := self._cond):
            w = C.wait; self._nw += 1
            while self._wa or self._nr > 0: await w()
            self._nw -= 1; self._wa = True
        try: yield
        finally:
            async with C: self._wa = False; C.notify_all()
class FairRWLock(RWLock):
    __slots__ = '_cond', '_qd', '_readers'
    def setup(self): self._cond, self._wa, self._readers, self._qd = Condition(), False, 0, deque()
    @asynccontextmanager
    async def reading(self):
        async with (C := self._cond):
            F, w = C._get_loop().create_future(), C.wait
            (Q := self._qd).append(E := (False, F))
            try:
                while True:
                    if Q[0][1] is not F or self._wa: await w()
                    else: self._readers += 1; Q.popleft(); F.set_result(True); break
            except:
                with ignore_valerrs: Q.remove(E)
                raise
        try: yield
        finally:
            async with C:
                if (r := self._readers-1) == 0: C.notify_all()
                self._readers = r
    @asynccontextmanager
    async def writing(self):
        async with (C := self._cond):
            F, w = C._get_loop().create_future(), C.wait
            (Q := self._qd).append(E := (True, F))
            try:
                while True:
                    if Q[0][1] is not F or self._wa or self._readers > 0: await w()
                    else: self._wa = True; Q.popleft(); F.set_result(True); break
            except:
                with ignore_valerrs: Q.remove(E)
                raise
        try: yield
        finally:
            async with C: self._wa = False; C.notify_all()
class PriorityRWLock(RWLock):
    __slots__ = '_cnt', '_cond', '_il', '_qd', '_readers'
    def __new__(cls, /, prefer_writers=None): return _rwlock_sub_new(WritePreferredPriorityRWLock if (getcontext().RWLOCK_DEFAULT_PREFER_WRITERS if prefer_writers is None else prefer_writers) else FairPriorityRWLock)
    def __init_subclass__(cls, /, **_):
        if getattr(cls, '__slots__', None) != (): raise TypeError('__slots__ must be an empty tuple')
        cls.__new__ = _rwlock_sub_new; super().__init_subclass__(**_)
    def setup(self): self._cond, self._cnt, self._il, self._wa, self._readers, self._qd = Condition(), 0, Lock(), False, 0, []
    async def _push_item(self, priority, is_writer):
        async with self._il: self._cnt = (c := self._cnt)+1
        heappush(self._qd, E := (priority, *((is_writer, c) if isinstance(self, WritePreferredPriorityRWLock) else (c, is_writer)), self._cond._get_loop().create_future())); return E
    @asynccontextmanager
    async def reading(self, priority=0):
        async with (C := self._cond):
            F, Q, w = (E := await self._push_item(priority, False))[-1], self._qd, C.wait
            try:
                while True:
                    if Q[0][-1] is not F or self._wa: await w()
                    else: self._readers += 1; heappop(Q); F.set_result(True); break
            except:
                with ignore_valerrs: Q.remove(E)
                raise
        try: yield
        finally:
            async with C:
                if (r := self._readers-1) == 0: C.notify_all()
                self._readers = r
    @asynccontextmanager
    async def writing(self, priority=0):
        async with (C := self._cond):
            F, Q, w = (E := await self._push_item(priority, True))[-1], self._qd, C.wait
            try:
                while True:
                    if Q[0][-1] is not F or self._wa or self._readers > 0: await w()
                    else: self._wa = True; heappop(Q); F.set_result(True); break
            except:
                with ignore_valerrs: Q.remove(E)
                raise
        try: yield
        finally:
            async with C: self._wa = False; C.notify_all()
class FairPriorityRWLock(PriorityRWLock): __slots__ = ()
class WritePreferredPriorityRWLock(PriorityRWLock): __slots__ = ()
del Base