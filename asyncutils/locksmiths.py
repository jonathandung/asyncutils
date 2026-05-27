import asyncio as I, asyncutils as A, asyncutils._internal.log as L
from asyncutils.constants import _NO_DEFAULT
from asyncutils._internal.helpers import check_methods, fullname, get_loop_and_set
from asyncutils._internal.submodules import locksmiths_all as __all__
from enum import IntEnum
from sys import audit
ForceResult, RecognitionResult = IntEnum('ForceResult', 'UNFORCABLE NO_CURRENT_TASK OWNER_COMPLETED ALREADY_BEING_FORCED RELEASED_WITH_FALSE SUCCESS RELEASED', module=__name__), IntEnum('RecognitionResult', 'FAILED_PRELIM FAILED_ACK ALREADY_RECOGNIZED SUCCESS', module=__name__)
succeeded = frozenset((ForceResult.SUCCESS, ForceResult.RELEASED, RecognitionResult.ALREADY_RECOGNIZED, RecognitionResult.SUCCESS)).__contains__
class LocksmithBase:
    __slots__ = '_lock', '_loop', '_recognized'; handlers = {} # noqa: RUF012
    @classmethod
    def register_handler(cls, h, /, *, shadow=True):
        def register(t, H=cls.handlers, h=h):
            if not isinstance(t, type): raise TypeError('asyncutils.locksmiths.LocksmithBase: non-type cannot be registered')
            if shadow: H[t] = h
            elif h is not (h := H.setdefault(t, h)): raise KeyError('asyncutils.locksmiths.LocksmithBase: handler for type already registered', t, h)
            return t
        return register
    @property
    def currently_recognized(self): return frozenset(self._recognized)
    def __init__(self, loop=None, ltyp=I.Lock): self._recognized, self._loop, self._lock = __import__('_weakrefset').WeakSet((l := ltyp(),)), loop or get_loop_and_set(), l
    async def recognize_lock(self, l, /):
        if not self.preliminary_check_lock(l): return RecognitionResult.FAILED_PRELIM
        async with self._lock:
            if l in (r := self._recognized): return RecognitionResult.ALREADY_RECOGNIZED
            if callable(f := getattr(l, 'acknowledge_locksmith_lock_held', None)):
                try: return bool((await f) if I.iscoroutine(f := f(self)) else f)
                except A.CRITICAL: raise A.Critical
                except: return RecognitionResult.FAILED_ACK
            r.add(l); return RecognitionResult.SUCCESS
    async def force(self, l, /, info=_NO_DEFAULT, *, purge_waiters=True): # noqa: PLR0912
        audit('asyncutils.locksmiths.LocksmithBase.force', id(self), id(l))
        async with self._lock:
            if not self.can_force_lock_held(l): return ForceResult.UNFORCABLE
        if info is _NO_DEFAULT: info = await self.get_info(l)
        try:
            if I.iscoroutine(r := l.release()): r = await r
        except A.CRITICAL: raise A.Critical
        except:
            if self.find_owner(l) is (o := I.current_task(self._loop)):
                if o is None: return await self.throw_fallback(l)
                if (c := o.get_coro()) is None: return await self.eager_fallback(l)
                E = A.LockForceRequest(self, (F := self._loop.create_future()).set_result, l, info) # ty: ignore[invalid-argument-type]
                try: c.throw(E)
                except A.CRITICAL as e: return self.task_raised_critical(l, e)
                except A.LockForceRequest as e:
                    if (r := e.requester) is not self: await I.gather(self.lock_busy(l, r), r.lock_busy(l, self))
                    elif e is E: await self.task_reraised_request(l)
                    else: return await self.already_forcing(l)
                except BaseException as e: await self.task_raised_other(l, e) # noqa: BLE001
                else: await self.answer_received(l, await F)
            try:
                if callable(f := self.handlers.get(type(l))) and I.iscoroutine(r := f(l)): await r
            except A.CRITICAL: raise A.Critical
            return ForceResult.SUCCESS
        else: return await self.release_returned_false(l) if r is False else ForceResult.RELEASED
        finally:
            if purge_waiters: await self.purge_waiters(l)
    async def purge_waiters(self, l, /):
        if w := getattr(l, '_waiters', None): await A.safe_cancel_batch(w, disembowel=True)
    async def host(self, t, l, /, *, timeout1=_NO_DEFAULT, timeout2=_NO_DEFAULT, timeout3=_NO_DEFAULT):
        await I.wait(f := tuple(map(self.wrap_task, (self.force(l, purge_waiters=False), l.acquire()))), return_when='FIRST_COMPLETED'); f, a, T = *f, A.getcontext().LOCKSMITH_BASE_DEFAULT_TIMEOUTS
        if await I.wait_for(f, T[0] if timeout1 is _NO_DEFAULT else timeout1): await a
        else:
            try: await I.wait_for(a, T[1] if timeout2 is _NO_DEFAULT else timeout2)
            except TimeoutError: raise TimeoutError(f'{fullname(self)}.host: failed to acquire lock {l!r} within {timeout2} seconds') from None
        self.patch_owner(t := self.wrap_task(t), l); return await I.wait_for(self._wait_on(t, l), T[2] if timeout3 is _NO_DEFAULT else timeout3)
    async def get_info(self, l, /): return f'potential deadlock situation involving {fullname(l)} at {id(l):#x}'
    async def lock_busy(self, *a): await A.transient_block(self._loop, L.info, 'lock busy: %r; requester: %r', *a)
    async def task_reraised_request(self, l, /): await A.transient_block(self._loop, L.warning, '%s.force: running task did not handle request to release %s at %#x properly', fullname(self), fullname(l), id(l))
    async def answer_received(self, l, a, /): await A.transient_block(self._loop, L.info, '%r received answer %r from %r', self, a, l)
    async def throw_fallback(self, _, /): return ForceResult.NO_CURRENT_TASK
    async def eager_fallback(self, _, /): return ForceResult.OWNER_COMPLETED
    async def release_returned_false(self, _, /): return ForceResult.RELEASED_WITH_FALSE
    async def already_forcing(self, _, /): return ForceResult.ALREADY_BEING_FORCED
    async def _wait_on(self, t, l, /):
        try: return await t
        finally:
            if l.locked() and I.iscoroutine(a := l.release()): await a
    async def task_raised_other(self, l, e, /):
        if not isinstance(e, RuntimeError): await A.transient_block(self._loop, L.error, 'error encountered in attempt to force %s at %#x', fullname(l), id(l), exc_info=e)
    def wrap_task(self, a, /): return self._loop.create_task(A.wrap_in_coro(a))
    def patch_owner(self, t, l, /):
        if hasattr(l, '_owner'): l._owner = t
    def find_owner(self, l, /): return getattr(l, '_owner', None)
    def preliminary_check_lock(self, l, /): return check_methods(l, 'acquire', 'release', 'locked')
    def task_raised_critical(self, _, e, /): raise A.Critical(e) from None
    def can_force_lock_held(self, l, /): return l in self._recognized and l.locked()