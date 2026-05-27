# ty: ignore[unresolved-attribute]
from asyncutils import coercedmethod, getcontext, ignore_valerrs
from asyncutils._internal.submodules import rwlocks_all as __all__
from _collections import defaultdict, deque
from asyncio import Condition, Lock, current_task
from contextlib import asynccontextmanager
from _heapq import heappush, heappop
def _rwlock_sub_new(cls, /): (_ := object.__new__(cls)).setup(); return _
class B:
    __slots__ = '__wrapped__', 'reader', 'reading', 'writer', 'writing'
    def __init__(self, l, f, /, _=__slots__[1:]):
        for s in _: setattr(self, s, getattr(l, s))
        self.__wrapped__ = f
    def __init_subclass__(cls, f=__import__('_operator').methodcaller, /, *, m, **_):
        if getattr(cls, '__slots__', True): raise TypeError('__slots__ must be an empty tuple')
        c = f(m)
        async def g(self, *a, **k):
            async with c(self): return await self.__wrapped__(*a, **k)
        cls.__call__ = g; super().__init_subclass__(**_) # ty: ignore[invalid-assignment]
    def __getattr__(self, n, /): return getattr(self.__wrapped__, n)
t = 'Locked', (B,), {'__slots__': ()}
def n(c, /, prefer_writers=None): return _rwlock_sub_new(c.__subclasses__()[getcontext().RWLOCK_DEFAULT_PREFER_WRITERS if prefer_writers is None else prefer_writers])
def s(c, n=n, /, **_):
    if not isinstance(c.__dict__.get('__slots__'), tuple): raise TypeError('must define tuple as __slots__')
    if c.__new__ is n: c.__new__ = _rwlock_sub_new
    super(c).__init_subclass__(**_)
def d(c, /, _=(n, classmethod(s))): c.__new__, c.__init_subclass__ = _; return c
@d
class RWLock:
    reader, writer = (coercedmethod(type(*t, m=m)) for m in ('reading', 'writing')); __slots__ = '_wa', # ty: ignore[no-matching-overload]
    def locked(self): return self._wa
    @classmethod
    def lock(cls, f, /): return cls().reader(f)
class ReadPreferredRWLock(RWLock):
    __slots__ = '_cm', '_nr'
    def setup(self): self._nr, self._cm, self._wa = 0, Lock(), Lock()
    @asynccontextmanager
    async def reading(self):
        async with self._cm:
            if (r := self._nr+1) == 1: await self._wa.acquire()
            self._nr = r
        try: yield
        finally:
            async with self._cm:
                if (r := self._nr-1) == 0: self._wa.release()
                self._nr = r
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
    __slots__ = '_cond', '_nr', '_qd'
    def setup(self): self._cond, self._wa, self._nr, self._qd = Condition(), False, 0, deque()
    @asynccontextmanager
    async def reading(self):
        async with (C := self._cond):
            (Q := self._qd).append(E := (False, C._get_loop().create_future()))
            w = C.wait
            try:
                while True:
                    if Q[0] is not E or self._wa: await w()
                    else: self._nr += 1; Q.popleft(); E[-1].set_result(True); break
            except:
                with ignore_valerrs: Q.remove(E)
                raise
        try: yield
        finally:
            async with C:
                if (r := self._nr-1) == 0: C.notify_all()
                self._nr = r
    @asynccontextmanager
    async def writing(self):
        async with (C := self._cond):
            w = C.wait
            (Q := self._qd).append(E := (True, C._get_loop().create_future()))
            try:
                while True:
                    if Q[0] is not E or self._wa or self._nr > 0: await w()
                    else: self._wa = True; Q.popleft(); E[-1].set_result(True); break
            except:
                with ignore_valerrs: Q.remove(E)
                raise
        try: yield
        finally:
            async with C: self._wa = False; C.notify_all()
@d
class PriorityRWLock(RWLock):
    __slots__ = '_cnt', '_cond', '_il', '_nr', '_qd'
    def setup(self): self._cond, self._cnt, self._il, self._wa, self._nr, self._qd = Condition(), 0, Lock(), False, 0, []
    async def _push_item(self, priority, is_writer):
        async with self._il: self._cnt = (c := self._cnt)+1
        heappush(self._qd, E := (priority, *((is_writer, c) if isinstance(self, WritePreferredPriorityRWLock) else (c, is_writer)), self._cond._get_loop().create_future())); return E
    @asynccontextmanager
    async def reading(self, priority=0):
        async with (C := self._cond):
            E, Q, w = await self._push_item(priority, False), self._qd, C.wait
            try:
                while True:
                    if Q[0] is not E or self._wa: await w()
                    else: self._nr += 1; heappop(Q); E[-1].set_result(True); break
            except:
                with ignore_valerrs: Q.remove(E)
                raise
        try: yield
        finally:
            async with C:
                if (r := self._nr-1) == 0: C.notify_all()
                self._nr = r
    @asynccontextmanager
    async def writing(self, priority=0):
        async with (C := self._cond):
            E, Q, w = await self._push_item(priority, True), self._qd, C.wait
            try:
                while True:
                    if Q[0] is not E or self._wa or self._nr > 0: await w()
                    else: self._wa = True; heappop(Q); E[-1].set_result(True); break
            except:
                with ignore_valerrs: Q.remove(E)
                raise
        try: yield
        finally:
            async with C: self._wa = False; C.notify_all()
class FairPriorityRWLock(PriorityRWLock): __slots__ = ()
class WritePreferredPriorityRWLock(PriorityRWLock): __slots__ = ()
class AgingRWLock(PriorityRWLock):
    __slots__ = '_rf', '_rt', '_wf', '_wt'
    def __new__(cls, /, rf=None, wf=None): C, _ = getcontext(), _rwlock_sub_new(cls); _._rf, _._wf = C.AGING_RWLOCK_DEFAULT_READ_PRIORITY_FACTOR if rf is None else rf, C.AGING_RWLOCK_DEFAULT_WRITE_PRIORITY_FACTOR if wf is None else wf; return _
    def setup(self): super().setup(); self._rt, self._wt = defaultdict(int), defaultdict(int)
    @asynccontextmanager
    async def reading(self, priority=None):
        d[i] = p = (d := self._rt)[i := id(current_task())]+1
        if priority is None: priority = self._rf*p
        async with super().reading(priority): d.pop(i, None); yield
    @asynccontextmanager
    async def writing(self, priority=None):
        d[i] = p = (d := self._wt)[i := id(current_task())]+1
        if priority is None: priority = self._wf*p
        async with super().writing(priority): d.pop(i, None); yield
    @property
    def cur_unsuccessful_reads(self): return sum(self._rt.values())
    @property
    def cur_unsuccessful_writes(self): return sum(self._wt.values())
del B, t, d, n, s