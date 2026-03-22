from .config import _NO_DEFAULT, RAISE, _randinst
from .constants import RECIP_E
from .base import safe_cancel_batch, adisembowel, iter_to_aiter, collect, take, aenumerate, dummy_task
from .util import safe_cancel, get_aiter_fromf
from .iterclasses import achain, anullcontext
from ._internal.helpers import copy_and_clear, stop_and_closer, _filter_out, _get_loop_and_set, _check_methods
from collections import defaultdict, Counter, deque
from functools import partial, lru_cache
from sys import audit
from asyncio.queues import Queue, QueueEmpty, QueueShutDown, LifoQueue
from asyncio.locks import Lock, Event, Semaphore
from asyncio.exceptions import CancelledError
from asyncio.tasks import gather, wait_for, sleep
from asyncio.coroutines import iscoroutine
from . import exceptions as E
import _operator as O, math as M
from ._internal.submodules import iters_all as __all__
async def fmap(fs, /, *a, **k): return await gather(*[f(*a, **k) async for f in iter_to_aiter(fs)])
async def fmap_sequential(fs, /, *a, **k):
    async for f in iter_to_aiter(fs): yield await f(*a, **k)
async def map_on_map(outer, inner, it, *, inner_await=False, outer_await=False):
    f, g = (l := []).append, l.clear
    async for _ in amap(inner, it, await_=inner_await):
        async for _ in amap(outer, _, await_=outer_await): f(_)
        yield tuple(l); g()
def tee(it, n=2, *, maxqsize=0, put_exc=True, loop=None):
    if n <= 0: raise ValueError('n must be positive')
    if loop is None: loop = _get_loop_and_set()
    Q, a, l = tuple(Queue(maxqsize) for _ in range(n)), _NO_DEFAULT, Lock()
    async def iterator(q):
        nonlocal n
        while True:
            if (i := await q.get()) is a:
                async with l: n -= 1
                if n == 0: await safe_cancel(t)
                break
            elif put_exc and E.exception_occurred(i): raise i.exc
            else: yield i
    async def feed():
        async def helper(i): await gather(*(q.put(i) for q in Q), return_exceptions=True)
        try: await gather(*to_list(amap(helper, it)))
        except E.CRITICAL: raise E.Critical
        except BaseException as e:
            if put_exc: await helper(E.wrap_exc(e))
        finally: await helper(a)
    t = loop.create_task(feed()); return tuple(map(iterator, Q))
async def _aunzip_put(Q, t):
    for q, i in zip(Q, t): await q.put(i)
class _aunzip_consumer_base:
    __slots__ = 'q'
    def __init__(self): self.q = Queue()
    def __aiter__(self): return self
    def close(self): self.q.shutdown()
async def aunzip(ait, put_batch=16, fillvalue=_NO_DEFAULT, _a=_aunzip_put, _b=_aunzip_consumer_base):
    audit('asyncutils.iters.aunzip', ait, *_filter_out(fillvalue)); l = len(t := await anext(ait := iter_to_aiter(ait), ()))
    class aunzip_consumer(_b):
        __slots__ = ()
        async def __anext__(self, L=Lock(), f=partial(take, ait, put_batch, default=RAISE)):
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
async def merge_async_iters(*I, reverse=False):
    audit('asyncutils.iters.merge_async_iters', I); q, c, e, l, a = (LifoQueue if reverse else Queue)(), None, Event(), _get_loop_and_set(), _NO_DEFAULT
    async def drain(i, f=q.put):
        async for _ in i: await f(_)
    async def close():
        if reverse: await q.put(a); e.set()
        await gather(*(l.create_task(drain(iter_to_aiter(i))) for i in I))
        if not reverse: await q.put(a); e.set()
    l.create_task(close()); await e.wait()
    while True:
        if (c := await q.get()) is a: break
        yield c
def aflatten(it): return achain.from_iterable(it).__aiter__()
async def batch(it, size, max_concurrent_batches=8, timeout=None, strict=False):
    f, s, b, _ = iter_to_aiter(it).__anext__, anullcontext() if max_concurrent_batches is None else Semaphore(max_concurrent_batches), [], 0
    while True:
        try:
            for _ in range(size):
                try: b.append(await wait_for(f(), timeout))
                except StopAsyncIteration: break
                except TimeoutError:
                    if b: break
            if b:
                if strict and _ < size: raise ValueError('incomplete batch')
                async with s: yield copy_and_clear(b)
        except CancelledError:
            if b: yield copy_and_clear(b)
            raise
def achunked(it, n, strict=False):
    I = get_aiter_fromf(partial(collect, it, *_filter_out(n)), [])
    if strict:
        if n is None: raise ValueError('n cannot be None when strict is True')
        async def ret():
            async for c in I:
                if len(c) != n: raise ValueError('length of iterable is not divisible by n')
                yield c
        return ret()
    return I
async def asideeffect(f, it, /, *, size=None, before=None, after=None):
    try:
        if before is not None: before()
        if size is None:
            if iscoroutine(r := f(i := await anext(I := iter_to_aiter(it)))):
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
    async def ret():
        async for s in I:
            if len(s) != n: raise ValueError('seq is not divisible by n')
            yield s
    return ret()
def batch_buffer(items, batch_size, buffer_size, *, loop=None):
    d = deque(maxlen=buffer_size)
    if loop is None: loop = _get_loop_and_set()
    async def consumer():
        async for b in batch(items, batch_size): d.extend(b)
    loop.create_task(consumer()); return d
def buffer(it, maxsize=0, timeout=None, cooldown=0.1, *, loop=None):
    q = Queue(maxsize)
    if loop is None: loop = _get_loop_and_set()
    async def producer():
        try:
            async for _ in it:
                try: await wait_for(q.put(_), timeout)
                except TimeoutError: break
        finally: await c.aclose()
    async def consumer():
        try:
            while True:
                try: yield await q.get(); q.task_done()
                except QueueEmpty: await sleep(cooldown)
        finally: await safe_cancel(t)
    t, c = loop.create_task(producer()), consumer(); return c
async def asplitat(it, pred, maxsplit=-1, keep_sep=False):
    I = iter_to_aiter(it)
    if not maxsplit:
        r = []
        async for i in I: r.append(i)
        yield r; return
    b = []
    async for i in I:
        if pred(i):
            yield b
            if keep_sep: yield [i]
            if maxsplit == 1:
                r = []
                async for i in I: r.append(i)
                yield r; return
            b = []; maxsplit -= 1
        else: b.append(i)
    yield b
async def batch_process(items, size, processor):
    async for b in batch(items, size): yield await processor(b)
async def window(it, size, step):
    if not size >= 1 <= step: raise ValueError('size and step should both be >=1')
    b, c = deque(maxlen=size), 0
    async for i in it:
        b.append(i)
        if len(b) == size:
            if not c%step: size, step = (yield tuple(b)) or (size, step)
            c += 1
async def aall(it):
    async for _ in iter_to_aiter(it):
        if not _: return False
    return True
async def aany(it):
    async for _ in iter_to_aiter(it):
        if _: return True
    return False
def _compare(a, b):
    try: return a < b
    except TypeError, NotImplementedError: return b > a
async def amax(it, *, cmp=None, key=None, default=_NO_DEFAULT, __cmp=_compare):
    if (r := await anext(I := iter_to_aiter(it), _NO_DEFAULT)) is _NO_DEFAULT:
        if default is _NO_DEFAULT: raise ValueError('empty (async) iterable passed to amax with no default value')
        return default
    if cmp is None:
        if key is None:
            async for _ in I:
                if _ > r: r = _
        else:
            k, cmp = key(r), __cmp
            async for _ in I:
                if cmp(k, x := key(_)): k, r = x, _
    elif key is None:
        async for _ in I:
            if cmp(r, _): r = _
    else: raise TypeError('cannot pass both cmp and key')
    return r
async def amin(it, *, cmp=None, key=None, default=_NO_DEFAULT, __cmp=_compare):
    if (r := await anext(I := iter_to_aiter(it), _NO_DEFAULT)) is _NO_DEFAULT:
        if default is _NO_DEFAULT: raise ValueError('empty (async) iterable passed to amax with no default value')
        return default
    if cmp is None:
        if key is None:
            async for _ in I:
                if _ < r: r = _
        else:
            k, cmp = key(r), __cmp
            async for _ in I:
                if cmp(x := key(_), k): k, r = x, _
    elif key is None:
        async for _ in I:
            if cmp(_, r): r = _
    else: raise TypeError('cannot pass both cmp and key')
    return r
async def azip(*I, strict=False, _y=dummy_task):
    i = tuple(map(iter_to_aiter, I))
    while True:
        try: yield tuple(await gather(*map(anext, i)))
        except StopAsyncIteration:
            if strict:
                for x, y in enumerate(i):
                    try: await anext(y); raise ValueError(f'azip: iterable {x} longer than shortest iterable')
                    except StopAsyncIteration: continue
            await gather(*(f() if (f := getattr(_, 'aclose', None)) else _y for _ in i)); break
async def amap(f, /, *its, await_=False, strict=False):
    async for _ in azip(*its, strict=strict): r = f(*_); yield (await r) if await_ else r
async def afilter(f, it):
    if f is None: f = bool
    async for _ in iter_to_aiter(it):
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
    l, I = [], iter_to_aiter(it)
    async for i in I: yield i; l.append(i)
    t = tuple(l)
    while True:
        for i in t: yield i
async def arepeat(elem, n=None):
    if n is None or n < 0:
        while True: yield elem
    else:
        while n > 0: yield elem; n -= 1
async def aaccumulate(it, func=O.add, *, initial=None):
    it = iter_to_aiter(it)
    if initial is None:
        try: initial = await anext(it)
        except StopAsyncIteration: return
    yield initial
    async for _ in it: yield (initial := func(initial, _))
async def acompress(data, selectors):
    async for i, j in azip(data, selectors):
        if j: yield i
async def adropwhile(pred, it):
    I = iter_to_aiter(it)
    async for _ in I:
        if not pred(_): yield _; break
    async for _ in I: yield _
def afilterfalse(f, it): return afilter(lambda i: not (f or bool)(i), it)
async def agroupby(it, key):
    I, e = iter_to_aiter(it), False
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
async def aislice(it, /, *a):
    x, y, z = 0 if (s := slice(*map(int, a))).start is None else s.start, s.stop, 1 if s.step is None else s.step
    if x < 0 or (y is not None and y < 0) or z <= 0: raise ValueError('invalid indices')
    I, n = acount() if y is None else arange(max(x, y)), x
    async for i, j in azip(I, it):
        if i == n: yield j; n += z
async def aiterindex(it, value, start=0, stop=None):
    async for i, j in aenumerate(aislice(it, start, stop), start):
        if j is value or j == value: yield i
async def asieve(n):
    if n < 2: return
    yield 2; s, d = 3, bytearray(range(2))*(n>>1)
    async for p in aiterindex(d, 1, s, M.isqrt(n)+1):
        async for i in aiterindex(d, 1, s, q := p*p): yield i
        d[q:n:x], s = bytes(len(range(q, n, x := p<<1))), q
    async for i in aiterindex(d, 1, s): yield i
async def apairwise(it):
    try: a = await anext(I := iter_to_aiter(it))
    except StopAsyncIteration: return
    async for b in I: yield a, b; a = b
async def atriplewise(it):
    a, b, c = tee(iter_to_aiter(it), 3); await gather(*(anext(g, None) for g in (b, c, c)))
    async for _ in azip(a, b, c): yield _
async def aproduct(*its, repeat=1):
    if repeat < 0: raise ValueError('repeat cannot be negative')
    r = [()]
    async for p in arepeat(amap(to_tuple, its, await_=True), repeat): r = [x+(y,) for x in r async for y in p]
    for _ in r: yield tuple(_)
async def astarmap(f, it, /, await_=False):
    async for _ in iter_to_aiter(it): yield (await f(*_)) if await_ else f(*_)
async def atakewhile(pred, it):
    if pred is None: pred = bool
    async for _ in iter_to_aiter(it):
        if not pred(_): break
        yield _
async def atotient(n):
    f = (s := set()).add
    async for p in afactor(n):
        if p not in s: f(p); n -= n//p
    return n
def asquaresum(it): return asumprod(*tee(it))
async def aziplongest(*its, fillvalue=None):
    n = len(I := list(map(iter_to_aiter, its)))
    while True:
        v = []
        for i, a in enumerate(I):
            try: _ = await anext(a)
            except StopAsyncIteration:
                n -= 1
                if not n: return
                I[i], _ = arepeat(fillvalue), fillvalue
            v.append(_)
        yield tuple(v)
def asumprod(p, q, /): return asum(amap(O.mul, p, q, strict=True))
async def aconvolve(signal, kernel):
    w = deque((0,), n := len(K := await to_tuple(await areversed(kernel))))*n
    async for x in achain(signal, arepeat(0, n-1)): w.append(x); yield await asumprod(K, w)
def atabulate(f, start=0, step=1, /, *, await_=False): return amap(f, acount(start, step), await_=await_)
async def asum(it, start=0):
    async for i in iter_to_aiter(it): start += i
    return start
async def aprod(it, start=1):
    async for i in iter_to_aiter(it): start *= i
    return start
async def amatprod(it, start):
    async for i in iter_to_aiter(it): start @= i
    return start
def atail(n, it, /):
    try: return aislice(it, max(0, len(it)-n), None)
    except TypeError:
        async def f():
            d = deque(maxlen=n)
            async for _ in iter_to_aiter(it): d.append(_)
            for _ in d: yield _
        return f()
def amultinomial(*c): return aprod(amap(M.comb, aaccumulate(c), c))
async def to_tuple(it, /): return tuple(await to_list(it))
async def to_list(it, /):
    f = (r := []).append
    async for _ in iter_to_aiter(it): f(_)
    return r
_randrange, _sample, _smallprimes, _perfect_test = _randinst.randrange, _randinst.sample, frozenset(_littleprimes := (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199)), ((2047, (2,)), (9080191, (31, 73)), (4759123141, (2, 7, 61)), (1122004669633, (2, 13, 23, 1662803)), (2152302898747, (2, 3, 5, 7, 11)), (3474749660383, (2, 3, 5, 7, 11, 13)), (18446744073709551616, (2, 325, 9375, 28178, 450775, 9780504, 1795265022)), (3317044064679887385961981, (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)))
async def aconsume(it, n=None):
    if n is None:
        async for _ in iter_to_aiter(it): ...
    else: await anext(aislice(it, n, n), None)
def anth(it, n, default=_NO_DEFAULT): return anext(aislice(it, n, None), *_filter_out(default, s=_NO_DEFAULT))
async def aallequal(it, key=lambda _: _, strict=False):
    I = agroupby(it, key)
    async for _ in I:
        async for _ in I: return False
        return True
    if strict: raise ValueError('iterable provided is empty')
    return True
async def acombinations(it, r):
    if r > (n := len(p := await to_tuple(it))): return
    I = list(range(r)); yield p[:r]
    while True:
        for i in reversed(range(r)):
            if I[i] != i+n-r: break
        else: return
        I[i] += 1
        for j in range(i+1, r): I[j] = I[j-1]+1
        yield tuple(p[i] for i in I)
async def acombinations_with_replacement(it, r):
    if not (n := len(p := await to_tuple(it))) and r: return
    I = [0]*r; yield (p[0],)*r
    while True:
        for i in reversed(range(r)):
            if I[i] != n-1: break
        else: return
        I[i:] = [I[i]+1]*(r-i); yield tuple(p[i] for i in I)
async def apermutations(it, r=None):
    n = len(p := await to_tuple(it))
    if (r := n if r is None else r) > n: return
    I, C = list(range(n)), list(range(n, n-r, -1)); yield p[:r]
    while n:
        for i in reversed(range(r)):
            C[i] -= 1
            if C[i]: I[i], I[-j] = I[-(j := C[i])], I[i]; yield tuple(p[i] for i in I[:r]); break
            else: I[i:], C[i] = I[i+1:]+I[i:i+1], n-i
        else: return
async def apowerset(it):
    s = await to_tuple(it)
    async for _ in achain.from_iterable(acombinations(s, r) for r in range(len(s)+1)): yield _
def aquantify(it, pred=bool): return asum(amap(pred, it))
def apadnone(it): return achain(it, arepeat(None)).__aiter__()
def agrouper(it, n, fillvalue=_NO_DEFAULT): I = (iter_to_aiter(it),)*n; return azip(*I, strict=True) if fillvalue is RAISE else azip(*I) if fillvalue is _NO_DEFAULT else aziplongest(*I, fillvalue=fillvalue)
async def aroundrobin(*its):
    I = (iter_to_aiter(i) for i in its)
    for i in range(len(its), 0, -1):
        async for _ in (I := acycle(aislice(I, i))): yield await anext(_)
async def aroundrobin2(*its):
    async for X in aziplongest(*its, fillvalue=_NO_DEFAULT):
        for x in X:
            if x is not _NO_DEFAULT: yield x
async def aunique_everseen(it, key=lambda _: _):
    A, a, C, c = (S := set()).add, (s := []).append, *map(O.attrgetter('__contains__'), (S, s))
    async for i in iter_to_aiter(it):
        k = key(i)
        try:
            if not C(k): A(k); yield i
        except TypeError:
            if not c(k): a(k); yield i
def aunique_justseen(it, key=lambda _: _, _=O.itemgetter): return amap(_(0), agroupby(it)) if key is None else amap(anext, amap(_(1), agroupby(it, key)), await_=True)
async def aunique(it, key=None, reverse=False):
    async for _ in aunique_justseen(await asorted(it, key=key, reverse=reverse), key): yield _
async def ancycles(it, n):
    async for _ in achain.from_iterable(arepeat(await to_tuple(it), n)): yield _
def apartition(pred, it):
    if pred is None: pred = bool
    s, t, p = tee(iter_to_aiter(it), 3); u, v = tee(amap(pred, p)); return acompress(s, amap(O.not_, u)), acompress(t, v)
async def aiterexcept(f, exc):
    while True:
        try: yield await f()
        except exc: return
async def ailen(it):
    i = 0
    async for _ in iter_to_aiter(it): i += 1
    return i
async def aiterate(f, start):
    while True: yield start; start = await f(start)
async def with_aiter(actxmgr):
    async with actxmgr as I:
        async for i in iter_to_aiter(I): yield i
async def asorted(it, *, key=lambda _, /: _, reverse=False):
    from heapq import heappush as f, heappop as g
    m, a = [], (r := []).append
    async for i, j in aenumerate(it): f(m, (key(j), i, j))
    while m: a(g(m))
    if reverse: r.reverse()
    return r
def acanonical(it): return asorted(it, key=id, reverse=True)
async def adistinctpermutations(it, r=None):
    async def _full(A):
        while True:
            yield tuple(A)
            for i in range(_-2, -1, -1):
                if A[i] < A[i+1]: break
            else: return
            j = _-1
            for j in range(j, i, -1):
                if A[i] < A[j]: break
            A[i], A[j] = A[j], A[i]; A[i+1:] = A[:i-_:-1]
    async def _partial(A):
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
    if (S := len(I := await to_list(it))) < (_ := S if r is None else r): yield (); return
    if _ <= 0: return
    a = _full if _ == S else _partial
    try: I.sort(); R = a(I)
    except TypeError:
        d = defaultdict(list)
        for i in I: d[I.index(i)].append(i)
        R = amap(lambda i, E={k: acycle(v) for k, v in d.items()}: to_tuple(await anext(E[_]) for _ in i), a(sorted(map(I.index, I))), await_=True)
    async for _ in R: yield _
async def auniquetoeach(*its):
    p = await to_tuple(amap(to_tuple, its, await_=True))
    async for _ in amap(partial(afilter, frozenset(i for i, j in Counter(await to_list(aflatten(map(frozenset, p)))).items() if j == 1).__contains__), p): yield _
async def aderangements(it, r=None):
    async for _ in acompress(apermutations(X := await to_tuple(it), r), amap(aall, amap(amap, arepeat(O.is_not), arepeat(Y := tuple(range(len(X)))), apermutations(Y, r)), await_=True)): yield _
def aintersperse(e, it, n=1):
    if n <= 0: raise ValueError('n must be positive')
    return aislice(ainterleave_stopearly(arepeat(e), it), 1, None) if n == 1 else aflatten(aislice(ainterleave_stopearly(arepeat((e,)), batch(it, n)), 1, None))
def ainterleave_stopearly(*it): return aflatten(azip(*it))
def ainterleave(*it): return afilter(O.is_not.__get__(_NO_DEFAULT), aflatten(aziplongest(*it, fillvalue=_NO_DEFAULT)))
def aspy(it, n=1): p, q = tee(it); return take(q, n), p
async def ainterleaveevenly(its, lengths=None):
    I = await to_tuple(its)
    try:
        if (X := len(I)) != len(L := await to_tuple(lengths or map(len, I))): raise ValueError('mismatch in length of its and lengths')
    except TypeError: raise ValueError('ainterleaveevenly: cannot determine lengths of (async) iterables') from None
    A, *a = map(f := L.__getitem__, _ := sorted(range(X), key=f, reverse=True)); B, *b = (iter_to_aiter(I[i]) for i in _); E, t = [A//X]*len(a), sum(L)
    while t:
        yield await anext(B); t -= 1; E = list(map(O.sub, E, a))
        for i, e in enumerate(E):
            if e < 0: yield await anext(b[i]); t -= 1; E[i] += A
async def ainterleaverandomly(its, _=_randrange):
    x = len(I := [iter_to_aiter(i) async for i in iter_to_aiter(its)])
    while x:
        i = _(x)
        try: yield await anext(I[i])
        except StopAsyncIteration: I[i] = I[-1]; del I[-1]; x -= 1
async def acollapse(it, base_typ=(str, bytes), levels=None):
    (S := deque()).appendleft((0, arepeat(iter_to_aiter(it), 1))); L, f, g = levels or float('inf'), S.popleft, S.extendleft
    while S:
        l, n = N = f()
        if l > L:
            async for i in n: yield i
            continue
        async for _ in n:
            if isinstance(_, base_typ): yield _
            else:
                try: t = iter_to_aiter(_); g(((l+1, t), N)); break
                except TypeError: yield _
def afirsttrue(it, default=_NO_DEFAULT, pred=None): F = afilter(pred, it); return anext(F, *_filter_out(default, _NO_DEFAULT))
def aprepend(val, it): return achain((val,), it).__aiter__()
async def arandomproduct(*a, n=1, _=_randinst.choice):
    async for i in ancycles(amap(to_tuple, a, await_=True), n): yield _(i)
async def arandomcombination(it, r, _=_sample):
    for i in sorted(_(range(len(p := await to_tuple(it))), r)): yield p[i]
async def arandom_combination_with_replacement(it, r, _=_randrange):
    n = len(p := await to_tuple(it))
    async for _ in amap(p.__getitem__, sorted(_(n) for _ in range(r))): yield _
async def arandompermutation(it, r=None, _=_sample):
    p = await to_tuple(it)
    if r is None: r = len(p)
    for _ in _(p, r): yield _
async def afirst(it, default=_NO_DEFAULT):
    try:
        async for i in it: return i
    except TypeError:
        for i in it: return i
    if default is _NO_DEFAULT: raise ValueError('afirst called on empty iterable without default value')
    return default
async def alast(it, default=_NO_DEFAULT, _=_check_methods):
    try:
        if _(it, '__getitem__'): return it[-1]
        return (await to_list(it))[-1] if (f := getattr(it, '__reversed__', None)) is None else f().__next__()
    except IndexError, TypeError, StopIteration, StopAsyncIteration:
        if default is _NO_DEFAULT: raise ValueError('alast() called on empty iterable without default value')
        return default
def anthorlast(it, n, default=_NO_DEFAULT): return alast(aislice(it, n+1), default)
def abeforeandafter(pred, it): a, b = tee(it); return acompress(atakewhile(pred, a), azip(b)), b
async def anthcombination(it, r, idx):
    if r > (n := len(p := await to_tuple(it))) or r < 0: raise ValueError('inappropriate value of r')
    c, k = 1, min(r, n-r)
    for i in range(1, k+1): c = c*(n-k+i)//i
    if idx < 0: idx += c
    if idx < 0 or idx >= c: raise IndexError('inappropriate value of idx')
    while r:
        c, n, r = c*r//n, n-1, r-1
        while idx >= c: idx -= c; c, n = c*(n-r)//n, n-1
        yield p[~n]
async def asubslices(it):
    async for _ in astarmap(O.getitem, azip(arepeat(s := await to_tuple(it)), astarmap(slice, acombinations(range(len(s)+1), 2)))): yield _
def arepeatfunc(f, times=None, *a): return astarmap(f, arepeat(a) if times is None else arepeat(a, times), True)
async def apolynomialfromroots(roots):
    p = arange(1, 2)
    async for r in iter_to_aiter(roots): p = aconvolve(p, (1, -r))
    async for _ in p: yield _
async def atranspose(it):
    async for _ in azip(*await to_tuple(it), strict=True): yield _
async def aflattentensor(tensor, base=(str, bytes), _c=_check_methods):
    I = iter_to_aiter(tensor)
    while True:
        try: v = await anext(I)
        except StopAsyncIteration: break
        I = aprepend(v, I)
        if isinstance(v, base) or not (_c(v, '__iter__') or _c(v, '__aiter__')): break
        I = aflatten(I)
    async for i in I: yield i
async def apolynomialderivative(coeff):
    f = (r := []).append
    async for _ in iter_to_aiter(coeff): f(_)
    async for _ in amap(O.mul, r, range(len(r)-1, 0)): yield _
async def apolynomialeval(coeff, x):
    if not (n := len(t := await to_tuple(coeff))): return type(x)(0)
    return await asumprod(t, amap(pow, arepeat(x), range(n-1, -1)))
async def areshape(mat, shape):
    if isinstance(shape, int): I = batch(aflatten(mat), shape, None)
    else: d = anext(shape := iter_to_aiter(shape)); from .func import areduce as f; I = aislice(await f(batch, areversed(shape), aflattentensor(mat), await_=False), d)
    async for i in I: yield i
async def _factor_pollard(n):
    if n == 4: return 2
    async for b in arange(1, n):
        x = y = 2; d = 1
        while d == 1: d = M.gcd((x := (x*x+b)%n)-(y := ((z := (y*y+b)%n)*z+b)%n), n)
        if d != n: return d
    raise ValueError(f'{n} is prime')
def _shift_to_odd(n):
    d = n>>(s := ((n-1)^n).bit_length()-1)
    if not ((1<<s)*d == n and d&1 and s > -1): raise ValueError('invalid n')
    return s, d
def _probable_prime(n, base, _=lru_cache(_shift_to_odd)):
    s, d = _(n-1)
    if (x := pow(base, d, n)) in (1, n-1): return True
    for _ in range(s-1):
        if (x := x*x%n) == n-1: return True
    return False
async def _aisprime(n, _smallprimes=_smallprimes, _perfect_test=_perfect_test, _randrange=_randrange, _probable_prime=_probable_prime):
    if n < 210: return n in _smallprimes
    if not (n&1 and n%3 and n%5 and n%7 and n%11 and n%13 and n%17): return False
    for l, B in _perfect_test:
        if n < l: break
    else: B = (_randrange(2, n-1) for _ in range(64))
    return await aall(amap(partial(_probable_prime, n), B))
async def afactor(n, _littleprimes=_littleprimes, _aisprime=_aisprime, _factor_pollard=_factor_pollard):
    if n < 2: raise ValueError('no prime factors')
    for p in _littleprimes:
        while not n%p: yield p; n //= p
    if n < 2: return
    t = [n]
    for n in t:
        if n < 44521 or await _aisprime(n): yield n
        else: t += (f := await _factor_pollard(n), n//f)
async def arunningmedian(it, *, maxlen=None):
    if maxlen is None:
        r, l, h = iter_to_aiter(it).__aiter__().__anext__, [], []; from heapq import heappush_max as a, heappush as b, heappushpop_max as c
        while True: a(l, await r()); yield l[0]; b(h, c(l, await r())); yield (l[0]+h[0])/2
    if (m := O.index(maxlen)) <= 0: raise ValueError('window size should be positiive')
    w, o = deque(), []; from bisect import bisect_left as b, insort_right as f
    async for i in iter_to_aiter(it):
        w.append(i); f(o, i)
        if (n := len(o)) > m: del o[b(o, w.popleft())]; n -= 1
        m = n>>1; yield o[m] if n&1 else (o[m-1]+o[m])/2
async def arandomderangement(it, _=_randinst.shuffle):
    s = await to_tuple(it)
    if (l := len(s)) < 2:
        if s: raise IndexError('no derangements to choose from')
        return ()
    i = tuple(p := list(range(l)))
    while True:
        _(p)
        if not await aany(amap(O.is_, i, p)): return O.itemgetter(*p)(s)
async def amatmul(M, N):
    M, N = map(iter_to_aiter, (M, N)); N = aprepend(t := await to_tuple(await anext(N)), N)
    async for i in batch(astarmap(asumprod, aproduct(M, atranspose(N)), True), len(t)): yield i
async def mat_vec_mul(M, V):
    n, v = len(p := await to_tuple(amap(to_tuple, M, await_=True))), await to_tuple(V)
    async for i in arange(n): yield await asum(p[i][j]*v[j] async for j in arange(n))
def vecs_eq(u, v): return aall(i == j async for i, j in azip(u, v))
async def afrievalds(A, B, C, k=2, _r=_randinst.randint): n = len(A := await to_tuple(A)); return await aall(await vecs_eq(mat_vec_mul(A, mat_vec_mul(B, r := tuple(_r(0, 1) for _ in range(n)))), mat_vec_mul(C, r)) async for _ in arange(k))
async def basic_collect(it, n):
    l = []
    async for _ in aislice(it, n): l.append(_)
    return l
async def asubstrings(it):
    s = []
    async for i in iter_to_aiter(it): s.append(i); yield i,
    c = len(s := tuple(s))+1
    async for n in arange(2, c):
        async for i in arange(c-n): yield s[i:i+n]
def asubstrindices(seq, reverse=False):
    r = range(1, x := len(seq)+1)
    if reverse: r = reversed(r)
    return ((seq[i:i+L], i, i+L) for L in r async for i in arange(x-L))
def iter_future(it, summaryf=aconsume):
    async def task(): t = L.time(); await summaryf(it); F.set_result(L.time()-t)
    F = (L := _get_loop_and_set()).create_future(); L.create_task(task()); return F
def agetitems_from_indices(it, indices, setatend=None, finish=False, _='index %r beyond the ends of (async) iterable %r'):
    L, r, I = _get_loop_and_set(), [], iter_to_aiter(it)
    async def consume():
        s, M, m, d = L.time(), 0, 0, defaultdict(list)
        async for x in amap(O.index, indices):
            if M is not None:
                if x < 0:
                    M = None
                    if x < m: m = x
                elif x > M: M = x
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
        for i, l in d.items():
            e = IndexError(_%(i, it))
            async for x, F in aenumerate(l):
                if F.cancelled(): continue
                if F.done(): raise ExceptionGroup('error while processing indices for which items were not successfully got', (e, E.FutureCorrupted(f'future at index {x} associated with index {i} in the agetitems_from_indices function called on (async) iterable {it!r} had its result/exception set by an external party')))
                else: F.set_exception(e)
        if finish: await aconsume(I)
        if setatend is None: return
        if setatend.done() and not setatend.cancelled(): raise E.FutureCorrupted(f'setatend {type(setatend).__qualname__} passed to agetitems_from_indices had its result set by an external party')
        setatend.set_result(L.time()-s)
    c = L.create_task(consume())
    if setatend is not None: setatend.add_done_callback(lambda _: L.run_until_complete(gather(safe_cancel(c), safe_cancel_batch(r))))
    audit('asyncutils.iters.agetitems_from_indices', it, r); return r
async def aintersend(i1, i2):
    audit('asyncutils.iters.aintersend', i1, i2); a, b = await gather(anext(i1), anext(i2))
    while True: yield a, b; a, b = await gather(i1.asend(b), i2.asend(a))
async def asendstream(i1, i2):
    audit('asyncutils.iters.asendstream', i1, i2)
    async for v in iter_to_aiter(i2): yield await i1.asend(v)
async def acat(first=None):
    audit('asyncutils.iters.acat', first)
    while True: first = yield first
async def aforever():
    audit('asyncutils.iters.aforever')
    while True: yield
async def aguessmax(it, estlen, *, key=None, default=_NO_DEFAULT, finish_event=None, __cmp=_compare):
    if (r := await amax(take(I := iter_to_aiter(it), M.ceil(estlen*RECIP_E)), key=(K := key or (lambda x: x)), default=(o := object()))) is o:
        if default is _NO_DEFAULT: raise ValueError('empty (async) iterable passed to aguessmax with no default value')
        return default
    k = K(r)
    try:
        async for i in I:
            if __cmp(k, K(i)): return i
        return r
    finally:
        if not (finish_event is None or finish_event.is_set()): (t := (f := (l := _get_loop_and_set()).create_task)(aconsume(I))).add_done_callback(lambda _: finish_event.set()); f(finish_event.wait()).add_done_callback(lambda _, t=t, l=l: t.cancel() or stop_and_closer(l))
async def aguessmin(it, estlen, *, key=None, default=_NO_DEFAULT, finish_event=None, __cmp=_compare):
    if (r := await amin(take(I := iter_to_aiter(it), M.ceil(estlen*RECIP_E)), key=(K := key or (lambda x: x)), default=(o := object()))) is o:
        if default is _NO_DEFAULT: raise ValueError('empty (async) iterable passed to aguessmax with no default value')
        return default
    k = K(r)
    try:
        async for i in I:
            if __cmp(K(i), k): return i
        return r
    finally:
        if not (finish_event is None or finish_event.is_set()): (t := (f := (l := _get_loop_and_set()).create_task)(aconsume(I))).add_done_callback(lambda _: finish_event.set()); f(finish_event.wait()).add_done_callback(lambda _, t=t, l=l: t.cancel() or stop_and_closer(l))
async def apowersoftwo(*, init=1, init_shift=0):
    init <<= init_shift
    while True: yield init; init <<= 1
async def areversed(it, /):
    try:
        async for i in iter_to_aiter(reversed(it)): yield i
    except TypeError:
        f = (l := []).append
        async for i in iter_to_aiter(it): f(i)
        for i in reversed(l): yield i
del _aunzip_consumer_base, _aunzip_put, _compare, _factor_pollard, _shift_to_odd, _probable_prime, _aisprime, _check_methods, _littleprimes, _randrange, _sample, _smallprimes, _perfect_test, _randinst