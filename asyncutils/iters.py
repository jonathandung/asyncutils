# ruff: noqa: RUF029
from asyncutils import aenumerate, getcontext, iter_to_agen
from asyncutils.config import _randinst
from asyncutils.constants import _NO_DEFAULT
from asyncutils._internal import py312 as Z, compat as C, helpers as H, patch as P
from asyncutils._internal.submodules import iters_all as __all__
import asyncutils as A, asyncio as B, operator as O, math as M
from collections import Counter, defaultdict, deque
from functools import partial, lru_cache, wraps
from itertools import repeat
from sys import audit, maxsize
from time import monotonic
_rand, _randrange, _sample, _smallprimes, _perfect_test, _identity = _randinst.random, _randinst.randrange, _randinst.sample, frozenset(_littleprimes := (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199)), ((0x7ff, (2,)), (0x8a8d7f, (31, 73)), (0x11baa74c5, (2, 7, 61)), (0x1053cb094c1, (2, 13, 23, 0x195f53)), (0x1f51f3fee3b, _littleprimes[:5]), (0x32907381cdf, _littleprimes[:6]), (1<<64, (2, 0x145, 0x249f, 0x6e12, 0x6e0d7, 0x953d18, 0x6b0191fe)), (0x2be6951adc5b22410a5fd, _littleprimes[:13]), (0x4c16c7697197146a6b8eb49518c5, _littleprimes[:18])), lambda _, /: _
def fmap(fs, /, *a, **k): return agather(f(*a, **k) async for f in iter_to_agen(fs))
async def fmap_sequential(fs, /, *a, **k):
    async for f in iter_to_agen(fs): yield await f(*a, **k)
async def fmap_parallel(fs, /, *a, **k):
    t = H.get_loop_and_set().create_task
    for r in await to_list(t(f(*a, **k)) async for f in iter_to_agen(fs)): yield await r
async def map_on_map(outer, inner, it, *, inner_await=False, outer_await=False):
    async for _ in amap(inner, it, await_=inner_await): yield await to_tuple(amap(outer, _, await_=outer_await))
def aevery(it, n, *, skip_first=False): return aislice(it, skip_first, None, n)
def aeveryother(it, *, skip_first=False): return aevery(it, 2, skip_first=skip_first)
async def agather(it_of_its, return_exceptions=False): return await B.gather(*await to_list(it_of_its), return_exceptions=return_exceptions)
def aawgenf2agenf(f, /):
    async def g(*a, **k):
        async for _ in await f(*a, **k): yield _
    return wraps(f)(g)
async def _tee_helper(Q, i, /): await agather((q.put(i) for q in Q), True)
def tee(it, n=2, *, maxqsize=None, put_exc=None, loop=None, _=_tee_helper):
    if n <= 0: raise ValueError('asyncutils.iters.tee: n must be positive')
    if n == 1: return iter_to_agen(it),
    C = getcontext()
    if loop is None: loop = H.get_loop_and_set()
    if put_exc is None: put_exc = C.TEE_DEFAULT_PUT_EXC
    if maxqsize is None: maxqsize = C.TEE_DEFAULT_MAX_QSIZE
    Q = tuple(Z.Queue(maxqsize) for _ in repeat(None, n))
    async def r(q):
        try:
            while True:
                i = await q.get()
                if put_exc and A.exception_occurred(i): raise A.unwrap_exc(i)
                yield i
        except Z.QueueShutDown:
            nonlocal n; n -= 1
            if n == 0: await A.safe_cancel(t)
    async def f():
        h = _.__get__(Q)
        try: await agather(amap(h, it))
        except A.CRITICAL: raise A.Critical
        except BaseException as e:
            if put_exc: await h(A.wrap_exc(e))
            else:
                for q in Q: q.shutdown(True)
                raise
        finally:
            for q in Q: q.shutdown()
    t = loop.create_task(f()); return tuple(map(r, Q))
async def adouble_starmap(f, it, /, await_=False):
    it = iter_to_agen(it)
    if await_:
        async for _ in it: yield await f(**_)
    else:
        async for _ in it: yield f(**_)
async def astarmap_with_kwds(f, it, /, await_=False):
    it = iter_to_agen(it)
    if await_:
        async for a, k in it: yield await f(*a, **k)
    else:
        async for a, k in it: yield f(*a, **k)
async def aloops(n, i=1024):
    if n is None: n = maxsize
    elif n <= 0: return
    m, n = divmod(n, i)
    for _ in repeat(None, m):
        for _ in repeat(None, i): yield
        await A.yield_to_event_loop
    for _ in repeat(None, n): yield
async def _aunzip_put(*_):
    for q, i in zip(*_, strict=True):
        with A.ignore_qshutdown: await q.put(i)
async def aunzip(ait, *, fillvalue=_NO_DEFAULT, put_batch=None, maxqsize=None, _a=_aunzip_put, _b=_identity):
    audit('asyncutils.iters.aunzip', H.fullname(ait)); l = len(t := await anext(ait := iter_to_agen(ait), ())); C = getcontext()
    if maxqsize is None: maxqsize = C.AUNZIP_DEFAULT_MAX_QSIZE
    if put_batch is None: put_batch = C.AUNZIP_DEFAULT_PUT_BATCH
    if maxqsize < put_batch: raise ValueError('asyncutils.iters.aunzip: maxqsize cannot be less than put_batch')
    f = partial(Z.Queue, maxqsize)
    class AUnzipConsumer:
        __slots__ = '__q',
        def __init__(self): self.__q = f()
        async def __anext__(self, l=B.Lock(), f=partial(A.take, ait, put_batch, default=A.RAISE)): # noqa: B008
            if self.__q.empty():
                async with l:
                    try:
                        async for _ in f(): await _a(Q, _)
                    except A.ItemsExhausted:
                        for q in Q: q.close()
            try: r = await self.__q.get()
            except Z.QueueShutDown: raise StopAsyncIteration from None
            if r is fillvalue: raise StopAsyncIteration
            return r
        def close(self): self.__q.shutdown()
        __aiter__, __anext__.__text_signature__ = _b, '($self)' # ty: ignore[unresolved-attribute]
    await _a(Q := await to_tuple(AUnzipConsumer() async for _ in aloops(l)), t); return Q
async def merge(*I, reverse=False, maxqsize=None, _=lambda p: lambda i: aconsume(amap(p, i, await_=True))):
    audit('asyncutils.iters.merge', I); p, g, l, a = (q := (Z.LifoQueue if reverse else Z.Queue)(getcontext().MERGE_DEFAULT_MAX_QSIZE if maxqsize is None else maxqsize)).put, q.get, H.get_loop_and_set(), object()
    async def close():
        await B.gather(*map(_(p), I))
        if not reverse: await p(a)
    if reverse: q.put_nowait(a)
    t = l.create_task(close())
    if reverse: await t
    while True:
        if (c := await g()) is a: break
        yield c
def aflatten(it, _=A.AChain.from_iterable): return aiter(_(it))
def acountdown(n, step=1, *, include_zero=False): return arange(n, -include_zero, -step)
async def _atraverse(s, n, q, f, i, /):
    a, c, g = (v := {s}).add, v.__contains__, q.append
    if i: yield s
    while q:
        async for _ in afilterfalse(c, n(f())): a(_); g(_); yield _
def abfs(start, neighbours, *, _=_atraverse, include_start=True): return _(start, lambda x, /, _=neighbours: areversed(_(x)), q := deque((start,)), q.popleft, include_start)
def adfs(start, neighbours, *, _=_atraverse, include_start=True): return _(start, neighbours, q := [start], q.pop, include_start)
async def asattolo(it, /, _=_randrange):
    i = len(a := await to_list(it))
    while i > 1:
        i -= 1
        a[j], a[i] = a[i], a[j := _(i)]
    return a
async def abrent(f, s, /):
    p = l = 1; t, h, m = s, await f(s), 0
    while t is not h:
        if p == l: t, l, p = h, 0, p<<1
        h, l = await f(h), l+1
    a = s, await A.iterf(l)(f)(s)
    while a[0] is not a[1]: a, m = await B.gather(*map(f, a)), m+1
    return a[0], l, m
async def asamplel(it, k, *, rrange=_randrange, rand=_rand):
    if k < 0: raise ValueError('asyncutils.iters.asamplel: expected non-negative sample size')
    if k == 0: return []
    R, W, i = await A.collect(it := iter_to_agen(it), k, default=A.RAISE), 1.0, k
    while True:
        W *= rand()**(1.0/k); i += (s := M.floor(M.log(rand(), 1-W))+1)
        try: R[rrange(k)] = await anth(it, s)
        except A.ItemsExhausted: return R
async def asample_weighted(it, k, *, rrange=_randrange, rand=_rand):
    if k < 0: raise ValueError('asyncutils.iters.asample_weighted: expected non-negative sample size')
    if k == 0: return []
    W, u, p = 0.0, rand(), 1.0
    async def agen(it):
        nonlocal W
        async for i, w in iter_to_agen(it):
            if w < 0: raise ValueError(f'asyncutils.iters.asample_weighted: weight {w} for item {i!r} is negative')
            W += w; yield i, w
    r = await A.collect(it := agen(it), k, default=A.RAISE)
    async for i, w in it:
        w /= W; u -= w*p; p *= 1-w # noqa: PLW2901
        if u <= 0: r[rrange(k)], u, p = i, rand(), 1.0
    return r
async def astarfilter(pred, it):
    if pred is None: pred = bool
    async for t in iter_to_agen(it):
        if (await r) if B.iscoroutine(r := pred(*await to_list(t))) else r: yield t
async def astarfilterfalse(pred, it):
    if pred is None: pred = bool
    async for t in iter_to_agen(it):
        if B.iscoroutine(r := pred(*await to_list(t))): r = await r
        if not r: yield t
def amultistarfilter(pred, /, *its, strict=False): return astarfilter(pred, azip(*its, strict=strict))
async def amultistarfilterfalse(pred, /, *its, strict=False): return astarfilterfalse(pred, azip(*its, strict=strict))
def amultifilter(pred, /, *its, strict=False): return afilter(pred, azip(*its, strict=strict))
def amultifilterfalse(pred, /, *its, strict=False): return afilterfalse(pred, azip(*its, strict=strict))
def ahamming_dist(i1, i2, /, cmpeq=H.check): return ailen(amultistarfilterfalse(cmpeq, i1, i2))
async def amerge_sorted_by(its, *, key=_identity, await_=False, reverse=False, _=A.ignore_stop_async_iteration):
    f = (h := []).append
    for i, it in enumerate(its := await to_tuple(amap(iter_to_agen, its))):
        with _:
            k = key(v := await anext(it))
            f(((await k) if await_ else k, i, v))
    if reverse: from asyncutils._internal.compat import heapify as a, heappop as b, heappush as c
    else: from heapq import heapify as a, heappop as b, heappush as c
    a(h)
    while h:
        k, i, v = b(h); yield v
        with _:
            k = key(v := await anext(its[i]))
            c(h, ((await k) if await_ else k, i, v))
async def batch(it, n, *, item_timeout=None, strict=False):
    f, g, _ = iter_to_agen(it).__anext__, (b := []).append, 0
    while True:
        for _ in range(n):
            try: g(await B.wait_for(f(), item_timeout))
            except StopAsyncIteration: break
            except TimeoutError:
                if b: break
        if b:
            if strict and _ < n-1: raise ValueError('asyncutils.iters.batch: incomplete batch')
            yield H.copy_and_clear(b)
def batch2(it, n, strict=False): return A.aiter_from_f(partial(A.collect, it, n, default=A.RAISE if strict else _NO_DEFAULT), [])
async def aside_effect(f, it, size=None, *, await_=True):
    if size is None:
        it = iter_to_agen(it)
        if await_:
            async for i in it: await f(i); yield i
        else:
            async for i in it: f(i); yield i
    else:
        it = batch(it, size)
        if await_:
            async for i in it:
                await f(i)
                for _ in i: yield _
        else:
            async for i in it:
                f(i)
                for _ in i: yield _
def asliced(seq, n, strict=False):
    I = atakewhile(None, (seq[i:i+n] async for i in acount(step=n)))
    if not strict: return I
    async def r():
        async for s in I:
            if len(s) != n: raise ValueError(f'asyncutils.iters.asliced: length of {seq!r} is not divisible by {n}')
            yield s
    return r()
async def _buffer_consume(g, d, f, t, c, /):
    x = t+c()
    while True:
        yield await g(); d()
        if c() > x: await f(); x = t+c()
def buffer(it, maxsize=0, *, timeout_get=None, timeout_put=None, cooldown=0.0, _=_buffer_consume):
    q = Z.Queue(maxsize)
    async def cons():
        try:
            async for i in _(q.get, q.task_done, B.sleep.__get__(cooldown), float('inf') if timeout_get is None else timeout_get, monotonic): yield i
        finally: await A.safe_cancel(t)
    async def prod(p=q.put):
        try:
            async for _ in iter_to_agen(it):
                try: await B.wait_for(p(_), timeout_put)
                except TimeoutError: break
        finally: c.close()
    c, t = cons(), H.get_loop_and_set().create_task(prod()); return c
async def asplitat(it, pred, maxsplit=-1, keep_sep=False):
    I, f = iter_to_agen(it), (b := []).append
    if not maxsplit: yield await to_list(I); return
    async for i in I:
        if not pred(i): f(i); continue
        yield b
        if keep_sep: yield [i]
        if maxsplit == 1: yield await to_list(I); return
        f = (b := []).append; maxsplit -= 1
    yield b
def batch_process(items, size, processor): return amap(processor, batch(items, size), await_=True)
async def window(it, size, step=1):
    if not size >= 1 <= step: raise ValueError('asyncutils.iters.window: size and step should both be >=1')
    a, c = (b := deque(maxlen=size)).append, 0
    async for i in iter_to_agen(it):
        a(i)
        if len(b) == size:
            if not c%step and (t := (yield tuple(b))) is not None: size, step = t
            c += 1
async def aall(it):
    async for _ in iter_to_agen(it):
        if not _: return False
    return True
async def aany(it):
    async for _ in iter_to_agen(it):
        if _: return True
    return False
async def aisempty(it):
    async for _ in iter_to_agen(it): return False
    return True
async def _aextreme(I, K, c, d=_NO_DEFAULT, /):
    if (r := await anext(I := iter_to_agen(I[0] if len(I) == 1 else I), _NO_DEFAULT)) is _NO_DEFAULT:
        if d is _NO_DEFAULT: raise ValueError('empty (async) iterable passed to asyncutils.iters.amax or asyncutils.iters.amin with no default value')
        return d
    k = K(r)
    async for i in I:
        if c(x := K(i), k): k, r = x, i
    return r
def amax(*it, key=_identity, default=_NO_DEFAULT, _=_aextreme): return _(it, key, O.gt, default)
def amin(*it, key=_identity, default=_NO_DEFAULT, _=_aextreme): return _(it, key, O.lt, default)
async def azip(*I, strict=False, _=A.ignore_stop_async_iteration.combined(RuntimeError)): # noqa: B008
    I = tuple(map(iter_to_agen, I))
    with _:
        while True: yield tuple(await B.gather(*map(anext, I))) # noqa: ASYNC119
    if not strict: return
    for x, y in enumerate(I):
        with _: await anext(y); raise ValueError(f'asyncutils.iters.azip: iterable {x} longer than shortest iterable')
async def amap(f, /, *its, await_=False, strict=False):
    it = azip(*its, strict=strict)
    if await_:
        async for _ in it: yield await f(*_)
    else:
        async for _ in it: yield f(*_)
async def afilter(f, it):
    if f is None: f = bool
    async for _ in iter_to_agen(it):
        if B.iscoroutine(r := f(_)): r = await r
        if r: yield _
def amapif(f, p, it, /, await_=False): return amap(f, afilter(p, it), await_)
def amultimapif(f, p, /, *its, await_=False): return astarmap(f, afilter(p, azip(*its)), await_)
def arange(*a): return iter_to_agen(range(*a))
async def acount(start=0, step=1):
    if isinstance(step, float):
        if step.is_integer(): step = int(step)
        else: start = float(start)
    elif start.is_integer(): start = int(start)
    while True: yield start; start += step
async def acycle(it):
    if type(it) in C.s: l = tuple(it)
    else:
        a = (l := []).append
        async for i in iter_to_agen(it): yield i; a(i)
        l = tuple(l)
    del it
    while True:
        for i in l: yield i
async def arepeat(elem, n=None):
    if n is None or n < 0:
        while True: yield elem
    else:
        while n: yield elem; n -= 1
async def aaccumulate(it, func=O.add, *, initial=None):
    it = iter_to_agen(it)
    if initial is None:
        try: initial = await anext(it)
        except StopAsyncIteration: return
    yield initial
    async for _ in it: yield (initial := func(initial, _))
async def acompress(data, selectors):
    async for i, j in azip(data, selectors):
        if j: yield i
async def adropwhile(pred, it, *, skip_first=False):
    async for _ in (it := iter_to_agen(it)):
        if pred(_): continue
        if not skip_first: yield _
        break
    async for _ in it: yield _
async def ac3merge(seqs):
    seqs, g, d, c = await to_list(afilter(None, seqs)), (n := []).append, n.clear, None
    while seqs:
        for s in seqs:
            c = s[0]
            for t in seqs:
                next(t := iter(t))
                if any(H.check(_, c) for _ in t): c = None; break
            else: break
        if c is None: raise ValueError('asyncutils.iters.ac3merge: cannot resolve sequences')
        yield c
        for s in seqs:
            if s[0] == c: del s[0]
            if s: g(s)
        seqs = tuple(n); d()
def afilterfalse(f, it): return afilter(lambda i: not (f or bool)(i), it)
async def agroupby(it, key=_identity, await_=False):
    it, e = iter_to_agen(it), False
    async def grouper(k):
        nonlocal cv, ck, e; yield cv
        async for cv in it:
            ck = key(cv)
            if await_: ck = await ck
            if ck != k: return
            yield cv
        e = True
    try:
        ck = key(cv := await anext(it))
        if await_: ck = await ck
    except StopAsyncIteration: return
    while not e:
        yield ck, (g := grouper(t := ck))
        if ck == t: await aconsume(g)
async def aislice(it, /, *a, _=lambda x: x if x is None else int(x, 0) if isinstance(x, str) else int(x)):
    x, y, z = 0 if (s := slice(*map(_, a))).start is None else s.start, s.stop, 1 if s.step is None else s.step
    if x < 0 or (y is not None and y < 0) or z <= 0: raise ValueError(f'asyncutils.iters.aislice: start={x}, stop={y}, step={z} is invalid')
    async for i, j in azip(acount() if y is None else arange(max(x, y)), it):
        if i == x: yield j; x += z
async def aiter_idx(it, value, start=0, stop=None, _=H.check):
    async for i, j in aenumerate(aislice(it, start, stop), start):
        if _(j, value): yield i
async def asieve(n):
    if n < 2: return # noqa: PLR2004
    yield 2; s, d = 3, bytearray((0, 1))*(n>>1)
    async for p in aiter_idx(d, 1, s, M.isqrt(n)+1):
        async for i in aiter_idx(d, 1, s, s := p*p): yield i
        d[s:n:x] = bytes(len(range(s, n, x := p<<1)))
    async for i in aiter_idx(d, 1, s): yield i
async def apairwise(it):
    try: a = await anext(I := iter_to_agen(it))
    except StopAsyncIteration: return
    async for b in I: yield a, b; a = b
@aawgenf2agenf
async def atriplewise(it):
    a, b, c = tee(iter_to_agen(it), 3, maxqsize=3); await B.gather(*(anext(g, None) for g in (b, c, c)))
    return azip(a, b, c)
async def aproduct(*its, repeat=1):
    if repeat < 0: raise ValueError('asyncutils.iters.aproduct: repeat cannot be negative')
    r = [()]
    async for p in arepeat(amap(to_tuple, its, await_=True), repeat): r = [(*x, y) for x in r async for y in p]
    for _ in r: yield _
async def astarmap(f, it, /, await_=False):
    it = iter_to_agen(it)
    if await_:
        async for _ in it: yield await f(*_)
    else:
        async for _ in it: yield f(*_)
async def atakewhile(pred, it):
    if pred is None: pred = bool
    async for _ in iter_to_agen(it):
        if not pred(_): break
        yield _
async def atakewhile_inclusive(pred, it):
    if pred is None: pred = bool
    async for _ in iter_to_agen(it):
        yield _
        if not pred(_): break
async def atakeuntil(pred, it):
    if pred is None: pred = bool
    async for _ in iter_to_agen(it):
        if pred(_): break
        yield _
async def atakeuntil_inclusive(pred, it):
    if pred is None: pred = bool
    async for _ in iter_to_agen(it):
        yield _
        if pred(_): break
def asquaresum(it): return asumprod(*tee(it))
async def aziplongest(*its, fillvalue=None):
    n = len(I := list(map(iter_to_agen, its)))
    while True:
        f = (v := []).append
        for i, a in enumerate(I):
            try: _ = await anext(a)
            except StopAsyncIteration:
                n -= 1
                if not n: return
                I[i], _ = arepeat(fillvalue), fillvalue
            f(_)
        yield tuple(v)
def asumprod(p, q, /): return asum(amap(O.mul, p, q, strict=True))
async def aconvolve(signal, kernel, _=A.AChain):
    f = (w := deque((0,), n := len(K := await to_tuple(areversed(kernel))))*n).append
    async for x in _(signal, arepeat(0, n-1)): f(x); yield await asumprod(K, w)
def atabulate(f, start=0, step=1, /, *, await_=False): return amap(f, acount(start, step), await_=await_)
async def asum(it, start=0):
    async for i in iter_to_agen(it): start += i
    return start
async def aprod(it, start=1):
    async for i in iter_to_agen(it): start *= i
    return start
async def amatprod(it, start):
    async for i in iter_to_agen(it): start @= i
    return start
def atail(n, it, /): return aislice(it, max(0, len(it)-n), None)
async def to_tuple(it, /): return tuple(await to_list(it))
async def to_set(it, /, frozen=False): r = await A.transient_block(H.get_loop_and_set(), set, it) if type(it) in C.s else {_ async for _ in iter_to_agen(it)}; return frozenset(r) if frozen else r
async def to_list(it, /): return await A.transient_block(H.get_loop_and_set(), list, it) if type(it) in C.s else [_ async for _ in iter_to_agen(it)]
async def aconsume(it, n=None, _=H.check_methods):
    if n == 0: return
    if n: it = A.take(it, n, default=A.RAISE)
    if _(it, '__iter__'): await H.get_loop_and_set().run_in_executor(H.create_executor(aconsume) if (E := getattr(aconsume, 'executor', None)) is None else E, deque, it, 0)
    else:
        async for _ in it: ...
def anth(it, n, default=_NO_DEFAULT): return anext(aislice(it, n, None), *H.filter_out(default, s=_NO_DEFAULT))
async def aallequal(it, key=_identity, strict=False):
    async for _ in (it := agroupby(it, key)):
        async for _ in it: return False
        return True
    if strict: raise ValueError('asyncutils.aallequal: iterable cannot be empty with strict=True')
    return True
async def acombinations(it, r):
    if r > (n := len(p := await to_tuple(it))): return
    I = list(range(r)); yield p[:r]
    while True:
        for i in range(r-1, -1, -1):
            if I[i] != i+n-r: break
        else: return
        I[i] += 1
        for j in range(i+1, r): I[j] = I[j-1]+1
        yield tuple(p[i] for i in I)
async def acombinations_with_replacement(it, r):
    if not (n := len(p := await to_tuple(it))) and r: return
    I = [0]*r; yield (p[0],)*r
    while True:
        for i in range(r-1, -1, -1):
            if I[i] != n-1: break
        else: return
        I[i:] = (I[i]+1,)*(r-i); yield tuple(p[i] for i in I)
async def apermutations(it, r=None):
    n = len(p := await to_tuple(it))
    if (r := n if r is None else r) > n: return
    I, C, x = list(range(n)), list(range(n, n-r, -1)), r-1; yield p[:r]
    while n:
        for i in range(x, -1, -1):
            C[i] -= 1
            if C[i]: I[i], I[-j] = I[-(j := C[i])], I[i]; yield tuple(p[i] for i in I[:r]); break
            else: I[i:], C[i] = I[i+1:]+I[i:i+1], n-i
        else: return
@aawgenf2agenf
async def apowerset(it): s = await to_tuple(it); return aflatten(acombinations(s, r) for r in range(len(s)+1))
def aquantify(it, pred=bool): return asum(amap(pred, it))
async def apadded(it, fillvalue, n=None):
    if n is None:
        async for i in iter_to_agen(it): yield i
        while True: yield fillvalue
    async for n, j in A.aenumerate(it, n-1, step=-1): yield j # noqa: B007,B020,PLR1704
    async for _ in aloops(n): yield fillvalue
def apadnone(it, n=None): return apadded(it, None, n)
def agrouper(it, n, fillvalue=_NO_DEFAULT): I = (iter_to_agen(it),)*n; return azip(*I, strict=fillvalue is A.RAISE) if isinstance(fillvalue, type(A.RAISE)) else aziplongest(*I, fillvalue=fillvalue)
async def aroundrobin(*its):
    I = (iter_to_agen(i) for i in its)
    for i in range(len(its), 0, -1):
        async for _ in (I := acycle(aislice(I, i))): yield await anext(_)
def aroundrobin2(*its): return afilter(partial(O.is_not, _NO_DEFAULT), aflatten(aziplongest(*its, fillvalue=_NO_DEFAULT)))
async def aunique_everseen(it, key=_identity):
    A, a = (S := set()).add, (s := []).append
    async for i in iter_to_agen(it):
        k = key(i)
        try:
            if k not in S: A(k); yield i
        except TypeError:
            if k not in s: a(k); yield i
def aunique_justseen(it, key=_identity, _=O.itemgetter): return amap(_(0), agroupby(it)) if key is None else amap(anext, amap(_(1), agroupby(it, key)), await_=True)
@aawgenf2agenf
async def aunique(it, key=None, reverse=False): return aunique_justseen(await asorted(it, key=key, reverse=reverse), key)
@aawgenf2agenf
async def ancycles(it, n): return aflatten(arepeat(await to_tuple(it), n))
def apartition(pred, it):
    if pred is None: pred = bool
    async def agen(q, _=iter_to_agen(it).__anext__): # noqa: B008
        p = q.popleft
        while True:
            while q: yield p()
            try: (T if pred(v := await _()) else F).append(v)
            except StopAsyncIteration: return
    return map(agen, (F := deque(), T := deque()))
async def aiterexcept(f, exc, first=None):
    if first is not None: yield await first()
    with A.IgnoreErrors(exc):
        while True: yield await f() # noqa: ASYNC119
async def ailen(it):
    i = 0
    async for _ in iter_to_agen(it): i += 1
    return i
async def aiterate(f, start):
    while True: yield start; start = await f(start)
async def asorted(it, *, key=_identity, reverse=False):
    from heapq import heappop as g, heapify as f
    b, a = (m := []).append, (r := []).append
    async for i, j in aenumerate(it): b((key(j), i, j))
    f(m)
    while m: a(g(m))
    if reverse: r.reverse()
    return r
def acanonical(it): return asorted(it, key=id, reverse=True)
async def _adpermfull(a, _):
    while True:
        yield tuple(a)
        async for i in arange(_-2, -1, -1):
            if a[i] < a[i+1]: break
        else: return
        async for j in arange(j := _-1, i, -1): # noqa: B020
            if a[i] < a[j]: break
        a[i], a[j] = a[j], a[i]; a[i+1:] = a[:i-_:-1]
async def _adpermpartial(a, _):
    h, R, l = a[:_], range(_-1, -1, -1), range(len(t := a[_:]))
    while True:
        yield tuple(h); p = t[-1]
        for i in R:
            if h[i] < p: break
            p = h[i]
        else: return
        p = h[i]
        for j in l:
            if (c := t[j]) > p: h[i], t[j] = c, p; break
        else:
            for j in R:
                if (c := h[j]) > p: h[i], h[j] = c, p; break
        t += h[:-(x := _-i):-1]; i += 1; h[i:], t[:] = t[:x], t[x:]; await A.yield_to_event_loop
async def empty_agen():
    if False: yield
async def agives(x, /): yield x
@aawgenf2agenf
async def adistinct_permutations(it, r=None, f=(_adpermpartial, _adpermfull)):
    if (S := len(I := await to_list(it))) < (_ := S if r is None else r): return agives(())
    if _ <= 0: return empty_agen()
    a = f[_ == S]
    try: I.sort(); return a(I, _)
    except TypeError:
        d = defaultdict(list)
        for i in I: d[I.index(i)].append(i)
        return amap(lambda i, E={k: acycle(v) for k, v in d.items()}: to_tuple(await anext(E[_]) for _ in i), a(await asorted(amap(I.index, I)), _), await_=True) # noqa: B008
async def aunique_to_each(*its):
    p = frozenset(await to_list(amap(to_tuple, its, await_=True)))
    for i, j in Counter(await to_list(aflatten(map(frozenset, p)))).items():
        if j == 1 and i in p: yield i
async def aderangements(it, r=None):
    async for _ in acompress(apermutations(X := await to_tuple(it), r), amap(aall, amap(partial(amap, O.is_not), arepeat(Y := tuple(range(len(X)))), apermutations(Y, r)), await_=True)): yield _
def aintersperse(e, it, n=1):
    if n <= 0: raise ValueError('asyncutils.iters.aintersperse: n must be positive')
    return aislice(ainterleave_stopearly(arepeat(e), it), 1, None) if n == 1 else aflatten(aislice(ainterleave_stopearly(arepeat((e,)), batch(it, n)), 1, None))
def ainterleave_stopearly(*its): return aflatten(azip(*its))
def aspy(it, n=1): p, q = tee(it, maxqsize=n); return A.take(q, n), p
async def ainterleave_evenly(its, lengths=None):
    I = await to_tuple(its)
    try:
        if (X := len(I)) != len(L := await to_tuple(lengths or map(len, I))): raise ValueError('asyncutils.iters.ainterleave_evenly: mismatch in length of its and lengths')
    except TypeError: raise ValueError('asyncutils.iters.ainterleave_evenly: cannot determine lengths of (async) iterables') from None
    A, *a = map(f := L.__getitem__, _ := sorted(range(X), key=f, reverse=True)); B, *b = (iter_to_agen(I[i]) for i in _); E, t = [A//X]*len(a), sum(L)
    while t:
        yield await anext(B); t -= 1; E[:] = map(O.sub, E, a)
        for i, e in enumerate(E):
            if e < 0: yield await anext(b[i]); t -= 1; E[i] += A
async def ainterleave_randomly(its, _=_randrange):
    x = len(I := await to_list(amap(iter_to_agen, its)))
    while x:
        i = _(x)
        try: yield await anext(I[i])
        except StopAsyncIteration: I[i] = I[-1]; del I[-1]; x -= 1
async def acollapse(it, base_typ=(str, bytes), levels=None):
    if levels is None: levels = float('inf')
    (g := (s := deque()).appendleft)((0, arepeat(iter_to_agen(it), 1))); f = s.popleft
    while s:
        l, n = N = f()
        if l > levels:
            async for i in n: yield i
            continue
        async for _ in n:
            if isinstance(_, base_typ): yield _
            else:
                try: t = iter_to_agen(_); g((l+1, t)); g(N); break
                except TypeError: yield _
def afirsttrue(it, default=_NO_DEFAULT, pred=None): return anext(afilter(pred, it), *H.filter_out(default, s=_NO_DEFAULT))
def afirstfalse(it, default=_NO_DEFAULT, pred=None): return anext(afilterfalse(pred, it), *H.filter_out(default, s=_NO_DEFAULT))
async def aprepend(val, it):
    yield val
    async for i in iter_to_agen(it): yield i
async def aappend(val, it):
    async for i in iter_to_agen(it): yield i
    yield val
async def awrap(it, start, end):
    yield start
    async for i in iter_to_agen(it): yield i
    yield end
async def arandom_product(*a, n=1, _=_randinst.choice):
    async for i in ancycles(amap(to_tuple, a, await_=True), n): yield _(i)
async def arandom_combination(it, r, _=_sample):
    (_ := _(range(len(p := await to_tuple(it))), r)).sort()
    for i in _: yield p[i]
@aawgenf2agenf
async def arandom_combination_with_replacement(it, r, _=_randrange): return amap((p := await to_tuple(it)).__getitem__, await asorted(arepeat_func(_, r, len(p))))
async def arandom_permutation(it, r=None, _=_sample):
    p = await to_tuple(it)
    if r is None: r = len(p)
    for i in _(p, r): yield i
async def afirst(it, default=_NO_DEFAULT):
    async for i in iter_to_agen(it): return i
    if default is _NO_DEFAULT: raise ValueError('asyncutils.iters.afirst called on empty iterable without default value')
    return default
async def alast(it, default=_NO_DEFAULT, _=H.check_methods):
    try:
        if _(it, '__getitem__'): return it[-1]
        return (await to_list(it)).pop() if (f := getattr(it, '__reversed__', None)) is None else next(f())
    except (IndexError, TypeError, StopIteration, StopAsyncIteration):
        if default is _NO_DEFAULT: raise ValueError('asyncutils.iters.alast called on empty iterable without default value') from None
        return default
def anth_or_last(it, n, default=_NO_DEFAULT): return alast(aislice(it, n+1), default)
async def awrapf(it, before=None, after=None):
    if before is not None:
        r = before()
        with A.ignore_typeerrs: await r
    it = iter_to_agen(it)
    try:
        async for i in it: yield i
    finally:
        if after is not None:
            r = after()
            with A.ignore_typeerrs: await r
def abefore_and_after(pred, it): a, b = tee(it); return acompress(atakewhile(pred, a), azip(b)), b
async def anth_combination(it, r, idx):
    if not 0 <= r <= (n := len(p := await to_tuple(it))): raise IndexError(f'asyncutils.iters.anth_combination: {r=} is out of range')
    c, k = 1, min(r, n-r)
    for i in range(1, k+1): c = c*(n-k+i)//i
    if idx < 0: idx += c
    if idx < 0 or idx >= c: raise IndexError(f'asyncutils.iters.anth_combination: {idx=} is out of range')
    while r:
        c, n, r = c*r//n, n-1, r-1
        while idx >= c: idx -= c; c, n = c*(n-r)//n, n-1
        yield p[~n]
@aawgenf2agenf
async def asubslices(it): return astarmap(O.getitem, azip(arepeat(s := await to_tuple(it)), astarmap(slice, acombinations(range(len(s)+1), 2))))
async def arepeat_func(f, n=None, /, *a):
    async def g(i=A.ignore_typeerrs, _=partial(f, *a)): # noqa: B008
        r = _()
        with i: r = await r
    async for _ in aloops(n): await g()
async def apolynomial_from_roots(roots, _=(1,)):
    async for r in iter_to_agen(roots): _ = aconvolve(_, (1, -r))
    async for i in iter_to_agen(_): yield i
@aawgenf2agenf
async def atranspose(mat): return azip(*await to_list(mat), strict=True)
@aawgenf2agenf
async def aflatten_tensor(tensor, base_typ=(str, bytes), _=H.check_methods):
    I = iter_to_agen(tensor)
    while True:
        try: v = await anext(I)
        except StopAsyncIteration: break
        I = aprepend(v, I)
        if isinstance(v, base_typ) or not (_(v, '__iter__') or _(v, '__aiter__')): break
        I = aflatten(I)
    return I
@aawgenf2agenf
async def apolynomial_derivative(coeff): return amap(O.mul, r := await to_tuple(coeff), range(len(r)-1, 0))
async def apolynomial_eval(coeff, x):
    if not (n := len(t := await to_tuple(coeff))): return type(x)(0)
    return await asumprod(t, areversed(await A.collect(apowers(x), n-1)))
@aawgenf2agenf
async def areshape(mat, shape):
    if isinstance(shape, int): return batch(aflatten(mat), shape)
    d = await anext(shape := iter_to_agen(shape)); return aislice(await A.areduce(batch, areversed(shape), aflatten_tensor(mat), await_=False), d)
async def _factor_pollard(n):
    if n == 4: return 2 # noqa: PLR2004
    async for b in arange(1, n):
        x = y = 2; d = 1
        while (d := M.gcd((x := (x*x+b)%n)-(y := ((z := (y*y+b)%n)*z+b)%n), n)) == 1: ...
        if d != n: return d
    raise ValueError(f'asyncutils.iters.afactor: internal error: {n} is prime')
@lru_cache
def _shift_to_odd(n):
    if not ((1<<(s := ((n-1)^n).bit_length()-1))*(d := n>>s) == n and d&1 and s > -1): raise ValueError(f'asyncutils.iters.aisprime: internal error: {n} is invalid')
    return s-1, d
async def _probable_prime(n, base, _=_shift_to_odd):
    s, d = _(m := n-1)
    if (x := pow(base, d, n)) in {1, m}: return True
    async for _ in aloops(s):
        if (x := x*x%n) == m: return True
    return False
async def aisprime(n, s=_smallprimes, p=_perfect_test, r=_randrange, f=_probable_prime):
    if n < 210: return n in s # noqa: PLR2004
    if not (n&1 and n%3 and n%5 and n%7 and n%11 and n%13 and n%17): return False
    for l, _ in p:
        if n < l: break
    else: _ = arepeat_func(r, 64, 2, n-1)
    return await aall(amap(partial(f, n), _, await_=True))
async def afactor(n, _=_littleprimes, F=_factor_pollard):
    if n < 1: raise ValueError('asyncutils.iters.afactor: no prime factors')
    if n == 1: return
    for p in _:
        while not n%p: yield p; n //= p
    if n == 1: return
    e = (t := [n]).extend
    for n in t:
        if n < 44521 or await aisprime(n): yield n # noqa: PLR2004
        else: e((f := await F(n), n//f))
async def arunning_median(it, *, maxlen=None):
    if maxlen is None:
        r, l, h = iter_to_agen(it).__anext__, [], []; from asyncutils._internal.compat import heappush as a, heappushpop as c; from heapq import heappush as b
        while True: a(l, await r()); yield l[0]; b(h, c(l, await r())); yield (l[0]+h[0])/2
    if (m := O.index(maxlen)) <= 0: raise ValueError('asyncutils.iters.arunning_median: window size should be positive')
    w, o = deque(), []; from bisect import bisect_left as b, insort_right as f
    async for i in iter_to_agen(it):
        w.append(i); f(o, i)
        if (n := len(o)) > m: del o[b(o, w.popleft())]; n -= 1
        m = n>>1; yield o[m] if n&1 else (o[m-1]+o[m])/2
async def arandom_derangement(it, _=_randinst.shuffle):
    if (l := len(s := await to_tuple(it))) < 2: # noqa: PLR2004
        if s: raise ValueError('asyncutils.iters.arandom_derangement: no derangements to choose from')
        return ()
    i = tuple(p := list(range(l)))
    while any(map(O.is_, i, p)): _(p)
    return O.itemgetter(*p)(s)
@aawgenf2agenf
async def amatmul(*a):
    M, N = map(iter_to_agen, a); N = aprepend(t := await to_tuple(await anext(N)), N)
    return batch(astarmap(asumprod, aproduct(M, atranspose(N)), True), len(t))
@aawgenf2agenf
async def mat_vec_mul(M, V): return amap(asumprod.__get__(await to_tuple(V)), amap(to_tuple, M, await_=True), await_=True)
async def vecs_eq(u, v, cmpeq=H.check, *, strict=True):
    try: return await aall(amap(cmpeq, u, v, strict=strict))
    except ValueError: return False
async def afreivalds(A, B, C, k=None, _r=_randrange): n = len(A := await to_tuple(A)); return await aall(await vecs_eq(mat_vec_mul(A, mat_vec_mul(B, r := await to_tuple(arepeat_func(_r, n, 2)))), mat_vec_mul(C, r), int.__eq__) async for _ in aloops(getcontext().AFREIVALDS_DEFAULT_K if k is None else k))
def basic_collect(*_): return to_list(aislice(*_) if len(_) > 1 else _[0])
async def asubstrings(it):
    for i in (s := await to_tuple(it)): yield i,
    async for n in arange(2, c := len(s)+1):
        async for i in arange(c-n): yield s[i:i+n]
def asubstr_indices(seq, reverse=False):
    r = range(1, x := len(seq)+1)
    if reverse: r = reversed(r)
    return ((seq[i:(j := i+L)], i, j) for L in r async for i in arange(x-L))
def iter_task(it, summaryf=aconsume):
    async def task(f): t = f(); await summaryf(it); return f()-t
    return (l := H.get_loop_and_set()).create_task(task(l.time))
def agetitems_from_indices(it, indices, setatend=None, finish=False, _='index %r beyond the ends of (async) iterable {!r}'.format, _c=A.AChain): # noqa: C901
    L, r, it = H.get_loop_and_set(), [], iter_to_agen(it)
    async def consume(f=r.append): # noqa: C901
        s, M, m, d = L.time(), 0, 0, defaultdict(list)
        async for x in amap(O.index, indices):
            if M is not None:
                if x < 0: M, m = None, min(m, x)
                else: M = max(x, M)
            d[x].append(F := L.create_future()); f(F)
        async def helper(i, j, d=d):
            async for x, F in aenumerate(d.pop(i, ())):
                if F.cancelled(): continue
                if F.done(): raise A.FutureCorrupted(f'asyncutils.iters.agetitems_from_indices: future at index {x} associated with index {i} called on (async) iterable {it!r} had its result/exception set by an external party')
                F.set_result(j)
        try:
            if M is None:
                b = deque(maxlen=-m)
                async def helper2(i, j): await helper(i, j); b.append(j)
                await aconsume(_c(astarmap(helper2, aenumerate(it)), amap(helper, acount(-1, -1), A.adisembowel_left(b), await_=True)))
            else: await aconsume(astarmap(helper, aenumerate(A.take(it, M)), True))
        except A.CRITICAL: raise A.Critical
        except BaseException as e:
            async for F in afilterfalse(O.methodcaller('done'), r): F.set_exception(e)
            raise
        a = _(it)
        for i, l in d.items():
            e = IndexError(a%i)
            async for x, F in aenumerate(l):
                if not F.cancelled():
                    if F.done(): raise ExceptionGroup('asyncutils.iters.agetitems_from_indices: error while processing indices for which items were not successfully got', (e, A.FutureCorrupted(f'asyncutils.iters.agetitems_from_indices: future at index {x} associated with index {i} called on (async) iterable {it!r} had its result/exception set by an external party')))
                    F.set_exception(e)
        if finish: await aconsume(it)
        if setatend is None: return
        if setatend.done() and not setatend.cancelled(): raise A.FutureCorrupted(f'asyncutils.iters.agetitems_from_indices: future setatend at {id(setatend):#x} (exact type {H.fullname(setatend)}) had its result set by an external party')
        setatend.set_result(L.time()-s)
    c = L.create_task(consume())
    if setatend is not None: setatend.add_done_callback(lambda _: setattr(_, '__cancel', t := B.gather(A.safe_cancel(c), A.safe_cancel_batch(r))) or t.add_done_callback(lambda _: delattr(setatend, '__cancel')))
    audit('asyncutils.iters.agetitems_from_indices', H.fullname(it)); return r
async def aintersend(i1, i2):
    audit('asyncutils.iters.aintersend', H.fullname(i1), H.fullname(i2)); t = None, None; f, g = i1.asend, i2.asend
    while True: yield (t := tuple(await B.gather(f(t[1]), g(t[0]))))
def asendstream(i1, i2): audit('asyncutils.iters.asendstream', H.fullname(i1), H.fullname(i2)); return amap(i1.asend, i2, await_=True)
async def acat(first=None):
    audit('asyncutils.iters.acat', first)
    while True: first = yield first
async def aforever():
    audit('asyncutils.iters.aforever')
    while True: yield
async def _aguess(I, l, K, d, e, C, c, a, _=_aextreme, /): # noqa: PLR0917
    if l is None and (l := O.length_hint(I, -1)) < 0: raise ValueError('asyncutils.iters.aguessmax or asyncutils.iters.aguessmin called with no estlen argument on iterable not implementing length (hint)')
    I = iter_to_agen(I)
    if (r := await _(A.take(I if c is None else aside_effect(c, I, await_=a), M.ceil(l*A.RECIPROCAL_E)), K, C)) is _NO_DEFAULT:
        if d is _NO_DEFAULT: raise ValueError('empty (async) iterable passed to asyncutils.iters.aguessmax or asyncutils.iters.aguessmin with no default value')
        return d
    k = K(r)
    try:
        if c is None:
            async for i in I:
                if C(K(i), k): return i
        elif a:
            async for i in I:
                if C(K(i), k): return i
                await c(i)
        else:
            async for i in I:
                if C(K(i), k): return i
                c(i)
        return r
    finally:
        if not (e is None or e.is_set()): (t := (_ := H.get_loop_and_set().create_task)(aconsume(I))).add_done_callback(lambda _: e.set()); _(e.wait()).add_done_callback(t.cancel)
def aguessmax(it, estlen=None, *, key=_identity, default=_NO_DEFAULT, finish_event=None, reject_cb=None, await_cb=False, _=_aguess): return _(it, estlen, key, default, finish_event, O.gt, reject_cb, await_cb)
def aguessmin(it, estlen=None, *, key=_identity, default=_NO_DEFAULT, finish_event=None, reject_cb=None, await_cb=False, _=_aguess): return _(it, estlen, key, default, finish_event, O.lt, reject_cb, await_cb)
async def apowers_of_two(*, init=1, init_shift=0, shift=1):
    init <<= init_shift
    while True: yield init; init <<= shift
def apowers(base, start=1): return aprepend(start, arepeat(0)) if base == 0 else arepeat(start) if base == 1 else apowers_of_two(init=base, shift=base.bit_length()-1) if base.bit_count() == 1 else aaccumulate(arepeat(base), O.mul, initial=start)
async def areversed(it, /):
    try:
        async for i in iter_to_agen(reversed(it)): yield i
    except TypeError:
        f = (it := await to_list(it)).pop
        while it: yield f()
async def arunlength_encode(it, /):
    async for k, g in agroupby(it): yield k, ailen(g)
def arunlength_decode(it, /): return aflatten(astarmap(arepeat, it))
async def _dfthelper(a, i=False, /): return await to_tuple(A.take(apowers(M.e**((1 if i else -1)*1j*M.tau/(N := len(a := await to_tuple(a))))), N)), N, a
async def adft(a, /, _=_dfthelper):
    R, N, a = await _(a)
    for k in range(N): yield M.sumprod(a, (R[k*i%N] for i in range(N)))
async def aidft(A, /, _=_dfthelper):
    R, N, A = await _(A, True)
    for k in range(N): yield M.sumprod(A, (R[k*n%N] for n in range(N)))/N
async def _aargminmax(it, key, default, f): return (await f(aenumerate(amap(key, it)), key=O.itemgetter(1), default=default))[0]
def aargmin(it, key=_identity, default=-1, _=_aargminmax): return _(it, key, default, amin)
def aargmax(it, key=_identity, default=-1, _=_aargminmax): return _(it, key, default, amax)
def arunning_mean(it): return amap(O.truediv, aaccumulate(it), acount(1))
@aawgenf2agenf
async def apowerset_of_sets(it, *, frozen=True): S = tuple(dict.fromkeys(await to_list(amap(frozenset, azip(it))))); return aflatten(astarmap((frozenset if frozen else set).union, acombinations(S, r)) async for r in arange(len(S)+1))
async def aserialize(it):
    l, n = B.Lock(), iter_to_agen(it).__anext__
    while True:
        async with l: x = await n()
        yield x # noqa: RUF070
async def aonline_sorter(it, *, key=_identity, reverse=False, slow=None):
    audit('asyncutils.iters.aonline_sorter', id(it)); c = C if reverse else __import__('heapq')
    if slow is None: slow = getcontext().AONLINE_SORTER_DEFAULT_SLOW
    if (e := getattr(aonline_sorter, 'executor', None)) is None: e = H.create_executor(aonline_sorter)
    q = partial(p := partial(H.get_loop_and_set().run_in_executor, e), key)
    await p(c.heapify, it := [(await q(x) if slow else key(x), i, x) async for i, x in aenumerate(it)])
    a, b, i = partial(c.heappop, it), partial(c.heappush, it), len(it)
    while it:
        if (j := (yield a()[2])) is not None: b(((await q(j)) if slow else key(j), i, j)); i += 1
async def acount_cycle(it, n=None):
    if n is None: c = acount(1)
    else:
        if n == 0: return
        if n < 0: raise ValueError('asyncutils.iters.acount_cycle: n must be non-negative')
        c = arange(1, n)
    a = (s := []).append
    async for i in iter_to_agen(it): yield 0, i; a(i)
    async for i in azip(arepeat_each(c, len(s := tuple(s))), acycle(s)): yield i
def arepeat_each(it, n=2): return aflatten(amap(arepeat, it, arepeat(n)))
async def arepeat_last(it, default=_NO_DEFAULT):
    async for default in iter_to_agen(it): yield default # noqa: PLR1704
    if default is _NO_DEFAULT: return
    if default is A.RAISE: raise A.ItemsExhausted('asyncutils.iters.arepeat_last: (async) iterable exhausted and ``default`` was :const:`~asyncutils.constants.RAISE`')
    while True: yield default
def aadjacent(pred, it, dist=1, *, await_pred=False):
    if dist < 0: raise ValueError('asyncutils.iters.aadjacent: dist must be non-negative')
    if pred is None:
        if await_pred: raise TypeError('asyncutils.iters.aadjacent: pred cannot be None if await_pred is True')
        pred = bool
    u, v = tee(it, maxqsize=dist+1); return azip(amap(aany, window(A.AChain(arepeat(False, dist), amap(pred, u, await_=await_pred), arepeat(False, dist)), (dist<<1)+1), await_=True), v)
def agroupby_transform(it, kf=_identity, vf=None, rf=None, *, await_kf=False, await_vf=False, await_rf=False):
    r = agroupby(it, kf, await_=await_kf)
    if vf is None:
        if await_vf: raise TypeError('asyncutils.iters.agroupby_transform: vf cannot be None if await_vf is True')
    else: r = ((k, amap(vf, g, await_=await_vf)) async for k, g in r)
    if rf is None:
        if await_rf: raise TypeError('asyncutils.iters.agroupby_transform: rf cannot be None if await_rf is True')
    else: r = ((k, await rf(g)) async for k, g in r) if await_rf else ((k, rf(g)) async for k, g in r)
    return r
async def adifference(it, func=O.sub, *, yield_initial=True, await_func=False):
    u, v = tee(it, maxqsize=1); i = await anext(v)
    if yield_initial: yield i
    async for i in amap(func, u, v, await_=await_func): yield i
async def aminmax(*I, default=_NO_DEFAULT):
    if not I:
        if default is _NO_DEFAULT: raise TypeError('asyncutils.iters.aminmax: expected at least 1 argument, got 0')
        return default
    if len(I) == 1: I = I[0]
    I = iter_to_agen(I)
    try: l = h = await anext(I)
    except StopAsyncIteration:
        if default is _NO_DEFAULT: raise ValueError('asyncutils.iters.aminmax called on empty iterable without default value') from None
        return default
    async for x, y in aziplongest(I, I, fillvalue=l): l, h = (min(l, y), max(h, x)) if y < x else (min(l, x), max(h, y))
    return l, h
async def aminmax_keyed(*I, key, default=_NO_DEFAULT):
    if not I:
        if default is _NO_DEFAULT: raise TypeError('asyncutils.iters.aminmax_keyed: expected at least 1 argument, got 0')
        return default
    if len(I) == 1: I = I[0]
    I = iter_to_agen(I)
    try: l = h = await anext(I)
    except StopAsyncIteration:
        if default is _NO_DEFAULT: raise ValueError('asyncutils.iters.aminmax_keyed called on empty iterable without default value') from None
        return default
    H = L = key(l)
    async for x, y in aziplongest(I, I, fillvalue=l):
        X, Y = key(x), key(y)
        if Y < X:
            if Y < L: l, L = y, Y
            if H < X: h, H = x, X
        else:
            if X < L: l, L = x, X
            if H < Y: h, H = y, Y
    return l, h
@aawgenf2agenf
async def aouter_product(f, X, Y, /, *a, **k): return batch(astarmap(C.partial(f, C.Placeholder, C.Placeholder, *a, **k), aproduct(X, Y := await to_tuple(Y)), True), len(Y))
P.patch_function_signatures((adifference, 'it, func={}, *, yield_initial=True, await_func=False'), (agroupby_transform, 'it, kf={}, vf=None, rf=None, *, await_kf=False, await_vf=False, await_rf=False'), (tee, 'it, n=2, *, maxqsize=None, put_exc=None, loop=None'), (aonline_sorter, 'it, *, key={}, reverse=False, slow=None'), (aside_effect, 'f, it, /, *, size=None, before=None, after=None'), (apolynomial_from_roots, 'roots'), (adistinct_permutations, 'it, r=None'), (abfs, _ := 'start, neighbours, *, include_start=True'), (adfs, _), (aaccumulate, 'it, func={}, *, initial=None'), (aconvolve, 'signal, kernel'), (aislice, 'it, /, *a'), (ainterleave_randomly, 'its'), (ahamming_dist, 'i1, i2, /, cmpeq={}'), (aiter_idx, 'it, value, start=0, stop=None'), (amerge_sorted_by, 'its, *, key={}, await_=False, reverse=False'), (amax, _ := '*it, key={}, default=_NO_DEFAULT'), (amin, _), (asample_weighted, _ := 'it, k, *, rrange={0}, rand={0}'), (asamplel, _), (arandom_combination, _ := 'it, r'), (arandom_combination_with_replacement, _), (asorted, 'it, *, key={}, reverse=False'), (aunique_justseen, _ := 'it, key={}'), (aunique_everseen, _), (agroupby, _), (vecs_eq, 'u, v, cmpeq={}, *, strict=True'), (adft, 'xarr, /'), (aidft, 'Xarr, /'), (aconsume, 'it, n=None'), (aallequal, 'it, key={}, strict=False'), (aprepend, 'val, it'), (arandom_product, '*a, n=1'), (asattolo, 'it, /'), (aargmin, _ := 'it, key={}, default=-1'), (aargmax, _), (afactor, _ := 'n'), (agetitems_from_indices, 'it, indices, setatend=None, finish=False'), (alast, 'it, default=_NO_DEFAULT'), (aisprime, _), (aguessmax, _ := 'it, estlen, *, key={}, default=_NO_DEFAULT, finish_event=None'), (aguessmin, _), (aflatten, _ := 'it'), (arandom_derangement, _), (afreivalds, 'A, B, C, k=None'), (basic_collect, 'it, n'), (iter_task, 'it, summaryf={}'), (apadnone, 'it'), (aunzip, 'ait, put_batch=None, fillvalue={}'), (aflatten_tensor, 'tensor, base_typ={}'), (arandom_permutation, 'it, r=None'))
del P, _tee_helper, _adpermpartial, _adpermfull, _atraverse, _aunzip_put, _aguess, _aargminmax, _aextreme, _buffer_consume, _factor_pollard, _shift_to_odd, _probable_prime, _dfthelper, _littleprimes, _randrange, _sample, _smallprimes, _perfect_test, _rand, _randinst, _identity, _
