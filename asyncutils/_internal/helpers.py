__lazy_modules__ = frozenset(('asyncio.events',))
import asyncio.events as E, sys as S
def filter_out(*a, s=None): yield from filter(lambda x, s=s: s is not x, a)
def get_loop_and_set(_=(lambda l: l.stop() or l.close()).__get__, f=__import__('atexit').register):
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
def subscriptable(cls, /, _=classmethod(type(list[int]))): cls.__class_getitem__ = _; return cls # noqa: B008
def check(a, b, /): return a is b or (False if (e := b.__eq__(a)) is NotImplemented else e)
def coerce_callable(o, /): return o if callable(o) else type(o)
def create_executor(f, /, save=True):
    S.audit('asyncutils/create_executor', f'{(F := coerce_callable(f)).__module__.removeprefix('asyncutils.')}.{F.__qualname__}'); from asyncutils import Executor; e = Executor()
    if save: f.executor = e
    return e
def fullname(f, /, rmpref=False, _=('__module__', '__qualname__')): f = coerce_callable(f); n = '.'.join(filter_out(*(getattr(f, a, None) for a in _))); return n.removeprefix('asyncutils.') if rmpref else n
def audit_fullname(f, /, rmpref=False): S.audit(fullname(f, rmpref))
def verify_compat(v, /, _='This module is only for python %s or under'):
    a, b = v.split('.', 1)
    if (int(a), int(b)+1) <= S.version_info: raise ImportError(_%v)
async def simple_wrap(aw, /): return await aw
class LoopMixinBase:
    __slots__ = '_loop',
    @property
    def loop(self):
        if (l := getattr(self, '_loop', None)) is None: self._loop = l = get_loop_and_set()
        elif l is not E._get_running_loop(): raise RuntimeError('could not bind loop')
        return l
    def make(self, aw, /): return self.loop.create_task(simple_wrap(aw))
    def make_fut(self): return self.loop.create_future()
    def make_multiple(self, aws, /): yield from map(self.make, aws)
@subscriptable
class Bag(dict): # noqa: FURB189
    __slots__ = ()
    def __getattr__(self, k, /):
        try: return self[k]
        except KeyError: raise AttributeError(name=k, obj=self) from None
    __setattr__, __delattr__ = dict.__setitem__, dict.__delitem__
ismodule.__text_signature__, subscriptable.__text_signature__, fullname.__text_signature__, verify_compat.__text_signature__, get_loop_and_set.__text_signature__ = '(o, /)', '(cls, /)', '(f, /, rmpref=False)', '(v, /)', '()' # ty: ignore[unresolved-attribute]