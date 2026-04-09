from .constants import RAISE, _NO_DEFAULT
from .exceptions import IgnoreErrors, Critical, ItemsExhausted, CRITICAL, unnest_reverse
from ._internal import patch as P, log as L, helpers as H
from asyncio.coroutines import iscoroutine
from asyncio.events import new_event_loop, _get_running_loop, set_event_loop
from asyncio.tasks import all_tasks, gather, sleep
from sys import exc_info, audit
from ._internal.submodules import base_all as __all__
b = H.check_methods
class event_loop:
    _ENTERED, _SHOULD_CLOSE, _INNER_EXIT, _INNER_AEXIT, _INTERNAL_MASK, __slots__, __reusable = 0x1000, 0x2000, 0x4000, 0x8000, 0xF000, ('_flags', '_loop', '_task'), []
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
    def from_flags(cls, flags, /): (r := object.__new__(cls))._flags = flags; return r
    def __new__(cls, /, *, dont_release_loop_on_finalization=False, silent_on_finalize=False, check_running=False, close_existing_on_exit=False, dont_always_stop_on_exit=False, dont_close_created_on_exit=False, cancel_all_tasks=False, keep_loop=False, suppress_runtime_errors=False, fail_silent=False, dont_allow_reuse=False, dont_reuse=False, dont_attempt_enter=False, attempt_aenter=False, suppress_inner_exit_on_runtime_error=False, suppress_inner_aexit_on_runtime_error=False): return cls.from_flags(dont_release_loop_on_finalization|silent_on_finalize<<1|check_running<<2|close_existing_on_exit<<3|dont_always_stop_on_exit<<4|dont_close_created_on_exit<<5|cancel_all_tasks<<6|keep_loop<<7|suppress_runtime_errors<<8|fail_silent<<9|dont_allow_reuse<<10|dont_reuse<<11|dont_attempt_enter<<16|attempt_aenter<<17|suppress_inner_exit_on_runtime_error<<18|suppress_inner_aexit_on_runtime_error<<19)
    def __enter__(self, _m='event_loop context already entered'):
        if (f := self._flags)&self._ENTERED:
            if f&0x200: return self._loop
            raise RuntimeError(_m)
        if (l := _get_running_loop()) is None: set_event_loop(l := self._get_unclosed_loop())
        elif f&4 and l.is_running(): l = self._get_unclosed_loop()
        else: f |= self._SHOULD_CLOSE
        if not f&0x10000 and callable(g := getattr(l, '__enter__', None)):
            try: g(); f |= self._INNER_EXIT
            except CRITICAL: raise Critical
            except BaseException as e:
                if not f&0x200: raise RuntimeError(f'{type(self).__qualname__}: exception occurred while calling __enter__ of associated event loop: {e}') from e
        if f&0x20000 and callable(g := getattr(l, '__aenter__', None)): l.call_soon(g); f |= self._INNER_AEXIT
        self._loop, self._flags = l, f|self._ENTERED; return l
    def __exit__(self, t, v, b, /, _m='%s context not entered', _n='%s context not entered, errors passed into __exit__', _i=IgnoreErrors(RuntimeError), _l=L): # noqa: PLR0912
        if not (f := self._flags)&(e := self._ENTERED):
            if f&0x200: return False
            N = type(self).__qualname__; raise RuntimeError(_m%N) if v is None else BaseExceptionGroup(_n%N, tuple(unnest_reverse(v))).with_traceback(b)
        f, l = f&~e, self._loop
        if f&0x40: self._task = l.create_task(safe_cancel_batch(all_tasks(l)))
        if not f&0x400: self.__reusable.append(l)
        if not ((c := f&self._SHOULD_CLOSE) and f&0x10):
            with _i: l.stop()
        q, r, self._flags = t is not None and issubclass(t, RuntimeError), False, f&~0xC0000
        if f&self._INNER_EXIT:
            if callable(g := getattr(l, '__exit__', None)):
                try: r = g(None, None, None) if f&0x40000 and q else g(t, v, b)
                except CRITICAL: _l.critical(f'{type(self).__qualname__} at {id(self):#x}: critical error while calling __exit__ of associated event loop', exc_info=True)
                except RuntimeError:
                    if not f&0x100: _l.error('RuntimeError exiting associated event loop', exc_info=True)
                except BaseException:
                    if not f&0x200: _l.error(f'{type(self).__qualname__} at {id(self):#x}: exception occurred while calling __exit__ of associated event loop', exc_info=True)
            elif not f&0x200: _l.error('__enter__ already called but __exit__ is not present')
        if f&self._INNER_AEXIT:
            if callable(g := getattr(l, '__aexit__', None)) and not r:
                try: r = l.run_until_complete(g(None, None, None) if f&0x80000 else g(t, v, b)) # type: ignore
                except CRITICAL: _l.critical(f'{type(self).__qualname__} at {id(self):#x}: critical error while calling __aexit__ of associated event loop', exc_info=True)
                except RuntimeError:
                    if not f&0x100: _l.error('RuntimeError exiting associated event loop', exc_info=True)
                except BaseException:
                    if not f&0x200: _l.error(f'{type(self).__qualname__} at {id(self):#x}: exception occurred while calling __aexit__ of associated event loop', exc_info=True)
            elif not f&0x200: _l.error('__aenter__ already called but __aexit__ is not present')
        if f&8 or not (c or f&0x20):
            with _i: l.close()
            set_event_loop(None)
        if not f&0x80: del self._loop
        return r or (q and bool(f&0x100))
    def __del__(self, _f=L.debug, w=L.warning, _m='garbage-collecting entered %s context; you are advised to refactor your code', _w='cannot suppress exceptions from within %s destructor'):
        b, n = not (f := self._flags)&2, type(self).__qualname__
        if f&self._ENTERED:
            if b: w(_m%n)
            if f&1: self._flags = f^0x400
            if self.__exit__(*exc_info()) and b: w(_w%n)
        elif b: _f(f'destroyed {n} at {id(self):#x}')
    def __reduce__(self, /): return self.from_flags.__func__, (self.__class__, self._flags)
    P.patch_method_signatures((__enter__, ''), (__exit__, 'typ, val, tb, /'), (__del__, ''), (_get_unclosed_loop, 'factory={}'))
def f(n):
    async def adisembowel(it, /):
        if callable(p := getattr(it, n, None)):
            while it: yield p()
            if callable(p := getattr(it, 'clear', None)) and iscoroutine(p := p()): await p
        else:
            async for i in iter_to_aiter(it): yield i
    return adisembowel
adisembowel, adisembowelleft = map(f, ('pop', 'popleft'))
async def safe_cancel_batch(t, *, callback=None, disembowel=False, raising=False):
    audit('asyncutils.base.safe_cancel_batch', t); l = []
    async for _ in (adisembowel if disembowel else iter_to_aiter)(t):
        if not _.done(): _.cancel(); l.append(_) # type: ignore[attr-defined]
    r = await gather(*l, return_exceptions=True)
    if callback is not None:
        async def f(a, /, _=callback): return (await r) if iscoroutine(r := _(a)) else r
        L = len(r := await gather(*map(f, r), return_exceptions=True))
        if raising and (E := tuple(unnest_reverse(*filter(BaseException.__instancecheck__, r)))): raise BaseExceptionGroup(f'safe_cancel_batch: {f"flattened {L} exception (groups)" if len(E) < L else f"collected {L} exceptions"} thrown by callback function {callback!r}', E)
class _iter_to_aiter_error_handler:
    __slots__ = 'it'
    def __init__(self, it): self.it = it
    def __bool__(self, _=b): return _(self.it, 'send', 'throw', 'close')
    def __enter__(self): ...
    def __exit__(self, t, v, b, /, _=frozenset(('StopIteration interacts badly with generators and cannot be raised into a Future', 'async generator raised StopIteration'))): return False if t is None else str(v) in _ if t is RuntimeError else ((self.it.close() if t is StopAsyncIteration else self.it.throw(v)) or True)
def iter_to_aiter(it, sentinel=_NO_DEFAULT, *, use_existing_executor=True, create_executor=False, _c=b, c=H.check, H=H, w=L.debug, _f=_iter_to_aiter_error_handler): # noqa: C901,PLR0912,PLR0915
    # ruff: disable[RUF029]
    audit('asyncutils.base.iter_to_aiter', type(it).__qualname__); f = sentinel is _NO_DEFAULT
    if _c(it, '__aiter__'): # noqa: PLR1702
        if not _c(it := it.__aiter__(), '__anext__'): raise TypeError('__aiter__ did not return an async iterator')
        if f: return it
        if _c(it, 'asend', 'athrow', 'aclose'):
            async def iterator(f=it.asend, c=c): # type: ignore[no-redef]
                l = await f(None)
                while True:
                    if c(l, sentinel): break
                    l = await f((yield l))
        else:
            async def iterator(c=c): # type: ignore[no-redef]
                async for l in it:
                    if c(l, sentinel): break
                    yield l
    elif _c(it, '__iter__') and _c(it := it.__iter__(), '__next__'):
        e, g = None, _f(it)
        if use_existing_executor:
            if (e := getattr(iter_to_aiter, 'executor', None)) is None:
                if create_executor: e = H.create_executor(iter_to_aiter)
                else: w('iter_to_aiter: no existing executor')
        elif create_executor: e = H.create_executor(iter_to_aiter, save=False)
        if e is None:
            if f:
                if g:
                    async def iterator(_=it.send): # type: ignore[no-redef]
                        l = _(None)
                        with g:
                            while True: l = _((yield l))
                else:
                    async def iterator(f=it.__next__): # type: ignore[no-redef]
                        while True: yield f()
            elif g:
                async def iterator(_=it.send, c=c): # type: ignore[no-redef]
                    l = _(None)
                    with g:
                        while True:
                            if c(l, sentinel): break
                            l = _((yield l))
            else:
                async def iterator(_=it.__next__, c=c): # type: ignore[no-redef]
                    while True:
                        if c((l := _()), sentinel): break
                        yield l
        else:
            def r(*a, _=H.get_loop_and_set().run_in_executor, e=e): return __import__('_functools').partial(_, e, *a)
            if f:
                if g:
                    async def iterator(_=r(it.send)): # type: ignore[no-redef]
                        l = await _(None)
                        with g:
                            while True: l = await _((yield l))
                else:
                    async def iterator(_=r(next, it)): # type: ignore[no-redef]
                        while True: yield await _()
            elif g:
                async def iterator(_=r(it.send), c=c): # type: ignore[no-redef]
                    l = await _(None)
                    with g:
                        while True:
                            if c(l, sentinel): break
                            l = await _((yield l))
            else:
                async def iterator(_=r(next, it, sentinel), c=H.check):
                    while True:
                        if c((l := await _()), sentinel): break
                        yield l
    else: raise TypeError('cannot iterate over it synchronously or asynchronously')
    return iterator()
    # ruff: enable[RUF029]
def aiter_to_iter(ait, _c=b):
    audit('asyncutils.base.aiter_to_iter', type(ait).__qualname__)
    if _c(ait, '__iter__') and _c(ait := ait.__iter__(), '__next__'): yield from ait; return
    if _c(ait, '__aiter__') and _c(ait := ait.__aiter__(), '__anext__'):
        a = (c := event_loop.from_flags(4)).__enter__().run_until_complete
        if _c(ait, 'asend', 'athrow', 'aclose'):
            def iterate(f=ait.asend, a=a): # type: ignore[no-redef]
                x = None
                while True: x = yield a(f(x))
        else:
            def iterate(f=ait.__anext__, a=a):
                while True: yield a(f())
        try: yield from iterate()
        except StopAsyncIteration: ...
        finally: c.__exit__(*exc_info())
    else: raise TypeError(f'cannot iterate over {ait!r} synchronously or asynchronously')
async def collect(it, n=None, default=_NO_DEFAULT, *, __reti=False, _=L.warning, m='collect ran out of items'):
    f, i = (r := []).append, 0
    async for i, _ in aenumerate(it):
        if i == n: break
        f(_)
    else:
        if default is RAISE: raise ItemsExhausted(m)
        if default is _NO_DEFAULT: _(m)
        elif n is not None: r.extend(default for _ in range(n-i-1))
    return (r, i) if __reti else r
async def take(it, n, default=_NO_DEFAULT):
    it = iter_to_aiter(it)
    if n is None:
        async for i in it: yield i
        return
    i = 0
    async for i, j in aenumerate(it):
        if i >= n: break
        yield j
    else:
        if default is RAISE: raise ItemsExhausted('take ran out of items')
        if default is not _NO_DEFAULT:
            for _ in range(n-i): yield default
async def drop(it, n, raising=False):
    i = 0
    async for i, _ in aenumerate(it):
        if i >= n: yield _
    if raising and i < n: raise ItemsExhausted('drop ran out of items')
async def aenumerate(it, start=0, *, step=1):
    async for _ in iter_to_aiter(it): yield start, _; start += step
async def sleep_forever(_=float('inf')): await sleep(_)
P.patch_function_signatures((iter_to_aiter, 'it, sentinel={}'), (aiter_to_iter, 'ait'), (collect, 'it, n=None, default={}'), (take, 'it, n, default={}'))
def a(_, r='asyncutils.base.yield_to_event_loop'): return r
yield_to_event_loop = object.__new__(type('', (), {'__new__': lambda _: yield_to_event_loop, '__await__': (_ := lambda _: (yield)), '__repr__': a, '__str__': a, '__reduce__': a}))
(dummy_task := type(_)(_.__code__.replace(co_flags=0x161), globals())(None)).close() # type: ignore[attr-defined]
_.__qualname__ = _.__name__ = 'dummy_task'
del f, _, P, L, b, H, _iter_to_aiter_error_handler