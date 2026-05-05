__lazy_modules__ = frozenset(('asyncio',))
from asyncutils import IgnoreErrors, getcontext
from asyncutils._internal.submodules import misc_all as __all__
from _collections import defaultdict # type: ignore[import-not-found]
from asyncio import Lock, Semaphore, gather
from sys import intern
class StateMachine:
    __slots__ = '_entries', '_exits', '_lock', '_state', '_transitions'
    def __init__(self, state): self._state, self._transitions, self._entries, self._exits, self._lock = intern(state), defaultdict(set), {}, {}, Lock()
    def add(self, from_state, to_state, condition=None): self._transitions[intern(from_state)].add((intern(to_state), condition))
    on_enter, on_exit = map(lambda attr: lambda self, state: lambda h, /: dict.__setitem__(getattr(self, attr), state, h) or h, __slots__[:2])
    async def transition(self, state):
        state, s = intern(state), self._state
        async with self._lock:
            for t, _ in self._transitions.get(s, ()):
                if t == state and (_ is None or await _(s, t)): break
            else: return False
            await self._helper(1); self._state = state; await self._helper(0); return True
    async def _helper(self, i, /, _=IgnoreErrors(KeyError)):
        async with _: await getattr(self, self.__slots__[i])[self._state]()
    _helper.__text_signature__ = '($self, attr)'
async def gather_with_limited_concurrency(n=None, /, *coros, ret_exc=False):
    async def wrapped(c, s=Semaphore(getcontext().GATHER_WITH_LIMITED_CONCURRENCY_DEFAULT_MAX_CONCURRENT if n is None else n)): # noqa: B008
        async with s: return await c
    return await gather(*map(wrapped, coros), return_exceptions=ret_exc)