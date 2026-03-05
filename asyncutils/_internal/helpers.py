from asyncio.events import new_event_loop, _get_running_loop, set_event_loop
from atexit import register
from sys import audit
pkgpref = 'asyncutils.'
def _filter_out(*a, s=None, f=__import__('_operator').is_not): yield from filter(lambda x, s=s: f(s, x), a)
def _get_loop_no_exit():
    audit(f'{pkgpref}_helpers._get_loop_no_exit')
    if (l := _get_running_loop()) is None: register(stop_and_closer(l := new_event_loop())); set_event_loop(l)
    return l
def _check_methods(obj, /, *meth):
    M = obj.__class__.__mro__
    for m in meth:
        for b in M:
            if (_ := b.__dict__.get(m, obj)) is None: return False
            elif _ is not obj: break
        else: return False
    return True
def stop_and_closer(loop, _=lambda l: l.stop() or l.close()): return _.__get__(loop)
def copy_and_clear(l): r = l.copy(); l.clear(); return r
def subscriptable(cls, /, _=classmethod(type(list[int]))): cls.__class_getitem__ = _; return cls # type: ignore
class _LoopMixinBase:
    __slots__ = 'loop', 'exiter', 'running_tasks', 'make_fut'
    def __init__(self): self.loop, self.exiter, self.make_fut, self.running_tasks = (l := new_event_loop()), register(l.close), l.create_future, set()
    def make(self, coro): (_ := self.running_tasks).add(t := self.loop.create_task(coro)); t.add_done_callback(_.discard); return t
    def make_multiple(self, C): yield from map(self.make, C)