from . import context
from ._internal.submodules import events_all as __all__
from .constants import RAISE
from .exceptions import EventValueError, ref
from .mixins import EventMixin
from _collections import deque # type: ignore[import-not-found]
from asyncio.tasks import wait, wait_for
from asyncio.timeouts import timeout as _timeout
from time import monotonic
class SingleWaiterEventWithValue(EventMixin):
    __slots__ = '_waiter',
    def set(self, value):
        if (w := self._waiter) is None or w.done(): self._waiter = w = self.make_fut()
        w.set_result(value)
    def is_set(self): return False if (w := self._waiter) is None else w.done()
    async def wait_for_next(self, timeout=None, *, strict=False):
        if w := self._waiter:
            if strict: raise RuntimeError('another waiter is waiting')
        else: self._waiter = w = self.make_fut()
        try: return await wait_for(w, timeout)
        finally: self._waiter = None
    def get(self, default=RAISE):
        if (w := self._waiter) is None or not w.done():
            if default is RAISE: raise EventValueError('no value is set')
            return default
        return w.result()
    clear = __init__ = lambda self: setattr(self, '_waiter', None)
class EventWithValue(EventMixin):
    __slots__ = '_hist', '_value', '_waiters'
    def __init__(self, *, maxhist=None): self._waiters, self._value, self._hist = set(), None, deque(maxlen=context.EVENT_WITH_VALUE_DEFAULT_MAX_HIST if maxhist is None else maxhist)
    def _record_hist(self): self._hist.append((monotonic(), ref(self._value)))
    def set(self, value, *, strict=True):
        if value != self._value: self._value = value; self._record_hist()
        if value is None:
            if strict: raise EventValueError('use clear instead')
        else:
            f, w = (t := []).append, self._waiters
            for _ in w: f(_) if _.done() else _.set_result(value)
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
        (w := self._waiters).add(F := self.make_fut())
        try: return await wait_for(F, timeout)
        finally: w.discard(F)
    def is_set(self): return self._value is not None
    @property
    def history(self): return [(t, q) for t, s in self._hist if (q := s()) is not None]
    @property
    def history_asdict(self): return {t: q for t, s in self._hist if (q := s()) is not None}
    def recent_history(self, duration=None):
        if duration is None: duration = context.EVENT_WITH_VALUE_DEFAULT_RECENT
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
            if force_transition: o = self.get(None); self.set(old); self.set(new); self.set(o, strict=False) # type: ignore[arg-type]
            return False
    async def wait_for_transition_unordered(self, a, b, timeout=None, *, force_transition=False): return await next(iter((await wait(map(self.loop.create_task, (self.wait_for_transition(a, b, timeout, force_transition=force_transition), self.wait_for_transition(b, a, timeout))), return_when='FIRST_COMPLETED'))[0]))