# ty: ignore[unresolved-attribute]
from asyncutils._internal import compat as Z, helpers as H, log as L, patch as P
from asyncutils._internal.submodules import base_all as __all__
from asyncutils.constants import _NO_DEFAULT, RAISE
from _functools import partial
import asyncutils as A, asyncio as I
from itertools import batched, repeat
from sys import audit, exc_info
b, c = H.check_methods, H.fullname
class event_loop: # noqa: N801
    __reusable, constructor_args = [], ('dont_release_loop_on_finalization', 'silent_on_finalize', 'dont_try_clear_tasks_on_reuse', 'close_existing_on_exit', 'dont_always_stop_on_exit', 'dont_close_created_on_exit', 'cancel_all_tasks', 'keep_loop', 'suppress_runtime_errors', 'fail_silent', 'dont_allow_reuse', 'dont_reuse', 'dont_attempt_enter', 'attempt_aenter', 'suppress_inner_exit_on_runtime_error', 'suppress_inner_aexit_on_runtime_error'); __slots__ = '_flags', '_istr', '_loop', '_state', '_task'
    def _get_unclosed_loop(self, factory=I.new_event_loop, _=A.IgnoreErrors(AttributeError)): # pragma: no cover
        if self._flags&0x800: return factory()
        p, L = (pool := self.__reusable).pop, None
        while pool and ((L := p()).is_closed() or L.is_running()): ...
        if L is None: return factory()
        if not self._flags&4:
            with _: L._ready.clear()
            with _: L._scheduled.clear()
        return L
    def factory_reset(self): self._flags = A.getcontext().EVENT_LOOP_BASE_FLAGS
    def clear_flags(self, mask_to_keep=0): self._flags &= mask_to_keep
    def copy_flags(self): return self.from_flags(self._flags)
    def flags_eq(self, o, /): return self._flags == (o if isinstance(o, int) else o._flags)
    @classmethod
    def from_flags(cls, flags, /, _=c, m=0x10000):
        if not 0 <= flags < m: raise OverflowError(f'asyncutils.base.event_loop: flags value {flags:#x} has forbidden bits set')
        r._flags, r._state, r._istr = flags, 0, f'{_(cls)} at {id(r := object.__new__(cls)):#x}'; return r
    def __new__(cls, /, **k):
        F, p, s = A.getcontext().EVENT_LOOP_BASE_FLAGS, k.pop, 1
        for f in cls.constructor_args:
            if (x := p(f, None)) is None: ...
            elif x: F |= s
            else: F &= ~s
            s <<= 1
        if k: A.raise_exc(TypeError, 'asyncutils.base.event_loop: got unexpected keyword arguments; shown below', notes=k) # pragma: no cover
        return cls.from_flags(F)
    def __hash__(self): return self._flags
    def __enter__(self, _='asyncutils.base.event_loop: context already entered'):
        f = self._flags
        if (s := self._state)&1: # pragma: no cover
            if f&0x200: return self._loop
            raise RuntimeError(_)
        if (l := I._get_running_loop()) is None: I.set_event_loop(l := self._get_unclosed_loop())
        else: s |= 2
        if not f&0x1000 and callable(g := getattr(l, '__enter__', None)): # pragma: no cover
            try: g(); s |= 4
            except A.CRITICAL: raise A.Critical
            except BaseException as e:
                if not f&0x200: raise RuntimeError(f'{self._istr}: exception occurred while calling __enter__ of associated event loop: {e}') from e
        if f&0x2000 and callable(g := getattr(l, '__aenter__', None)):
            try: I.run_coroutine_threadsafe(g(), l).result(); s |= 8
            except A.CRITICAL: raise A.Critical
            except BaseException as e:
                if not f&0x200: raise RuntimeError(f'{self._istr}: exception occurred while calling __aenter__ of associated event loop: {e}') from e
        self._loop, self._state = l, s+1; return l
    def __exit__(self, t, v, b, /, _m='%s context not entered', _n='%s context not entered with errors passed into __exit__', _i=A.IgnoreErrors(RuntimeError), _l=L): # noqa: C901,PLR0912
        n, f, l = self._istr, self._flags, self._loop
        if not (s := self._state)&1:
            if f&0x200: return False
            raise RuntimeError(_m%n) if v is None else BaseExceptionGroup(_n%n, tuple(A.unnest_reverse(v))).with_traceback(b)
        if f&0x40: self._task = l.create_task(safe_cancel_batch(I.all_tasks(l)))
        if not f&0x400: self.__reusable.append(l)
        if not ((c := s&2) and f&0x10):
            with _i: l.stop()
        q, r, self._state = t is not None and issubclass(t, RuntimeError), False, s-1
        if s&4: # pragma: no cover
            if callable(g := getattr(l, '__exit__', None)):
                try: r = g(None, None, None) if f&0x4000 and q else g(t, v, b)
                except A.CRITICAL: _l.critical('%s: critical error while calling __exit__ of associated event loop', n, exc_info=True)
                except RuntimeError:
                    if not f&0x100: _l.exception('event loop management shenanigans while exiting associated event loop')
                except:
                    if not f&0x200: _l.exception('%s: exception occurred while calling __exit__ of associated event loop', n)
            elif not f&0x200: _l.error('%s: __enter__ already called but __exit__ is not present', n)
        if s&8: # pragma: no cover
            if callable(g := getattr(l, '__aexit__', None)) and not r:
                try: r = I.run_coroutine_threadsafe(g(None, None, None) if f&0x8000 else g(t, v, b), l).result()
                except A.CRITICAL: _l.critical('%s: critical error while calling __aexit__ of associated event loop', n, exc_info=True)
                except RuntimeError:
                    if not f&0x100: _l.exception('runtime error exiting associated event loop')
                except:
                    if not f&0x200: _l.exception('%s: exception occurred while calling __aexit__ of associated event loop', n)
            elif not f&0x200: _l.error('%s: __aenter__ already called but __aexit__ is not present', n)
        if f&8 or not (c or f&0x20):
            with _i: l.close()
            I.set_event_loop(None)
        if not f&0x80: del self._loop
        return r or (q and (f>>8)&1)
    def __del__(self, _f=L.debug, _g=L.warning, _m='%s: garbage-collecting entered context; you are advised to refactor your code', _w='%s: cannot suppress exceptions from within destructor', _d='destroyed %s'): # pragma: no cover
        b, n = not (f := self._flags)&2, self._istr
        if not self._state&1:
            if b: _f(_d, n)
            return
        if b: _g(_m, n)
        if f&1: self._flags = f^0x400
        if self.__exit__(*exc_info()) and b: _g(_w, n)
    def __reduce__(self, /): return self.from_flags, (self._flags,)
    def __repr__(self, _=c): return f'{_(self)}.from_flags({self._flags:#4x})'
    P.patch_method_signatures((__enter__, ''), (__exit__, P.xsig), (__del__, ''), (_get_unclosed_loop, 'factory={}')); P.patch_classmethod_signatures((from_flags, 'flags, /'), (__new__, f'*, {"={0}, ".join(constructor_args)}={{0}}'))
def f(n):
    async def adisembowel(it, /): # pragma: no cover
        if callable(p := getattr(it, n, None)):
            while it: yield p()
            if callable(p := getattr(it, 'clear', None)) and I.iscoroutine(p := p()): await p
        else:
            async for i in iter_to_agen(it): yield i
    return adisembowel
adisembowel, adisembowelleft = map(f, ('pop', 'popleft'))
async def safe_cancel_batch(t, /, *, callback=None, disembowel=False, raising=False, _=c):
    audit('asyncutils.base.safe_cancel_batch', _(t)); a = (l := []).append
    async for F in (adisembowel if disembowel else iter_to_agen)(t):
        if not F.done(): F.cancel(); a(F)
    r = await I.gather(*l, return_exceptions=True)
    if callback is not None:
        async def f(a, /, _=callback): return (await r) if I.iscoroutine(r := _(a)) else r
        L = len(r := await I.gather(*map(f, r), return_exceptions=True))
        if raising and (E := tuple(A.unnest_reverse(*filter(BaseException.__instancecheck__, r)))): raise BaseExceptionGroup(f'asyncutils.base.safe_cancel_batch: {f"flattened {L} exception (groups)" if len(E) < L else f"collected {L} exceptions"} thrown by callback function {callback!r}', E)
async def iter_to_agen(it, sentinel=_NO_DEFAULT, *, use_existing_executor=None, create_executor=None, strict=None, a=c, b=b, c=H.check, s=H.create_executor, h=H.get_loop_and_set, w=L.debug, _=type('', (), {'__slots__': ('it',), '__init__': lambda self, it: setattr(self, 'it', it), '__bool__': lambda self, _=b: _(self.it, 'send', 'throw', 'close'), '__enter__': lambda self: None, '__exit__': lambda self, t, v, b, /, _=frozenset(('StopIteration interacts badly with generators and cannot be raised into a Future', 'async generator raised StopIteration')): False if t is None else str(v) in _ if t is RuntimeError else (((True if (C := getattr(self.it, 'close', None)) is None else C()) if t is StopAsyncIteration else (True if (T := getattr(self.it, 'throw', None)) is None else T(v))) or True)})): # noqa: ARG005,C901,PLR0912
    audit('asyncutils.base.iter_to_agen', a(it))
    if type(it) in Z.s:
        for i in batched(it, 0x400):
            for _ in i: yield _
            await A.yield_to_event_loop
        return
    C = A.getcontext()
    if b(it, '__aiter__') and not (C.ITER_TO_AGEN_DEFAULT_STRICT if strict is None else strict):
        if sentinel is _NO_DEFAULT:
            async for _ in it: yield _
        elif b(it, 'asend', 'athrow', 'aclose'):
            l = await (_ := it.asend)(None)
            while not c(l, sentinel): l = await _((yield l))
        else:
            async for l in it:
                if c(l, sentinel): break
                yield l
        return
    elif not b(it, '__iter__'): raise TypeError(f'asyncutils.base.iter_to_agen: cannot iterate over {it!r} synchronously or asynchronously')
    e, g = None, _(it := iter(it))
    if create_executor is None: create_executor = C.ITER_TO_AGEN_DEFAULT_MAY_CREATE_EXECUTOR
    if C.ITER_TO_AGEN_DEFAULT_USE_EXISTING_EXECUTOR if use_existing_executor is None else use_existing_executor:
        if (e := getattr(iter_to_agen, 'executor', None)) is None:
            if create_executor: e = s(iter_to_agen)
            else: w('asyncutils.base.iter_to_agen: no existing executor')
    elif create_executor: e = s(iter_to_agen, False)
    with g:
        if e is None:
            if g:
                l = (_ := it.send)(None)
                while not c(l, sentinel): l = _((yield l)); await A.yield_to_event_loop
            else:
                while not c(l := next(it, sentinel), sentinel): yield l; await A.yield_to_event_loop
        else:
            def r(*a, _=h().run_in_executor, e=e): return partial(_, e, *a)
            if g:
                l = await (_ := r(it.send))(None)
                while True:
                    if c(l, sentinel): break
                    l = await _((yield l))
            else:
                _ = r(next, it)
                while True:
                    if c((l := await _()), sentinel): break
                    yield l
def aiter_to_gen(ait, *, use_futures=None, loop=None, strict=None, a=c, b=b, g=H.get_loop_and_set):
    audit('asyncutils.base.aiter_to_gen', a(ait)); C, e = A.getcontext(), I.futures._chain_future
    if b(ait, '__iter__') and not (C.AITER_TO_GEN_DEFAULT_STRICT if strict is None else strict): yield from ait; return
    if not b(ait, '__aiter__'): raise TypeError(f'asyncutils.base.aiter_to_gen: cannot iterate over {ait!r} synchronously or asynchronously')
    d = b(ait := aiter(ait), 'asend', 'athrow', 'aclose')
    with A.ignore_stopaiteration:
        if loop is None: loop = g()
        if loop.is_running():
            if not (C.AITER_TO_GEN_DEFAULT_ALLOW_FUTURES if use_futures is None else use_futures): raise RuntimeError(f'asyncutils.base.aiter_to_gen: cannot convert async iterator {ait!r} to sync in running event loop without using futures')
            def f(*a, f, c=loop.create_task, g=e, t=I.Future): return g(c(f(*a)), F := t()) or F.result()
            if d:
                p, x = partial(f, f=ait.asend), None
                while True: x = yield p(x)
            else:
                p = partial(f, f=ait.__anext__)
                while True: yield p()
        else:
            a = loop.run_until_complete
            if d:
                p, x = ait.asend, None
                while True: x = yield a(p(x))
            else:
                p = ait.__anext__
                while True: yield a(p())
async def take(it, n=None, *, default=_NO_DEFAULT, _=L.debug, m='asyncutils.base.take: ran out of items'):
    if n is None:
        async for i in iter_to_agen(it): yield i
        return
    async for n, i in aenumerate(it, n-1, step=-1): # noqa: B020,PLR1704
        yield i
        if n == 0: return
    if default is RAISE: raise A.ItemsExhausted(m)
    if default is _NO_DEFAULT: _(m)
    else:
        for _ in repeat(default, n): yield _
async def collect(it, n=None, *, default=_NO_DEFAULT, _='asyncutils.base.collect: ran out of items'): return [i async for i in take(it, n, default=default, m=_)]
async def drop(it, n, *, raising=False, _=L.debug, m='asyncutils.base.drop: ran out of items'):
    async for i, j in aenumerate(it := iter_to_agen(it)):
        if i == n: yield j; break
    else:
        if raising: raise A.ItemsExhausted(m)
        _(m); return
    async for j in it: yield j
async def aenumerate(it, start=0, *, step=1):
    async for _ in iter_to_agen(it): yield start, _; start += step
P.patch_function_signatures((safe_cancel_batch, 'batch, /, *, callback=None, disembowel=False, raising=False'), (iter_to_agen, 'it, sentinel={}, *, use_existing_executor=None, create_executor=None, strict=None'), (aiter_to_gen, 'ait, *, use_futures=None, loop=None, strict=None'), (collect, 'it, n=None, *, default={}'), (take, 'it, n, *, default={}'), (drop, 'it, n, *, raising=False'))
yield_to_event_loop, sleep_forever = object.__new__(type('', (), {'__new__': lambda _: yield_to_event_loop, '__await__': (_ := lambda _: (yield)), **dict.fromkeys(('__repr__', '__str__', '__reduce__'), lambda _, r='asyncutils.base.yield_to_event_loop': r)})), I.sleep.__get__(float('inf'))
(dummy_task := type(_)(_.__code__.replace(co_flags=0x161, co_name=(_ := 'dummy_task'), co_qualname=_), globals())(None)).close()
del f, _, P, L, b, c, H