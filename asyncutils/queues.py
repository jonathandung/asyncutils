from . import exceptions as E
from ._internal.compat import Placeholder, Queue, QueueEmpty, QueueFull, QueueShutDown, partial
from ._internal.helpers import get_loop_and_set, fullname
from ._internal.log import info
from ._internal.submodules import queues_all as __all__
from .base import collect, iter_to_aiter
from .constants import _NO_DEFAULT
from .futures import AsyncCallbacksFuture
from .mixins import EventualLoopMixin
from .util import safe_cancel, sync_await
from _collections import deque  # type: ignore[import-not-found]
from abc import ABCMeta, abstractmethod
from asyncio.locks import Event
from asyncio.tasks import gather, wait_for
from asyncio.timeouts import timeout as _timeout
from contextlib import asynccontextmanager
from itertools import count, starmap
from sys import _getframe, audit, intern
ignore_qempty, ignore_qfull = map((f := (ignore_qshutdown := E.IgnoreErrors(QueueShutDown)).combined), _ := (QueueEmpty, QueueFull))
ignore_qerrs, ignore_valerrs, f = f(*_), E.IgnoreErrors(ValueError), object.__setattr__
def _wakeup_next(W):
    P = W.popleft
    while W:
        if not (w := P()).done(): w.set_result(None); break
class Q:
    exc = E.ForbiddenOperation
    __slots__ = 'maxsize', 'empty', 'qsize', 'full', 'get', 'get_nowait', 'put', 'put_nowait', 'change_get_password', 'change_put_password', 'task_done', 'join', 'shutdown', 'cancel_extend' # noqa: RUF023
    def __repr__(self): return f'<password-protected queue at {id(self):#x}>'
    def __new__(cls, /, *a, _=f):
        s = super().__new__(cls)
        for a in zip(cls.__slots__, a): _(s, *a) # noqa: B020,PLR1704
        return s
    def __setattr__(self, name, value, /, _='cancel_extend', f=f, s=frozenset(__slots__)):
        if name not in s: raise AttributeError(f'object of type {fullname(self)!r} has no attribute {name!r}')
        if name != _: raise AttributeError(f'attribute/method {name!r} on password-protected queue is read-only')
        f(self, name, value)
    def __init_subclass__(cls, /, e=exc('subclass'), **_): raise e
    # ruff: disable[PLR6301]
    def _get(self, _=exc('call _get() on')): raise _
    def _put(self, _=exc('call _put() on')): raise _
    def _init(self, maxsize, _=exc('call _init() on')): raise _ # noqa: ARG002
    # ruff: enable[PLR6301]
def password_queue(password_put=_NO_DEFAULT, password_get=_NO_DEFAULT, maxsize=0, *, protect_get=False, protect_put=True, can_change_get=False, can_change_put=False, priority=False, lifo=False, init_items=(), strict=True, get_from='password', put_from='password', gettyp=object, puttyp=object, _=E, Q=Q): # noqa: C901,PLR0912,PLR0915
    audit('asyncutils.queues.password_queue', get_from if protect_get else None, put_from if protect_put else None)
    if protect_get:
        try:
            if password_get is _NO_DEFAULT and (password_get := (F := _getframe(1)).f_locals.get(get_from := get_from.strip(), o := object())) is o is (password_get := F.f_globals.get(get_from, o)): raise _.GetPasswordRetrievalError(get_from)
        except ValueError: raise _.GetPasswordRetrievalError(get_from) from None
        if not isinstance(password_get, gettyp): raise _.WrongPasswordType(None, type(password_get), None, gettyp)
        if isinstance(password_get, str): password_get, strict = intern(password_get), False
    if protect_put:
        try:
            if password_put is _NO_DEFAULT and (password_put := (F := _getframe(1)).f_locals.get(put_from := put_from.strip(), o := object())) is o is (password_put := F.f_globals.get(put_from, o)): raise _.PutPasswordRetrievalError(put_from)
        except ValueError: raise _.GetPasswordRetrievalError(get_from) from None
        if not isinstance(password_put, puttyp): raise _.WrongPasswordType(None, type(password_put), None, puttyp)
        if isinstance(password_put, str): password_put, strict = intern(password_put), False
    def u(pwd):
        if not protect_get: return
        if not pwd: raise _.GetPasswordMissing
        pwd, = pwd
        if not isinstance(pwd, gettyp): raise _.WrongPasswordType(pwd, type(pwd), q, gettyp)
        if pwd is not password_get and (strict or not (type(pwd) is type(password_get) and (e := pwd.__eq__(password_get)) is not NotImplemented and e)): raise _.WrongPassword(q, pwd)
    def v(pwd):
        if not protect_put: return
        if not pwd: raise _.PutPasswordMissing
        pwd, = pwd
        if not isinstance(pwd, puttyp): raise _.WrongPasswordType(pwd, type(pwd), q, puttyp)
        if pwd is not password_put and (strict or pwd != password_put): raise _.WrongPassword(q, pwd)
    (E := Event()).set(); G, P, U, S, m, b = deque(), deque(), 0, False, (L := get_loop_and_set()).create_future, object()
    if priority: l, s = [], '_max'*lifo; g, p = (partial(getattr(__import__('heapq'), f'heapp{_}{s}'), l) for _ in ('op', 'ush'))
    else: g, p = (l := []).pop if lifo else (l := deque()).popleft, l.append
    def full(): return 0 < maxsize <= len(l)
    async def get(*p, _=G.append):
        u(p)
        while not l:
            if S: raise QueueShutDown
            try: _(F := m()); await F
            except:
                F.cancel()
                with ignore_valerrs: G.remove(F)
                if l and not F.cancelled(): _wakeup_next(G)
                raise
        return get_nowait(backdoor=b)
    def get_nowait(*p, backdoor=None):
        if not l: raise QueueShutDown if S else QueueEmpty
        if backdoor is not b: u(p)
        i = g(); _wakeup_next(P); return i
    async def put(item, *p, _=P.append):
        v(p)
        while full():
            if S: raise QueueShutDown
            _(F := m())
            try: await F
            except:
                F.cancel()
                with ignore_valerrs: P.remove(F)
                if not (full() or F.cancelled()): _wakeup_next(P)
                raise
        return put_nowait(item, backdoor=b)
    def put_nowait(item, *P, backdoor=None):
        if S: raise QueueShutDown
        if full(): raise QueueFull
        if backdoor is not b: v(P)
        p(item); nonlocal U; U += 1; E.clear(); _wakeup_next(G)
    # ruff: disable[E722]
    def change_get_password(old_pwd, new_pwd):
        if not can_change_get: return False
        if not isinstance(new_pwd, gettyp): return False
        try: u(old_pwd)
        except _.CRITICAL: raise _.Critical
        except: return False
        nonlocal password_get; password_get = new_pwd; return True
    def change_put_password(old_pwd, new_pwd):
        if not can_change_put: return False
        if not isinstance(new_pwd, puttyp): return False
        try: v(old_pwd)
        except _.CRITICAL: raise _.Critical
        except: return False
        nonlocal password_put; password_put = new_pwd; return True
    # ruff: enable[E722]
    def task_done():
        nonlocal U
        if U == 0: raise ValueError('task_done() called too many times')
        U -= 1
        if U == 0: E.set()
    def shutdown(immediate=False):
        nonlocal S; S = True
        if immediate:
            nonlocal U; U -= len(l)
            if U <= 0: U = 0; E.set()
            l.clear()
        for D in (G, P):
            f = D.popleft
            while D:
                if not (F := f()).done(): F.set_result(None)
    q = Q(maxsize, lambda: not l, lambda: len(l), full, get, get_nowait, put, put_nowait, change_get_password, change_put_password, task_done, E.wait, shutdown, lambda msg=None: False) # noqa: ARG005
    if init_items:
        async def extend(f=partial(put, Placeholder, password_put)):
            async for i in iter_to_aiter(init_items): await f(i)
        q.cancel_extend = L.create_task(extend()).cancel # type: ignore[no-redef]
    return q
class PotentQueueBase(Queue, EventualLoopMixin, metaclass=ABCMeta): # noqa: PLR0904
    @abstractmethod
    def _init(self, maxsize): ...
    @abstractmethod
    def _get(self): ...
    @abstractmethod
    def _put(self, item): ...
    @abstractmethod
    def peek_all(self): ...
    @abstractmethod
    def qsize(self): ...
    def __init__(self, maxsize=0): super().__init__(maxsize); self._event = Event()
    def reset(self): super().__init__(self.maxsize); self._event.clear()
    async def smart_put(self, item, *, timeout=None, raising=True):
        try: self.put_nowait(item); return True
        except QueueFull:
            try: await wait_for(self.put(item), timeout); return False
            except TimeoutError as e:
                if raising: raise e from None
    async def smart_get(self, *, timeout=None, default=_NO_DEFAULT):
        f = default is _NO_DEFAULT
        try: return self.get_nowait()
        except QueueShutDown:
            if f: raise
            return default
        except QueueEmpty:
            try: return await wait_for(self.get(), timeout)
            except TimeoutError as e:
                if f: raise e from None
                return default
    async def extend(self, it, timeout=None):
        info(f'extending {fullname(self)} with iterable {it!r}')
        async with _timeout(timeout):
            async for i in iter_to_aiter(it): await self.smart_put(i)
    def sync_put(self, item, *, timeout=None): return sync_await(self.smart_put(item, timeout=timeout), loop=self.loop)
    def sync_get(self, *, timeout=None, default): return sync_await(self.smart_get(timeout=timeout, default=default), loop=self.loop)
    def push(self, item):
        try:
            if self.full(): audit(f'{fullname(self)}.push', id(self), item, self.get_nowait())
            self.put_nowait(item); return True
        except QueueShutDown: return False
    async def drain_persistent(self, max=None, timeout=None, _=ignore_qshutdown.combined(TimeoutError)):
        m, c = abs(max or float('inf')), 0; info(f'persistent draining of {fullname(self)} started')
        with _:
            while c < m: yield await wait_for(self.get(), timeout); self.task_done(); c += 1
    def drain_until_empty(self, max=None):
        max, c = abs(max or float('inf')), 0; info(f'draining of {fullname(self)} started')
        with ignore_qempty:
            while c < max: yield self.get_nowait(); c += 1
    def drain_retlist(self, max=None): return list(self.drain_until_empty(max))
    __iter__, __aiter__, __repr__ = drain_persistent, drain_until_empty, object.__repr__
    def shutdown(self, immediate=False): self._event.set(); super().shutdown(immediate)
    def __str__(self): return f'{fullname(self)}({self.maxsize})'
    @property
    def is_shutdown(self): return self._event.is_set()
    @is_shutdown.setter
    def is_shutdown(self, val, /): self.shutdown() if val else self.__init__(self.maxsize)
    @property
    def can_put_now(self): return not (self.is_shutdown or self.full())
    @property
    def can_get_now(self): return not (self.is_shutdown or self.empty())
    @property
    def fully_functional(self): return not (self.is_shutdown or self.full() or self.empty())
    @property
    def capacity(self): return m if (m := self.maxsize) > 0 else float('inf')
    @property
    def remaining_capacity(self): return self.capacity-self.qsize() # type: ignore
    @property
    def utilization_rate(self): return self.qsize()/self.maxsize # type: ignore
    def pushpop_nowait(self, item, raising=True):
        if self.is_shutdown:
            if raising: raise QueueShutDown
            return
        if self.empty():
            if raising: raise QueueEmpty(f'{fullname(self)}.pushpop_nowait on {item!r} expected non-empty queue with raising=True')
            return self.put_nowait(item)
        if self.full():
            if raising: raise QueueFull(f'{fullname(self)}.pushpop_nowait on {item!r} expected non-full queue with raising=True')
            r = self.get_nowait(); self.put_nowait(item); return r
        self.put_nowait(item); return self.get_nowait()
    def poppush_nowait(self, item, raising=True):
        if self.is_shutdown:
            if raising: raise QueueShutDown
            return
        if self.empty():
            if raising: raise QueueEmpty(f'{fullname(self)}.pushpop_nowait on {item!r} expected non-empty queue with raising=True')
            return self.put_nowait(item)
        r = self.get_nowait(); self.put_nowait(item); return r
    async def pushpop(self, item): await self.put(item); return await self.get()
    async def poppush(self, item): r = await self.get(); await self.put(item); return r
    def clear(self):
        with ignore_qempty:
            while True: self.get_nowait()
    @asynccontextmanager
    async def transaction(self, _=E.IgnoreErrors(TimeoutError)):
        audit((s := f'{fullname(self)}.transaction/%s')%'start', i := id(self)); q = self.peek_all()
        try: yield self
        except:
            self.clear()
            with _: await self.extend(q, 0.1)
            raise
        finally: audit(s%'end', i)
    def empty(self): return self.qsize() == 0
    def __bool__(self): return self.qsize() >= 0 # type: ignore
    def map(self, f, stop_when=None, *, lifo=False):
        audit(f'{fullname(self)}.map', id(self), fullname(f))
        if stop_when is None:
            stop_when, E = AsyncCallbacksFuture(), (QueueShutDown, QueueEmpty)
            async def get(g=self.drain_until_empty, /): # noqa: RUF029
                try:
                    for i in g(): yield i
                finally: stop_when.set_result(None)
        else:
            E = (QueueShutDown,)
            async def get(g=self.get, /):
                with ignore_qshutdown:
                    while True: yield await g()
        async def feed(q, s, g, /, f=f):
            try:
                while True: await q.put(await f(await anext(g)))
            except E: await safe_cancel(s)
        (s := AsyncCallbacksFuture(loop=self.loop)).add_noargs_async_callback(partial(safe_cancel, self.make(feed(q := (SmartLifoQueue if lifo else SmartQueue)(self.maxsize), s, get()))))
        if stop_when: stop_when.add_done_callback(s.cancel)
        return q
    def starmap(self, f, stop_when=None, *, lifo=False):
        audit(f'{fullname(self)}.starmap', id(self), fullname(f))
        if stop_when is None:
            stop_when, E = AsyncCallbacksFuture(), (QueueShutDown, QueueEmpty)
            async def get(g=self.drain_until_empty, /): # noqa: RUF029
                try:
                    for i in g(): yield i
                finally: stop_when.set_result(None)
        else:
            E = QueueShutDown,
            async def get(g=self.get, /):
                while True: yield await g()
        async def feed(q, s, g, /, f=f):
            try:
                async for _ in g: await q.put(await f(*_))
            except E: await safe_cancel(s)
        (s := AsyncCallbacksFuture(loop=self.loop)).add_noargs_async_callback(partial(safe_cancel, self.make(feed(q := (SmartLifoQueue if lifo else SmartQueue)(self.maxsize), s, get()))))
        if stop_when: stop_when.add_done_callback(s.cancel)
        return q
    def filter(self, pred=bool, *, lifo=False):
        audit(f'{fullname(self)}.filter', id(self), fullname(pred))
        q = (SmartLifoQueue if lifo else SmartQueue)(self.maxsize)
        async def feed():
            with ignore_qshutdown:
                while True: await (self if pred(i := await self.get()) else q).smart_put(i)
        self.make(feed()); return q
    def enumerate(self, *, lifo=False):
        audit(f'{fullname(self)}.enumerate', id(self))
        q = (SmartLifoQueue if lifo else SmartQueue)(self.maxsize)
        async def feed():
            i = 0
            with ignore_qempty:
                while True: await q.smart_put((i, await self.get())); i += 1
        self.make(feed()); return q
    def map_nowait(self, f, /): return self.loop.run_until_complete(gather(*map(f, self.peek_all()))) # type: ignore
    def starmap_nowait(self, f, /): return self.loop.run_until_complete(gather(*starmap(f, self.peek_all()))) # type: ignore
    def filter_nowait(self, pred=bool, /):
        f, g = (k := []).append, (r := []).append
        with ignore_qempty:
            while True: (f if pred(i := self.get_nowait()) else g)(i)
        h, j = self.put_nowait, len(r)
        for i in k:
            try: h(i)
            except QueueFull: g(i)
        return r, j
    def enumerate_nowait(self):
        i = 0
        with ignore_qempty:
            while True: yield i, self.get_nowait(); i += 1
class SmartQueue(PotentQueueBase):
    def _init(self, maxsize): self.__queue = deque(maxlen=maxsize if maxsize > 0 else None)
    def _get(self): return self.__queue.popleft()
    def _put(self, item): self.__queue.append(item)
    def peek(self):
        if q := self.__queue: return q[0]
        raise QueueEmpty
    def peek_all(self): return list(self.__queue)
    def qsize(self): return len(self.__queue)
    def rotate(self, n=1, /): self.__queue.rotate(n)
    def __bool__(self): return bool(self.__queue)
    def empty(self): return not self
class SmartLifoQueue(PotentQueueBase):
    def _init(self, maxsize): self.__queue = [] # noqa: ARG002
    def _get(self): return self.__queue.pop()
    def _put(self, item): self.__queue.append(item)
    def peek(self, i=-1, /):
        s = self.qsize()
        if i < 0: i += s
        if 0 <= i < s: return self.__queue[i]
        raise IndexError(f'failed to peek {fullname(self)} item at index {i}')
    def peek_all(self): return self.__queue.copy()
    def qsize(self): return len(self.__queue)
    def __bool__(self): return bool(self.__queue)
    def empty(self): return not self
    def pushpop(self): raise NotImplementedError
    def pushpop_nowait(self): raise NotImplementedError
class SmartPriorityQueue(PotentQueueBase):
    def __init__(self, maxsize=0, *, init_items=()): super().__init__(maxsize); self.make(self.start(maxsize, init_items))
    async def start(self, maxsize, init_items): q, n = await collect(I := iter_to_aiter(init_items), maxsize, __reti=True); import heapq as H; H.heapify(q); self.__get, self.__put, self._unfinished_tasks, self.__queue = partial(H.heappop, q), partial(H.heappush, q), n, q; self._finished.clear(); await self.extend(I) # type: ignore[attr-defined]
    def _init(self, maxsize): ...
    def _get(self): return self.__get()
    def _put(self, item): self.__put(item)
    def peek(self): return self.__queue[0]
    def peek_all(self): return self.__queue.copy()
    def qsize(self): return len(self.__queue)
    def __bool__(self): return bool(self.__queue)
    def empty(self): return not self
class UserPriorityQueue(SmartPriorityQueue):
    @classmethod
    def from_iter_of_tuples(cls, items, maxsize=0, _=SmartPriorityQueue): _.__init__(Q := object.__new__(cls), maxsize, init_items=items); Q.__tiebreak = count(); return Q
    def __init__(self, maxsize=0, *, init_items=(), init_priority=0): self.__tiebreak = count(); super().__init__(maxsize, init_items=((init_priority, self._tiebreak, j) async for j in iter_to_aiter(init_items)))
    @property
    def _tiebreak(self): return next(self.__tiebreak)
    def put_nowait(self, item, priority=0): super().put_nowait((priority, self._tiebreak, item))
    def put(self, item, priority=0): return super().put((priority, self._tiebreak, item))
    def get_nowait(self): return super().get_nowait()[-1]
    async def get(self): return (await super().get())[-1]
del E, f, _, Q