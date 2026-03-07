# type: ignore
from .config import _NO_DEFAULT, RAISE, _randinst
from .constants import RECIP_E
from .exceptions import Critical, ItemsExhausted, FutureCorrupted, exception_occurred, wrap_exc, CRITICAL
from .base import safe_cancel_batch, adisembowel, iter_to_aiter, collect, take, aenumerate, aiter_to_iter, dummy_task
from .util import safe_cancel, to_async, get_aiter_fromf
from .func import areduce
from .iterclasses import achain, anullcontext
from ._internal.log import debug
from ._internal.helpers import copy_and_clear, stop_and_closer, _filter_out, _get_loop_no_exit, _check_methods, pkgpref
from collections import defaultdict, Counter, deque
from functools import partial, lru_cache
from _operator import attrgetter, itemgetter, methodcaller, add, mul, not_, is_, is_not, sub, getitem, index
from sys import audit
from bisect import insort_right, bisect_left
from heapq import heappush, heappush_max, heappushpop_max
from math import isqrt, comb, gcd, ceil
from asyncio.queues import Queue, QueueEmpty, QueueShutDown, LifoQueue
from asyncio.locks import Lock, Event, Semaphore
from asyncio.exceptions import CancelledError
from asyncio.tasks import gather, wait_for, sleep
from asyncio.coroutines import iscoroutine
TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import SupportsIndex, Any, Literal, overload
    from _collections_abc import Awaitable, Iterable, AsyncIterable, AsyncGenerator, AsyncIterator, Callable, Coroutine, Hashable, Sequence
    from asyncio.events import AbstractEventLoop
    from asyncio.futures import Future
    from ._internal.protocols import SupportsIteration, Exceptable, SupportsRichComparison, AsyncContextManager, SupportsSlicing
    __all__ = ('tee', 'aunzip', 'merge_async_iters', 'aflatten', 'batch', 'achunked', 'asideeffect', 'asliced', 'batch_buffer', 'buffer', 'asplitat', 'batch_process', 'window', 'aall', 'aany', 'amax', 'amin', 'azip', 'amap', 'afilter', 'arange', 'acount', 'acycle', 'arepeat', 'aaccumulate', 'acompress', 'adropwhile', 'afilterfalse', 'agroupby', 'aislice', 'aiterindex', 'asieve', 'apairwise', 'atriplewise',
        'aproduct', 'astarmap', 'atakewhile', 'atotient', 'asquaresum', 'aziplongest', 'asumprod', 'aconvolve', 'atabulate', 'asum', 'aprod', 'atail', 'amultinomial', 'to_tuple', 'anth', 'aconsume', 'aallequal', 'acombinations', 'acombinations_with_replacement', 'apermutations', 'apowerset', 'aquantify', 'apadnone', 'agrouper', 'aroundrobin', 'aroundrobin2', 'aunique_everseen', 'aunique_justseen',
        'aunique', 'ancycles', 'apartition', 'aiterexcept', 'ailen', 'aiterate', 'with_aiter', 'asorted', 'acanonical', 'adistinctpermutations', 'auniquetoeach', 'aderangements', 'aintersperse', 'ainterleave', 'ainterleaveevenly', 'ainterleaverandomly', 'aspy', 'acollapse', 'afirsttrue', 'aprepend', 'arandomproduct', 'arandomcombination', 'arandom_combination_with_replacement', 'afirst',
        'alast', 'anthorlast', 'abeforeandafter', 'anthcombination', 'arepeatfunc', 'asubslices', 'atranspose', 'apolynomialfromroots', 'apolynomialeval', 'apolynomialderivative', 'areshape', 'afactor', 'arunningmedian', 'arandomderangement', 'amatmul', 'mat_vec_mul', 'vecs_eq', 'afrievalds', 'basic_collect', 'asubstrings', 'asubstrindices', 'iter_future', 'agetitems_from_indices', 'aintersend',
        'asendstream', 'acat', 'aforever', 'aguessmax', 'aguessmin', 'apowersoftwo', 'amatprod', 'amapif', 'amultimapif', 'fmap', 'fmap_sequential', 'map_on_map', 'areversed')
else: from ._internal.submodules import iters_all as __all__; Any, overload = None, lambda _, /: None
async def fmap[T, **P](fs: SupportsIteration[Callable[P, Awaitable[T]]], *a: P.args, **k: P.kwargs): return await gather(*[f(*a, **k) async for f in iter_to_aiter(fs)])
async def fmap_sequential[T, **P](fs: SupportsIteration[Callable[P, Awaitable[T]]], *a: P.args, **k: P.kwargs):
    async for f in iter_to_aiter(fs): yield await f(*a, **k)
@overload
def map_on_map[T, R, V](outer: Callable[[R], V], inner: Callable[[T], SupportsIteration[R]], it: SupportsIteration[T], *, inner_await: Literal[False]=..., outer_await: Literal[False]=...) -> AsyncGenerator[tuple[V, ...], None]: ...
@overload
def map_on_map[T, R, V](outer: Callable[[R], Awaitable[V]], inner: Callable[[T], SupportsIteration[R]], it: SupportsIteration[T], *, inner_await: Literal[False]=..., outer_await: Literal[True]) -> AsyncGenerator[tuple[V, ...], None]: ...
@overload
def map_on_map[T, R, V](outer: Callable[[R], V], inner: Callable[[T], Awaitable[SupportsIteration[R]]], it: SupportsIteration[T], *, inner_await: Literal[True], outer_await: Literal[False]=...) -> AsyncGenerator[tuple[V, ...], None]: ...
@overload
def map_on_map[T, R, V](outer: Callable[[R], Awaitable[V]], inner: Callable[[T], Awaitable[SupportsIteration[R]]], it: SupportsIteration[T], *, inner_await: Literal[True], outer_await: Literal[True]) -> AsyncGenerator[tuple[V, ...], None]: ...
async def map_on_map(outer, inner, it, *, inner_await=False, outer_await=False):
    f, g = (l := []).append, l.clear
    async for _ in amap(inner, it, await_=inner_await):
        async for _ in amap(outer, _, await_=outer_await): f(_)
        yield tuple(l); g()
def tee[T](it: SupportsIteration[T], n: int=2, *, maxqsize: int=0, put_exc: bool=True, loop: AbstractEventLoop|None=None) -> tuple[AsyncGenerator[T], ...]:
    if n <= 0: raise ValueError('n must be positive')
    if loop is None: loop = _get_loop_no_exit()
    Q, a, l = tuple(Queue(maxqsize) for _ in range(n)), _NO_DEFAULT, Lock()
    async def iterator(q):
        nonlocal n
        while True:
            if (i := await q.get()) is a:
                async with l: n -= 1
                if n == 0: await safe_cancel(t)
                break
            elif put_exc and exception_occurred(i): raise i.exc
            else: yield i
    async def feed():
        async def helper(i): await gather(*(q.put(i) for q in Q), return_exceptions=True)
        try: await gather(*(helper(i) for i in aiter_to_iter(it)))
        except CRITICAL: raise Critical
        except BaseException as e:
            if put_exc: await helper(wrap_exc(e))
        finally: await helper(a)
    t = loop.create_task(feed()); return tuple(map(iterator, Q))
async def _aunzip_put(Q, t):
    for q, i in zip(Q, t): await q.put(i)
@overload
async def aunzip[T](ait: SupportsIteration[tuple[T]], put_batch: int=...) -> tuple[AsyncIterator[T]]: ...
@overload
async def aunzip[T, R](ait: SupportsIteration[tuple[T|R]], put_batch: int, fillvalue: R) -> tuple[AsyncIterator[T]]: ...
@overload
async def aunzip[T, R](ait: SupportsIteration[tuple[T|R]], *, fillvalue: R) -> tuple[AsyncIterator[T]]: ...
@overload
async def aunzip[T, S](ait: SupportsIteration[tuple[T, S]], put_batch: int=...) -> tuple[AsyncIterator[T], AsyncIterator[S]]: ...
@overload
async def aunzip[T, S, R](ait: SupportsIteration[tuple[T|R, S|R]], put_batch: int, fillvalue: R) -> tuple[AsyncIterator[T], AsyncIterator[S]]: ...
@overload
async def aunzip[T, S, R](ait: SupportsIteration[tuple[T|R, S|R]], *, fillvalue: R) -> tuple[AsyncIterator[T], AsyncIterator[S]]: ...
@overload
async def aunzip[T, S, V](ait: SupportsIteration[tuple[T, S, V]], put_batch: int=...) -> tuple[AsyncIterator[T], AsyncIterator[S], AsyncIterator[V]]: ...
@overload
async def aunzip[T, S, V, R](ait: SupportsIteration[tuple[T|R, S|R, V|R]], put_batch: int, fillvalue: R) -> tuple[AsyncIterator[T], AsyncIterator[S], AsyncIterator[V]]: ...
@overload
async def aunzip[T, S, V, R](ait: SupportsIteration[tuple[T|R, S|R, V|R]], *, fillvalue: R) -> tuple[AsyncIterator[T], AsyncIterator[S], AsyncIterator[V]]: ...
@overload
async def aunzip[T, S, V, U](ait: SupportsIteration[tuple[T, S, V, U]], put_batch: int=...) -> tuple[AsyncIterator[T], AsyncIterator[S], AsyncIterator[V], AsyncIterator[U]]: ...
@overload
async def aunzip[T, S, V, U, R](ait: SupportsIteration[tuple[T|R, S|R, V|R, U|R]], put_batch: int, fillvalue: R) -> tuple[AsyncIterator[T], AsyncIterator[S], AsyncIterator[V], AsyncIterator[U]]: ...
@overload
async def aunzip[T, S, V, U, R](ait: SupportsIteration[tuple[T|R, S|R, V|R, U|R]], *, fillvalue: R) -> tuple[AsyncIterator[T], AsyncIterator[S], AsyncIterator[V], AsyncIterator[U]]: ...
@overload
async def aunzip[T](ait: SupportsIteration[tuple[T, ...]], put_batch: int=...) -> tuple[AsyncIterator[T], ...]: ...
@overload
async def aunzip[T, R](ait: SupportsIteration[tuple[T|R, ...]], put_batch: int, fillvalue: R) -> tuple[AsyncIterator[T], ...]: ...
@overload
async def aunzip[T, R](ait: SupportsIteration[tuple[T|R, ...]], *, fillvalue: R) -> tuple[AsyncIterator[T], ...]: ...
@overload
async def aunzip(ait: SupportsIteration[tuple[Any, ...]], put_batch: int=..., fillvalue: Any=...) -> tuple[AsyncIterator[Any], ...]: ...
async def aunzip(ait, put_batch=16, fillvalue=_NO_DEFAULT, _a=_aunzip_put):
    audit(f'{pkgpref}iters.aunzip', ait, *_filter_out(fillvalue)); l = len(t := await anext(I := iter_to_aiter(ait), ()))
    class aunzip_consumer:
        def __init__(self): self.q = Queue()
        def __aiter__(self): return self
        async def __anext__(self, L=Lock(), I=I):
            if self.q.empty():
                async with L:
                    try:
                        async for _ in take(I, put_batch, default=RAISE): await _a(Q, _)
                    except ItemsExhausted:
                        for q in Q: q.close()
            try:
                if (r := await self.q.get()) is fillvalue: raise StopAsyncIteration
                return r
            except QueueShutDown: raise StopAsyncIteration from None
        def close(self): self.q.shutdown()
    await _a(Q := tuple(aunzip_consumer() for _ in range(l)), t); return Q
async def merge_async_iters[T](*I: SupportsIteration[T], reverse: bool=False) -> AsyncGenerator[T, None]:
    audit(f'{pkgpref}iters.merge_async_iters', I); q, c, e, l, a = (LifoQueue if reverse else Queue)[T](), None, Event(), _get_loop_no_exit(), _NO_DEFAULT
    async def drain(i: AsyncIterable[T], f=q.put):
        async for _ in i: await f(_)
    async def close():
        if reverse: await q.put(a); e.set()
        await gather(*(l.create_task(drain(iter_to_aiter(i))) for i in I))
        if not reverse: await q.put(a); e.set()
    l.create_task(close()); await e.wait()
    while True:
        if (c := await q.get()) is a: break
        yield c
def aflatten[T](it: SupportsIteration[SupportsIteration[T]]) -> AsyncGenerator[T, None]: return achain.from_iterable(it).__aiter__()
async def batch[T](it: SupportsIteration[T], size: int, max_concurrent_batches: int|None=8, timeout: float|None=None, strict: bool=False) -> AsyncGenerator[list[T], None]:
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
@overload
def achunked[T](it: SupportsIteration[T], n: int, strict: Literal[True]) -> AsyncGenerator[list[T], None]: ...
@overload
def achunked[T](it: SupportsIteration[T], n: int|None, strict: Literal[False]=...) -> AsyncGenerator[list[T], None]: ...
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
@overload
def asideeffect[T](f: Callable[[list[T]]], it: SupportsIteration[T], /, *, size: int, before: Callable[[]]|None=..., after: Callable[[]]|None=...) -> AsyncGenerator[T, None]: ...
@overload
def asideeffect[T](f: Callable[[T]], it: SupportsIteration[T], /, *, size: None=..., before: Callable[[]]|None=..., after: Callable[[]]|None=...) -> AsyncGenerator[T, None]: ...
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
def asliced[T](seq: SupportsSlicing[T], n: int, strict: bool=False):
    I = atakewhile(None, (seq[i:i+n] async for i in acount(step=n)))
    if not strict: return I
    async def ret():
        async for s in I:
            if len(s) != n: raise ValueError('seq is not divisible by n')
            yield s
    return ret()
def batch_buffer[T](items: SupportsIteration[T], batch_size: int, buffer_size: int, *, loop: AbstractEventLoop|None=None):
    d = deque[T](maxlen=buffer_size)
    if loop is None: loop = _get_loop_no_exit()
    async def consumer():
        async for b in batch(items, batch_size): d.extend(b)
    loop.create_task(consumer()); return d
def buffer[T](it: AsyncIterable[T], maxsize: int=0, timeout: float|None=None, cooldown: float=0.1, *, loop: AbstractEventLoop|None=None):
    q = Queue[T](maxsize)
    if loop is None: loop = _get_loop_no_exit()
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
async def asplitat[T](it: SupportsIteration[T], pred: Callable[[T], bool], maxsplit: int=-1, keep_sep: bool=False):
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
async def batch_process[T, R](items: SupportsIteration[T], size: int, processor: Callable[[list[T]], Awaitable[R]]) -> AsyncGenerator[R, None]:
    async for b in batch(items, size): yield await processor(b)
async def window[T](it: AsyncIterable[T], size: int, step: int=1) -> AsyncGenerator[tuple[T, ...], tuple[int, int]|None]:
    if not size >= 1 <= step: raise ValueError('size and step should both be >=1')
    b, c = deque[T](maxlen=size), 0
    async for i in it:
        b.append(i)
        if len(b) == size:
            if not c%step: size, step = (yield tuple(b)) or (size, step)
            c += 1
async def aall(it: SupportsIteration[Any]):
    async for _ in iter_to_aiter(it):
        if not _: return False
    return True
async def aany(it: SupportsIteration[Any]):
    async for _ in iter_to_aiter(it):
        if _: return True
    return False
def _compare(a, b):
    try: return a < b
    except TypeError, NotImplementedError: return b > a
@overload
async def amax[C: SupportsRichComparison](it: SupportsIteration[C]) -> C: ...
@overload
async def amax[T](it: SupportsIteration[T], *, cmp: Callable[[T, T], bool]) -> T: ...
@overload
async def amax[T](it: SupportsIteration[T], *, key: Callable[[T], SupportsRichComparison]) -> T: ...
@overload
async def amax[C: SupportsRichComparison](it: SupportsIteration[C], *, default: C) -> C: ...
@overload
async def amax[T](it: SupportsIteration[T], *, cmp: Callable[[T, T], bool], default: T) -> T: ...
@overload
async def amax[T](it: SupportsIteration[T], *, key: Callable[[T], SupportsRichComparison], default: T) -> T: ...
@overload
async def amin[C: SupportsRichComparison](it: SupportsIteration[C]) -> C: ...
@overload
async def amin[T](it: SupportsIteration[T], *, cmp: Callable[[T, T], bool]) -> T: ...
@overload
async def amin[T](it: SupportsIteration[T], *, key: Callable[[T], SupportsRichComparison]) -> T: ...
@overload
async def amin[C: SupportsRichComparison](it: SupportsIteration[C], *, default: C) -> C: ...
@overload
async def amin[T](it: SupportsIteration[T], *, cmp: Callable[[T, T], bool], default: T) -> T: ...
@overload
async def amin[T](it: SupportsIteration[T], *, key: Callable[[T], SupportsRichComparison], default: T) -> T: ...
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
@overload
def azip[T](i1: SupportsIteration[T], /) -> AsyncGenerator[tuple[T], None]: ...
@overload
def azip[T, R](i1: SupportsIteration[T], i2: SupportsIteration[R], /) -> AsyncGenerator[tuple[T, R], None]: ...
@overload
def azip[T, R](i1: SupportsIteration[T], i2: SupportsIteration[R], /, *, strict: Literal[True]) -> AsyncGenerator[tuple[T, R], None]: ...
@overload
def azip[T, R, V](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], /) -> AsyncGenerator[tuple[T, R, V], None]: ...
@overload
def azip[T, R, V](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], /, *, strict: Literal[True]) -> AsyncGenerator[tuple[T, R, V], None]: ...
@overload
def azip[T, R, V, U](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], /) -> AsyncGenerator[tuple[T, R, V, U], None]: ...
@overload
def azip[T, R, V, U](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], /, *, strict: Literal[True]) -> AsyncGenerator[tuple[T, R, V, U], None]: ...
@overload
def azip[T, R, V, U, S](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], i5: SupportsIteration[S], /) -> AsyncGenerator[tuple[T, R, V, U, S], None]: ...
@overload
def azip[T, R, V, U, S](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], i5: SupportsIteration[S], /, *, strict: Literal[True]) -> AsyncGenerator[tuple[T, R, V, U, S], None]: ...
@overload
def azip[T](*I: SupportsIteration[T], strict: bool=...) -> AsyncGenerator[tuple[T, ...], None]: ...
@overload
def azip(*I: SupportsIteration[Any], strict: bool=...) -> AsyncGenerator[tuple[Any, ...], None]: ...
async def azip(*I, strict=False, _y=dummy_task) -> AsyncGenerator[tuple, None]:
    i = tuple(map(iter_to_aiter, I))
    while True:
        try: yield tuple(await gather(*map(anext, i)))
        except StopAsyncIteration:
            if strict:
                for x, y in enumerate(i):
                    try: await anext(y); raise ValueError(f'azip: iterable {x} longer than shortest iterable')
                    except StopAsyncIteration: continue
            await gather(*(f() if (f := getattr(_, 'aclose', None)) else _y for _ in i)); break
@overload
def amap[T, R](f: Callable[[T], Awaitable[R]], it: SupportsIteration[T], /, *, await_: Literal[True], strict: Literal[False]=False) -> AsyncGenerator[R, None]: ...
@overload
def amap[T, R](f: Callable[[T], R], it: SupportsIteration[T], /, *, await_: Literal[False]=False, strict: Literal[False]=False) -> AsyncGenerator[R, None]: ...
@overload
def amap[T, S, R](f: Callable[[T, S], Awaitable[R]], i1: SupportsIteration[T], i2: SupportsIteration[S], /, *, await_: Literal[True], strict: bool=False) -> AsyncGenerator[R, None]: ...
@overload
def amap[T, S, R](f: Callable[[T, S], R], i1: SupportsIteration[T], i2: SupportsIteration[S], /, *, await_: Literal[False]=False, strict: bool=False) -> AsyncGenerator[R, None]: ...
@overload
def amap[T, S, V, R](f: Callable[[T, S, V], Awaitable[R]], i1: SupportsIteration[T], i2: SupportsIteration[S], i3: SupportsIteration[V], /, *, await_: Literal[True], strict: bool=False) -> AsyncGenerator[R, None]: ...
@overload
def amap[T, S, V, R](f: Callable[[T, S, V], R], i1: SupportsIteration[T], i2: SupportsIteration[S], i3: SupportsIteration[V], /, *, await_: Literal[False]=False, strict: bool=False) -> AsyncGenerator[R, None]: ...
@overload
def amap[T, S, V, U, R](f: Callable[[T, S, V, U], Awaitable[R]], i1: SupportsIteration[T], i2: SupportsIteration[S], i3: SupportsIteration[V], i4: SupportsIteration[U], /, *, await_: Literal[True], strict: bool=False) -> AsyncGenerator[R, None]: ...
@overload
def amap[T, S, V, U, R](f: Callable[[T, S, V, U], R], i1: SupportsIteration[T], i2: SupportsIteration[S], i3: SupportsIteration[V], i4: SupportsIteration[U], /, *, await_: Literal[False]=False, strict: bool=False) -> AsyncGenerator[R, None]: ...
@overload
def amap[T, R](f: Callable[[*tuple[T, ...]], Awaitable[R]], /, *its: SupportsIteration[T], await_: Literal[True], strict: bool=False) -> AsyncGenerator[R, None]: ...
@overload
def amap[T, R](f: Callable[[*tuple[T, ...]], R], /, *its: SupportsIteration[T], await_: Literal[False]=False, strict: bool=False) -> AsyncGenerator[R, None]: ...
@overload
def amap[R](f: Callable[..., Awaitable[R]], /, *its: SupportsIteration[Any], await_: Literal[True], strict: bool=False) -> AsyncGenerator[R, None]: ...
@overload
def amap[R](f: Callable[..., R], /, *its: SupportsIteration[Any], await_: Literal[False]=False, strict: bool=False) -> AsyncGenerator[R, None]: ...
async def amap(f, /, *its, await_=False, strict=False):
    async for _ in azip(*its, strict=strict): r = f(*_); yield (await r) if await_ else r
@overload
def afilter[T](f: Callable[[T]], it: SupportsIteration[T]) -> AsyncGenerator[T, None]: ...
@overload
def afilter[T](f: None, it: SupportsIteration[T]) -> AsyncGenerator[T, None]: ...
async def afilter(f, it):
    if f is None: f = bool
    async for _ in iter_to_aiter(it):
        if issubclass(type(r := f(_)), Awaitable): r = await r
        if r: yield _
@overload
def amapif[T, R](f: Callable[[T], R], p: Callable[[T]]|None, it: SupportsIteration[T], /, await_: Literal[False]=...) -> AsyncGenerator[R, None]: ...
@overload
def amapif[T, R](f: Callable[[T], Awaitable[R]], p: Callable[[T]]|None, it: SupportsIteration[T], /, await_: Literal[True]) -> AsyncGenerator[R, None]: ...
def amapif(f, p, it, /, await_=False): return amap(f, afilter(p, it), await_=await_)
@overload
def amultimapif[*Ts, R](f: Callable[[*Ts], R], p: Callable[[tuple[*Ts]], bool], /, *its: SupportsIteration, await_: Literal[False]=...) -> AsyncGenerator[R, None]: ...
@overload
def amultimapif[*Ts, R](f: Callable[[*Ts], Awaitable[R]], p: Callable[[tuple[*Ts]], bool], /, *its: SupportsIteration, await_: Literal[True]) -> AsyncGenerator[R, None]: ...
def amultimapif(f, p, /, *its, await_=False): return astarmap(f, afilter(p, azip(*its)), await_)
@overload
def arange(stop: int, /) -> AsyncGenerator[int, None]: ...
@overload
def arange(start: int, stop: int, /) -> AsyncGenerator[int, None]: ...
@overload
def arange(start: int, stop: int, step: int, /) -> AsyncGenerator[int, None]: ...
async def arange(a, b=None, c=1, /):
    if not c: raise ValueError('step cannot be zero')
    if b is None: a, b = 0, a
    f = b.__lt__ if c < 0 else b.__gt__
    while f(a): yield a; a += c
@overload
def acount(start: int=0, step: int=1) -> AsyncGenerator[int, None]: ...
@overload
def acount(start: float, step: int=1) -> AsyncGenerator[float, None]: ...
@overload
def acount(start: float, step: float) -> AsyncGenerator[float, None]: ...
@overload
def acount(start: int, step: float) -> AsyncGenerator[float, None]: ...
@overload
def acount(*, step: float) -> AsyncGenerator[float, None]: ...
async def acount(start: float=0, step: float=1):
    if isinstance(step, float):
        if step.is_integer(): step = int(step)
        else: start = float(start)
    elif start.is_integer(): start = int(start)
    while True: yield start; start += step
async def acycle[T](it: SupportsIteration[T]):
    l, I = list[T](), iter_to_aiter(it)
    async for i in I: yield i; l.append(i)
    t = tuple(l)
    while True:
        for i in t: yield i
@overload
def arepeat[T](elem: T, n: int) -> AsyncGenerator[T, None]: ...
@overload
def arepeat[T](elem: T) -> AsyncGenerator[T, None]: ...
async def arepeat(elem, n: int|None=None):
    if n is None or n < 0:
        while True: yield elem
    else:
        while n > 0: yield elem; n -= 1
async def aaccumulate[T](it: SupportsIteration[T], func: Callable[[T, T], T]=add, *, initial: T|None=None) -> AsyncGenerator[T, None]:
    it = iter_to_aiter(it)
    if initial is None:
        try: initial = await anext(it)
        except StopAsyncIteration: return
    yield initial
    async for _ in it: yield (initial := func(initial, _))
async def acompress[T](data: SupportsIteration[T], selectors: SupportsIteration[Any]) -> AsyncGenerator[T, None]:
    async for i, j in azip(data, selectors):
        if j: yield i
async def adropwhile[T](pred: Callable[[T], bool], it: SupportsIteration[T]) -> AsyncGenerator[T, None]:
    I = iter_to_aiter(it)
    async for _ in I:
        if not pred(_): yield _; break
    async for _ in I: yield _
def afilterfalse[T](f: Callable[[T], bool]|None, it: SupportsIteration[T]): return afilter(lambda i: not (f or bool)(i), it)
async def agroupby[T, R](it: SupportsIteration[T], key: Callable[[T], R]=lambda _: _) -> AsyncGenerator[tuple[R, AsyncGenerator[T, None]], None]:
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
async def aislice[T](it: SupportsIteration[T], *a: int|None) -> AsyncGenerator[T, None]:
    x, y, z = 0 if (s := slice(*a)).start is None else s.start, s.stop, 1 if s.step is None else s.step
    if x < 0 or (y is not None and y < 0) or z <= 0: raise ValueError('invalid indices')
    I, n = acount() if y is None else range(max(x, y)), x
    async for i, j in azip(I, it):
        if i == n: yield j; n += z
async def aiterindex[T](it: SupportsIteration[T], value: T, start: int=0, stop: int|None=None) -> AsyncGenerator[int, None]:
    async for i, j in aenumerate(aislice(it, start, stop), start):
        if j is value or j == value: yield i
async def asieve(n: int) -> AsyncGenerator[int, None]:
    if n < 2: return
    yield 2; s, d = 3, bytearray(range(2))*(n>>1)
    async for p in aiterindex(d, 1, s, isqrt(n)+1):
        async for i in aiterindex(d, 1, s, q := p*p): yield i
        d[q:n:x], s = bytes(len(range(q, n, x := p<<1))), q
    async for i in aiterindex(d, 1, s): yield i
async def apairwise[T](it: SupportsIteration[T]) -> AsyncGenerator[tuple[T, T], None]:
    try: a = await anext(I := iter_to_aiter(it))
    except StopAsyncIteration: return
    async for b in I: yield a, b; a = b
async def atriplewise[T](it: SupportsIteration[T]): a, b, c = tee(iter_to_aiter(it), 3); await gather(*map(lambda g: anext(g, None), (b, c, c))); return azip(a, b, c)
@overload
def aproduct[T](i1: SupportsIteration[T], /, *, repeat: Literal[1]=...) -> AsyncGenerator[tuple[T], None]: ...
@overload
def aproduct[T](i1: SupportsIteration[T], /, *, repeat: int) -> AsyncGenerator[tuple[T, ...], None]: ...
@overload
def aproduct[T, R](i1: SupportsIteration[T], i2: SupportsIteration[R], /, *, repeat: Literal[1]=...) -> AsyncGenerator[tuple[T, R], None]: ...
@overload
def aproduct[T, R](i1: SupportsIteration[T], i2: SupportsIteration[R], /, *, repeat: int) -> AsyncGenerator[tuple[T|R, ...], None]: ...
@overload
def aproduct[T, R, V](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], /, *, repeat: Literal[1]=...) -> AsyncGenerator[tuple[T, R, V], None]: ...
@overload
def aproduct[T, R, V](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], /, *, repeat: int) -> AsyncGenerator[tuple[T|R|V, ...], None]: ...
@overload
def aproduct[T, R, V, U](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], /, *, repeat: Literal[1]=...) -> AsyncGenerator[tuple[T, R, V, U], None]: ...
@overload
def aproduct[T, R, V, U](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], /, *, repeat: int) -> AsyncGenerator[tuple[T|R|V|U, ...], None]: ...
@overload
def aproduct[T, R, V, U, S](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], i5: SupportsIteration[S], /, *, repeat: Literal[1]=...) -> AsyncGenerator[tuple[T, R, V, U, S], None]: ...
@overload
def aproduct[T, R, V, U, S](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], i5: SupportsIteration[S], /, *, repeat: int) -> AsyncGenerator[tuple[T|R|V|U|S, ...], None]: ...
@overload
def aproduct[T](*its: SupportsIteration[T], repeat: int=1) -> AsyncGenerator[tuple[T, ...], None]: ...
@overload
def aproduct(i1: SupportsIteration[Any], i2: SupportsIteration[Any], i3: SupportsIteration[Any], i4: SupportsIteration[Any], i5: SupportsIteration[Any], /, *its: SupportsIteration[Any], repeat: int=...) -> AsyncGenerator[tuple[Any, ...], None]: ...
async def aproduct(*its, repeat=1):
    if repeat < 0: raise ValueError('repeat cannot be negative')
    r = [()]
    async for p in arepeat(amap(to_tuple, its), repeat): r = [x+(y,) for x in r async for y in p]
    for _ in r: yield tuple(_)
@overload
def astarmap[*Ts, R](f: Callable[[*Ts], R], it: SupportsIteration[tuple[*Ts]], /, await_: Literal[False]=False) -> AsyncGenerator[R, None]: ...
@overload
def astarmap[*Ts, R](f: Callable[[*Ts], Awaitable[R]], it: SupportsIteration[tuple[*Ts]], /, await_: Literal[True]) -> AsyncGenerator[R, None]: ...
async def astarmap(f, it, /, await_=False):
    async for _ in iter_to_aiter(it): yield (await f(*_)) if await_ else f(*_)
async def atakewhile[T](pred: Callable[[T], bool]|None, it: SupportsIteration[T]) -> AsyncGenerator[T, None]:
    p = pred or bool
    async for _ in iter_to_aiter(it):
        if not p(_): break
        yield _
async def atotient(n: int):
    s = set()
    async for p in afactor(n):
        if p not in s: s.add(p); n -= n//p
    return n
def asquaresum[X: (int, float, complex)](it: SupportsIteration[X]): return asumprod(*tee(it))
@overload
def aziplongest[T](i1: SupportsIteration[T], /) -> AsyncGenerator[tuple[T], None]: ...
@overload
def aziplongest[T, R](i1: SupportsIteration[T], i2: SupportsIteration[R], /, *, fillvalue: Any=...) -> AsyncGenerator[tuple[T, R], None]: ...
@overload
def aziplongest[T, R, V](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], /, *, fillvalue: Any=...) -> AsyncGenerator[tuple[T, R, V], None]: ...
@overload
def aziplongest[T, R, V, U](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], /, *, fillvalue: Any=...) -> AsyncGenerator[tuple[T, R, V, U], None]: ...
@overload
def aziplongest[T, R, V, U, S](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], i5: SupportsIteration[S], /, *, fillvalue: Any=...) -> AsyncGenerator[tuple[T, R, V, U, S], None]: ...
@overload
def aziplongest[T](*its: SupportsIteration[T], fillvalue: Any=...) -> AsyncGenerator[tuple[T, ...], None]: ...
@overload
def aziplongest(*its: SupportsIteration[Any], fillvalue: Any=...) -> AsyncGenerator[tuple[Any, ...], None]: ...
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
def asumprod[X: (int, float, complex)](p: SupportsIteration[X], q: SupportsIteration[X], /) -> Coroutine[Any, Any, X]: return asum(amap(mul, p, q, strict=True))
async def aconvolve[X: (int, float, complex)](signal: SupportsIteration[X], kernel: SupportsIteration[X]) -> AsyncGenerator[X, None]:
    w = deque[X]((0,), n := len(K := to_tuple(kernel)[::-1]))*n
    async for x in achain(signal, arepeat(0, n-1)): w.append(x); yield await asumprod(K, w)
@overload
def atabulate[T](f: Callable[[int], T], start: int=..., step: int=..., /, *, await_: Literal[False]=...) -> AsyncGenerator[T, None]: ...
@overload
def atabulate[T](f: Callable[[int], Awaitable[T]], start: int=..., step: int=..., /, *, await_: Literal[True]) -> AsyncGenerator[T, None]: ...
def atabulate(f, start=0, step=1, /, *, await_=False): return amap(f, acount(start, step), await_=await_)
async def asum[X: (int, float, complex)](it: SupportsIteration[X], start=0) -> X:
    async for i in iter_to_aiter(it): start += i
    return start
async def aprod[X: (int, float, complex)](it: SupportsIteration[X], start=1) -> X:
    async for i in iter_to_aiter(it): start *= i
    return start
async def amatprod(it: SupportsIteration, start: Any):
    async for i in iter_to_aiter(it): start @= i
    return start
def atail[T](n: int, it: SupportsIteration[T]):
    try: return aislice(it, max(0, len(it)-n), None)
    except TypeError:
        async def f():
            d = deque[T](maxlen=n)
            async for _ in iter_to_aiter(it): d.append(_)
            for _ in d: yield _
        return f()
def amultinomial(*c: int): return aprod(amap(comb, aaccumulate(c), c))
def to_tuple[T](it: SupportsIteration[T]): return tuple(aiter_to_iter(it))
_randrange, _sample, _smallprimes, _perfect_test = _randinst.randrange, _randinst.sample, frozenset(_littleprimes := (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199)), ((2047, (2,)), (9080191, (31, 73)), (4759123141, (2, 7, 61)), (1122004669633, (2, 13, 23, 1662803)), (2152302898747, (2, 3, 5, 7, 11)), (3474749660383, (2, 3, 5, 7, 11, 13)), (18446744073709551616, (2, 325, 9375, 28178, 450775, 9780504, 1795265022)), (3317044064679887385961981, (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)))
def aconsume[T](it: SupportsIteration[T], n: int|None=None, _extender=to_async(deque(maxlen=0).extend)[0]) -> Coroutine[None, None, T|None]: return _extender(aiter_to_iter(it)) if n is None else anext(aislice(it, n, n), None)
def anth[T, R=Any](it: SupportsIteration[T], n: int, default: R=_NO_DEFAULT): return anext(aislice(it, n, None), *_filter_out(default, s=_NO_DEFAULT))
async def aallequal[T](it: SupportsIteration[T], key: Callable[[T], Any]=lambda _: _, strict: bool=False):
    I = agroupby(it, key)
    async for _ in I:
        async for _ in I: return False
        return True
    if strict: raise ValueError('iterable provided is empty')
    return True
async def acombinations[T](it: SupportsIteration[T], r: int):
    if r > (n := len(p := to_tuple(it))): return
    I = list(range(r)); yield p[:r]
    while True:
        for i in reversed(range(r)):
            if I[i] != i+n-r: break
        else: return
        I[i] += 1
        for j in range(i+1, r): I[j] = I[j-1]+1
        yield tuple(p[i] for i in I)
async def acombinations_with_replacement[T](it: SupportsIteration[T], r: int):
    if not (n := len(p := to_tuple(it))) and r: return
    I = [0]*r; yield (p[0],)*r
    while True:
        for i in reversed(range(r)):
            if I[i] != n-1: break
        else: return
        I[i:] = [I[i]+1]*(r-i); yield tuple(p[i] for i in I)
async def apermutations[T](it: SupportsIteration[T], r: int|None=None):
    n = len(p := to_tuple(it))
    if (r := n if r is None else r) > n: return
    I, C = list(range(n)), list(range(n, n-r, -1)); yield p[:r]
    while n:
        for i in reversed(range(r)):
            C[i] -= 1
            if C[i]: I[i], I[-j] = I[-(j := C[i])], I[i]; yield tuple(p[i] for i in I[:r]); break
            else: I[i:], C[i] = I[i+1:]+I[i:i+1], n-i
        else: return
def apowerset[T](it: SupportsIteration[T]): s = to_tuple(it); return aflatten(acombinations(s, r) for r in range(len(s)+1))
def aquantify[T](it: SupportsIteration[T], pred: Callable[[T], bool]=bool): return asum(amap(pred, it))
def apadnone[T](it: SupportsIteration[T]): return achain(it, arepeat(None))
def agrouper[T=Any](it: SupportsIteration[T], n: int, fillvalue: T=_NO_DEFAULT) -> AsyncGenerator[tuple[T|None, ...], None]: I = (iter_to_aiter(it),)*n; return azip(*I, strict=True) if fillvalue is RAISE else azip(*I) if fillvalue is _NO_DEFAULT else aziplongest(*I, fillvalue=fillvalue)
async def aroundrobin[T](*its: SupportsIteration[T]) -> AsyncGenerator[T, None]:
    I = (iter_to_aiter(i) for i in its)
    for i in range(len(its), 0, -1):
        async for _ in (I := acycle(aislice(I, i))): yield await anext(_)
async def aroundrobin2[T](*its: SupportsIteration[T]) -> AsyncGenerator[T, None]:
    async for X in aziplongest(*its):
        for x in X:
            if x is not _NO_DEFAULT: yield x
async def aunique_everseen[T](it: SupportsIteration[T], key: Callable[[T]]=lambda _: _):
    A, a, C, c = (S := set()).add, (s := []).append, *map(attrgetter('__contains__'), (S, s))
    async for i in iter_to_aiter(it):
        k = key(i)
        try:
            if not C(k): A(k); yield i
        except TypeError:
            if not c(k): a(k); yield i
def aunique_justseen[T](it: SupportsIteration[T], key: Callable[[T]]=lambda _: _) -> AsyncGenerator[T, None]:
    if key is None: return amap(itemgetter(0), agroupby(it))
    return amap(anext, amap(itemgetter(1), agroupby(it, key)), await_=True)
def aunique[T](it: SupportsIteration[T], key: Callable[[T], SupportsRichComparison]|None=None, reverse: bool=False): return aunique_justseen(sorted(aiter_to_iter(it), key=key, reverse=reverse), key)
def ancycles[T](it: SupportsIteration[T], n: int): return aflatten(arepeat(to_tuple(it), n))
async def apartition[T](pred: Callable[[T], bool]|None, it: SupportsIteration[T]):
    if pred is None: pred = bool
    s, t, p = tee(iter_to_aiter(it), 3); u, v = tee(amap(pred, p)); return acompress(s, amap(not_, u)), acompress(t, v)
async def aiterexcept[T](f: Callable[[], Awaitable[T]], exc: Exceptable):
    while True:
        try: yield await f()
        except exc: return
async def ailen(it: SupportsIteration):
    i = 0
    async for _ in iter_to_aiter(it): i += 1
    return i
async def aiterate[T](f: Callable[[T], Awaitable[T]], start: T):
    while True: yield start; start = await f(start)
async def with_aiter[T](actxmgr: AsyncContextManager[AsyncIterable[T]]):
    async with actxmgr as I:
        async for i in I: yield i
@overload
def asorted[C: SupportsRichComparison](it: SupportsIteration[C], *, key: None=..., reverse: bool=...) -> list[C]: ...
@overload
def asorted[T](it: SupportsIteration[T], *, key: Callable[[T], SupportsRichComparison], reverse: bool=...) -> list[T]: ...
def asorted(it, *, key=None, reverse=False): (L := list(aiter_to_iter(it))).sort(key=key, reverse=reverse); return L
def acanonical[T](it: SupportsIteration[T]) -> list[T]: return asorted(it, key=id, reverse=True)
def adistinctpermutations[T](it: SupportsIteration[T], r: int|None=None) -> AsyncGenerator[tuple[T, ...], None]:
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
    S = len(I := list(aiter_to_iter(it))); _ = S if r is None else r
    if not 0 < _ <= S: return iter_to_aiter(() if _ else ((),))
    a = _full if _ == S else _partial
    try: I.sort(); return a(I)
    except TypeError:
        d = defaultdict(list)
        for i in I: d[I.index(i)].append(i)
        E = {k: acycle(v) for k, v in d.items()}; return amap(lambda i: to_tuple(await anext(E[_]) for _ in i), a(sorted(map(I.index, I))))
def auniquetoeach[H: Hashable](*its: SupportsIteration[H]) -> AsyncGenerator[AsyncGenerator[H, None], None]: p = tuple(map(to_tuple, its)); return amap(partial(afilter, {i for i, j in Counter(aiter_to_iter(aflatten(map(set, p)))).items() if j == 1}.__contains__), p)
def aderangements[T](it: SupportsIteration[T], r: int|None=None): return acompress(apermutations(X := to_tuple(it), r), amap(aall, amap(amap, arepeat(is_not), arepeat(Y := tuple(range(len(X)))), apermutations(Y, r)), await_=True))
def aintersperse[T](e: T, it: SupportsIteration[T], n: int=1):
    if n <= 0: raise ValueError('n must be positive')
    return aislice(ainterleave(arepeat(e), it), 1, None) if n == 1 else aflatten(aislice(ainterleave(arepeat((e,)), batch(it, n)), 1, None))
def ainterleave[T](*it: SupportsIteration[T]): return aflatten(azip(*it))
def aspy[T](it: SupportsIteration[T], n: int=1): p, q = tee(it); return take(q, n), p
async def ainterleaveevenly[T](its: SupportsIteration[SupportsIteration[T]], lengths: SupportsIteration[int]|None=None):
    I = to_tuple(its)
    try:
        if (X := len(I)) != len(L := to_tuple(lengths or map(len, I))): raise ValueError('mismatch in length of its and lengths')
    except TypeError: raise ValueError('cannot determine lengths of (async) iterables') from None
    A, *a = map(L.__getitem__, _ := sorted(range(X), key=L.__getitem__, reverse=True)); B, *b = map(lambda i: iter_to_aiter(I[i]), _); E, t = [A//X]*len(a), sum(L)
    while t:
        yield await anext(B); t -= 1; E = list[int](map(sub, E, a))
        for i, e in enumerate(E):
            if e < 0: yield await anext(b[i]); t -= 1; E[i] += A
async def ainterleaverandomly[T](*its: SupportsIteration[T], _randrange=_randrange):
    x = len(I := [iter_to_aiter(i) for i in its])
    while x:
        i = _randrange(x)
        try: yield await anext(I[i])
        except StopAsyncIteration: I[i] = I[-1]; del I[-1]; x -= 1
async def acollapse(it, base_typ=(str, bytes), levels=None):
    (S := deque[tuple[int, AsyncIterator]]()).appendleft((0, arepeat(iter_to_aiter(it), 1))); L = levels or float('inf')
    while S:
        l, n = N = S.popleft()
        if l > L:
            async for i in n: yield i
            continue
        async for _ in n:
            if isinstance(_, base_typ): yield _
            else:
                try: t = iter_to_aiter(_); S.extendleft(((l+1, t), N)); break
                except TypeError: yield _
@overload
async def afirsttrue[T](it: Iterable[T], default: T, pred: Callable[[T]]) -> T: ...
@overload
async def afirsttrue[T](it: Iterable[T], *, pred: Callable[[T]]) -> T: ...
@overload
async def afirsttrue[T](it: Iterable[T], default: T) -> T: ...
@overload
async def afirsttrue[T](it: Iterable[T]) -> T: ...
@overload
async def afirsttrue[T](it: AsyncIterable[T], default: T, pred: Callable[[T]]) -> T: ...
@overload
async def afirsttrue[T](it: AsyncIterable[T], *, pred: Callable[[T]]) -> T: ...
@overload
async def afirsttrue[T](it: AsyncIterable[T], default: T) -> T: ...
@overload
async def afirsttrue[T](it: AsyncIterable[T]) -> T: ...
def afirsttrue(it, default=_NO_DEFAULT, pred=None): F = afilter(pred, it); return anext(F, *_filter_out(default, _NO_DEFAULT))
def aprepend[T](val: T, it: SupportsIteration[T]): return achain((val,), it).__aiter__()
async def arandomproduct[T](*a: SupportsIteration[T], n: int=1, _choice=_randinst.choice):
    async for i in ancycles(map(to_tuple, a), n): yield _choice(i)
async def arandomcombination[T](it: SupportsIteration[T], r: int, _sample=_sample):
    for i in sorted(_sample(range(len(p := to_tuple(it))), r)): yield p[i]
def arandom_combination_with_replacement[T](it: SupportsIteration[T], r: int, _randrange=_randrange): n = len(p := to_tuple(it)); return amap(p.__getitem__, sorted(_randrange(n) for _ in range(r)))
async def arandom_permutation[T](it: SupportsIteration[T], r: int|None=None, _sample=_sample):
    p = to_tuple(it)
    if r is None: r = len(p)
    for i in _sample(p, r): yield i
@overload
async def afirst[T](it: SupportsIteration[T]) -> T: ...
@overload
async def afirst[T](it: SupportsIteration[T], default: T) -> T: ...
async def afirst(it, default=_NO_DEFAULT):
    try:
        async for i in it: return i
    except TypeError:
        for i in it: return i
    if default is _NO_DEFAULT: raise ValueError('afirst() called on empty iterable without default value')
    return default
async def alast[T=Any](it: SupportsIteration[T], default: T=_NO_DEFAULT) -> T:
    try:
        if isinstance(it, Sequence): return it[-1]
        if (f := getattr(it, '__reversed__', None)): return f().__next__()
        return deque(aiter_to_iter(it), 1)[-1]
    except IndexError, TypeError, StopIteration, StopAsyncIteration:
        if default is _NO_DEFAULT: raise ValueError('alast() called on empty iterable without default value')
        return default
def anthorlast[T=Any](it: SupportsIteration[T], n: int, default: T=_NO_DEFAULT) -> T: return alast(aislice(it, n+1), default)
def abeforeandafter[T](pred: Callable[[T], bool], it: SupportsIteration[T]): a, b = tee(it); return acompress(atakewhile(pred, a), azip(b)), b
async def anthcombination[T](it: SupportsIteration[T], r: int, idx: int) -> AsyncGenerator[T, None]:
    if r > (n := len(p := to_tuple(it))) or r < 0: raise ValueError('inappropriate value of r')
    c, k = 1, min(r, n-r)
    for i in range(1, k+1): c = c*(n-k+i)//i
    if idx < 0: idx += c
    if idx < 0 or idx >= c: raise IndexError('inappropriate value of idx')
    while r:
        c, n, r = c*r//n, n-1, r-1
        while idx >= c: idx -= c; c, n = c*(n-r)//n, n-1
        yield p[-1-n]
def asubslices[T](it: SupportsIteration[T]): return astarmap(getitem, azip(arepeat(s := to_tuple(it)), astarmap(slice.__new__, acombinations(range(len(s)+1), 2))))
def arepeatfunc[T, *Ts](f: Callable[[*Ts], Awaitable[T]], times: int|None=None, *a: *Ts): return astarmap(f, arepeat(a) if times is None else arepeat(a, times), True)
async def apolynomialfromroots[X: (int, float, complex)](roots: SupportsIteration[X]) -> AsyncGenerator[X, None]:
    p = arange(1, 2)
    async for r in iter_to_aiter(roots): p = aconvolve(p, (1, -r))
    async for _ in p: yield _
def atranspose[T](it: SupportsIteration[SupportsIteration[T]]): return azip(*aiter_to_iter(it), strict=True)
async def aflattentensor(tensor: SupportsIteration, base=(str, bytes), _c=_check_methods):
    I = iter_to_aiter(tensor)
    while True:
        try: v = await anext(I)
        except StopAsyncIteration: break
        I = aprepend(v, I)
        if isinstance(v, base) or not (_c(v, '__iter__') or _c(v, '__aiter__')): break
        I = aflatten(I)
    async for i in I: yield i
def apolynomialderivative[X: (int, float, complex)](coeff: SupportsIteration[X]) -> AsyncGenerator[X, None]: return amap(mul, t := to_tuple(coeff), range(len(t)-1, 0))
async def apolynomialeval[X: (int, float, complex)](coeff: SupportsIteration[X], x: X):
    if not (n := len(t := to_tuple(coeff))): return type(x)(0)
    return await asumprod(t, amap(pow, arepeat(x), range(n-1, -1)))
@overload
def areshape(mat: SupportsIteration[SupportsIteration], shape: int) -> AsyncGenerator[list, None]: ...
@overload
def areshape(mat: SupportsIteration, shape: SupportsIteration[int]) -> AsyncGenerator[list, None]: ...
async def areshape(mat, shape):
    if isinstance(shape, int): I = batch(aflatten(mat), shape, None)
    else: d, *D = aiter_to_iter(shape); I = aislice(await areduce(batch, reversed(D), aflattentensor(mat), await_=False), d)
    async for i in I: yield i
async def _factor_pollard(n: int):
    if n == 4: return 2
    async for b in arange(1, n):
        x = y = 2; d = 1
        while d == 1: d = gcd((x := (x*x+b)%n)-(y := ((z := (y*y+b)%n)*z+b)%n), n)
        if d != n: return d
    raise ValueError(f'{n} is prime')
def _shift_to_odd(n: int):
    d = n>>(s := ((n-1)^n).bit_length()-1)
    if not ((1<<s)*d == n and d&1 and s > -1): raise ValueError('invalid n')
    return s, d
def _probable_prime(n: int, base: int, _shift_to_odd=lru_cache(_shift_to_odd)):
    s, d = _shift_to_odd(n-1)
    if (x := pow(base, d, n)) in (1, n-1): return True
    for _ in range(s-1):
        if (x := x*x%n) == n-1: return True
    return False
async def _aisprime(n: int, _smallprimes=_smallprimes, _perfect_test=_perfect_test, _randrange=_randrange, _probable_prime=_probable_prime):
    if n < 210: return n in _smallprimes
    if not (n&1 and n%3 and n%5 and n%7 and n%11 and n%13 and n%17): return False
    for l, B in _perfect_test:
        if n < l: break
    else: B = (_randrange(2, n-1) for _ in range(64))
    return await aall(amap(partial(_probable_prime, n), B))
async def afactor(n: int, _littleprimes=_littleprimes, _aisprime=_aisprime, _factor_pollard=_factor_pollard) -> AsyncGenerator[int, None]:
    if n < 2: raise ValueError('no prime factors')
    for p in _littleprimes:
        while not n%p: yield p; n //= p
    if n < 2: return
    t = [n]
    for n in t:
        if n < 44521 or await _aisprime(n): yield n
        else: t += (f := await _factor_pollard(n), n//f)
async def arunningmedian(it: SupportsIteration[float], *, maxlen: SupportsIndex|None=None):
    if maxlen is None:
        r, l, h = iter_to_aiter(it).__aiter__().__anext__, list[float](), list[float]()
        while True: heappush_max(l, await r()); yield l[0]; heappush(h, heappushpop_max(l, await r())); yield (l[0]+h[0])/2
    if (m := index(maxlen)) <= 0: raise ValueError('window size should be positiive')
    w, o = deque[float](), list[float]()
    async for i in iter_to_aiter(it):
        w.append(i); insort_right(o, i)
        if (n := len(o)) > m: del o[bisect_left(o, w.popleft())]; n -= 1
        m = n>>1; yield o[m] if n&1 else (o[m-1]+o[m])/2
async def arandomderangement[T](it: SupportsIteration[T], _shuffle=_randinst.shuffle) -> tuple[T, ...]:
    s = to_tuple(it)
    if (l := len(s)) < 2:
        if s: raise IndexError('no derangements to choose from')
        return ()
    i = tuple(p := list(range(l)))
    while True:
        _shuffle(p)
        if not await aany(amap(is_, i, p)): return itemgetter(*p)(s)
async def amatmul[X: (int, float, complex)](M: SupportsIteration[SupportsIteration[X]], N: SupportsIteration[SupportsIteration[X]]) -> SupportsIteration[SupportsIteration[X]]:
    M, N = iter_to_aiter(M), iter_to_aiter(N); N = aprepend(t := to_tuple(await anext(N)), N)
    async for i in batch(astarmap(asumprod, aproduct(M, atranspose(N)), True), len(t)): yield i
def mat_vec_mul(M: SupportsIteration[SupportsIteration[int]], V: SupportsIteration[int]): n, v = len(p := to_tuple(to_tuple(i) async for i in iter_to_aiter(M))), to_tuple(V); return (await asum(p[i][j]*v[j] async for j in arange(n)) async for i in arange(n))
def vecs_eq(u: SupportsIteration[int], v: SupportsIteration[int]): return aall(i == j async for i, j in azip(u, v))
def afrievalds(A: SupportsIteration[SupportsIteration[int]], B: SupportsIteration[SupportsIteration[int]], C: SupportsIteration[SupportsIteration[int]], k: int=2, _randint=_randinst.randint): n = len(A := to_tuple(A)); return aall(await vecs_eq(mat_vec_mul(A, mat_vec_mul(B, r := tuple(_randint(0, 1) for _ in range(n)))), mat_vec_mul(C, r)) async for _ in arange(k))
async def basic_collect[T](it: SupportsIteration[T], n: int):
    l = list[T]()
    async for _ in aislice(it, n): l.append(_)
    return l
async def asubstrings[T](it: SupportsIteration[T]):
    s = []
    async for i in iter_to_aiter(it): s.append(i); yield i,
    c = len(s := tuple(s))+1
    async for n in arange(2, c):
        async for i in arange(c-n): yield s[i:i+n]
@overload
def asubstrindices[S: (str, bytes, bytearray)](seq: S, reverse: bool=...) -> AsyncGenerator[tuple[S, int, int], None]: ...
@overload
def asubstrindices[T](seq: SupportsSlicing[T], reverse: bool=...) -> AsyncGenerator[tuple[Iterable[T], int, int], None]: ...
def asubstrindices(seq, reverse=False):
    r = range(1, x := len(seq)+1)
    if reverse: r = reversed(r)
    return ((seq[i:i+L], i, i+L) for L in r async for i in arange(x-L))
def iter_future[T](it: SupportsIteration[T], summaryf: Callable[[SupportsIteration[T]], Awaitable]=aconsume) -> Future[float]:
    async def task(): t = L.time(); await summaryf(it); F.set_result(L.time()-t)
    F = (L := _get_loop_no_exit()).create_future(); L.create_task(task()); return F
def agetitems_from_indices[T](it: SupportsIteration[T], indices: SupportsIteration[SupportsIndex], setatend: Future[float]|None=None, finish: bool=False) -> list[Future[T]]:
    '''Takes an (async) iterable and an (async) iterable of integers interpreted as indices, and immediately returns a list of futures whose eventual results represent
    the items of that iterable at the index, beginning consumption of the iterable in the background. Exceptions will be set in the futures that are not done if results
    are encountered during iteration or if the index is out of bounds. Supports negative indices. Do not set the result of any returned future; instead, if the result
    is no longer relevant, cancel the future. The consumption stops as soon as all the required results are pushed into the respective futures. Pass in a Future for the
    setatend parameter, which cancels the background consumption of the async iterable once it is done and cancels the undone futures.'''
    L, r, I = _get_loop_no_exit(), [], iter_to_aiter(it)
    async def consume():
        s, M, m, d = L.time(), 0, 0, defaultdict(list)
        async for x in amap(index, indices):
            if M is not None:
                if x < 0:
                    M = None
                    if x < m: m = x
                elif x > M: M = x
            d[x].append(F := L.create_future()); r.append(F)
        async def helper(i: int, j: T, d=d):
            async for x, F in aenumerate(d.pop(i, ())):
                if F.cancelled(): continue
                if F.done(): raise FutureCorrupted(f'future at index {x} associated with index {i} in the agetitems_from_indices function called on (async) iterable {it!r} had its result/exception set by an external party')
                F.set_result(j)
        try:
            if M is None:
                async def helper2(i: int, j: T): await helper(i, j); b.append(j)
                await aconsume(achain(astarmap(helper2, aenumerate(I)), amap(helper, acount(-1, -1), adisembowel(b := deque[T](maxlen=-m)), await_=True)))
            else: await aconsume(astarmap(helper, aenumerate(take(I, M)), True))
        except CRITICAL: raise Critical
        except BaseException as e:
            async for F in afilterfalse(methodcaller('done'), r): F.set_exception(e)
            raise
        t = f'index {{!r}} beyond the ends of (async) iterable {it!r}'
        for i, l in d.items():
            e = IndexError(t.format(i))
            async for x, F in aenumerate(l):
                if F.cancelled(): continue
                if F.done(): raise ExceptionGroup('error while processing indices for which items were not successfully got', (e, FutureCorrupted(f'future at index {x} associated with index {i} in the agetitems_from_indices function called on (async) iterable {it!r} had its result/exception set by an external party')))
                else: F.set_exception(e)
        if finish: await aconsume(I)
        if setatend is None: return
        if setatend.done() and not setatend.cancelled(): raise FutureCorrupted(f'setatend {type(setatend).__qualname__} passed to agetitems_from_indices had its result set by an external party')
        setatend.set_result(L.time()-s)
    c = L.create_task(consume())
    if setatend is not None: setatend.add_done_callback(lambda _: L.run_until_complete(gather(safe_cancel(c), safe_cancel_batch(r))))
    audit(f'{pkgpref}iters.agetitems_from_indices', it, r); return r
async def aintersend[T, R](i1: AsyncGenerator[T, R], i2: AsyncGenerator[R, T]):
    debug('aintersend called'); a, b = await gather(anext(i1), anext(i2))
    while True: yield a, b; a, b = await gather(i1.asend(b), i2.asend(a))
async def asendstream[T, R](i1: AsyncGenerator[T, R], i2: SupportsIteration[R]):
    debug('asendstream called')
    async for v in iter_to_aiter(i2): yield await i1.asend(v)
async def acat(first=None):
    debug('acat called')
    while True: first = yield first
async def aforever():
    debug('aforever called')
    while True: yield
async def aguessmax[T=Any](it: SupportsIteration[T], estlen: int, *, key: Callable[[T], SupportsRichComparison]|None=None, default: T=_NO_DEFAULT, finish_event: Event|None=None, __cmp=_compare) -> T:
    if (r := await amax(take(I := iter_to_aiter(it), ceil(estlen*RECIP_E)), key=(K := key or (lambda x: x)), default=(o := object()))) is o:
        if default is _NO_DEFAULT: raise ValueError('empty (async) iterable passed to aguessmax with no default value')
        return default
    k = K(r)
    try:
        async for i in I:
            if __cmp(k, K(i)): return i
        return r
    finally:
        if not (finish_event is None or finish_event.is_set()): (t := (f := (l := _get_loop_no_exit()).create_task)(aconsume(I))).add_done_callback(lambda _: finish_event.set()); f(finish_event.wait()).add_done_callback(lambda _, t=t, l=l: t.cancel() or stop_and_closer(l))
async def aguessmin[T=Any](it: SupportsIteration[T], estlen: int, *, key: Callable[[T], SupportsRichComparison]|None=None, default: T=_NO_DEFAULT, finish_event: Event|None=None, __cmp=_compare) -> T:
    if (r := await amin(take(I := iter_to_aiter(it), ceil(estlen*RECIP_E)), key=(K := key or (lambda x: x)), default=(o := object()))) is o:
        if default is _NO_DEFAULT: raise ValueError('empty (async) iterable passed to aguessmax with no default value')
        return default
    k = K(r)
    try:
        async for i in I:
            if __cmp(K(i), k): return i
        return r
    finally:
        if not (finish_event is None or finish_event.is_set()): (t := (f := (l := _get_loop_no_exit()).create_task)(aconsume(I))).add_done_callback(lambda _: finish_event.set()); f(finish_event.wait()).add_done_callback(lambda _, t=t, l=l: t.cancel() or stop_and_closer(l))
async def apowersoftwo(*, init: int=1, init_shift: int=0):
    init <<= init_shift
    while True: yield init; init <<= 1
async def areversed(it):
    try:
        async for i in iter_to_aiter(reversed(it)): yield i
    except TypeError:
        f = (l := []).append
        async for i in iter_to_aiter(it): f(i)
        for i in reversed(l): yield i
del _aunzip_put, _compare, _factor_pollard, _shift_to_odd, _probable_prime, _aisprime, _littleprimes, _randrange, _sample, _smallprimes, _perfect_test, _randinst, TYPE_CHECKING