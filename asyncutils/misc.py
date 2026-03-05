from collections import defaultdict
from sys import intern
from asyncio.locks import Lock
from asyncio.tasks import gather
from .util import semaphore
from .exceptions import IgnoreErrors
from ._internal.submodules import misc_all as __all__
class StateMachine:
    __slots__ = '_state', '_transitions', '_entries', '_exits', '_lock'
    def __init__(self, state, /): self._state, self._transitions, self._entries, self._exits, self._lock = intern(state), defaultdict(set), {}, {}, Lock()
    def add(self, from_state, to_state, condition=None): self._transitions[intern(from_state)].add((intern(to_state), condition))
    on_enter, on_exit = map(lambda attr: lambda self, state, handler: getattr(self, attr).__setitem__(state, handler), ('_entries', '_exits'))
    async def transition(self, state):
        state = intern(state)
        async with self._lock:
            for t, _ in self._transitions.get(self._state, ()):
                if t == state:
                    if _ is None or await _(): break
            else: return False
            await self._helper('_exits'); self._state = state; await self._helper('_entries')
            return True
    async def _helper(self, attr, _h=IgnoreErrors(KeyError)):
        async with _h: await getattr(self, attr)[self._state]()
async def gather_with_limited_concurrency(n, /, *coros, bounded=False, ret_exc=False):
    async def wrapped(c, s=semaphore(bounded, n)):
        async with s: return await c
    return await gather(*map(wrapped, coros), return_exceptions=ret_exc)