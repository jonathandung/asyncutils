# type: ignore
from asyncutils import CRITICAL, RAISE, Critical, IgnoreErrors, ItemsExhausted, getcontext, unnest_reverse
from asyncutils.constants import _NO_DEFAULT
from asyncutils._internal import helpers as H, log as L, patch as P
from asyncutils._internal.submodules import base_all as __all__
from _functools import partial
from asyncio import Future, _get_running_loop, all_tasks, gather, iscoroutine, new_event_loop, run_coroutine_threadsafe, set_event_loop, sleep
from sys import audit, exc_info
b, c = H.check_methods, H.fullname
class event_loop: # noqa: N801
    _ENTERED, _SHOULD_CLOSE, _INNER_EXIT, _INNER_AEXIT, _INTERNAL_MASK, __reusable = 0x1000, 0x2000, 0x4000, 0x8000, 0xF000, []; __slots__ = '_flags', '_istr', '_loop', '_task'
    def _get_unclosed_loop(self, factory=new_event_loop, _=IgnoreErrors(AttributeError)):
        if self._flags&0x800: return factory()
        pool = self.__reusable
        while pool:
            if (L := pool.pop()).is_closed() or L.is_running(): continue
            with _: L._ready.clear()
            with _: L._scheduled.clear()
            return L
        return factory()
    def clear_flags(self, mask_to_keep=0): self._flags &= mask_to_keep|self._INTERNAL_MASK
    def copy_flags(self): return self.from_flags(self._flags&~self._INTERNAL_MASK)
    @classmethod
    def from_flags(cls, flags, /, _=c): r._flags, r._istr = flags, f'{_(cls)} at {id(r := object.__new__(cls)):#x}'; return r
    def __new__(cls, /, *, dont_release_loop_on_finalization=False, silent_on_finalize=False, check_running=False, close_existing_on_exit=False, dont_always_stop_on_exit=False, dont_close_created_on_exit=False, cancel_all_tasks=False, keep_loop=False, suppress_runtime_errors=False, fail_silent=False, dont_allow_reuse=False, dont_reuse=False, dont_attempt_enter=False, attempt_aenter=False, suppress_inner_exit_on_runtime_error=False, suppress_inner_aexit_on_runtime_error=False): return cls.from_flags(dont_release_loop_on_finalization|silent_on_finalize<<1|check_running<<2|close_existing_on_exit<<3|dont_always_stop_on_exit<<4|dont_close_created_on_exit<<5|cancel_all_tasks<<6|keep_loop<<7|suppress_runtime_errors<<8|fail_silent<<9|dont_allow_reuse<<10|dont_reuse<<11|dont_attempt_enter<<16|attempt_aenter<<17|suppress_inner_exit_on_runtime_error<<18|suppress_inner_aexit_on_runtime_error<<19) # noqa: PLR0913
    def __enter__(self, _='event_loop context already entered'):
        if (f := self._flags)&self._ENTERED:
            if f&0x200: return self._loop
            raise RuntimeError(_)
        if (l := _get_running_loop()) is None: set_event_loop(l := self._get_unclosed_loop())
        elif f&4 and l.is_running(): l = self._get_unclosed_loop()
        else: f |= self._SHOULD_CLOSE
        if not f&0x10000 and callable(g := getattr(l, '__enter__', None)):
            try: g(); f |= self._INNER_EXIT
            except CRITICAL: raise Critical
            except BaseException as e:
                if not f&0x200: raise RuntimeError(f'{self._istr}: exception occurred while calling __enter__ of associated event loop: {e}') from e
        if f&0x20000 and callable(g := getattr(l, '__aenter__', None)): l.call_soon(g); f |= self._INNER_AEXIT
        self._loop, self._flags = l, f|self._ENTERED; return l
    def __exit__(self, t, v, b, /, _m='%s context not entered', _n='%s context not entered with errors passed into __exit__', _i=IgnoreErrors(RuntimeError), _l=L): # noqa: PLR0912
        N = self._istr
        if not (f := self._flags)&(e := self._ENTERED):
            if f&0x200: return False
            raise RuntimeError(_m%N) if v is None else BaseExceptionGroup(_n%N, tuple(unnest_reverse(v))).with_traceback(b)
        f &= ~e; l = self._loop
        if f&0x40: self._task = l.create_task(safe_cancel_batch(all_tasks(l)))
        if not f&0x400: self.__reusable.append(l)
        if not ((c := f&self._SHOULD_CLOSE) and f&0x10):
            with _i: l.stop()
        q, r, self._flags = t is not None and issubclass(t, RuntimeError), False, f&~0xC0000
        if f&self._INNER_EXIT:
            if callable(g := getattr(l, '__exit__', None)):
                try: r = g(None, None, None) if f&0x40000 and q else g(t, v, b)
                except CRITICAL: _l.critical('%s: critical error while calling __exit__ of associated event loop', N, exc_info=True)
                except RuntimeError:
                    if not f&0x100: _l.exception('RuntimeError exiting associated event loop')
                except:
                    if not f&0x200: _l.exception('%s: exception occurred while calling __exit__ of associated event loop', N)
            elif not f&0x200: _l.error('%s: __enter__ already called but __exit__ is not present', N)
        if f&self._INNER_AEXIT:
            if callable(g := getattr(l, '__aexit__', None)) and not r:
                try: r = run_coroutine_threadsafe(g(None, None, None) if f&0x80000 else g(t, v, b), l).result()
                except CRITICAL: _l.critical('%s: critical error while calling __aexit__ of associated event loop', N, exc_info=True)
                except RuntimeError:
                    if not f&0x100: _l.exception('RuntimeError exiting associated event loop')
                except:
                    if not f&0x200: _l.exception('%s: exception occurred while calling __aexit__ of associated event loop', N)
            elif not f&0x200: _l.error('%s: __aenter__ already called but __aexit__ is not present', N)
        if f&8 or not (c or f&0x20):
            with _i: l.close()
            set_event_loop(None)
        if not f&0x80: del self._loop
        return r or (q and bool(f&0x100))
    def __del__(self, _f=L.debug, _g=L.warning, _m='%s: garbage-collecting entered context; you are advised to refactor your code', _w='%s: cannot suppress exceptions from within destructor', _d='destroyed %s'):
        b, N = not (f := self._flags)&2, self._istr
        if f&self._ENTERED:
            if b: _g(_m, N)
            if f&1: self._flags = f^0x400
            if self.__exit__(*exc_info()) and b: _g(_w, N)
        elif b: _f(_d, N)
    def __reduce__(self, /): return self.from_flags, (self._flags,)
    P.patch_method_signatures((__enter__, ''), (__exit__, P.xsig), (__del__, ''), (_get_unclosed_loop, 'factory={}')); P.patch_classmethod_signatures((from_flags, 'flags, /'))
def f(n):
    async def adisembowel(it, /):
        if callable(p := getattr(it, n, None)):
            while it: yield p()
            if callable(p := getattr(it, 'clear', None)) and iscoroutine(p := p()): await p
        else:
            async for i in iter_to_agen(it): yield i
    return adisembowel
adisembowel, adisembowelleft = map(f, ('pop', 'popleft'))
async def safe_cancel_batch(t, /, *, callback=None, disembowel=False, raising=False, _=c):
    audit('asyncutils.base.safe_cancel_batch', _(t)); f = (l := []).append
    async for _ in (adisembowel if disembowel else iter_to_agen)(t):
        if not _.done(): _.cancel(); f(_)
    r = await gather(*l, return_exceptions=True)
    if callback is not None:
        async def f(a, /, _=callback): return (await r) if iscoroutine(r := _(a)) else r
        L = len(r := await gather(*map(f, r), return_exceptions=True))
        if raising and (E := tuple(unnest_reverse(*filter(BaseException.__instancecheck__, r)))): raise BaseExceptionGroup(f'safe_cancel_batch: {f"flattened {L} exception (groups)" if len(E) < L else f"collected {L} exceptions"} thrown by callback function {callback!r}', E)
async def iter_to_agen(it, sentinel=_NO_DEFAULT, *, use_existing_executor=None, create_executor=None, strict=None, a=c, b=b, c=H.check, s=H.create_executor, h=H.get_loop_and_set, w=L.debug, _=type('', (), {'__slots__': ('it',), '__init__': lambda self, it: setattr(self, 'it', it), '__bool__': lambda self, _=b: _(self.it, 'send', 'throw', 'close'), '__enter__': lambda self: None, '__exit__': lambda self, t, v, b, /, _=frozenset(('StopIteration interacts badly with generators and cannot be raised into a Future', 'async generator raised StopIteration')): False if t is None else str(v) in _ if t is RuntimeError else (((True if (C := getattr(self.it, 'close', None)) is None else C()) if t is StopAsyncIteration else (True if (T := getattr(self.it, 'throw', None)) is None else T(v))) or True)})): # noqa: ARG005,C901,PLR0912,PLR0915
    audit('asyncutils.base.iter_to_agen', a(it)); f, C = sentinel is _NO_DEFAULT, getcontext()
    if b(it, '__aiter__') and not (C.ITER_TO_AGEN_DEFAULT_STRICT if strict is None else strict):
        if f:
            async for _ in it: yield _
        elif b(it, 'asend', 'athrow', 'aclose'):
            l = await (f := it.asend)(None)
            while not c(l, sentinel): l = await f((yield l))
        else:
            async for l in it:
                if _(l, sentinel): break
                yield l
        return
    elif not b(it, '__iter__'): raise TypeError(f'iter_to_agen: cannot iterate over {it!r} synchronously or asynchronously')
    e, g = None, _(it := iter(it))
    if create_executor is None: create_executor = C.ITER_TO_AGEN_DEFAULT_MAY_CREATE_EXECUTOR
    if C.ITER_TO_AGEN_DEFAULT_USE_EXISTING_EXECUTOR if use_existing_executor is None else use_existing_executor:
        if (e := getattr(iter_to_agen, 'executor', None)) is None:
            if create_executor: e = s(iter_to_agen)
            else: w('iter_to_agen: no existing executor')
    elif create_executor: e = s(iter_to_agen, False)
    with g:
        if e is None:
            if g:
                l = (_ := it.send)(None)
                if f:
                    while True: l = _((yield l))
                else:
                    while not c(l, sentinel): l = _((yield l))
            elif f:
                for i in it: yield i
            else:
                while not c(l := next(it, sentinel), sentinel): yield l
        else:
            def r(*a, _=h().run_in_executor, e=e): return partial(_, e, *a)
            if g:
                l = await (_ := r(it.send))(None)
                if f:
                    while True: l = await _((yield l))
                else:
                    while True:
                        if c(l, sentinel): break
                        l = await _((yield l))
            else:
                _ = r(next, it)
                if f:
                    while True: yield await _()
                else:
                    while True:
                        if c((l := await _()), sentinel): break
                        yield l
def aiter_to_gen(ait, *, use_futures=None, loop=None, strict=None, a=c, b=b):
    audit('asyncutils.base.aiter_to_gen', a(ait)); from asyncio.futures import _chain_future as e; C = getcontext()
    if b(ait, '__iter__') and not (C.AITER_TO_GEN_DEFAULT_STRICT if strict is None else strict): yield from ait; return
    if not b(ait, '__aiter__'): raise TypeError(f'aiter_to_gen: cannot iterate over {ait!r} synchronously or asynchronously')
    c, d = None, b(ait := aiter(ait), 'asend', 'athrow', 'aclose')
    try:
        if (loop := (c := event_loop.from_flags(0)).__enter__() if loop is None else loop).is_running():
            if not (C.AITER_TO_GEN_DEFAULT_ALLOW_FUTURES if use_futures is None else use_futures): raise RuntimeError(f'aiter_to_gen: cannot convert async iterator {ait!r} to sync in running event loop without using futures')
            def f(*a, f, c=loop.create_task, g=e, t=Future): return g(c(f(*a)), F := t()) or F.result()
            if d:
                f, x = partial(f, f=ait.asend), None
                while True: x = yield f(x)
            else:
                f = partial(f, f=ait.__anext__)
                while True: yield f()
        else:
            a = loop.run_until_complete
            if d:
                f, x = ait.asend, None
                while True: x = yield a(f(x))
            else:
                f = ait.__anext__
                while True: yield a(f())
    except StopAsyncIteration: ...
    finally:
        if c: c.__exit__(*exc_info())
async def take(it, n=None, *, default=_NO_DEFAULT, _=L.debug, m='base.take ran out of items'):
    if n is None:
        async for i in iter_to_agen(it): yield i
        return
    async for n, i in aenumerate(it, n-1, step=-1): # noqa: B020,PLR1704
        yield i
        if n == 0: return
    if default is RAISE: raise ItemsExhausted(m)
    if default is _NO_DEFAULT: _(m)
    else:
        for _ in range(n): yield default
async def collect(it, n=None, *, default=_NO_DEFAULT, _='base.collect ran out of items'): return [i async for i in take(it, n, default=default, m=_)]
async def drop(it, n, *, raising=False, _=L.debug, m='base.drop ran out of items'):
    i, it = 0, iter_to_agen(it)
    async for i, _ in aenumerate(it):
        if i >= n: yield _
    if i < n:
        if raising: raise ItemsExhausted(m)
        else: _(m)
async def aenumerate(it, start=0, *, step=1):
    async for _ in iter_to_agen(it): yield start, _; start += step
P.patch_function_signatures((safe_cancel_batch, 'batch, /, *, callback=None, disembowel=False, raising=False'), (iter_to_agen, 'it, sentinel={}, *, use_existing_executor=None, create_executor=None, strict=None'), (aiter_to_gen, 'ait, *, use_futures=None, loop=None, strict=None'), (collect, 'it, n=None, *, default={}'), (take, 'it, n, *, default={}'), (drop, 'it, n, *, raising=False'))
yield_to_event_loop, sleep_forever = object.__new__(type('', (), {'__new__': lambda _: yield_to_event_loop, '__await__': (_ := lambda _: (yield)), **dict.fromkeys(('__repr__', '__str__', '__reduce__'), lambda _, r='asyncutils.base.yield_to_event_loop': r)})), sleep.__get__(float('inf'))
(dummy_task := type(_)(_.__code__.replace(co_flags=0x161), globals())(None)).close()
_.__qualname__ = _.__name__ = 'dummy_task'
del f, _, P, L, b, c, H