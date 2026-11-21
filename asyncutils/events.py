import asyncio as I, asyncutils as A
from _collections import deque
from time import monotonic
from asyncutils._internal.submodules import events_all as __all__
from asyncutils.constants import _NO_DEFAULT
class SingleWaiterEventWithValue(A.EventMixin):
    __slots__ = '__w',
    def set(self, value):
        if (w := self.__w) is None or w.done(): self.__w = w = self.loop.create_future()
        w.set_result(value)
    def is_set(self): return False if (w := self.__w) is None else w.done()
    async def wait_for_next(self, timeout=None, *, strict=False):
        if w := self.__w:
            if strict: raise RuntimeError('asyncutils.events.SingleWaiterEventWithValue: another waiter is already waiting and strict=True was passed')
        else: self.__w = w = self.loop.create_future()
        try: return await I.wait_for(w, timeout)
        finally: self.__w = None
    def get(self, default=_NO_DEFAULT):
        if (w := self.__w) is None or not w.done():
            if default is _NO_DEFAULT: raise A.EventValueError('asyncutils.events.SingleWaiterEventWithValue: no value is set and no default was provided')
            return default
        return w.result()
    def clear(self): self.__w = None
    __init__ = clear
class EventWithValue(A.EventMixin):
    __slots__ = '__h', '__v', '__w'
    def __init__(self, *, maxhist=_NO_DEFAULT): self.__w, self.__v, self.__h = set(), None, deque(maxlen=A.getcontext().EVENT_WITH_VALUE_DEFAULT_MAX_HIST if maxhist is _NO_DEFAULT else maxhist)
    def _rh(self): self.__h.append((monotonic(), A.ref(self.__v)))
    def set(self, value, *, strict=True):
        if value != self.__v: self.__v = value; self._rh()
        if value is None:
            if strict: raise A.EventValueError('asyncutils.events.EventWithValue: use clear instead')
        else:
            f, w = (t := []).append, self.__w
            for _ in w: f(_) if _.done() else _.set_result(value)
            w.difference_update(t)
    def remove_done_waiters(self, _=__import__('operator').methodcaller('done')): (W := self.__w).difference_update(filter(_, W)) # ruff: ignore[function-call-in-default-argument]
    def set_once(self, value): v = self.__v; self.set(value); self.set(v)
    def clear(self): self.set(None, strict=False)
    def get(self, default=_NO_DEFAULT):
        if (v := self.__v) is None:
            if _NO_DEFAULT is default: raise A.EventValueError('asyncutils.events.EventWithValue: no value is set and no default was provided')
            return default
        return v
    async def wait_for_next(self, timeout=None):
        (w := self.__w).add(F := self.loop.create_future())
        try: return await I.wait_for(F, timeout)
        finally: w.discard(F)
    def is_set(self): return self.__v is not None
    @property
    def history(self): return [(t, q) for t, s in self.__h if (q := s()) is not None]
    @property
    def history_asdict(self): return {t: q for t, s in self.__h if (q := s()) is not None}
    def recent_history(self, duration=None):
        if duration is None: duration = A.getcontext().EVENT_WITH_VALUE_DEFAULT_RECENT
        x, I = monotonic()-duration, iter(self.__h)
        for t, _ in I:
            if t >= x: yield t, _; yield from I
