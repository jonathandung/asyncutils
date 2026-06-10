__lazy_modules__ = frozenset(('asyncio', 'time'))
import asyncutils as A, asyncio as I
from asyncutils.constants import _NO_DEFAULT
from asyncutils._internal.submodules import events_all as __all__
from _collections import deque
from time import monotonic
class SingleWaiterEventWithValue(A.EventMixin):
    __slots__ = '_waiter',
    def set(self, value):
        if (w := self._waiter) is None or w.done(): self._waiter = w = self.make_fut()
        w.set_result(value)
    def is_set(self): return False if (w := self._waiter) is None else w.done()
    async def wait_for_next(self, timeout=None, *, strict=False):
        if w := self._waiter:
            if strict: raise RuntimeError('asyncutils.events.SingleWaiterEventWithValue: another waiter is waiting')
        else: self._waiter = w = self.make_fut()
        try: return await I.wait_for(w, timeout)
        finally: self._waiter = None
    def get(self, default=_NO_DEFAULT):
        if (w := self._waiter) is None or not w.done():
            if default is _NO_DEFAULT: raise A.EventValueError('asyncutils.events.SingleWaiterEventWithValue: no value is set')
            return default
        return w.result()
    def clear(self): self._waiter = None
    __init__ = clear
class EventWithValue(A.EventMixin):
    __slots__ = '_hist', '_value', '_waiters'
    def __init__(self, *, maxhist=_NO_DEFAULT): self._waiters, self._value, self._hist = set(), None, deque(maxlen=A.getcontext().EVENT_WITH_VALUE_DEFAULT_MAX_HIST if maxhist is _NO_DEFAULT else maxhist)
    def _record_hist(self): self._hist.append((monotonic(), A.ref(self._value)))
    def set(self, value, *, strict=True):
        if value != self._value: self._value = value; self._record_hist()
        if value is None:
            if strict: raise A.EventValueError('asyncutils.events.EventWithValue: use clear instead')
        else:
            f, w = (t := []).append, self._waiters
            for _ in w: f(_) if _.done() else _.set_result(value)
            w.difference_update(t)
    def remove_done_waiters(self, _=__import__('operator').methodcaller('done')): (W := self._waiters).difference_update(filter(_, W)) # noqa: B008
    def set_once(self, value): v = self._value; self.set(value); self.set(v)
    def clear(self): self.set(None, strict=False)
    def get(self, default=_NO_DEFAULT):
        if (v := self._value) is None:
            if _NO_DEFAULT.is_(default): raise A.EventValueError('asyncutils.events.EventWithValue: no value is set')
            return default
        return v
    async def wait_for_next(self, timeout=None):
        (w := self._waiters).add(F := self.make_fut())
        try: return await I.wait_for(F, timeout)
        finally: w.discard(F)
    def is_set(self): return self._value is not None
    @property
    def history(self): return [(t, q) for t, s in self._hist if (q := s()) is not None]
    @property
    def history_asdict(self): return {t: q for t, s in self._hist if (q := s()) is not None}
    def recent_history(self, duration=None):
        if duration is None: duration = A.getcontext().EVENT_WITH_VALUE_DEFAULT_RECENT
        x, I = monotonic()-duration, iter(self._hist)
        for t, _ in I:
            if t >= x: yield t, _; yield from I
    async def wait_for_transition(self, old, new, timeout=None, *, force_transition=False, legacy=False):
        x = new
        try:
            async with I.timeout(timeout):
                while True:
                    if legacy or x is not old: await self.wait_for_value(old)
                    if new is (x := await self.wait_for_next()): return True
        except TimeoutError:
            if force_transition: o = self.get(None); (s := self.set)(old); s(new); s(o, strict=False)
            return False
    async def wait_for_transition_unordered(self, a, b, timeout=None, *, force_transition=False, legacy=False): return await next(iter((await I.wait(map(self.loop.create_task, (self.wait_for_transition(a, b, timeout, force_transition=force_transition, legacy=legacy), self.wait_for_transition(b, a, timeout, legacy=legacy))), return_when='FIRST_COMPLETED'))[0]))
