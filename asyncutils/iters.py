__lazy_modules__ = frozenset(('asyncio', 'asyncutils._internal.compat'))
from asyncutils import exceptions as E, achain, adisembowel, aenumerate, aiter_from_f, areduce, collect, getcontext, iter_to_agen, iterf, safe_cancel, safe_cancel_batch, take, RAISE, RECIP_E, ignore_qshutdown
from asyncutils.config import _randinst
from asyncutils.constants import _NO_DEFAULT
from asyncutils._internal.compat import LifoQueue, Queue, QueueEmpty, QueueShutDown, partial, Placeholder
from asyncutils._internal.helpers import check, check_methods, copy_and_clear, create_executor, filter_out, fullname, get_loop_and_set
from asyncutils._internal.submodules import iters_all as __all__
import _operator as O, math as M
from asyncio import CancelledError, Lock, gather, iscoroutine, sleep, wait_for
from collections import Counter, defaultdict, deque
from functools import lru_cache
from sys import audit
_randrange, _sample, _smallprimes, _perfect_test, _identity = _randinst.randrange, _randinst.sample, frozenset(_littleprimes := (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199)), ((0x7ff, (2,)), (0x8a8d7f, (31, 73)), (0x11baa74c5, (2, 7, 61)), (0x1053cb094c1, (2, 13, 23, 0x195f53)), (0x1f51f3fee3b, _littleprimes[:5]), (0x32907381cdf, _littleprimes[:6]), (1<<64, (2, 0x145, 0x249f, 0x6e12, 0x6e0d7, 0x953d18, 0x6b0191fe)), (0x2be6951adc5b22410a5fd, _littleprimes[:13]), (0x4c16c7697197146a6b8eb49518c5, _littleprimes[:18])), lambda _, /: _
async def fmap(fs, /, *a, **k): return await gather(*[f(*a, **k) async for f in iter_to_agen(fs)])
async def fmap_sequential(fs, /, *a, **k):
    async for f in iter_to_agen(fs): yield await f(*a, **k)
async def fmap_parallel(fs, /, *a, **k):
    t = get_loop_and_set().create_task
    for r in await to_list(t(f(*a, **k)) async for f in iter_to_agen(fs)): yield await r
async def map_on_map(outer, inner, it, *, inner_await=False, outer_await=False):
    f, g = (l := []).append, l.clear
    async for _ in amap(outer, it, await_=outer_await):
        async for i in amap(inner, _, await_=inner_await): f(i)
        yield tuple(l); g()
def tee(it, n=2, *, maxqsize=0, put_exc=None, loop=None):
    if n <= 0: raise ValueError('n must be positive')
    if loop is None: loop = get_loop_and_set()
    if put_exc is None: put_exc = getcontext().TEE_DEFAULT_PUT_EXC
    Q, a, l = tuple(Queue(maxqsize) for _ in range(n)), _NO_DEFAULT, Lock()
    async def iterator(q):
        nonlocal n
        while True:
            if (i := await q.get()) is a:
                async with l: n -= 1
                if n == 0: await safe_cancel(t)
                break
            elif put_exc and E.exception_occurred(i): raise E.unwrap_exc(i)
            else: yield i
    async def feed():
        async def helper(i): await gather(*(q.put(i) for q in Q), return_exceptions=True)
        try: await gather(*await to_list(amap(helper, it)))
        except E.CRITICAL: raise E.Critical
        except BaseException as e: # noqa: BLE001
            if put_exc: await helper(E.wrap_exc(e))
        finally: await helper(a)
    t = loop.create_task(feed()); return tuple(map(iterator, Q))
async def _aunzip_put(Q, t):
    for q, i in zip(Q, t):
        with ignore_qshutdown: await q.put(i)
class _aunzip_consumer_base:
    __slots__ = 'q',
    def __init__(self): self.q = Queue()
    def __aiter__(self): return self
    def close(self): self.q.shutdown()
async def aunzip(ait, put_batch=None, fillvalue=_NO_DEFAULT, _a=_aunzip_put, _b=_aunzip_consumer_base):
    audit('asyncutils.iters.aunzip', fullname(ait)); l = len(t := await anext(ait := iter_to_agen(ait), ()))
    class aunzip_consumer(_b):
        __slots__ = ()
        async def __anext__(self, L=Lock(), f=partial(take, ait, getcontext().AUNZIP_DEFAULT_PUT_BATCH if put_batch is None else put_batch, default=RAISE)): # noqa: B008
            if self.q.empty():
                async with L:
                    try:
                        async for _ in f(): await _a(Q, _)
                    except E.ItemsExhausted:
                        for q in Q: q.close()
            try:
                if (r := await self.q.get()) is fillvalue: raise StopAsyncIteration
                return r
            except QueueShutDown: raise StopAsyncIteration from None
    await _a(Q := tuple(aunzip_consumer() for _ in range(l)), t); return Q
async def merge(*I, reverse=False):
    audit('asyncutils.iters.merge', I); q, c, F, a = (LifoQueue if reverse else Queue)(), None, (l := get_loop_and_set()).create_future(), object()
    async def drain(i, f=q.put):
        async for _ in i: await f(_)
    async def close():
        if reverse: await q.put(a); F.set_result(None)
        await gather(*(l.create_task(drain(iter_to_agen(i))) for i in I))
        if not reverse: await q.put(a); F.set_result(None)
    l.create_task(close()); await F
    while True:
        if (c := await q.get()) is a: break
        yield c
def aflatten(it): return achain.from_iterable(it).__aiter__()
def acountdown(n, step=1, *, include_zero=False): return arange(n, -include_zero, -step)
async def abfs(start, neighbours, *, include_start=True):
    a, c, f, g = (v := {start}).add, v.__contains__, (q := deque((start,))).popleft, q.append
    if include_start: yield start
    while q:
        async for _ in afilterfalse(c, neighbours(f())): a(_); g(_); yield _
async def adfs(start, neighbours, *, include_start=True):
    a, c, f, g = (v := {start}).add, v.__contains__, (s := [start]).pop, s.append
    if include_start: yield start
    while s:
        async for _ in afilterfalse(c, areversed(neighbours(f()))): a(_); g(_); yield _
async def asattolo(it, _=_randrange):
    i = len(a := await to_list(it))
    while i > 1:
        i -= 1
        a[j], a[i] = a[i], a[j := _(i)]
    return a
async def abrent(f, start, /):
    p = l = 1; t, h = start, await f(start)
    while t is not h:
        if p == l: t, l, p = h, 0, p<<1
        h, l = await f(h), l+1
    a, m = (start, await iterf(l)(f)(start)), 0
    while a[0] is not a[1]: a, m = await gather(*map(f, a)), m+1
    return a[0], l, m
async def asampleweighted(it, k, rrange=_randrange, rand=_randinst.random):
    W, u, p = 0.0, rand(), 1.0
    async def agen(it):
        nonlocal W
        async for i, w in iter_to_agen(it):
            if w < 0: raise ValueError(f'iters.asampleweighted: weight {w} for item {i!r} is negative')
            W += w; yield i, w
    r = await collect(it := agen(it), k, default=RAISE)
    async for i, w in it:
        w /= W; u -= w*p; p *= 1-w # noqa: PLW2901
        if u <= 0: r[rrange(k)], u, p = i, rand(), 1.0
    return r
async def astarfilter(pred, it):
    if pred is None: pred = bool
    async for t in iter_to_agen(it):
        if iscoroutine(r := pred(*await to_list(t))): r = await r
        if r: yield t
async def astarfilterfalse(pred, it):
    if pred is None: pred = bool
    async for t in iter_to_agen(it):
        if iscoroutine(r := pred(*await to_list(t))): r = await r
        if not r: yield t
async def amultistarfilter(pred, *its, strict=False):
    if pred is None: pred = bool
    async for t in azip(*its, strict=strict):
        if iscoroutine(r := pred(*await to_list(t))): r = await r
        if r: yield t
async def amultistarfilterfalse(pred, *its, strict=False):
    if pred is None: pred = bool
    async for t in azip(*its, strict=strict):
        if iscoroutine(r := pred(*await to_list(t))): r = await r
        if not r: yield t
def amultifilter(pred, *its, strict=False): return afilter(pred, azip(*its, strict=strict))
def amultifilterfalse(pred, *its, strict=False): return afilterfalse(pred, azip(*its, strict=strict))
def ahammingdist(i1, i2, /, cmpeq=check): return ailen(amultistarfilterfalse(cmpeq, i1, i2))
async def amergesortedby(its, *, key=_identity, await_=False, reverse=False):
    f = (h := []).append
    for i, it in enumerate(its := await to_tuple(map(iter_to_agen, its))):
        try:
            k = key(v := await anext(it))
            f(((await k) if await_ else k, i, v))
        except StopAsyncIteration: ...
    if reverse: from asyncutils._internal.compat import heapify as a, heappop as b, heappush as c
    else: from _heapq import heapify as a, heappop as b, heappush as c
    a(h)
    while h:
        _, i, v = b(h)
        yield v
        try:
            k = key(v := await anext(its[i]))
            c(h, ((await k) if await_ else k, i, v))
        except StopAsyncIteration: ...
async def batch(it, n, *, item_timeout=None, strict=False):
    f, g, _ = iter_to_agen(it).__anext__, (b := []).append, 0
    while True:
        try:
            for _ in range(n):
                try: g(await wait_for(f(), item_timeout))
                except StopAsyncIteration: break
                except TimeoutError:
                    if b: break
            if b:
                if strict and _ < n-1: raise ValueError('incomplete batch')
                yield copy_and_clear(b)
        except CancelledError:
            if b: yield copy_and_clear(b)
            raise
def batch2(it, n, strict=False): return aiter_from_f(partial(collect, it, n, default=RAISE if strict else _NO_DEFAULT), [])
async def asideeffect(f, it, /, *, size=None, before=None, after=None):
    try:
        if before is not None: before()
        if size is None:
            if iscoroutine(r := f(i := await anext(I := iter_to_agen(it)))):
                await r; yield i
                async for i in I: await f(i); yield i
            else:
                yield i
                async for i in I: f(i); yield i
        elif iscoroutine(r := f(i := await anext(I := batch(it, size)))):
            await r
            for _ in i: yield _
            async for i in I:
                await f(i)
                for _ in i: yield _
        else:
            for _ in i: yield _
            async for i in I:
                f(i)
                for _ in i: yield _
    finally:
        if after is not None: after()
def asliced(seq, n, strict=False):
    I = atakewhile(None, (seq[i:i+n] async for i in acount(step=n)))
    if not strict: return I
    async def r():
        async for s in I:
            if len(s) != n: raise ValueError(f'length of {seq!r} is not divisible by {n}')
            yield s
    return r()
def buffer(it, maxsize=0, timeout=None, cooldown=0, *, loop=None):
    q = Queue(maxsize)
    async def consumer():
        try:
            while True:
                try: yield await q.get(); q.task_done()
                except QueueEmpty: await sleep(cooldown)
        finally: await safe_cancel(t)
    c = consumer()
    async def producer():
        try:
            async for _ in iter_to_agen(it):
                try: await wait_for(q.put(_), timeout)
                except TimeoutError: break
        finally: await c.aclose()
    if loop is None: loop = get_loop_and_set()
    t = loop.create_task(producer()); return c
async def asplitat(it, pred, maxsplit=-1, keep_sep=False):
    I, f = iter_to_agen(it), (b := []).append
    if not maxsplit: yield await to_list(I); return
    async for i in I:
        if pred(i):
            yield b
            if keep_sep: yield [i]
            if maxsplit == 1: yield await to_list(I); return
            f = (b := []).append; maxsplit -= 1
        else: f(i)
    yield b
async def batch_process(items, size, processor):
    async for b in batch(items, size): yield await processor(b)
async def window(it, size, step=1):
    if not size >= 1 <= step: raise ValueError('size and step should both be >=1')
    b, c = deque(maxlen=size), 0
    async for i in iter_to_agen(it):
        b.append(i)
        if len(b) == size:
            if not c%step: size, step = (yield tuple(b)) or (size, step)
            c += 1
async def aall(it):
    async for _ in iter_to_agen(it):
        if not _: return False
    return True
async def aany(it):
    async for _ in iter_to_agen(it):
        if _: return True
    return False
async def _aextreme(it, key, default, cmp):
    if (r := await anext(I := iter_to_agen(it), _NO_DEFAULT)) is _NO_DEFAULT:
        if default is _NO_DEFAULT: raise ValueError('empty (async) iterable passed with no default value')
        return default
    k = key(r)
    async for i in I:
        if cmp(x := key(i), k): k, r = x, i
    return r
def amax(*it, key=_identity, default=_NO_DEFAULT, _=_aextreme): return _(it[0] if len(it) == 1 else it, key, default, O.gt)
def amin(*it, key=_identity, default=_NO_DEFAULT, _=_aextreme): return _(it[0] if len(it) == 1 else it, key, default, O.lt)
async def azip(*I, strict=False):
    I = tuple(map(iter_to_agen, I))
    try:
        while True: yield tuple(await gather(*map(anext, I)))
    except (StopAsyncIteration, RuntimeError):
        if strict:
            for x, y in enumerate(I):
                try: await anext(y); raise ValueError(f'azip: iterable {x} longer than shortest iterable')
                except (StopAsyncIteration, RuntimeError): continue
async def amap(f, /, *its, await_=False, strict=False):
    async for _ in azip(*its, strict=strict): r = f(*_); yield (await r) if await_ else r
async def afilter(f, it):
    if f is None: f = bool
    async for _ in iter_to_agen(it):
        if iscoroutine(r := f(_)): r = await r
        if r: yield _
def amapif(f, p, it, /, await_=False): return amap(f, afilter(p, it), await_)
def amultimapif(f, p, /, *its, await_=False): return astarmap(f, afilter(p, azip(*its)), await_)
async def arange(a, b=None, c=1, /):
    if not c: raise ValueError('step cannot be zero')
    if b is None: a, b = 0, a
    f = b.__lt__ if c < 0 else b.__gt__
    while f(a): yield a; a += c
async def acount(start=0, step=1):
    if isinstance(step, float):
        if step.is_integer(): step = int(step)
        else: start = float(start)
    elif start.is_integer(): start = int(start)
    while True: yield start; start += step
async def acycle(it):
    l, I = [], iter_to_agen(it)
    async for i in I: yield i; l.append(i)
    t = tuple(l)
    while True:
        for i in t: yield i
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
async def adropwhile(pred, it):
    I = iter_to_agen(it)
    async for _ in I:
        if not pred(_): yield _; break
    async for _ in I: yield _
def afilterfalse(f, it): return afilter(lambda i: not (f or bool)(i), it)
async def agroupby(it, key=_identity):
    I, e = iter_to_agen(it), False
    async def grouper(k):
        nonlocal cv, ck, e; yield cv
        async for cv in I:
            if (ck := key(cv)) != k: return
            yield cv
        e = True
    try: ck = key(cv := await anext(I))
    except StopAsyncIteration: return
    while not e:
        yield ck, (g := grouper(t := ck))
        if ck == t: await aconsume(g)
async def aislice(it, /, *a, _=lambda x: x if x is None else int(x, 0) if isinstance(x, str) else int(x)):
    x, y, z = 0 if (s := slice(*map(_, a))).start is None else s.start, s.stop, 1 if s.step is None else s.step
    if x < 0 or (y is not None and y < 0) or z <= 0: raise ValueError('invalid indices')
    I, n = acount() if y is None else arange(max(x, y)), x
    async for i, j in azip(I, it):
        if i == n: yield j; n += z
async def aiterindex(it, value, start=0, stop=None, _=check):
    async for i, j in aenumerate(aislice(it, start, stop), start):
        if _(j, value): yield i
async def asieve(n):
    if n < 2: return
    yield 2; s, d = 3, bytearray((0, 1))*(n>>1)
    async for p in aiterindex(d, 1, s, M.isqrt(n)+1):
        async for i in aiterindex(d, 1, s, s := p*p): yield i
        d[s:n:x] = bytes(len(range(s, n, x := p<<1)))
    async for i in aiterindex(d, 1, s): yield i
async def apairwise(it):
    try: a = await anext(I := iter_to_agen(it))
    except StopAsyncIteration: return
    async for b in I: yield a, b; a = b
async def atriplewise(it):
    a, b, c = tee(iter_to_agen(it), 3); await gather(*(anext(g, None) for g in (b, c, c)))
    async for _ in azip(a, b, c): yield _
async def aproduct(*its, repeat=1):
    if repeat < 0: raise ValueError('repeat cannot be negative')
    r = [()]
    async for p in arepeat(amap(to_tuple, its, await_=True), repeat): r = [(*x, y) for x in r async for y in p]
    for _ in r: yield _
async def astarmap(f, it, /, await_=False):
    async for _ in iter_to_agen(it): yield (await f(*_)) if await_ else f(*_)
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
async def atakewhilenot(pred, it):
    if pred is None: pred = bool
    async for _ in iter_to_agen(it):
        if pred(_): break
        yield _
async def atakewhilenot_inclusive(pred, it):
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
async def aconvolve(signal, kernel):
    f = (w := deque((0,), n := len(K := await to_tuple(areversed(kernel))))*n).append
    async for x in achain(signal, arepeat(0, n-1)): f(x); yield await asumprod(K, w)
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
def atail(n, it, /):
    try: return aislice(it, max(0, len(it)-n), None)
    except TypeError:
        async def f():
            g = (d := deque(maxlen=n)).append
            async for _ in iter_to_agen(it): g(_)
            for _ in d: yield _
        return f()
def amultinomial(*c): return aprod(amap(M.comb, aaccumulate(c), c))
async def to_tuple(it, /): return tuple(await to_list(it))
async def to_list(it, /): return [_ async for _ in iter_to_agen(it)]
async def aconsume(it, n=None, _=check_methods):
    if n == 0: return
    if n: it = take(it, n)
    if _(it, '__iter__'): await get_loop_and_set().run_in_executor(create_executor(aconsume) if (E := getattr(aconsume, 'executor', None)) is None else E, deque, it, 0)
    else:
        async for _ in it: ...
def anth(it, n, default=_NO_DEFAULT): return anext(aislice(it, n, None), *filter_out(default, s=_NO_DEFAULT))
async def aallequal(it, key=_identity, strict=False):
    async for _ in (I := agroupby(it, key)):
        async for _ in I: return False
        return True
    if strict: raise ValueError('iterable provided is empty')
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
async def apowerset(it):
    s = await to_tuple(it)
    async for _ in aflatten(acombinations(s, r) for r in range(len(s)+1)): yield _
def aquantify(it, pred=bool): return asum(amap(pred, it))
def apadnone(it): return achain(it, arepeat(None)).__aiter__()
def agrouper(it, n, fillvalue=_NO_DEFAULT): I = (iter_to_agen(it),)*n; return azip(*I, strict=fillvalue is RAISE) if isinstance(fillvalue, type(RAISE)) else aziplongest(*I, fillvalue=fillvalue)
async def aroundrobin(*its):
    I = (iter_to_agen(i) for i in its)
    for i in range(len(its), 0, -1):
        async for _ in (I := acycle(aislice(I, i))): yield await anext(_)
async def aroundrobin2(*its):
    async for X in aziplongest(*its, fillvalue=_NO_DEFAULT):
        for x in X:
            if x is not _NO_DEFAULT: yield x
async def aunique_everseen(it, key=_identity):
    A, a = (S := set()).add, (s := []).append
    async for i in iter_to_agen(it):
        k = key(i)
        try:
            if k not in S: A(k); yield i
        except TypeError:
            if k not in s: a(k); yield i
def aunique_justseen(it, key=_identity, _=O.itemgetter): return amap(_(0), agroupby(it)) if key is None else amap(anext, amap(_(1), agroupby(it, key)), await_=True)
async def aunique(it, key=None, reverse=False):
    async for _ in aunique_justseen(await asorted(it, key=key, reverse=reverse), key): yield _
async def ancycles(it, n):
    async for _ in aflatten(arepeat(await to_tuple(it), n)): yield _
def apartition(pred, it):
    if pred is None: pred = bool
    async def agen(q, _=iter_to_agen(it).__anext__): # noqa: B008
        while True:
            while q: yield q.popleft()
            try: (T if pred(v := await _()) else F).append(v)
            except StopAsyncIteration: return
    return map(agen, (F := deque(), T := deque()))
async def aiterexcept(f, exc, first=None):
    with E.IgnoreErrors(exc):
        if first is not None: yield await first()
        while True: yield await f()
async def ailen(it):
    i = 0
    async for _ in iter_to_agen(it): i += 1
    return i
async def aiterate(f, start):
    while True: yield start; start = await f(start)
async def with_aiter(actxmgr):
    async with actxmgr as I:
        async for i in iter_to_agen(I): yield i
async def asorted(it, *, key=_identity, reverse=False):
    from _heapq import heappop as g, heapify as f
    b, a = (m := []).append, (r := []).append
    async for i, j in aenumerate(it): b((key(j), i, j))
    f(m)
    while m: a(g(m))
    if reverse: r.reverse()
    return r
def acanonical(it): return asorted(it, key=id, reverse=True)
async def adistinctpermutations(it, r=None):
    if (S := len(I := await to_list(it))) < (_ := S if r is None else r): yield (); return
    if _ <= 0: return
    if _ == S:
        async def a(A):
            while True:
                yield tuple(A)
                for i in range(_-2, -1, -1):
                    if A[i] < A[i+1]: break
                else: return
                for j in range(j := _-1, i, -1): # noqa: B020
                    if A[i] < A[j]: break
                A[i], A[j] = A[j], A[i]; A[i+1:] = A[:i-_:-1]
    else:
        async def a(A):
            h, R, l = A[:_], range(_-1, -1, -1), range(len(t := A[_:]))
            while True:
                yield tuple(h); p = t[-1]
                for i in R:
                    if h[i] < p: break
                    p = h[i]
                else: return
                for j in l:
                    if t[j] > h[i]: h[i], t[j] = t[j], h[i]; break
                else:
                    for j in R:
                        if h[j] > h[i]: h[i], h[j] = h[j], h[i]; break
                t += h[:-(x := _-i):-1]; i += 1; h[i:], t[:] = t[:x], t[x:]
    try: I.sort(); R = a(I)
    except TypeError:
        d = defaultdict(list)
        for i in I: d[I.index(i)].append(i)
        R = amap(lambda i, E={k: acycle(v) for k, v in d.items()}: to_tuple(await anext(E[_]) for _ in i), a(sorted(map(I.index, I))), await_=True) # noqa: B008
    async for t in R: yield t
async def auniquetoeach(*its):
    p = frozenset(await to_list(amap(to_tuple, its, await_=True)))
    for i, j in Counter(await to_list(aflatten(map(frozenset, p)))).items():
        if j == 1 and i in p: yield i
async def aderangements(it, r=None):
    async for _ in acompress(apermutations(X := await to_tuple(it), r), amap(aall, amap(partial(amap, O.is_not), arepeat(Y := tuple(range(len(X)))), apermutations(Y, r)), await_=True)): yield _
def aintersperse(e, it, n=1):
    if n <= 0: raise ValueError('n must be positive')
    return aislice(ainterleave_stopearly(arepeat(e), it), 1, None) if n == 1 else aflatten(aislice(ainterleave_stopearly(arepeat((e,)), batch(it, n)), 1, None))
def ainterleave_stopearly(*it): return aflatten(azip(*it))
def ainterleave(*it): return afilter(O.is_not.__get__(_NO_DEFAULT), aflatten(aziplongest(*it, fillvalue=_NO_DEFAULT)))
def aspy(it, n=1): p, q = tee(it); return take(q, n), p
async def ainterleaveevenly(its, lengths=None):
    I = await to_tuple(its)
    try:
        if (X := len(I)) != len(L := await to_tuple(lengths or map(len, I))): raise ValueError('ainterleaveevenly: mismatch in length of its and lengths')
    except TypeError: raise ValueError('ainterleaveevenly: cannot determine lengths of (async) iterables') from None
    A, *a = map(f := L.__getitem__, _ := sorted(range(X), key=f, reverse=True)); B, *b = (iter_to_agen(I[i]) for i in _); E, t = [A//X]*len(a), sum(L)
    while t:
        yield await anext(B); t -= 1; E[:] = map(O.sub, E, a)
        for i, e in enumerate(E):
            if e < 0: yield await anext(b[i]); t -= 1; E[i] += A
async def ainterleaverandomly(its, _=_randrange):
    x = len(I := await to_list(amap(iter_to_agen, its)))
    while x:
        i = _(x)
        try: yield await anext(I[i])
        except StopAsyncIteration: I[i] = I[-1]; del I[-1]; x -= 1
async def acollapse(it, base_typ=(str, bytes), levels=None):
    if levels is None: levels = float('inf')
    (g := (S := deque()).appendleft)((0, arepeat(iter_to_agen(it), 1))); f = S.popleft
    while S:
        l, n = N = f()
        if l > levels:
            async for i in n: yield i
            continue
        async for _ in n:
            if isinstance(_, base_typ): yield _
            else:
                try: t = iter_to_agen(_); g((l+1, t)); g(N); break
                except TypeError: yield _
def afirsttrue(it, default=_NO_DEFAULT, pred=None): return anext(afilter(pred, it), *filter_out(default, s=_NO_DEFAULT))
def aprepend(val, it): return achain((val,), it).__aiter__()
async def arandomproduct(*a, n=1, _=_randinst.choice):
    async for i in ancycles(amap(to_tuple, a, await_=True), n): yield _(i)
async def arandomcombination(it, r, _=_sample):
    (_ := _(range(len(p := await to_tuple(it))), r)).sort()
    for i in _: yield p[i]
async def arandom_combination_with_replacement(it, r, _=_randrange):
    n = len(p := await to_tuple(it))
    async for i in amap(p.__getitem__, sorted(_(n) for i in range(r))): yield i
async def arandompermutation(it, r=None, _=_sample):
    p = await to_tuple(it)
    if r is None: r = len(p)
    for i in _(p, r): yield i
async def afirst(it, default=_NO_DEFAULT):
    try:
        async for i in it: return i
    except TypeError:
        for i in it: return i
    if default is _NO_DEFAULT: raise ValueError('iters.afirst called on empty iterable without default value')
    return default
async def alast(it, default=_NO_DEFAULT, _=check_methods):
    try:
        if _(it, '__getitem__'): return it[-1]
        return (await to_list(it))[-1] if (f := getattr(it, '__reversed__', None)) is None else f().__next__()
    except (IndexError, TypeError, StopIteration, StopAsyncIteration):
        if default is _NO_DEFAULT: raise ValueError('iters.alast called on empty iterable without default value') from None
        return default
def anthorlast(it, n, default=_NO_DEFAULT): return alast(aislice(it, n+1), default)
def abeforeandafter(pred, it): a, b = tee(it); return acompress(atakewhile(pred, a), azip(b)), b
async def anthcombination(it, r, idx):
    if not 0 <= r <= (n := len(p := await to_tuple(it))): raise IndexError(f'iters.anthcombination: r={r} is out of range')
    c, k = 1, min(r, n-r)
    for i in range(1, k+1): c = c*(n-k+i)//i
    if idx < 0: idx += c
    if idx < 0 or idx >= c: raise IndexError(f'iters.anthcombination: idx={idx} is out of range')
    while r:
        c, n, r = c*r//n, n-1, r-1
        while idx >= c: idx -= c; c, n = c*(n-r)//n, n-1
        yield p[~n]
async def asubslices(it):
    async for _ in astarmap(O.getitem, azip(arepeat(s := await to_tuple(it)), astarmap(slice, acombinations(range(len(s)+1), 2)))): yield _
def arepeatfunc(f, times=None, *a): return astarmap(f, arepeat(a, times), True)
async def apolynomialfromroots(roots, p=(1,)):
    async for r in iter_to_agen(roots): p = aconvolve(p, (1, -r))
    async for _ in iter_to_agen(p): yield _
async def atranspose(it):
    async for _ in azip(*await to_tuple(it), strict=True): yield _
async def aflattentensor(tensor, base_typ=(str, bytes), _c=check_methods):
    I = iter_to_agen(tensor)
    while True:
        try: v = await anext(I)
        except StopAsyncIteration: break
        I = aprepend(v, I)
        if isinstance(v, base_typ) or not (_c(v, '__iter__') or _c(v, '__aiter__')): break
        I = aflatten(I)
    async for i in I: yield i
async def apolynomialderivative(coeff):
    async for _ in amap(O.mul, r := await to_tuple(coeff), range(len(r)-1, 0)): yield _
async def apolynomialeval(coeff, x):
    if not (n := len(t := await to_tuple(coeff))): return type(x)(0)
    return await asumprod(t, areversed(await collect(apowers(x), n-1)))
async def areshape(mat, shape):
    if isinstance(shape, int): I = batch(aflatten(mat), shape)
    else: d = anext(shape := iter_to_agen(shape)); I = aislice(await areduce(batch, areversed(shape), aflattentensor(mat), await_=False), d)
    async for i in I: yield i
async def _factor_pollard(n):
    if n == 4: return 2
    async for b in arange(1, n):
        x = y = 2; d = 1
        while (d := M.gcd((x := (x*x+b)%n)-(y := ((z := (y*y+b)%n)*z+b)%n), n)) == 1: ...
        if d != n: return d
    raise ValueError(f'afactor: internal error: {n} is prime')
@lru_cache
def _shift_to_odd(n):
    if not ((1<<(s := ((n-1)^n).bit_length()-1))*(d := n>>s) == n and d&1 and s > -1): raise ValueError('invalid n')
    return s, d
def _probable_prime(n, base, _=_shift_to_odd): s, d = _(n-1); return (x := pow(base, d, n)) in {1, n-1} or any((x := x*x%n) == n-1 for _ in range(s-1))
async def aisprime(n, s=_smallprimes, p=_perfect_test, r=_randrange, f=_probable_prime):
    if n < 210: return n in s
    if not (n&1 and n%3 and n%5 and n%7 and n%11 and n%13 and n%17): return False
    for l, _ in p:
        if n < l: break
    else: _ = (r(2, n-1) for _ in range(64))
    return await aall(amap(partial(f, n), _))
async def afactor(n, _=_littleprimes, F=_factor_pollard):
    if n < 2: raise ValueError('iters.afactor: no prime factors')
    for p in _:
        while not n%p: yield p; n //= p
    if n < 2: return
    e = (t := [n]).extend
    for n in t:
        if n < 44521 or await aisprime(n): yield n
        else: e((f := await F(n), n//f))
async def arunningmedian(it, *, maxlen=None):
    if maxlen is None:
        r, l, h = iter_to_agen(it).__aiter__().__anext__, [], []; from asyncutils._internal.compat import heappush as a, heappushpop as c; from _heapq import heappush as b
        while True: a(l, await r()); yield l[0]; b(h, c(l, await r())); yield (l[0]+h[0])/2
    if (m := O.index(maxlen)) <= 0: raise ValueError('iters.arunningmedian: window size should be positive')
    w, o = deque(), []; from _bisect import bisect_left as b, insort_right as f
    async for i in iter_to_agen(it):
        w.append(i); f(o, i)
        if (n := len(o)) > m: del o[b(o, w.popleft())]; n -= 1
        m = n>>1; yield o[m] if n&1 else (o[m-1]+o[m])/2
async def arandomderangement(it, _=_randinst.shuffle):
    if (l := len(s := await to_tuple(it))) < 2:
        if s: raise ValueError('iters.arandomderangement: no derangements to choose from')
        return ()
    i = tuple(p := list(range(l)))
    while any(map(O.is_, i, p)): _(p)
    return O.itemgetter(*p)(s)
async def amatmul(*a):
    M, N = map(iter_to_agen, a); N = aprepend(t := await to_tuple(await anext(N)), N)
    async for i in batch(astarmap(asumprod, aproduct(M, atranspose(N)), True), len(t)): yield i
async def mat_vec_mul(M, V):
    n, v = len(p := await to_tuple(amap(to_tuple, M, await_=True))), await to_tuple(V)
    async for i in arange(n): yield await asum(p[i][j]*v[j] async for j in arange(n))
async def vecs_eq(u, v, cmpeq=check, *, strict=True):
    try: return await aall(cmpeq(i, j) async for i, j in azip(u, v, strict=strict))
    except ValueError: return False
async def afreivalds(A, B, C, k=None, _r=_randrange): n = len(A := await to_tuple(A)); return await aall(await vecs_eq(mat_vec_mul(A, mat_vec_mul(B, r := tuple(_r(2) for _ in range(n)))), mat_vec_mul(C, r), int.__eq__) async for _ in arange(getcontext().AFRIEVALDS_DEFAULT_K if k is None else k))
def basic_collect(it, n): return to_list(aislice(it, n))
async def asubstrings(it):
    for i in (s := await to_tuple(it)): yield i,
    async for n in arange(2, c := len(s)+1):
        async for i in arange(c-n): yield s[i:i+n]
def asubstrindices(seq, reverse=False):
    r = range(1, x := len(seq)+1)
    if reverse: r = reversed(r)
    return ((seq[i:(j := i+L)], i, j) for L in r async for i in arange(x-L))
def iter_future(it, summaryf=aconsume):
    async def task(): t = L.time(); await summaryf(it); F.set_result(L.time()-t)
    F = (L := get_loop_and_set()).create_future(); L.create_task(task()); return F
def agetitems_from_indices(it, indices, setatend=None, finish=False, _='index %r beyond the ends of (async) iterable {!r}'.format):
    L, r, I = get_loop_and_set(), [], iter_to_agen(it)
    async def consume():
        s, M, m, d = L.time(), 0, 0, defaultdict(list)
        async for x in amap(O.index, indices):
            if M is not None:
                if x < 0: M, m = None, min(m, x)
                else: M = max(x, M)
            d[x].append(F := L.create_future()); r.append(F)
        async def helper(i, j, d=d):
            async for x, F in aenumerate(d.pop(i, ())):
                if F.cancelled(): continue
                if F.done(): raise E.FutureCorrupted(f'future at index {x} associated with index {i} in the agetitems_from_indices function called on (async) iterable {it!r} had its result/exception set by an external party')
                F.set_result(j)
        try:
            if M is None:
                async def helper2(i, j): await helper(i, j); b.append(j)
                await aconsume(achain(astarmap(helper2, aenumerate(I)), amap(helper, acount(-1, -1), adisembowel(b := deque(maxlen=-m)), await_=True)))
            else: await aconsume(astarmap(helper, aenumerate(take(I, M)), True))
        except E.CRITICAL: raise E.Critical
        except BaseException as e:
            async for F in afilterfalse(O.methodcaller('done'), r): F.set_exception(e)
            raise
        a = _(it)
        for i, l in d.items():
            e = IndexError(a%i)
            async for x, F in aenumerate(l):
                if not F.cancelled():
                    if F.done(): raise ExceptionGroup('error while processing indices for which items were not successfully got', (e, E.FutureCorrupted(f'future at index {x} associated with index {i} in the agetitems_from_indices function called on (async) iterable {it!r} had its result/exception set by an external party')))
                    F.set_exception(e)
        if finish: await aconsume(I)
        if setatend is None: return
        if setatend.done() and not setatend.cancelled(): raise E.FutureCorrupted(f'future setatend at {id(setatend):#x} (exact type {fullname(setatend)}) passed to agetitems_from_indices had its result set by an external party')
        setatend.set_result(L.time()-s)
    c = L.create_task(consume())
    if setatend is not None: setatend.add_done_callback(lambda _: setattr(_, '__cancel', t := gather(safe_cancel(c), safe_cancel_batch(r))) or t.add_done_callback(lambda _: delattr(setatend, '__cancel')))
    audit('asyncutils.iters.agetitems_from_indices', fullname(it)); return r
async def aintersend(i1, i2):
    audit('asyncutils.iters.aintersend', fullname(i1), fullname(i2)); t = None, None; f, g = i1.asend, i2.asend
    while True: yield (t := tuple(await gather(f(t[1]), g(t[0]))))
async def asendstream(i1, i2):
    audit('asyncutils.iters.asendstream', fullname(i1), fullname(i2)); f = i1.asend
    async for v in iter_to_agen(i2): yield await f(v)
async def acat(first=None):
    audit('asyncutils.iters.acat', first)
    while True: first = yield first
async def aforever():
    audit('asyncutils.iters.aforever')
    while True: yield
async def _aguess(it, estlen, key, default, finish_event, cmp, f=_aextreme):
    if (r := await f(take(I := iter_to_agen(it), M.ceil(estlen*RECIP_E)), key, RAISE, cmp)) is RAISE:
        if default is _NO_DEFAULT: raise ValueError('empty (async) iterable passed with no default value')
        return default
    k = key(r)
    try:
        async for i in I:
            if cmp(key(i), k): return i
        return r
    finally:
        if not (finish_event is None or finish_event.is_set()): (t := (f := get_loop_and_set().create_task)(aconsume(I))).add_done_callback(lambda _: finish_event.set()); f(finish_event.wait()).add_done_callback(lambda _, t=t: t.cancel())
def aguessmax(it, estlen, *, key=_identity, default=_NO_DEFAULT, finish_event=None, _=_aguess): return _(it, estlen, key, default, finish_event, O.gt)
def aguessmin(it, estlen, *, key=_identity, default=_NO_DEFAULT, finish_event=None, _=_aguess): return _(it, estlen, key, default, finish_event, O.lt)
async def apowersoftwo(*, init=1, init_shift=0):
    init <<= init_shift
    while True: yield init; init <<= 1
def apowers(base, start=1): return aaccumulate(arepeat(base), O.mul, initial=start)
async def areversed(it, /):
    try:
        async for i in iter_to_agen(reversed(it)): yield i
    except TypeError:
        for i in reversed(await to_list(it)): yield i
async def arunlengthencode(it, /):
    async for k, g in agroupby(it): yield k, ailen(g)
def arunlengthdecode(it, /): return aflatten(astarmap(arepeat, it))
async def _dfthelper(a, i=False, /): return await to_tuple(take(apowers(M.e**((1 if i else -1)*1j*M.tau/(N := len(a := await to_tuple(a))))), N)), N, a
async def adft(a, /, _=_dfthelper):
    R, N, a = await _(a)
    async for k in arange(N): yield await asumprod(a, (R[k*i%N] async for i in arange(N)))
async def aidft(A, /, _=_dfthelper):
    R, N, A = await _(A, True)
    async for k in arange(N): yield await asumprod(A, (R[k*n%N] async for n in arange(N)))/N
async def _aargminmax(it, key, default, f): return (await f(aenumerate(amap(key, it)), key=O.itemgetter(1), default=default))[0]
def aargmin(it, key=_identity, default=-1, _=_aargminmax): return _(it, key, default, amin)
def aargmax(it, key=_identity, default=-1, _=_aargminmax): return _(it, key, default, amax)
def arunningmean(it): return amap(O.truediv, aaccumulate(it), acount(1))
async def apowersetofsets(it, *, frozen=True):
    S = tuple(dict.fromkeys(await to_list(amap(frozenset, azip(it)))))
    async for _ in aflatten(astarmap((frozenset if frozen else set).union, acombinations(S, r)) async for r in arange(len(S)+1)): yield _
async def aserialize(it):
    l, n = Lock(), iter_to_agen(it).__anext__
    while True:
        async with l: yield await n()
async def aonlinesorter(it=None):
    audit('asyncutils.iters.aonlinesorter'); from _heapq import heapify, heappop, heappush
    if (e := getattr(aonlinesorter, 'executor', None)) is None: e = create_executor(aonlinesorter)
    await (f := partial(get_loop_and_set().run_in_executor, e, Placeholder, h := [] if it is None else await to_list(it)))(heapify)
    while h:
        if (i := (yield await f(heappop))) is not None: await f(heappush, i)
del _aunzip_consumer_base, _aunzip_put, _aguess, _aargminmax, _aextreme, _factor_pollard, _shift_to_odd, _probable_prime, _dfthelper, check, check_methods, _littleprimes, _randrange, _sample, _smallprimes, _perfect_test, _randinst, _identity