from atexit import register
from sys import audit, _getframe, version_info
def filter_out(*a, s=None, f=__import__('_operator').is_not): yield from filter(lambda x, s=s: f(s, x), a)
def get_loop_and_set():
    import asyncio.events as E
    if (l := E._get_running_loop()) is None: register(stop_and_closer(l := E.new_event_loop())); E.set_event_loop(l)
    audit('asyncutils/get_loop_and_set', l); return l
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
def subscriptable(cls, /, _=classmethod(type(list[int]))): cls.__class_getitem__ = _; return cls # noqa: B008
def check(a, b, /): return a is b or (False if (e := b.__eq__(a)) is NotImplemented else e)
def coerce_callable(o, /): return o if callable(o) else type(o)
def create_executor(f, /, save=True):
    audit('asyncutils/create_executor', f'{(F := coerce_callable(f)).__module__.removeprefix('asyncutils.')}.{F.__qualname__}'); from asyncutils import Executor; e = Executor()
    if save: f.executor = e
    return e
def fullname(f, /, rmpref=False, _=('__module__', '__qualname__')): f = coerce_callable(f); n = '.'.join(filter_out(*(getattr(f, a, None) for a in _))); return n.removeprefix('asyncutils.') if rmpref else n
def audit_fullname(f, /, rmpref=False): audit(fullname(f, rmpref))
def verify_compat(v, /, _='This module is only for python %s or under'):
    a, b = v.split('.', 1)
    if (int(a), int(b)+1) > version_info: return False
    frame = _getframe(1)
    while frame := frame.f_back:
        if frame.f_code.co_qualname == 'import_module':
            if (c := frame.f_back.f_code).co_filename.endswith(('mypy/stubtest.py', 'mypy\\stubtest.py')) and c.co_qualname == 'silent_import_module': return True
            break
    raise ImportError(_%v)
class LoopMixinBase:
    __slots__ = ()
    def make(self, coro): return self.loop.create_task(coro)
    def make_fut(self): return self.loop.create_future()
    def make_multiple(self, C): yield from map(self.make, C)