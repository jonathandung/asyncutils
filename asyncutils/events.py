from .mixins import EventMixin
from . import constants
from .config import RAISE
from .exceptions import EventValueError, ref
from _collections import deque
from asyncio.timeouts import timeout as _timeout
from asyncio.tasks import wait_for, wait
from asyncio.events import get_running_loop
from time import monotonic
from ._internal.submodules import events_all as __all__
class SingleWaiterEventWithValue(EventMixin):
    def __init__(self): self.clear()
    def set(self, value):
        self._set = True
        if (w := self._waiter) and not w.done(): w.set_result(value); self._value = value
    def clear(self): self._set, self._waiter = False, None; del self._value
    def is_set(self): return self._set
    async def wait_for_next(self, timeout=None, *, strict=False):
        if self._waiter:
            if strict: raise RuntimeError('another waiter')
        else: self._waiter = self.loop.create_future()
        try: return await wait_for(self._waiter, timeout)
        finally: self._waiter = None
    def get(self, default=RAISE):
        if default is RAISE: raise EventValueError('no value is set')
        return self._value if self._set else default
class EventWithValue(EventMixin):
    def __init__(self, *, maxhist=None): self._waiters, self._value, self._hist = set(), None, deque(maxlen=constants.EVENT_WITH_VALUE_DEFAULT_MAXHIST if maxhist is None else maxhist)
    def _record_hist(self): self._hist.append((monotonic(), ref(self._value)))
    def set(self, value, *, strict=True):
        if value != self._value: self._value = value; self._record_hist()
        if value is None:
            if strict: raise EventValueError('use clear instead')
        else:
            t, w = [], self._waiters
            for _ in w: t.append(_) if _.done() else _.set_result(value)
            w.difference_update(t)
    def remove_done_waiters(self): (W := self._waiters).difference_update(filter(lambda w: w.done(), W))
    def set_once(self, value): v = self._value; self.set(value); self.set(v)
    def clear(self): self.set(None, strict=False)
    def get(self, default=RAISE):
        if (v := self._value) is None:
            if default is RAISE: raise EventValueError('no value is set')
            return default
        return v
    async def wait_for_next(self, timeout=None):
        self._waiters.add(F := self.loop.create_future())
        try: return await wait_for(F, timeout)
        finally: self._waiters.discard(F)
    def is_set(self): return self._value is not None
    @property
    def history(self): return [(t, q) for t, s in self._hist if (q := s()) is not None]
    @property
    def history_asdict(self): return {t: q for t, s in self._hist if (q := s()) is not None}
    def recent_history(self, duration=None):
        if duration is None: duration = constants.EVENT_WITH_VALUE_DEFAULT_RECENT
        x, I = monotonic()-duration, iter(self._hist)
        for t, _ in I:
            if t >= x: yield t, _; yield from I
    async def wait_for_transition(self, old, new, timeout=None, *, force_transition=False):
        try:
            async with _timeout(timeout):
                while True:
                    await self.wait_for_value(old)
                    if new is await self.wait_for_next(): return True
        except TimeoutError:
            if force_transition: o = self.get(None); self.set(old); self.set(new); self.set(o, strict=False)
            return False
    async def wait_for_transition_unordered(self, a, b, timeout=None, *, force_transition=False, loop=None): return await next(iter((await wait(map((loop or get_running_loop()).create_task, (self.wait_for_transition(a, b, timeout, force_transition=force_transition), self.wait_for_transition(b, a, timeout))), return_when='FIRST_COMPLETED'))[0]))