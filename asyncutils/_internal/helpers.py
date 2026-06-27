__lazy_modules__ = frozenset(('asyncio.events',))
from asyncutils._internal import patch as P
import sys as S
def filter_out(*a, s=None): yield from filter(lambda x, s=s: s is not x, a)
def get_loop_and_set(_=(lambda l: l.stop() or l.close()).__get__, f=__import__('atexit').register):
    import asyncio.events as E
    if (l := E._get_running_loop()) is None: f(_(l := E.new_event_loop())); E.set_event_loop(l)
    S.audit('asyncutils/get_loop_and_set', l); return l
def check_methods(obj, /, *meth):
    M = obj.__class__.__mro__
    for m in meth:
        for b in M:
            if (_ := b.__dict__.get(m, obj)) is None: return False
            if _ is not obj: break
        else: return False
    return True
def copy_and_clear(l): r = l.copy(); l.clear(); return r
def ismodule(o, /, _=frozenset(('asyncutils._internal.initialize.Module', 'builtins.module'))): return fullname(type(o)) in _
def subscriptable(cls, /, _=classmethod(type(list[int]))):
    if hasattr(cls, '__class_getitem__'): raise TypeError('class is already subscriptable')
    cls.__class_getitem__ = _; return cls
def check(a, b, /): return a is b or (False if (e := b.__eq__(a)) is NotImplemented else e) # noqa: PLC2801
def coerce_callable(o, /): return o if callable(o) else type(o)
def create_executor(f, /, save=True): # pragma: no cover
    S.audit('asyncutils/create_executor', f'{(F := coerce_callable(f)).__module__.removeprefix('asyncutils.')}.{F.__qualname__}'); from asyncutils import Executor; e = Executor()
    if save: f.executor = e
    return e
def fullname(f, /, remove_prefix=False, _=('__module__', '__qualname__')): f = coerce_callable(f); n = '.'.join(filter_out(*(getattr(f, a, None) for a in _))); return n.removeprefix('asyncutils.') if remove_prefix else n
def audit_fullname(f, /, remove_prefix=False): S.audit(fullname(f, remove_prefix))
async def simple_wrap(aw, /): return await aw
class LoopMixinBase:
    __slots__ = '_loop',
    @property
    def loop(self):
        if (l := getattr(self, '_loop', None)) is None: self._loop = l = get_loop_and_set()
        elif l is not __import__('asyncio.events', fromlist=('',))._get_running_loop(): raise RuntimeError('asyncutils: could not bind loop')
        return l
    def make(self, a, /): return self.loop.create_task(simple_wrap(a))
    def make_fut(self): return self.loop.create_future()
    def make_multiple(self, a, /): yield from map(self.make, a)
class Bag(dict): # noqa: FURB189
    __slots__, __setattr__, __delattr__ = (), dict.__setitem__, dict.__delitem__
    def __getattr__(self, k, /):
        try: return self[k]
        except KeyError: raise AttributeError(name=k, obj=self) from None
P.patch_function_signatures((ismodule, 'o, /'), (subscriptable, 'cls, /'), (fullname, 'f, /, remove_prefix=False'), (get_loop_and_set, ''))
del P
