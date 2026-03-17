# type: ignore
from _collections import deque
from itertools import count
from abc import ABCMeta, abstractmethod
from sys import _getframe, intern, audit
from functools import partial
from contextlib import asynccontextmanager
from asyncio.tasks import gather, wait_for
from asyncio.queues import Queue, QueueShutDown, QueueFull, QueueEmpty
from asyncio.locks import Event
from asyncio.timeouts import timeout as _timeout
from .exceptions import CRITICAL, Critical, GetPasswordRetrievalError, PutPasswordRetrievalError, ForbiddenOperation, WrongPassword, WrongPasswordType, IgnoreErrors
from .config import _NO_DEFAULT
from ._internal.log import warning, info
from .mixins import EventualLoopMixin
from .base import aiter_to_iter, iter_to_aiter, collect
from .util import sync_await, safe_cancel
from .futures import AsyncCallbacksFuture
from ._internal.helpers import _get_loop_no_exit
from ._internal.submodules import queues_all as __all__
ignore_qempty, ignore_qfull = map((f := (ignore_qshutdown := IgnoreErrors(QueueShutDown)).combined), _ := (QueueFull, QueueEmpty))
ignore_qerrs, ignore_valerrs = f(*_), IgnoreErrors(ValueError)
def password_queue(password_put=_NO_DEFAULT, password_get=_NO_DEFAULT, maxsize=0, *, protect_get=False, protect_put=True, can_change_get=False, can_change_put=False, priority=False, lifo=False, wait=False, init_items=(), raising=True, strict=True, get_from='password', put_from='password', gettyp=object, puttyp=object, log=warning, auditf=audit, _heapq=__import__('heapq')):
    auditf('asyncutils.queues.password_queue', protect_get, protect_put, get_from, put_from)
    if protect_get:
        try:
            if password_get is _NO_DEFAULT and (password_get := (F := _getframe(1)).f_locals.get(get_from := get_from.strip(), o := object())) is o is (password_get := F.f_globals.get(get_from, o)): raise GetPasswordRetrievalError(get_from)
        except ValueError: raise GetPasswordRetrievalError(get_from) from None
        if not isinstance(password_get, gettyp): raise WrongPasswordType(None, type(password_get), None, gettyp)
        if isinstance(password_get, str): password_get, strict = intern(password_get), False
        def u(pwd):
            if not isinstance(pwd, gettyp): raise WrongPasswordType(pwd, type(pwd), q, gettyp)
            if pwd is not password_get and (strict or pwd != password_get): raise WrongPassword(q, pwd)
    if protect_put:
        try:
            if password_put is _NO_DEFAULT and (password_put := (F := _getframe(1)).f_locals.get(put_from := put_from.strip(), o := object())) is o is (password_put := F.f_globals.get(put_from, o)): raise PutPasswordRetrievalError(put_from)
        except ValueError: raise GetPasswordRetrievalError(get_from) from None
        if not isinstance(password_put, puttyp): raise WrongPasswordType(None, type(password_put), None, puttyp)
        if isinstance(password_put, str): password_put, strict = intern(password_put), False
        def v(pwd):
            if not isinstance(pwd, puttyp): raise WrongPasswordType(pwd, type(pwd), q, puttyp)
            if pwd is not password_put and (strict or pwd != password_put): raise WrongPassword(q, pwd)
    class PasswordQueue(Queue):
        def _format(self): raise NotImplementedError
        if protect_get:
            async def get(self, pwd):
                u(pwd); G, f = self._getters, self._wakeup_next
                while self.empty():
                    if self._is_shutdown: raise QueueShutDown
                    G.append(F := L.create_future())
                    try: await F
                    except:
                        F.cancel()
                        with ignore_valerrs: G.remove(F)
                        if not (self.empty() or G.cancelled()): f(G)
                        raise
                return self.get_nowait(pwd)
            def get_nowait(self, pwd):
                if self.empty(): raise QueueShutDown if self._is_shutdown else QueueEmpty
                v(pwd); i = g(); self._wakeup_next(self._putters); return i
            get.__qualname__, get_nowait.__qualname__ = get.__name__, get_nowait.__name__
        if protect_put:
            async def put(self, item, pwd):
                v(pwd); P, f = self._putters, self._wakeup_next
                while self.full():
                    if self._is_shutdown: raise QueueShutDown
                    P.append(F := L.create_future())
                    try: await F
                    except:
                        F.cancel()
                        with ignore_valerrs: P.remove(F)
                        if not (self.full() or F.cancelled()): f(P)
                        raise
                return self.put_nowait(item, pwd)
            def put_nowait(self, item, pwd):
                if self._is_shutdown: raise QueueShutDown
                if self.full(): raise QueueFull
                v(pwd); p(item); self._unfinished_tasks += 1; self._finished.clear(); self._wakeup_next(self._getters)
            put.__qualname__, put_nowait.__qualname__ = put.__name__, put_nowait.__name__
        def _init(self, maxsize): ...
        def _get(self): raise ForbiddenOperation('call _get on')
        def _put(self, item): raise ForbiddenOperation('call _put with %r on', item)
        def __init_subclass__(cls): raise ForbiddenOperation('subclass')
        def __new__(cls): raise ForbiddenOperation('instantiate')
        handle = None
    if can_change_get:
        def change_get_password(old_pwd, new_pwd):
            if not isinstance(new_pwd, gettyp): return False
            try: u(old_pwd)
            except CRITICAL: raise Critical
            except: return False
            nonlocal password_get; password_get = new_pwd; return True
    else:
        def change_get_password(old_pwd, new_pwd): return bool()
    if can_change_put:
        def change_put_password(old_pwd, new_pwd):
            if not isinstance(new_pwd, puttyp): return False
            try: v(old_pwd)
            except CRITICAL: raise Critical
            except: return False
            nonlocal password_put; password_put = new_pwd; return True
    else:
        def change_put_password(old_pwd, new_pwd): return bool()
    (q := object.__new__(PasswordQueue)).__init__(maxsize); f, I, L, q.change_get_password, q.change_put_password, change_get_password.__qualname__, change_put_password.__qualname__ = partial(q.put_nowait, pwd=password_put), aiter_to_iter(init_items), _get_loop_no_exit(), change_get_password, change_put_password, change_get_password.__name__, change_put_password.__name__; PasswordQueue.__repr__ = PasswordQueue.__str__ = lambda self, _=f'<password-protected queue at {id(q):#x}>': _; g, p = map(lambda f, l=(l := []): lambda *a: f(l, *a), (_heapq.heappop_max, _heapq.heappush_max) if lifo else (_heapq.heappop, _heapq.heappush)) if priority else ((l := []).pop if lifo else (l := deque(maxlen=maxsize)).popleft, l.append); PasswordQueue.qsize, PasswordQueue.empty = lambda self, l=l: len(l), lambda self, l=l: not l
    try:
        for i in I: f(i)
    except QueueFull:
        if raising: raise
        log('not all items from init_items put into password-protected queue'); PasswordQueue.handle = F = gather(*map(partial(q.put, pwd=password_put), I)); sync_await(F) if wait else log('creating background task to put in remaining items')
    return q
class PotentQueueBase(Queue, EventualLoopMixin, metaclass=ABCMeta):
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
            except TimeoutError:
                if raising: raise
    async def smart_get(self, *, timeout=None, default=_NO_DEFAULT):
        f = default is _NO_DEFAULT
        try: return self.get_nowait()
        except QueueShutDown:
            if f: raise
            return default
        except QueueEmpty:
            try: return await wait_for(self.get(), timeout)
            except TimeoutError:
                if f: raise
                return default
    async def extend(self, it, timeout=None):
        info(f'extending {type(self).__qualname__} with iterable {it!r}')
        async with _timeout(timeout):
            async for i in iter_to_aiter(it): await self.smart_put(i)
    def sync_put(self, item, *, timeout=None): return sync_await(self.smart_put(item, timeout=timeout), loop=self.loop)
    def sync_get(self, *, timeout=None, default): return sync_await(self.smart_get(timeout=timeout, default=default), loop=self.loop)
    def push(self, item):
        try:
            if self.full(): audit(f'asyncutils.queues.{type(self).__name__}.push', item, self.get_nowait())
            self.put_nowait(item); return True
        except QueueShutDown: return False
    async def drain_persistent(self, max=None, timeout=None):
        m, c = abs(max or float('inf')), 0; info(f'persistent draining of {type(self).__qualname__} started')
        while c < m:
            try: yield await wait_for(self.get(), timeout); self.task_done(); c += 1
            except TimeoutError, QueueShutDown: break
    def drain_until_empty(self, max=None):
        max, c = abs(max or float('inf')), 0; info(f'draining of {type(self).__qualname__} started')
        while c < max:
            try: yield self.get_nowait(); c += 1
            except QueueEmpty, QueueShutDown: break
    def drain_retlist(self, max=None): return list(self.drain_until_empty(max))
    __iter__, __aiter__, __repr__ = drain_persistent, drain_until_empty, object.__repr__
    def shutdown(self, immediate=False): self._event.set(); super().shutdown(immediate)
    def __str__(self): return f'{type(self).__qualname__}({self.maxsize})'
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
    def remaining_capacity(self): return self.capacity-self.qsize()
    @property
    def utilization_rate(self): return self.qsize()/self.maxsize
    def pushpop_nowait(self, item, raising=True):
        if self.is_shutdown:
            if raising: raise QueueShutDown
            return
        if self.empty():
            if raising: raise QueueEmpty(f'{type(self).__qualname__}.pushpop_nowait expected non-empty queue')
            return self.put_nowait(item)
        if self.full():
            if raising: raise QueueFull(f'{type(self).__qualname__}.pushpop_nowait expected non-full queue')
            r = self.get_nowait(); self.put_nowait(item); return r
        self.put_nowait(item); return self.get_nowait()
    def poppush_nowait(self, item, raising=True):
        if self.is_shutdown:
            if raising: raise QueueShutDown
            return
        if self.empty():
            if raising: raise QueueEmpty(f'{type(self).__qualname__}.pushpop_nowait expected non-empty queue')
            return self.put_nowait(item)
        r = self.get_nowait(); self.put_nowait(item); return r
    async def pushpop(self, item): await self.put(item); return await self.get()
    async def poppush(self, item): r = await self.get(); await self.put(item); return r
    def clear(self) -> None:
        with ignore_qempty:
            while True: self.get_nowait()
    @asynccontextmanager
    async def transaction(self, _=IgnoreErrors(TimeoutError)):
        audit(f'{type(self).__qualname__}.transaction', self); q = self.peek_all()
        try: yield self
        except:
            self.clear()
            with _: await self.extend(q, 0.1)
            raise
    def __bool__(self): return not self.empty()
    def map(self, f, stop_when=None, *, lifo=False):
        audit(f'{type(self).__qualname__}.map', self, f)
        if stop_when is None:
            stop_when, E = AsyncCallbacksFuture(), (QueueShutDown, QueueEmpty)
            async def get(g=self.drain_until_empty, /):
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
        audit(f'{type(self).__qualname__}.starmap', self, f)
        if stop_when is None:
            stop_when, E = AsyncCallbacksFuture(), (QueueShutDown, QueueEmpty)
            async def get(g=self.drain_until_empty, /):
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
        audit(f'{type(self).__qualname__}.filter', self, pred)
        q = (SmartLifoQueue if lifo else SmartQueue)(self.maxsize)
        async def feed():
            with ignore_qshutdown:
                while True: await (self if pred(i := await self.get()) else q).smart_put(i)
        self.make(feed()); return q
    def enumerate(self, *, lifo=False):
        audit(f'{type(self).__qualname__}.enumerate', self)
        q = (SmartLifoQueue if lifo else SmartQueue)(self.maxsize)
        async def feed():
            i = 0
            with ignore_qempty:
                while True: await q.smart_put((i, await self.get())); i += 1
        self.make(feed()); return q
    def map_nowait(self, f, /): return self.loop.run_until_complete(gather(*(f(i) for i in self.peek_all())))
    def starmap_nowait(self, f, /): return self.loop.run_until_complete(gather(*(f(*i) for i in self.peek_all())))
    def filter_nowait(self, pred=bool, /):
        k, r = [], []; f, g = k.append, r.append
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
    def peek(self): return self.__queue[0]
    def peek_all(self): return list(self.__queue)
    def qsize(self): return len(self.__queue)
    def rotate(self, n=1, /): self.__queue.rotate(n)
    def __bool__(self): return bool(self.__queue)
    def empty(self): return not self
class SmartLifoQueue(PotentQueueBase):
    def _init(self, maxsize): self.__queue = []
    def _get(self): return self.__queue.pop()
    def _put(self, item): self.__queue.append(item)
    def peek(self, i=-1, /):
        s = self.qsize()
        if i < 0: i += s
        if 0 <= i < s: return self.__queue[i]
        raise IndexError(f'failed to peek {type(self).__qualname__} item at index {i}')
    def peek_all(self): return self.__queue.copy()
    def qsize(self): return len(self.__queue)
    def __bool__(self): return bool(self.__queue)
    def empty(self): return not self
    def pushpop(self): raise NotImplementedError
    def pushpop_nowait(self): raise NotImplementedError
class SmartPriorityQueue(PotentQueueBase):
    def __init__(self, maxsize=0, *, init_items=(), _heapq=__import__('heapq')): q, n = sync_await(collect(I := iter_to_aiter(init_items), maxsize, __retn=True)); _heapq.heapify(q); super().__init__(maxsize); self.__get, self.__put, self._unfinished_tasks, self.__queue = partial(_heapq.heappop, q), partial(_heapq.heappush, q), n, q; self._finished.clear(); self.make(self.extend(I))
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
    def from_iter_of_tuples(cls, items, maxsize=0, _pqimpl=SmartPriorityQueue): _pqimpl.__init__(Q := object.__new__(cls), maxsize, init_items=items); Q.__tiebreak = count(); return Q
    def __init__(self, maxsize=0, *, init_items=(), init_priority=0): self.__tiebreak = count(); super().__init__(maxsize, init_items=((init_priority, self._tiebreak, j) async for j in iter_to_aiter(init_items)))
    @property
    def _tiebreak(self): return next(self.__tiebreak)
    def put_nowait(self, item, priority=0): super().put_nowait((priority, self._tiebreak, item))
    def put(self, item, priority=0): return super().put((priority, self._tiebreak, item))
    def get_nowait(self): return super().get_nowait()[-1]
    async def get(self): return (await super().get())[-1]
del f, _