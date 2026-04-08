from asyncio.events import new_event_loop, _get_running_loop, set_event_loop
from atexit import register
from sys import audit
def filter_out(*a, s=None, f=__import__('_operator').is_not): yield from filter(lambda x, s=s: f(s, x), a)
def get_loop_and_set():
    if (l := _get_running_loop()) is None: register(stop_and_closer(l := new_event_loop())); set_event_loop(l)
    audit('asyncutils._internal.helpers._get_loop_and_set', l); return l
def check_methods(obj, /, *meth):
    M = obj.__class__.__mro__
    for m in meth:
        for b in M:
            if (_ := b.__dict__.get(m, obj)) is None: return False
            if _ is not obj: break
        else: return False
    return True
def stop_and_closer(loop, _=lambda l: l.stop() or l.close()): return _.__get__(loop)
def copy_and_clear(l): r = l.copy(); l.clear(); return r
def subscriptable(cls, /, _=classmethod(type(list[int]))): cls.__class_getitem__ = _; return cls # type: ignore
def check(a, b, /): return a is b or (False if (e := b.__eq__(a)) is NotImplemented else e)
def new_executor(f, /, save=True):
    audit('asyncutils/create_executor', f'{(F := f if callable(f) else type(f)).__module__.removeprefix('asyncutils.')}.{F.__qualname__}'); from ..config import Executor as E; e = E()
    if save: f.executor = e
    return e
class _LoopMixinBase:
    __slots__ = 'exiter', 'loop', 'make_fut', 'running_tasks'
    def __init__(self): self.exiter, self.loop, self.make_fut, self.running_tasks = register(stop_and_closer(l := new_event_loop())), l, l.create_future, set()
    def make(self, coro): (_ := self.running_tasks).add(t := self.loop.create_task(coro)); t.add_done_callback(_.discard); return t
    def make_multiple(self, C): yield from map(self.make, C)