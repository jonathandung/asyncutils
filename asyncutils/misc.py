__lazy_modules__ = frozenset(('asyncio',))
import asyncutils as A, asyncio as I
from asyncutils.constants import _NO_DEFAULT
from asyncutils._internal.helpers import filter_out
from asyncutils._internal.submodules import misc_all as __all__
from _collections import defaultdict
from sys import exc_info, intern
class StateMachine:
    __slots__ = '_entries', '_exits', '_lock', '_state', '_transitions'
    def __init__(self, state): self._state, self._transitions, self._entries, self._exits, self._lock = intern(state), defaultdict(lambda: defaultdict(set)), {}, {}, I.Lock()
    def add(self, from_state, to_state, condition=None): self._transitions[intern(from_state)][intern(to_state)].add(condition)
    on_enter, on_exit = map(lambda attr: lambda self, state: lambda h, /: dict.__setitem__(getattr(self, attr), state, h) or h, __slots__[:2])
    async def transition(self, state):
        state, s = intern(state), self._state
        async with self._lock:
            if None not in (S := self._transitions[s][state]):
                for _ in S:
                    if await _(s, state): break
                else: return False
            await self._helper(1); self._state = state; await self._helper(0); return True
    async def _helper(self, i, /, _=A.IgnoreErrors(KeyError), s=__slots__):
        async with _: await getattr(self, s[i])[self._state]()
    _helper.__text_signature__ = '($self, attr)' # ty: ignore[unresolved-attribute]
async def gather_with_limited_concurrency(n=None, /, *coros, ret_exc=False):
    async def wrapped(c, s=I.Semaphore(A.getcontext().GATHER_WITH_LIMITED_CONCURRENCY_DEFAULT_MAX_CONCURRENT if n is None else n)): # noqa: B008
        async with s: return await c
    return await I.gather(*map(wrapped, coros), return_exceptions=ret_exc)
class CallbackAccumulator(__import__('_collections').deque, A.ExecutorRequiredAsyncContextMixin):
    __slots__ = 'call_once', 'default_getter', 't'
    def __init__(self, name, it=(), maxlen=None, default=_NO_DEFAULT, call_once=True, default_getter=None): super().__init__(A.aiter_to_gen(it), maxlen); self.t, self.call_once, self.default_getter = tuple(filter_out(name, default, s=_NO_DEFAULT)), call_once, (lambda: (exc_info(), {}) if name == '__exit__' else ((), {})) if default_getter is None else default_getter
    def __call__(self, *a, **k):
        for f in self: f(*a, **k)
    def __enter__(self): return self
    def __exit__(self, /, *_): a, k = self.default_getter(); self(*a, **k)
    def add(self, o, /): self.append(getattr(o, *self.t))
    def offer_last(self, o, /):
        if (x := self.maxlen) is None or x > len(self): self.add(o); return True
        return False
    @property
    def callbacks(self): return self.copy()
    def __iter__(self):
        if self.call_once:
            p = self.popleft
            while self: yield p()
        else: yield from self.callbacks