# ty: ignore[invalid-argument-type]
import asyncutils as A
from asyncutils.constants import _NO_DEFAULT
from asyncutils._internal import compat as D, patch as P
from asyncutils._internal.helpers import LoopMixinBase, check, get_loop_and_set, fullname
from asyncutils._internal.log import info
from asyncutils._internal.submodules import queues_all as __all__
from _collections import deque
from _functools import partial
from abc import ABCMeta, abstractmethod
from asyncio import Event, timeout as _timeout, wait_for
from itertools import count
from sys import _getframe, audit
ignore_qempty, ignore_qfull = map((f := (ignore_qshutdown := A.IgnoreErrors(D.QueueShutDown)).combined), _ := (D.QueueEmpty, D.QueueFull))
ignore_qerrs, f = f(*_), object.__setattr__
def _wakeup_next(W):
    P = W.popleft
    while W:
        if not (w := P()).done(): w.set_result(None); break
class Q:
    exc = A.ForbiddenOperation; __slots__ = 'maxsize', 'empty', 'qsize', 'full', 'get', 'get_nowait', 'put', 'put_nowait', 'change_get_password', 'change_put_password', 'task_done', 'join', 'shutdown', 'cancel_extend' # noqa: RUF023
    def __repr__(self): return f'<password-protected queue at {id(self):#x}>'
    def __new__(cls, /, *a, _=f.__get__, x='pwdq.'):
        (f := _(s := super().__new__(cls)))(*next(i := zip(cls.__slots__, a)))
        for n, v in i: v.__qualname__ = x+n; f(n, v)
        return s
    def __setattr__(self, name, value, /, _=__slots__[-1], f=f, s=frozenset(__slots__)):
        if name not in s: raise AttributeError(f'password-protected queue has no attribute {name!r}')
        if name != _: raise AttributeError(f'attribute/method {name!r} on password-protected queue is read-only')
        f(self, name, value)
    def __init_subclass__(cls, /, _=exc('subclass'), **k): raise _
    def _get(self, _=exc('call _get() on')): raise _
    def _put(self, _=exc('call _put() on')): raise _
    def _init(self, maxsize, _=exc('call _init() on')): raise _
    P.patch_method_signatures((__setattr__, 'name, value, /'), (_get, ''), (_put, ''), (_init, 'maxsize')); P.patch_classmethod_signatures((__init_subclass__, '**k'), (__new__, 'maxsize, empty, qsize, full, get, get_nowait, put, put_nowait, change_get_password, change_put_password, task_done, join, shutdown, cancel_extend, /'))
def password_queue(password_put=_NO_DEFAULT, password_get=_NO_DEFAULT, maxsize=0, *, protect_get=False, protect_put=True, can_change_get=False, can_change_put=False, priority=False, lifo=False, init_items=(), strict=True, get_from=None, put_from=None, gettyp=object, puttyp=object, _=Q): # noqa: C901,PLR0913,PLR0915
    audit('asyncutils.queues.password_queue', get_from if protect_get else None, put_from if protect_put else None); C = A.getcontext()
    try: F = _getframe(1)
    except ValueError: F = None
    if protect_get:
        if password_get is _NO_DEFAULT:
            if F is None or (password_get := F.f_locals.get(get_from := (C.PASSWORD_QUEUE_DEFAULT_GET_FROM if get_from is None else get_from).strip())) is None is (password_get := F.f_globals.get(get_from)): raise A.GetPasswordRetrievalError(get_from)
        elif get_from is not None: raise ValueError('asyncutils.queues.password_queue: only pass one of get_from or password_get')
        if not isinstance(password_get, gettyp): raise A.WrongPasswordType(None, password_get, type(password_get), gettyp)
    if protect_put:
        if password_put is _NO_DEFAULT:
            if F is None or (password_put := F.f_locals.get(put_from := (C.PASSWORD_QUEUE_DEFAULT_PUT_FROM if put_from is None else put_from).strip())) is None is (password_put := F.f_globals.get(put_from)): raise A.PutPasswordRetrievalError(put_from)
        elif put_from is not None: raise ValueError('asyncutils.queues.password_queue: only pass one of put_from or password_put')
        if not isinstance(password_put, puttyp): raise A.WrongPasswordType(None, password_put, type(password_put), puttyp)
    def s(p):
        if not isinstance(p, gettyp): raise A.WrongPasswordType(q, p, type(p), gettyp)
        if p is not password_get and (strict or not check(p, password_get)): raise A.WrongPassword(q, p)
    def t(p):
        if not isinstance(p, puttyp): raise A.WrongPasswordType(q, p, type(p), puttyp)
        if p is not password_put and (strict or not check(p, password_put)): raise A.WrongPassword(q, p)
    def u(p):
        if not protect_get: return
        if not p: raise A.GetPasswordMissing
        p, = p; s(p)
    def v(p):
        if not protect_put: return
        if not p: raise A.PutPasswordMissing
        p, = p; t(p)
    E, G, P, U, S, m, b = A.done_evt(), deque(), deque(), 0, False, (L := get_loop_and_set()).create_future, object()
    if priority: g, p = partial((M := D if lifo else __import__('heapq')).heappop, l := []), partial(M.heappush, l)
    else: g, p = (l := []).pop if lifo else (l := deque()).popleft, l.append
    async def get(*p):
        u(p); _ = G.append
        while not l:
            if S: raise D.QueueShutDown
            F = m()
            try: _(F); await F
            except:
                F.cancel()
                with A.ignore_valerrs: G.remove(F)
                if l and not F.cancelled(): _wakeup_next(G)
                raise
        return get_nowait(_=b)
    def get_nowait(*p, _=None):
        if not l: raise D.QueueShutDown if S else D.QueueEmpty
        if _ is not b: u(p)
        i = g(); _wakeup_next(P); return i
    async def put(i, /, *p):
        v(p); _ = P.append
        while full():
            if S: raise D.QueueShutDown
            _(F := m())
            try: await F
            except:
                F.cancel()
                with A.ignore_valerrs: P.remove(F)
                if not (full() or F.cancelled()): _wakeup_next(P)
                raise
        return put_nowait(i, _=b)
    def put_nowait(i, /, *P, _=None):
        if S: raise D.QueueShutDown
        if full(): raise D.QueueFull
        if _ is not b: v(P)
        p(i); nonlocal U; U += 1; E.clear(); _wakeup_next(G)
    def change_get_password(opw, npw):
        if (S and not l) or not can_change_get: return False
        if not isinstance(npw, gettyp): return False
        try: s(opw)
        except A.CRITICAL: raise A.Critical
        except: return False
        nonlocal password_get; password_get = npw; return True
    def change_put_password(opw, npw):
        if S or not can_change_put: return False
        if not isinstance(npw, puttyp): return False
        try: t(opw)
        except A.CRITICAL: raise A.Critical
        except: return False
        nonlocal password_put; password_put = npw; return True
    def task_done():
        nonlocal U
        if U == 0: raise ValueError('task_done() called too many times')
        U -= 1
        if U == 0: E.set()
    def shutdown(immediate=False):
        nonlocal S, U; S = True
        if immediate:
            U -= len(l)
            if U <= 0: U = 0; E.set()
            l.clear()
        for d in (G, P):
            f = d.popleft
            while d:
                if not (F := f()).done(): F.set_result(None)
    q = _(maxsize, lambda: not l, lambda: len(l), full := lambda: 0 < maxsize <= len(l), get, get_nowait, put, put_nowait, change_get_password, change_put_password, task_done, A.discard_retval(E.wait), shutdown, lambda msg=None: False) # noqa: ARG005
    if init_items:
        async def extend(f=D.partial(put, D.Placeholder, password_put)):
            async for i in A.iter_to_agen(init_items): await f(i)
        q.cancel_extend = L.create_task(extend()).cancel
    return q
class PotentQueueBase(D.Queue, LoopMixinBase, metaclass=ABCMeta):
    @abstractmethod
    def _init(self, maxsize): raise NotImplementedError
    @abstractmethod
    def _get(self): raise NotImplementedError
    @abstractmethod
    def _put(self, item): raise NotImplementedError
    @abstractmethod
    def peek_all(self): raise NotImplementedError
    @abstractmethod
    def qsize(self): raise NotImplementedError
    def __init__(self, maxsize=0): super().__init__(maxsize); self._event = Event()
    def reset(self): super().__init__(self.maxsize); self._event.clear()
    async def smart_put(self, item, *, timeout=None, raising=True):
        try: self.put_nowait(item); return True
        except D.QueueFull: ...
        try: await wait_for(self.put(item), timeout); return False
        except TimeoutError:
            if raising: raise
    async def smart_get(self, *, timeout=None, default=_NO_DEFAULT):
        f = default is _NO_DEFAULT
        try: return self.get_nowait()
        except D.QueueShutDown:
            if f: raise
            return default
        except D.QueueEmpty:
            try: return await wait_for(self.get(), timeout)
            except TimeoutError as e:
                if f: raise e from None
                return default
    async def extend(self, it, timeout=None):
        info(f'extending {fullname(self)} with iterable {it!r}'); f = self.smart_put
        async with _timeout(timeout):
            async for i in A.iter_to_agen(it): await f(i)
    def push(self, item):
        try:
            if self.full(): audit(f'{fullname(self)}.push', id(self), item, self.get_nowait())
            self.put_nowait(item); return True
        except D.QueueShutDown: return False
    async def drain_persistent(self, max_items=None, timeout=None, _=ignore_qshutdown.combined(TimeoutError)):
        m, c = abs(max_items or float('inf')), 0; info(f'persistent draining of {fullname(self)} started')
        with _:
            while c < m: yield await wait_for(self.get(), timeout); self.task_done(); c += 1 # noqa: ASYNC119
    def drain_until_empty(self, max_items=None):
        max_items, c = abs(max_items or float('inf')), 0; info(f'draining of {fullname(self)} started')
        with ignore_qempty:
            while c < max_items: yield self.get_nowait(); c += 1
    def drain_retlist(self, max_items=None): return list(self.drain_until_empty(max_items))
    __iter__, __aiter__ = drain_persistent, drain_until_empty
    def shutdown(self, immediate=False): self._event.set(); super().shutdown(immediate)
    def __repr__(self): return f'{fullname(self)}({self.maxsize})'
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
        if self.is_shutdown: raise D.QueueShutDown
        if self.empty():
            if raising: raise D.QueueEmpty(f'{fullname(self)}.pushpop_nowait on {item!r} expected non-empty queue with raising=True')
            return self.put_nowait(item)
        if self.full():
            if raising: raise D.QueueFull(f'{fullname(self)}.pushpop_nowait on {item!r} expected non-full queue with raising=True')
            r = self.get_nowait(); self.put_nowait(item); return r
        self.put_nowait(item); return self.get_nowait()
    def poppush_nowait(self, item, raising=True):
        if self.is_shutdown: raise D.QueueShutDown
        if self.empty():
            if raising: raise D.QueueEmpty(f'{fullname(self)}.pushpop_nowait on {item!r} expected non-empty queue with raising=True')
            return self.put_nowait(item)
        r = self.get_nowait(); self.put_nowait(item); return r
    async def pushpop(self, item): await self.put(item); return await self.get()
    async def poppush(self, item): r = await self.get(); await self.put(item); return r
    def clear(self):
        with ignore_qempty:
            while True: self.get_nowait()
    @A.dualcontextmanager
    def transaction(self, _=A.IgnoreErrors(TimeoutError)):
        audit((s := f'{fullname(self)}.transaction/%s')%'start', i := id(self)); q = self.peek_all()
        try: yield self
        except:
            self.clear(); f = self.put_nowait
            for _ in q: f(_)
            raise
        finally: audit(s%'end', i)
    def empty(self): return self.qsize() == 0
    def __bool__(self): return self.qsize() >= 0
    def map(self, f, stop_when=None, *, lifo=False):
        audit(f'{fullname(self)}.map', id(self), fullname(f))
        if stop_when is None:
            stop_when, E = A.AsyncCallbacksFuture(), (D.QueueShutDown, D.QueueEmpty)
            async def get(g=self.drain_until_empty, /): # noqa: RUF029
                try:
                    for i in g(): yield i
                finally: stop_when.set_result(None)
        else:
            E = (D.QueueShutDown,)
            async def get(g=self.get, /):
                with ignore_qshutdown:
                    while True: yield await g() # noqa: ASYNC119
        async def feed(q, s, g, /, f=f):
            try:
                while True: await q.put(await f(await anext(g)))
            except E: await A.safe_cancel(s)
        (s := A.AsyncCallbacksFuture(loop=self.loop)).add_noargs_async_callback(partial(A.safe_cancel, self.make(feed(q := (SmartLifoQueue if lifo else SmartQueue)(self.maxsize), s, get()))))
        if stop_when: stop_when.add_done_callback(s.cancel)
        return q
    def starmap(self, f, stop_when=None, *, lifo=False):
        audit(f'{fullname(self)}.starmap', id(self), fullname(f))
        if stop_when is None:
            stop_when, E = A.AsyncCallbacksFuture(), (D.QueueShutDown, D.QueueEmpty)
            async def get(g=self.drain_until_empty, /): # noqa: RUF029
                try:
                    for i in g(): yield i
                finally: stop_when.set_result(None)
        else:
            E = D.QueueShutDown,
            async def get(g=self.get, /):
                while True: yield await g()
        async def feed(q, s, g, /, f=f):
            try:
                async for _ in g: await q.put(await f(*_))
            except E: await A.safe_cancel(s)
        (s := A.AsyncCallbacksFuture(loop=self.loop)).add_noargs_async_callback(partial(A.safe_cancel, self.make(feed(q := (SmartLifoQueue if lifo else SmartQueue)(self.maxsize), s, get()))))
        if stop_when: stop_when.add_done_callback(s.cancel)
        return q
    def filter(self, pred=bool, *, lifo=False):
        audit(f'{fullname(self)}.filter', id(self), fullname(pred))
        q = (SmartLifoQueue if lifo else SmartQueue)(self.maxsize)
        async def feed(f=self.smart_put, g=q.smart_put, h=self.get, _=pred):
            with ignore_qshutdown:
                while True: await (f if _(i := await h()) else g)(i)
        self.make(feed()); return q
    def enumerate(self, *, lifo=False):
        audit(f'{fullname(self)}.enumerate', id(self))
        q = (SmartLifoQueue if lifo else SmartQueue)(self.maxsize)
        async def feed():
            i = 0
            with ignore_qempty:
                while True: await q.smart_put((i, await self.get())); i += 1
        self.make(feed()); return q
    def filter_nowait(self, pred=bool, /):
        f, g, a = (k := []).append, (r := []).append, self.get_nowait
        with ignore_qempty:
            while True: (f if pred(i := a()) else g)(i)
        h, j = self.put_nowait, len(r)
        for i in k:
            try: h(i)
            except D.QueueFull: g(i)
        return r, j
    def enumerate_nowait(self, start=0, *, step=1):
        with ignore_qempty:
            while True: yield start, self.get_nowait(); start += step
    P.patch_method_signatures((filter_nowait, 'pred=bool'), (transaction, ''), (drain_persistent, 'max_items=None, timeout=None'))
class SmartQueue(PotentQueueBase):
    def _init(self, maxsize): self.__queue = deque(maxlen=maxsize if maxsize > 0 else None)
    def _get(self): return self.__queue.popleft()
    def _put(self, item): self.__queue.append(item)
    def peek(self):
        if q := self.__queue: return q[0]
        raise D.QueueEmpty
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
        raise IndexError(f'asyncutils.queues.SmartLifoQueue: failed to peek item at index {i}')
    def peek_all(self): return self.__queue.copy()
    def qsize(self): return len(self.__queue)
    def __bool__(self): return bool(self.__queue)
    def empty(self): return not self
    def pushpop(self, item): raise NotImplementedError
    def pushpop_nowait(self, item, raising=True): raise NotImplementedError
class SmartPriorityQueue(PotentQueueBase):
    def __init__(self, maxsize=0, *, init_items=()): super().__init__(maxsize); self.make(self.start(maxsize, init_items))
    async def start(self, maxsize, init_items): q = await A.collect(I := A.iter_to_agen(init_items), maxsize); import heapq as H; H.heapify(q); self.__get, self.__put, self._unfinished_tasks, self.__queue = partial(H.heappop, q), partial(H.heappush, q), len(q), q; self._finished.clear(); await self.extend(I) # ty: ignore[unresolved-attribute]
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
    def __init__(self, maxsize=0, *, init_items=(), init_priority=0): self.__tiebreak = count(); super().__init__(maxsize, init_items=((init_priority, self._tiebreak, j) async for j in A.iter_to_agen(init_items)))
    @property
    def _tiebreak(self): return next(self.__tiebreak)
    def put_nowait(self, item, priority=0): super().put_nowait((priority, self._tiebreak, item))
    def put(self, item, priority=0): return super().put((priority, self._tiebreak, item))
    def get_nowait(self): return super().get_nowait()[-1]
    async def get(self): return (await super().get())[-1]
del f, _, Q
