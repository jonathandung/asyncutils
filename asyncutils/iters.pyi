'''| Functional and chainable interface to get async generators from (async) iterables. Many of the algorithms here are taken from :mod:`more_itertools`.
| However, since they must support both sync and async iterables, they are much less efficient than their sync counterparts.'''
from ._internal.prots import EventProt, Exceptable, RaiseType, SupportsIteration, SupportsMatMul, SupportsRichComparison, SupportsSlicing, AUnzipConsumer
from asyncio import AbstractEventLoop, Future, Task
from collections.abc import AsyncIterable, AsyncGenerator, Awaitable, Callable, Hashable, Iterable, Mapping, MutableSequence, Reversible
from typing import Any, Literal, Never, SupportsIndex, overload
__all__ = 'aaccumulate', 'aall', 'aallequal', 'aany', 'aappend', 'aargmax', 'aargmin', 'aawgenf2agenf', 'abefore_and_after', 'abfs', 'abrent', 'ac3merge', 'acanonical', 'acat', 'acollapse', 'acombinations', 'acombinations_with_replacement', 'acompress', 'aconsume', 'aconvolve', 'acount', 'acountdown', 'acycle', 'aderangements', 'adfs', 'adft', 'adistinct_permutations', 'adoublestarmap', 'adropwhile', 'aevery', 'aeveryother', 'afactor', 'afilter', 'afilterfalse', 'afirst', 'afirsttrue', 'aflatten', 'aflatten_tensor', 'aforever', 'afreivalds', 'agather', 'agetitems_from_indices', 'agives', 'agroupby', 'agrouper', 'aguessmax', 'aguessmin', 'ahammingdist', 'aidft', 'ailen', 'ainterleave_evenly', 'ainterleave_randomly', 'ainterleave_stopearly', 'aintersend', 'aintersperse', 'aisempty', 'aislice', 'aisprime', 'aiter_idx', 'aiterate', 'aiterexcept', 'alast', 'aloops', 'amap', 'amapif', 'amatmul', 'amatprod', 'amax', 'amergesortedby', 'amin', 'amultifilter', 'amultifilterfalse', 'amultimapif', 'amultistarfilter', 'amultistarfilterfalse', 'ancycles', 'anth', 'anth_or_last', 'anthcombination', 'aonline_sorter', 'apadnone', 'apairwise', 'apartition', 'apermutations', 'apolynomial_derivative', 'apolynomial_eval', 'apolynomial_from_roots', 'apowers', 'apowers_of_two', 'apowerset', 'apowersetofsets', 'aprepend', 'aprod', 'aproduct', 'aquantify', 'arandom_combination_with_replacement', 'arandom_derangement', 'arandom_permutation', 'arandomcombination', 'arandomproduct', 'arange', 'arepeat', 'arepeatfunc', 'areshape', 'areversed', 'aroundrobin', 'aroundrobin2', 'arunlength_decode', 'arunlength_encode', 'arunning_median', 'arunningmean', 'asample_weighted', 'asamplel', 'asattolo', 'asendstream', 'aserialize', 'aside_effect', 'asieve', 'asliced', 'asorted', 'asplitat', 'aspy', 'asquaresum', 'astarfilter', 'astarfilterfalse', 'astarmap', 'astarmap_with_kwds', 'asubslices', 'asubstr_indices', 'asubstrings', 'asum', 'asumprod', 'atabulate', 'atail', 'atakewhile', 'atakewhile_inclusive', 'atakewhilenot', 'atakewhilenot_inclusive', 'atranspose', 'atriplewise', 'aunique', 'aunique_everseen', 'aunique_justseen', 'aunique_to_each', 'aunzip', 'azip', 'aziplongest', 'basic_collect', 'batch', 'batch2', 'batch_process', 'buffer', 'empty_agen', 'fmap', 'fmap_parallel', 'fmap_sequential', 'iter_task', 'map_on_map', 'mat_vec_mul', 'merge', 'tee', 'to_list', 'to_set', 'to_tuple', 'vecs_eq', 'window'
def agives[T](x: T, /) -> AsyncGenerator[T]: '''Yield the given value, then return.'''
def empty_agen() -> AsyncGenerator[Never]: '''Return an async generator that yields nothing. Due to async generator finalization issues, this is not a constant like :const:`~base.yield_to_event_loop`.'''
def aawgenf2agenf[T, **P](f: Callable[P, AsyncIterable[T]], /) -> Callable[P, AsyncGenerator[T]]: '''Convert a function that returns an awaitable resolving to an async iterable into one returning an async generator.'''
async def fmap[T, **P](fs: SupportsIteration[Callable[P, Awaitable[T]]], /, *a: P.args, **k: P.kwargs) -> list[T]: '''Return a list of the results of calling each async function in the first argument (an (async) iterable of functions), with the provided arguments.'''
def fmap_sequential[T, **P](fs: SupportsIteration[Callable[P, Awaitable[T]]], /, *a: P.args, **k: P.kwargs) -> AsyncGenerator[T]: '''Like :func:`fmap`, but only call a function after the last completes and the result is gotten.'''
def fmap_parallel[T, **P](fs: SupportsIteration[Callable[P, Awaitable[T]]], /, *a: P.args, **k: P.kwargs) -> AsyncGenerator[T]: '''Like :func:`fmap_sequential`, but starts background tasks for each call.'''
async def agather[T](it_of_its: SupportsIteration[Awaitable[T]], return_exceptions: bool=...) -> list[T]: '''Wraps :func:`asyncio.gather` to accept (async) iterables as the first argument, so that unpacking is not needed.'''
@overload
def map_on_map[T, R, V](outer: Callable[[R], V], inner: Callable[[T], SupportsIteration[R]], it: SupportsIteration[T], *, inner_await: Literal[False]=..., outer_await: Literal[False]=...) -> AsyncGenerator[tuple[V, ...]]: ...
@overload
def map_on_map[T, R, V](outer: Callable[[R], Awaitable[V]], inner: Callable[[T], SupportsIteration[R]], it: SupportsIteration[T], *, inner_await: Literal[False]=..., outer_await: Literal[True]) -> AsyncGenerator[tuple[V, ...]]: ...
@overload
def map_on_map[T, R, V](outer: Callable[[R], V], inner: Callable[[T], Awaitable[SupportsIteration[R]]], it: SupportsIteration[T], *, inner_await: Literal[True], outer_await: Literal[False]=...) -> AsyncGenerator[tuple[V, ...]]: ...
@overload
def map_on_map[T, R, V](outer: Callable[[R], Awaitable[V]], inner: Callable[[T], Awaitable[SupportsIteration[R]]], it: SupportsIteration[T], *, inner_await: Literal[True], outer_await: Literal[True]) -> AsyncGenerator[tuple[V, ...]]: '''Apply a transformation on an (async) iterable on top of another.'''
@overload
def tee[T](it: SupportsIteration[T], n: Literal[1]) -> tuple[AsyncGenerator[T]]: ...
@overload
def tee[T](it: SupportsIteration[T], n: Literal[2]=..., *, maxqsize: int=..., put_exc: bool=..., loop: AbstractEventLoop|None=...) -> tuple[AsyncGenerator[T], AsyncGenerator[T]]: ...
@overload
def tee[T](it: SupportsIteration[T], n: Literal[3], *, maxqsize: int=..., put_exc: bool=..., loop: AbstractEventLoop|None=...) -> tuple[AsyncGenerator[T], AsyncGenerator[T], AsyncGenerator[T]]: ...
@overload
def tee[T](it: SupportsIteration[T], n: Literal[4], *, maxqsize: int=..., put_exc: bool=..., loop: AbstractEventLoop|None=...) -> tuple[AsyncGenerator[T], AsyncGenerator[T], AsyncGenerator[T], AsyncGenerator[T]]: ...
@overload
def tee[T](it: SupportsIteration[T], n: Literal[5], *, maxqsize: int=..., put_exc: bool=..., loop: AbstractEventLoop|None=...) -> tuple[AsyncGenerator[T], AsyncGenerator[T], AsyncGenerator[T], AsyncGenerator[T], AsyncGenerator[T]]: ...
@overload
def tee[T](it: SupportsIteration[T], n: Literal[6], *, maxqsize: int=..., put_exc: bool=..., loop: AbstractEventLoop|None=...) -> tuple[AsyncGenerator[T], AsyncGenerator[T], AsyncGenerator[T], AsyncGenerator[T], AsyncGenerator[T], AsyncGenerator[T]]: ...
@overload
def tee[T](it: SupportsIteration[T], n: int, *, maxqsize: int=..., put_exc: bool=..., loop: AbstractEventLoop|None=...) -> tuple[AsyncGenerator[T], ...]:
    '''| Create ``n`` independent async generators from a single (async) iterable `it` that yield the same items, caching items in a queue when needed.
    | A background task will be spawned to consume the iterable.
    | Unlike :func:`itertools.tee`, the returned iterators are plain async generators, and the flattening step with a linked list as specified in the
    | :mod:`itertools` docs is not done.
    | ``maxqsize`` (default :data:`context.TEE_DEFAULT_MAX_QSIZE`) specifies how many unproduced items can be consumed from the source ahead of the
    | slowest consumer(s) before the background task and the faster consumers start blocking to wait for them. 0 or below indicates an unbounded queue.
    | If ``put_exc`` is ``True`` (default :data:`context.TEE_DEFAULT_PUT_EXC`), an exception raised by the source iterable will be propagated as late
    | as possible; that is, only when the caller gets to that point. Slower consumers are not immediately affected.
    | Otherwise, the exception will be raised in the background task used to consume the iterable, and :exc:`~asyncio.QueueShutDown` will be propagated
    | to callers waiting on consumers.'''
def adoublestarmap[T](f: Callable[..., T], it: SupportsIteration[Mapping[str, Any]], /) -> AsyncGenerator[T]: '''Like :func:`amap`, but the iterables should yield mappings that are unpacked as arguments to the function.'''
def astarmap_with_kwds[T](f: Callable[..., T], it: SupportsIteration[tuple[Iterable[Any], Mapping[str, Any]]], /) -> AsyncGenerator[T]: '''Like :func:`amap`, but the iterable should yield tuples of the form ``(args, kwargs)``, where ``args`` is an iterable of positional arguments and ``kwargs`` is a mapping of keyword arguments.'''
@overload
async def aunzip[T](ait: SupportsIteration[tuple[T]], *, put_batch: int=...) -> tuple[AUnzipConsumer[T]]: ...
@overload
async def aunzip[T, R](ait: SupportsIteration[tuple[T|R]], *, put_batch: int=..., fillvalue: R, maxqsize: int=...) -> tuple[AUnzipConsumer[T]]: ...
@overload
async def aunzip[T, S](ait: SupportsIteration[tuple[T, S]], *, put_batch: int=..., maxqsize: int=...) -> tuple[AUnzipConsumer[T], AUnzipConsumer[S]]: ...
@overload
async def aunzip[T, S, R](ait: SupportsIteration[tuple[T|R, S|R]], *, put_batch: int=..., fillvalue: R, maxqsize: int=...) -> tuple[AUnzipConsumer[T], AUnzipConsumer[S]]: ...
@overload
async def aunzip[T, S, V](ait: SupportsIteration[tuple[T, S, V]], *, put_batch: int=..., maxqsize: int=...) -> tuple[AUnzipConsumer[T], AUnzipConsumer[S], AUnzipConsumer[V]]: ...
@overload
async def aunzip[T, S, V, R](ait: SupportsIteration[tuple[T|R, S|R, V|R]], *, put_batch: int=..., fillvalue: R, maxqsize: int=...) -> tuple[AUnzipConsumer[T], AUnzipConsumer[S], AUnzipConsumer[V]]: ...
@overload
async def aunzip[T, S, V, U](ait: SupportsIteration[tuple[T, S, V, U]], *, put_batch: int=..., maxqsize: int=...) -> tuple[AUnzipConsumer[T], AUnzipConsumer[S], AUnzipConsumer[V], AUnzipConsumer[U]]: ...
@overload
async def aunzip[T, S, V, U, R](ait: SupportsIteration[tuple[T|R, S|R, V|R, U|R]], *, put_batch: int=..., fillvalue: R, maxqsize: int=...) -> tuple[AUnzipConsumer[T], AUnzipConsumer[S], AUnzipConsumer[V], AUnzipConsumer[U]]: ...
@overload
async def aunzip[T](ait: SupportsIteration[tuple[T, ...]], *, put_batch: int=..., maxqsize: int=...) -> tuple[AUnzipConsumer[T], ...]: ...
@overload
async def aunzip[T, R](ait: SupportsIteration[tuple[T|R, ...]], *, put_batch: int=..., fillvalue: R, maxqsize: int=...) -> tuple[AUnzipConsumer[T], ...]: ...
@overload
async def aunzip(ait: SupportsIteration[tuple[Any, ...]], *, put_batch: int=..., fillvalue: object=..., maxqsize: int=...) -> tuple[AUnzipConsumer[Any], ...]:
    '''| Undo the effect of :class:`zip`, :func:`itertools.zip_longest`, :func:`aziplongest` or :func:`azip`.
    | This function operates lazily, consuming items from the async iterable only when needed, in batches of size ``put_batch`` (default
    | :data:`context.AUNZIP_DEFAULT_PUT_BATCH`) and caching other items in queues of capacity ``maxqsize`` (default
    | :data:`context.AUNZIP_DEFAULT_MAX_QSIZE`).

    .. warning:: This function may require significant auxiliary space.'''
def merge[T](*I: SupportsIteration[T], reverse: bool=..., maxqsize: int=...) -> AsyncGenerator[T]:
    '''| Merge items from the (async) iterables into a single async generator, according to the order in which they come.
    | If ``reverse`` is ``True``, the order is reversed, but the returned generator only starts when all items are available.
    | ``maxqsize`` (default :data:`context.MERGE_DEFAULT_MAX_QSIZE`) controls the maximum number of items the consumer can fall behind
    | the producers before the producers cease to be advanced.

    .. caution:: If ``maxqsize`` is smaller than the total number of items in the sources in reverse mode, a deadlock will occur.'''
def aflatten[T](it: SupportsIteration[SupportsIteration[T]]) -> AsyncGenerator[T]: '''Flatten one level of nesting using :class:`~iterclasses.achain` and return an async iterator over it.'''
def batch[T](it: SupportsIteration[T], n: int, *, item_timeout: float|None=..., strict: bool=...) -> AsyncGenerator[list[T]]: '''More flexible but slightly slower implementation of :func:`batch2`, supporting timeouts waiting for each item, that raises :exc:`ValueError` instead of :exc:`~exceptions.ItemsExhausted` in the case of the length of the iterable being indivisible by the batch size.'''
@overload
def batch2[T](it: SupportsIteration[T], n: int, strict: Literal[True]) -> AsyncGenerator[list[T]]: ...
@overload
def batch2[T](it: SupportsIteration[T], n: int|None, strict: Literal[False]=...) -> AsyncGenerator[list[T]]: '''Batch an (async) iterable into an async generator of lists. If ``strict=True`` is specified, raise :exc:`~exceptions.ItemsExhausted` on the last batch if it is discovered then that the iterable does not have enough items for a complete batch.'''
def aevery[T](it: SupportsIteration[T], n: int, *, skip_first: bool=...) -> AsyncGenerator[T]: '''Yield every ``n``-th item from an (async) iterable, optionally skipping the first item.'''
def aeveryother[T](it: SupportsIteration[T], *, skip_first: bool=...) -> AsyncGenerator[T]: '''Yield every other item from an (async) iterable, optionally skipping the first item.'''
@overload
def aside_effect[T](f: Callable[[list[T]], object], it: SupportsIteration[T], /, *, size: int, before: Callable[[], object]|None=..., after: Callable[[], object]|None=...) -> AsyncGenerator[T]: ...
@overload
def aside_effect[T](f: Callable[[T], object], it: SupportsIteration[T], /, *, size: None=..., before: Callable[[], object]|None=..., after: Callable[[], object]|None=...) -> AsyncGenerator[T]:
    '''| Apply a side effect function ``f`` to each item in an (async) iterable ``it`` and yield the items unchanged in an async generator.
    | If ``size`` is specified, the side effect function is applied to batches of that size instead of individual items, but the items are
    | still yielded separately.
    | The ``before`` and ``after`` functions are called before and after the iteration, respectively, but ``after`` is not called if
    | ``before`` fails.'''
def asliced[T: SupportsSlicing[Any]](seq: T, n: int, strict: bool=...) -> AsyncGenerator[T]:
    '''| Slice a slicable object ``seq`` (so named because these are usually sequences) and yield slices of the size ``n``, which should be of the same type as ``seq``, from the start to the end.
    | If ``strict`` is ``True``, raise :exc:`ValueError` if the length of any slice is less than ``n`` (should only happen for the last slice unless the :meth:`~object.__getitem__` method is misimplemented).'''
def buffer[T](it: SupportsIteration[T], maxsize: int=..., *, timeout_get: float|None=..., timeout_put: float|None=..., cooldown: float=..., loop: AbstractEventLoop|None=...) -> AsyncGenerator[T]:
    '''| Buffer the given (async) iterable in an async generator, with an async queue as buffer of capacity `maxsize` (default unbounded) and optional timeouts for getting and putting items into the buffer.
    | ``cooldown`` specifies how long to wait after hitting a get timeout before trying again; whereas when a put timeout is reached, the async generator finishes.'''
def asplitat[T](it: SupportsIteration[T], pred: Callable[[T], object], maxsplit: int=..., keep_sep: bool=...) -> AsyncGenerator[list[T]]: '''Split an async iterator at each item satisfying `pred`, with ``keep_sep`` dictating whether the separator is to be included as the last item of each list.'''
def batch_process[T, R](items: SupportsIteration[T], size: int, processor: Callable[[list[T]], Awaitable[R]]) -> AsyncGenerator[R]: '''Apply ``processor`` to each batch of size `size` in `items` and yield the results awaited.'''
def window[T](it: SupportsIteration[T], size: int, step: int=...) -> AsyncGenerator[tuple[T, ...], tuple[int, int]|None]: '''Window an async iterable into an async generator of tuples of the specified size and step. You can send in a tuple ``(size, step)`` to change the behaviour of the iterator.'''
async def aall(it: SupportsIteration[object]) -> bool: '''Async version of :func:`all`.'''
async def aany(it: SupportsIteration[object]) -> bool: '''Async version of :func:`any`.'''
@overload
async def amax[C: SupportsRichComparison](it: SupportsIteration[C], *, default: C=...) -> C: ...
@overload
async def amax[C: SupportsRichComparison](arg1: C, arg2: C, /, *args: C, default: C=...) -> C: ...
@overload
async def amax[T](it: SupportsIteration[T], *, key: Callable[[T], SupportsRichComparison], default: T=...) -> T: ...
@overload
async def amax[T](arg1: T, arg2: T, /, *args: T, key: Callable[[T], SupportsRichComparison], default: T=...) -> T: '''Async version of :func:`max`.'''
@overload
async def amin[C: SupportsRichComparison](it: SupportsIteration[C], *, default: C=...) -> C: ...
@overload
async def amin[C: SupportsRichComparison](arg1: C, arg2: C, /, *args: C, default: C=...) -> C: ...
@overload
async def amin[T](it: SupportsIteration[T], *, key: Callable[[T], SupportsRichComparison], default: T=...) -> T: ...
@overload
async def amin[T](arg1: T, arg2: T, /, *args: T, key: Callable[[T], SupportsRichComparison], default: T=...) -> T: '''Async version of :func:`min`.'''
@overload
def azip[T](i1: SupportsIteration[T], /) -> AsyncGenerator[tuple[T]]: ...
@overload
def azip[T, R](i1: SupportsIteration[T], i2: SupportsIteration[R], /) -> AsyncGenerator[tuple[T, R]]: ...
@overload
def azip[T, R](i1: SupportsIteration[T], i2: SupportsIteration[R], /, *, strict: Literal[True]) -> AsyncGenerator[tuple[T, R]]: ...
@overload
def azip[T, R, V](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], /) -> AsyncGenerator[tuple[T, R, V]]: ...
@overload
def azip[T, R, V](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], /, *, strict: Literal[True]) -> AsyncGenerator[tuple[T, R, V]]: ...
@overload
def azip[T, R, V, U](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], /) -> AsyncGenerator[tuple[T, R, V, U]]: ...
@overload
def azip[T, R, V, U](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], /, *, strict: Literal[True]) -> AsyncGenerator[tuple[T, R, V, U]]: ...
@overload
def azip[T, R, V, U, S](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], i5: SupportsIteration[S], /) -> AsyncGenerator[tuple[T, R, V, U, S]]: ...
@overload
def azip[T, R, V, U, S](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], i5: SupportsIteration[S], /, *, strict: Literal[True]) -> AsyncGenerator[tuple[T, R, V, U, S]]: ...
@overload
def azip[T](*its: SupportsIteration[T], strict: bool=...) -> AsyncGenerator[tuple[T, ...]]: '''Async version of :class:`zip` that is not a class.'''
@overload
def amap[T, R](f: Callable[[T], Awaitable[R]], it: SupportsIteration[T], /, *, await_: Literal[True], strict: Literal[False]=...) -> AsyncGenerator[R]: ...
@overload
def amap[T, R](f: Callable[[T], R], it: SupportsIteration[T], /, *, await_: Literal[False]=..., strict: Literal[False]=...) -> AsyncGenerator[R]: ...
@overload
def amap[T, S, R](f: Callable[[T, S], Awaitable[R]], i1: SupportsIteration[T], i2: SupportsIteration[S], /, *, await_: Literal[True], strict: bool=...) -> AsyncGenerator[R]: ...
@overload
def amap[T, S, R](f: Callable[[T, S], R], i1: SupportsIteration[T], i2: SupportsIteration[S], /, *, await_: Literal[False]=..., strict: bool=...) -> AsyncGenerator[R]: ...
@overload
def amap[T, S, V, R](f: Callable[[T, S, V], Awaitable[R]], i1: SupportsIteration[T], i2: SupportsIteration[S], i3: SupportsIteration[V], /, *, await_: Literal[True], strict: bool=...) -> AsyncGenerator[R]: ...
@overload
def amap[T, S, V, R](f: Callable[[T, S, V], R], i1: SupportsIteration[T], i2: SupportsIteration[S], i3: SupportsIteration[V], /, *, await_: Literal[False]=..., strict: bool=...) -> AsyncGenerator[R]: ...
@overload
def amap[T, S, V, U, R](f: Callable[[T, S, V, U], Awaitable[R]], i1: SupportsIteration[T], i2: SupportsIteration[S], i3: SupportsIteration[V], i4: SupportsIteration[U], /, *, await_: Literal[True], strict: bool=...) -> AsyncGenerator[R]: ...
@overload
def amap[T, S, V, U, R](f: Callable[[T, S, V, U], R], i1: SupportsIteration[T], i2: SupportsIteration[S], i3: SupportsIteration[V], i4: SupportsIteration[U], /, *, await_: Literal[False]=..., strict: bool=...) -> AsyncGenerator[R]: ...
@overload
def amap[T, R](f: Callable[[*tuple[T, ...]], Awaitable[R]], /, *its: SupportsIteration[T], await_: Literal[True], strict: bool=...) -> AsyncGenerator[R]: ...
@overload
def amap[T, R](f: Callable[[*tuple[T, ...]], R], /, *its: SupportsIteration[T], await_: Literal[False]=..., strict: bool=...) -> AsyncGenerator[R]: ...
@overload
def amap[R](f: Callable[..., Awaitable[R]], /, *its: SupportsIteration[object], await_: Literal[True], strict: bool=...) -> AsyncGenerator[R]: ...
@overload
def amap[R](f: Callable[..., R], /, *its: SupportsIteration[object], await_: Literal[False]=..., strict: bool=...) -> AsyncGenerator[R]: '''Async version of :class:`map` that is not a class, with ``await_`` dictating whether the return value of the function is to be awaited before yielding.'''
def afilter[T](f: Callable[[T], object]|None, it: SupportsIteration[T]) -> AsyncGenerator[T]: '''Async version of :class:`filter` that is not a class.'''
@overload
def amapif[T, R](f: Callable[[T], R], pred: Callable[[T], object]|None, it: SupportsIteration[T], /, await_: Literal[False]=...) -> AsyncGenerator[R]: ...
@overload
def amapif[T, R](f: Callable[[T], Awaitable[R]], pred: Callable[[T], object]|None, it: SupportsIteration[T], /, await_: Literal[True]) -> AsyncGenerator[R]: '''Essentially the restriction of :func:`amultimapif` to one (async) iterable, which allows for more flexibility.'''
@overload
def amultimapif[T, R](f: Callable[[T], R], pred: Callable[[tuple[T]], object], it: SupportsIteration[T], /, *, await_: Literal[False]=...) -> AsyncGenerator[R]: ...
@overload
def amultimapif[T, R](f: Callable[[T], Awaitable[R]], pred: Callable[[tuple[T]], object], it: SupportsIteration[T], /, *, await_: Literal[True]) -> AsyncGenerator[R]: ...
@overload
def amultimapif[T, V, R](f: Callable[[T, V], R], pred: Callable[[tuple[T, V]], object], i1: SupportsIteration[T], i2: SupportsIteration[V], /, *, await_: Literal[False]=...) -> AsyncGenerator[R]: ...
@overload
def amultimapif[T, V, R](f: Callable[[T, V], Awaitable[R]], pred: Callable[[tuple[T, V]], object], i1: SupportsIteration[T], i2: SupportsIteration[V], /, *, await_: Literal[True]) -> AsyncGenerator[R]: ...
@overload
def amultimapif[T, V, S, R](f: Callable[[T, V, S], R], pred: Callable[[tuple[T, V, S]], object], i1: SupportsIteration[T], i2: SupportsIteration[V], i3: SupportsIteration[S], /, *, await_: Literal[False]=...) -> AsyncGenerator[R]: ...
@overload
def amultimapif[T, V, S, R](f: Callable[[T, V, S], Awaitable[R]], pred: Callable[[tuple[T, V, S]], object], i1: SupportsIteration[T], i2: SupportsIteration[V], i3: SupportsIteration[S], /, *, await_: Literal[True]) -> AsyncGenerator[R]: ...
@overload
def amultimapif[T, V, S, U, R](f: Callable[[T, V, S, U], R], pred: Callable[[tuple[T, V, S, U]], object], i1: SupportsIteration[T], i2: SupportsIteration[V], i3: SupportsIteration[S], i4: SupportsIteration[U], /, *, await_: Literal[False]=...) -> AsyncGenerator[R]: ...
@overload
def amultimapif[T, V, S, U, R](f: Callable[[T, V, S, U], Awaitable[R]], pred: Callable[[tuple[T, V, S, U]], object], i1: SupportsIteration[T], i2: SupportsIteration[V], i3: SupportsIteration[S], i4: SupportsIteration[U], /, *, await_: Literal[True]) -> AsyncGenerator[R]: ...
@overload
def amultimapif[*Ts, R](f: Callable[[*Ts], R], pred: Callable[[tuple[*Ts]], object], /, *its: SupportsIteration[object], await_: Literal[False]=...) -> AsyncGenerator[R]: ...
@overload
def amultimapif[*Ts, R](f: Callable[[*Ts], Awaitable[R]], pred: Callable[[tuple[*Ts]], object], /, *its: SupportsIteration[object], await_: Literal[True]) -> AsyncGenerator[R]: '''Composition of :func:`astarmap`, :func:`afilter` and :func:`azip`.'''
@overload
def arange(stop: int, /) -> AsyncGenerator[int]: ...
@overload
def arange(start: int, stop: int, /) -> AsyncGenerator[int]: ...
@overload
def arange(start: int, stop: int, step: int, /) -> AsyncGenerator[int]: '''Async version of :class:`range` that is not a class.'''
@overload
def acount(start: int=..., step: int=...) -> AsyncGenerator[int]: ...
@overload
def acount(start: float, step: int=...) -> AsyncGenerator[float]: ...
@overload
def acount(start: float, step: float) -> AsyncGenerator[float]: ...
@overload
def acount(*, step: float) -> AsyncGenerator[float]: '''Async version of :func:`itertools.count` that is not a class.'''
def acycle[T](it: SupportsIteration[T]) -> AsyncGenerator[T]: '''Async version of :func:`itertools.cycle` that is not a class.'''
def arepeat[T](elem: T, n: int=...) -> AsyncGenerator[T]: '''Async version of :func:`itertools.repeat` that is not a class.'''
def aaccumulate[T](it: SupportsIteration[T], func: Callable[[T, T], T]=..., *, initial: T|None=...) -> AsyncGenerator[T]: '''Async version of :func:`itertools.accumulate` that is not a class.'''
def acompress[T](data: SupportsIteration[T], selectors: SupportsIteration[object]) -> AsyncGenerator[T]: '''Async version of :func:`itertools.compress` that is not a class.'''
def adropwhile[T](pred: Callable[[T], object], it: SupportsIteration[T], *, skip_first: bool=...) -> AsyncGenerator[T]:
    '''| Async version of :func:`itertools.dropwhile` that is not a class.
    | If ``skip_first`` is ``True``, drop also the first item that fails the predicate.'''
def afilterfalse[T](f: Callable[[T], object]|None, it: SupportsIteration[T]) -> AsyncGenerator[T]: '''Async version of :func:`itertools.filterfalse` that is not a class.'''
async def asattolo[T](it: SupportsIteration[T], /) -> list[T]: '''Return a list representing a random full-length permutation of the items in ``it``.'''
@overload
def agroupby[T](it: SupportsIteration[T], key: Callable[[T], T]=...) -> AsyncGenerator[tuple[T, AsyncGenerator[T]]]: ...
@overload
def agroupby[T, R](it: SupportsIteration[T], key: Callable[[T], R]) -> AsyncGenerator[tuple[R, AsyncGenerator[T]]]: '''Async version of :func:`itertools.groupby` that is not a class.'''
@overload
def aislice[T](it: SupportsIteration[T], stop: SupportsIndex|None=..., /) -> AsyncGenerator[T]: ...
@overload
def aislice[T](it: SupportsIteration[T], start: SupportsIndex|None, stop: SupportsIndex|None, step: SupportsIndex|None=..., /) -> AsyncGenerator[T]: '''Async version of :func:`itertools.islice` that is not a class.'''
def aiter_idx[T](it: SupportsIteration[T], value: T, start: int=..., stop: int|None=...) -> AsyncGenerator[int]: '''Yield the indices at which ``value`` occurs in ``it`` within ``start`` and ``stop``.'''
def asieve(n: int) -> AsyncGenerator[int]: '''Implementation of the Sieve of Eratosthenes, yielding prime numbers strictly smaller than ``n`` in order in an async generator.'''
def apairwise[T](it: SupportsIteration[T]) -> AsyncGenerator[tuple[T, T]]: '''Async version of :func:`itertools.pairwise` that is not a class.'''
def atriplewise[T](it: SupportsIteration[T]) -> AsyncGenerator[tuple[T, T, T]]: '''Yield overlapping triples of items from an (async) iterable.'''
@overload
def aproduct[T](i1: SupportsIteration[T], /, *, repeat: Literal[1]=...) -> AsyncGenerator[tuple[T]]: ...
@overload
def aproduct[T](i1: SupportsIteration[T], /, *, repeat: int) -> AsyncGenerator[tuple[T, ...]]: ...
@overload
def aproduct[T, R](i1: SupportsIteration[T], i2: SupportsIteration[R], /, *, repeat: Literal[1]=...) -> AsyncGenerator[tuple[T, R]]: ...
@overload
def aproduct[T, R](i1: SupportsIteration[T], i2: SupportsIteration[R], /, *, repeat: int) -> AsyncGenerator[tuple[T | R, ...]]: ...
@overload
def aproduct[T, R, V](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], /, *, repeat: Literal[1]=...) -> AsyncGenerator[tuple[T, R, V]]: ...
@overload
def aproduct[T, R, V](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], /, *, repeat: int) -> AsyncGenerator[tuple[T | R | V, ...]]: ...
@overload
def aproduct[T, R, V, U](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], /, *, repeat: Literal[1]=...) -> AsyncGenerator[tuple[T, R, V, U]]: ...
@overload
def aproduct[T, R, V, U](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], /, *, repeat: int) -> AsyncGenerator[tuple[T | R | V | U, ...]]: ...
@overload
def aproduct[T, R, V, U, S](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], i5: SupportsIteration[S], /, *, repeat: Literal[1]=...) -> AsyncGenerator[tuple[T, R, V, U, S]]: ...
@overload
def aproduct[T, R, V, U, S](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], i5: SupportsIteration[S], /, *, repeat: int) -> AsyncGenerator[tuple[T | R | V | U | S, ...]]: ...
@overload
def aproduct(i1: SupportsIteration[object], i2: SupportsIteration[object], i3: SupportsIteration[object], i4: SupportsIteration[object], i5: SupportsIteration[object], /, *its: SupportsIteration[object], repeat: int=...) -> AsyncGenerator[tuple[Any, ...]]: ...
@overload
def aproduct[T](*its: SupportsIteration[T], repeat: int=...) -> AsyncGenerator[tuple[T, ...]]: '''Async version of :func:`itertools.product` that is not a class.'''
@overload
def astarmap[*Ts, R](f: Callable[[*Ts], R], it: SupportsIteration[tuple[*Ts]], /, await_: Literal[False]=...) -> AsyncGenerator[R]: ...
@overload
def astarmap[*Ts, R](f: Callable[[*Ts], Awaitable[R]], it: SupportsIteration[tuple[*Ts]], /, await_: Literal[True]) -> AsyncGenerator[R]: '''Async version of :func:`itertools.starmap` that is not a class. ``await_`` specifies whether to await the return value of the transformation function.'''
def atakewhile[T](pred: Callable[[T], object]|None, it: SupportsIteration[T]) -> AsyncGenerator[T]: '''Async version of :func:`itertools.takewhile` that is not a class.'''
def atakewhilenot[T](pred: Callable[[T], object]|None, it: SupportsIteration[T]) -> AsyncGenerator[T]: '''Take items from the iterable while the predicate called on the item does not hold.'''
def atakewhile_inclusive[T](pred: Callable[[T], object]|None, it: SupportsIteration[T]) -> AsyncGenerator[T]: ''':func:`atakewhile`, but yielding the first falsy item last.'''
def atakewhilenot_inclusive[T](pred: Callable[[T], object]|None, it: SupportsIteration[T]) -> AsyncGenerator[T]: ''':func:`atakewhilenot`, but yielding the first truthy item last.'''
def ac3merge[T](seqs: SupportsIteration[MutableSequence[T]]) -> AsyncGenerator[T]: '''Async version of ``functools._c3_merge`` that doesn't assume the input is an synchronous iterable of mutable sequences of classes.'''
async def asquaresum[X: (int, float, complex)](it: SupportsIteration[X]) -> X: '''Return the sum of squares of items in an (async) iterable of numbers as a number of the same type.'''
@overload
def aziplongest[T](i1: SupportsIteration[T], /) -> AsyncGenerator[tuple[T]]: ...
@overload
def aziplongest[T, R](i1: SupportsIteration[T], i2: SupportsIteration[R], /, *, fillvalue: object=...) -> AsyncGenerator[tuple[T, R]]: ...
@overload
def aziplongest[T, R, V](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], /, *, fillvalue: object=...) -> AsyncGenerator[tuple[T, R, V]]: ...
@overload
def aziplongest[T, R, V, U](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], /, *, fillvalue: object=...) -> AsyncGenerator[tuple[T, R, V, U]]: ...
@overload
def aziplongest[T, R, V, U, S](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], i5: SupportsIteration[S], /, *, fillvalue: object=...) -> AsyncGenerator[tuple[T, R, V, U, S]]: ...
@overload
def aziplongest[T](*its: SupportsIteration[T], fillvalue: T=...) -> AsyncGenerator[tuple[T, ...]]: '''Async version of :func:`itertools.zip_longest` that is not a class. The first overload does not accept ``fillvalue``, because passing it with only one iterable does not make sense.'''
async def asumprod[X: (int, float, complex)](p: SupportsIteration[X], q: SupportsIteration[X], /) -> X: '''Return the sum of products of items in two iterables of numbers as a number of the same type. Not as precise as :func:`math.fsumprod` for floating-point numbers, but supports async iterables.'''
def aconvolve[X: (int, float, complex)](signal: SupportsIteration[X], kernel: SupportsIteration[X]) -> AsyncGenerator[X]: '''Polynomial multiplication with coefficients from the two iterables. The first iterable is advanced on demand, meaning it may be infinite, but the second iterable is exhausted immediately, storing all its items in memory.'''
@overload
def atabulate[T](f: Callable[[int], T], start: int=..., step: int=..., /, *, await_: Literal[False]=...) -> AsyncGenerator[T]: ...
@overload
def atabulate[T](f: Callable[[int], Awaitable[T]], start: int=..., step: int=..., /, *, await_: Literal[True]) -> AsyncGenerator[T]: '''Composition of :func:`amap` and :func:`acount`.'''
async def asum[X: (int, float, complex)](it: SupportsIteration[X], start: X=...) -> X: '''Return the sum of the items in the (async) iterable, preceded by ``start`` if passed.'''
async def aprod[X: (int, float, complex)](it: SupportsIteration[X], start: X=...) -> X: '''Return the product of the items in the (async) iterable, preceded by ``start`` if passed.'''
async def amatprod[M: SupportsMatMul](it: SupportsIteration[M], start: M) -> M: '''Return the product of the matrices in the (async) iterable, preceded by ``start`` if passed.'''
def acountdown(n: int, step: int=..., *, include_zero: bool=...) -> AsyncGenerator[int]: '''Count down from ``n`` to zero, excluding zero if it is to appear and ``include_zero`` is ``False`` (the default), by a step size of ``step``.'''
def atail[T](n: int, it: SupportsIteration[T], /) -> AsyncGenerator[T]: '''Yield the last ``n`` items from the (async) iterable ``it``.'''
def abfs[H: Hashable](start: H, neighbours: Callable[[H], SupportsIteration[H]], *, include_start: bool=...) -> AsyncGenerator[H]: '''Breadth-first search on a start node ``start``, given a function ``neighbours`` that returns an (async) iterable of neighbours to be traversed in order. If ``include_start`` is ``True``, the start node is yielded first.'''
def adfs[H: Hashable](start: H, neighbours: Callable[[H], SupportsIteration[H]], *, include_start: bool=...) -> AsyncGenerator[H]: '''Depth-first search on a start node ``start``, given a function ``neighbours`` that returns an (async) iterable of neighbours to be traversed in order. If ``include_start`` is ``True``, the start node is yielded first.'''
async def abrent[T](next_node: Callable[[T], SupportsIteration[T]], start: T, /) -> tuple[T, int, int]: '''Brent's algorithm for cycle detection, assuming that a cycle is indeed present, given a function ``next_node`` returning the next node from the previous. Return a tuple ``(node, la, mu)``, where ``node`` is the first node involved in a cycle. ``next_node`` should be deterministic.'''
async def ahammingdist[T](a: SupportsIteration[T], b: SupportsIteration[T], /, cmpeq: Callable[[T, T], object]=...) -> int: '''Return the Hamming distance between two (async) iterables, using ``cmpeq`` to check for equality if passed.'''
@overload
def amergesortedby[C: SupportsRichComparison](its: SupportsIteration[SupportsIteration[C]], *, key: Callable[[C], C]=..., await_: Literal[False]=..., reverse: bool=...) -> AsyncGenerator[C]: ...
@overload
def amergesortedby[T](its: SupportsIteration[SupportsIteration[T]], *, key: Callable[[T], SupportsRichComparison], await_: Literal[False]=..., reverse: bool=...) -> AsyncGenerator[T]: ...
@overload
def amergesortedby[T](its: SupportsIteration[SupportsIteration[T]], *, key: Callable[[T], Awaitable[SupportsRichComparison]], await_: Literal[True], reverse: bool=...) -> AsyncGenerator[T]: '''Async version of :func:`heapq.merge`.'''
@overload
def amultifilter[T](pred: Callable[[tuple[T]], object], it: SupportsIteration[T], /, *, strict: bool=...) -> AsyncGenerator[tuple[T]]: ...
@overload
def amultifilter[T, R](pred: Callable[[tuple[T, R]], object], i1: SupportsIteration[T], i2: SupportsIteration[R], /, *, strict: bool=...) -> AsyncGenerator[tuple[T, R]]: ...
@overload
def amultifilter[T, R, V](pred: Callable[[tuple[T, R, V]], object], i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], /, *, strict: bool=...) -> AsyncGenerator[tuple[T, R, V]]: ...
@overload
def amultifilter[T, R, V, U](pred: Callable[[tuple[T, R, V, U]], object], i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], /, *, strict: bool=...) -> AsyncGenerator[tuple[T, R, V, U]]: ...
@overload
def amultifilter[T, R, V, U, S](pred: Callable[[tuple[T, R, V, U, S]], object], i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], i5: SupportsIteration[S], /, *, strict: bool=...) -> AsyncGenerator[tuple[T, R, V, U, S]]: ...
@overload
def amultifilter[T](pred: Callable[[tuple[T, ...]], object], /, *its: SupportsIteration[T], strict: bool=...) -> AsyncGenerator[tuple[T, ...]]: ...
@overload
def amultifilter(pred: Callable[[tuple[Any, ...]], object], i1: SupportsIteration[object], i2: SupportsIteration[object], i3: SupportsIteration[object], i4: SupportsIteration[object], i5: SupportsIteration[object], /, *its: SupportsIteration[object], strict: bool=...) -> AsyncGenerator[tuple[Any, ...]]: '''Composition of :func:`afilter` and :func:`azip`.'''
@overload
def amultifilterfalse[T](pred: Callable[[tuple[T]], object], it: SupportsIteration[T], /, *, strict: bool=...) -> AsyncGenerator[tuple[T]]: ...
@overload
def amultifilterfalse[T, R](pred: Callable[[tuple[T, R]], object], i1: SupportsIteration[T], i2: SupportsIteration[R], /, *, strict: bool=...) -> AsyncGenerator[tuple[T, R]]: ...
@overload
def amultifilterfalse[T, R, V](pred: Callable[[tuple[T, R, V]], object], i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], /, *, strict: bool=...) -> AsyncGenerator[tuple[T, R, V]]: ...
@overload
def amultifilterfalse[T, R, V, U](pred: Callable[[tuple[T, R, V, U]], object], i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], /, *, strict: bool=...) -> AsyncGenerator[tuple[T, R, V, U]]: ...
@overload
def amultifilterfalse[T, R, V, U, S](pred: Callable[[tuple[T, R, V, U, S]], object], i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], i5: SupportsIteration[S], /, *, strict: bool=...) -> AsyncGenerator[tuple[T, R, V, U, S]]: ...
@overload
def amultifilterfalse[T](pred: Callable[[tuple[T, ...]], object], /, *its: SupportsIteration[T], strict: bool=...) -> AsyncGenerator[tuple[T, ...]]: ...
@overload
def amultifilterfalse(pred: Callable[[tuple[Any, ...]], object], i1: SupportsIteration[object], i2: SupportsIteration[object], i3: SupportsIteration[object], i4: SupportsIteration[object], i5: SupportsIteration[object], /, *its: SupportsIteration[object], strict: bool=...) -> AsyncGenerator[tuple[Any, ...]]: '''Composition of :func:`afilterfalse` and :func:`azip`.'''
@overload
def amultistarfilter[T](pred: Callable[[T], object], it: SupportsIteration[T], /, *, strict: bool=...) -> AsyncGenerator[tuple[T]]: ...
@overload
def amultistarfilter[T, R](pred: Callable[[T, R], object], i1: SupportsIteration[T], i2: SupportsIteration[R], /, *, strict: bool=...) -> AsyncGenerator[tuple[T, R]]: ...
@overload
def amultistarfilter[T, R, V](pred: Callable[[T, R, V], object], i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], /, *, strict: bool=...) -> AsyncGenerator[tuple[T, R, V]]: ...
@overload
def amultistarfilter[T, R, V, U](pred: Callable[[T, R, V, U], object], i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], /, *, strict: bool=...) -> AsyncGenerator[tuple[T, R, V, U]]: ...
@overload
def amultistarfilter[T, R, V, U, S](pred: Callable[[T, R, V, U, S], object], i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], i5: SupportsIteration[S], /, *, strict: bool=...) -> AsyncGenerator[tuple[T, R, V, U, S]]: ...
@overload
def amultistarfilter[T](pred: Callable[[*tuple[T, ...]], object], /, *its: SupportsIteration[T], strict: bool=...) -> AsyncGenerator[tuple[T, ...]]: ...
@overload
def amultistarfilter(pred: Callable[[*tuple[Any, ...]], object], i1: SupportsIteration[object], i2: SupportsIteration[object], i3: SupportsIteration[object], i4: SupportsIteration[object], i5: SupportsIteration[object], /, *its: SupportsIteration[object], strict: bool=...) -> AsyncGenerator[tuple[Any, ...]]: '''Composition of :func:`astarfilter` and :func:`azip`.'''
@overload
def amultistarfilterfalse[T](pred: Callable[[T], object], it: SupportsIteration[T], /, *, strict: bool=...) -> AsyncGenerator[tuple[T]]: ...
@overload
def amultistarfilterfalse[T, R](pred: Callable[[T, R], object], i1: SupportsIteration[T], i2: SupportsIteration[R], /, *, strict: bool=...) -> AsyncGenerator[tuple[T, R]]: ...
@overload
def amultistarfilterfalse[T, R, V](pred: Callable[[T, R, V], object], i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], /, *, strict: bool=...) -> AsyncGenerator[tuple[T, R, V]]: ...
@overload
def amultistarfilterfalse[T, R, V, U](pred: Callable[[T, R, V, U], object], i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], /, *, strict: bool=...) -> AsyncGenerator[tuple[T, R, V, U]]: ...
@overload
def amultistarfilterfalse[T, R, V, U, S](pred: Callable[[T, R, V, U, S], object], i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], i5: SupportsIteration[S], /, *, strict: bool=...) -> AsyncGenerator[tuple[T, R, V, U, S]]: ...
@overload
def amultistarfilterfalse[T](pred: Callable[[*tuple[T, ...]], object], /, *its: SupportsIteration[T], strict: bool=...) -> AsyncGenerator[tuple[T, ...]]: ...
@overload
def amultistarfilterfalse(pred: Callable[[*tuple[Any, ...]], object], i1: SupportsIteration[object], i2: SupportsIteration[object], i3: SupportsIteration[object], i4: SupportsIteration[object], i5: SupportsIteration[object], /, *its: SupportsIteration[object], strict: bool=...) -> AsyncGenerator[tuple[Any, ...]]: '''Composition of :func:`astarfilterfalse` and :func:`azip`.'''
async def asample_weighted[T](it: SupportsIteration[tuple[T, float]], k: int, *, rrange: Callable[[int], int]=..., rand: Callable[[], float]=...) -> list[T]: '''The A-Chao with Jumps reservoir sampling algorithm. Chooses `k` items from an (async) iterable of ``(item, weight)`` pairs, where the probability of each item being chosen is proportional to its weight. ``rrange`` and ``rand`` should be the :meth:`randrange` and :meth:`random` methods of a random device respectively.'''
async def asamplel[T](it: SupportsIteration[T], k: int, *, rrange: Callable[[int], int]=..., rand: Callable[[], float]=...) -> list[T]: '''Algorithm L. Chooses `k` items from an (async) iterable of items, where each item is chosen with equal probability. ``rrange`` and ``rand`` should be the :meth:`~random.Random.randrange` and :meth:`~random.Random.random` methods of a random device respectively.'''
def astarfilter[T](pred: Callable[[*tuple[T, ...]], object], it: SupportsIteration[SupportsIteration[T]]) -> AsyncGenerator[tuple[T, ...]]: '''Filter an (async) iterable of tuples of items, yielding only those tuples for which the predicate returns a truthy value when called on the tuple unpacked.'''
def astarfilterfalse[T](pred: Callable[[*tuple[T, ...]], object], it: SupportsIteration[SupportsIteration[T]]) -> AsyncGenerator[tuple[T, ...]]: '''Filter an (async) iterable of tuples of items, yielding only those tuples for which the predicate returns a falsy value when called on the tuple unpacked.'''
async def to_tuple[T](it: SupportsIteration[T], /) -> tuple[T, ...]: '''Convert the output of :func:`to_list` into a tuple.'''
@overload
async def to_set[H: Hashable](it: SupportsIteration[H], /, frozen: Literal[False]=...) -> set[H]: ...
@overload
async def to_set[H: Hashable](it: SupportsIteration[H], /, frozen: Literal[True]) -> frozenset[H]: '''Convert the output of :func:`to_list` into a set or frozenset depending on the ``frozen`` parameter (``False`` by default).'''
async def aconsume[T](it: SupportsIteration[T], n: int|None=...) -> None: '''Advance the (async) iterable ``it`` by ``n`` steps, using a function-scoped executor created on demand where appropriate. If you want the item at the final position, use :func:`anth` instead.'''
async def anth[T](it: SupportsIteration[T], n: int, default: T=...) -> T: '''Return the ``n``-th item of the (async) iterable ``it``, or ``default`` if passed and there is no such item.'''
async def aallequal[T](it: SupportsIteration[T], key: Callable[[T], object]=..., strict: bool=...) -> bool: '''Whether all items in the (async) iterable are equal to each other according to the ``key`` function. Check for identity rather than equality if ``strict`` is ``True``.'''
def acombinations[T](it: SupportsIteration[T], r: int) -> AsyncGenerator[tuple[T, ...]]: '''Async version of :func:`itertools.combinations` that is not a class.'''
def acombinations_with_replacement[T](it: SupportsIteration[T], r: int) -> AsyncGenerator[tuple[T, ...]]: '''Async version of :func:`itertools.combinations_with_replacement` that is not a class.'''
def apermutations[T](it: SupportsIteration[T], r: int|None=...) -> AsyncGenerator[tuple[T, ...]]: '''Async version of :func:`itertools.permutations` that is not a class.'''
def apowerset[T](it: SupportsIteration[T]) -> AsyncGenerator[tuple[T, ...]]: '''Yield all the subsets of the (async) iterable ``it`` (by index!) as tuples, starting with the empty tuple.'''
async def aquantify[T](it: SupportsIteration[T], pred: Callable[[T], object]=...) -> int: '''Return the number of items in the (async) iterable for which the predicate is true.'''
def apadnone[T](it: SupportsIteration[T]) -> AsyncGenerator[T|None]: '''Yield the items in the (async) iterable ``it``, followed by ``None`` indefinitely.'''
def agrouper[T](it: SupportsIteration[T], n: int, fillvalue: T|RaiseType=...) -> AsyncGenerator[tuple[T | None, ...]]:
    '''| Collect items of the (async) iterable ``it`` into tuples of length ``n`` each.
    | If ``fillvalue`` is :data:`constants.RAISE`, raise :exc:`ValueError` if the last group is not of length ``n``.
    | Otherwise, pad the last group with ``fillvalue`` to length ``n`` if needed. No padding is done if not passed.'''
def aroundrobin[T](*its: SupportsIteration[T]) -> AsyncGenerator[T]: '''Yield items from the given (async) iterables in round-robin order, skipping exhausted iterables. Prefer over :func:`aroundrobin2` for less iterables.'''
def aroundrobin2[T](*its: SupportsIteration[T]) -> AsyncGenerator[T]: '''Yield items from the given (async) iterables in round-robin order, skipping exhausted iterables. Prefer over :func:`aroundrobin` for more iterables.'''
def aunique_everseen[T](it: SupportsIteration[T], key: Callable[[T], object]=...) -> AsyncGenerator[T]: '''Yield items from the (async) iterable ``it``, without yielding items already previously yielded.'''
def aunique_justseen[T](it: SupportsIteration[T], key: Callable[[T], object]=...) -> AsyncGenerator[T]: '''Yield items from the (async) iterable ``it``, without yielding consecutive duplicate items.'''
def aunique[T](it: SupportsIteration[T], key: Callable[[T], SupportsRichComparison]|None=..., reverse: bool=...) -> AsyncGenerator[T]: '''Yield unique elements from ``it`` in sorted order, according to ``key``, which should not be too expensive. If ``reverse`` is ``True``, yield in descending order.'''
def ancycles[T](it: SupportsIteration[T], n: int) -> AsyncGenerator[T]: '''Yield the items in the (async) iterable ``it`` over and over for a total of ``n`` cycles.'''
def apartition[T](pred: Callable[[T], object]|None, it: SupportsIteration[T]) -> tuple[AsyncGenerator[T], AsyncGenerator[T]]: '''Return a tuple ``(fgen, tgen)``. ``tgen`` is an async generator yielding the items in ``it`` passing the predicate, and ``fgen`` the others.'''
def aiterexcept[T](f: Callable[[], Awaitable[T]], exc: Exceptable, first: Callable[[], Awaitable[T]]=...) -> AsyncGenerator[T]: '''Yield the awaited output of ``first``, then ``f`` called with no arguments repeatedly until an exception present in ``exc`` occurs.'''
async def ailen(it: SupportsIteration[object]) -> int: '''Return the length of the (async) iterable ``it``, consuming it entirely.'''
def aiterate[T](f: Callable[[T], Awaitable[T]], start: T) -> AsyncGenerator[T]: '''Yield ``start``, then the awaited output of ``f`` called on the previous output repeatedly.'''
@overload
def asorted[C: SupportsRichComparison](it: SupportsIteration[C], *, reverse: bool=...) -> list[C]: ...
@overload
def asorted[T](it: SupportsIteration[T], *, key: Callable[[T], SupportsRichComparison], reverse: bool=...) -> list[T]: '''Async version of :func:`sorted`. O(n log n) time and O(n) space, but nowhere near as optimized as the builtin version.'''
def acanonical[T](it: SupportsIteration[T]) -> list[T]: '''Return a canonicalized ordering of the items in ``it``, which may change across different Python invocations or sessions.'''
def adistinct_permutations[T](it: SupportsIteration[T], r: int|None=...) -> AsyncGenerator[tuple[T, ...]]: '''Successive distinct permutations of the elements in ``it`` of size ``r``, or all sizes if not passed.'''
async def aisempty(it: SupportsIteration[object]) -> bool: '''Whether the (async) iterable ``it`` is empty.'''
def aunique_to_each[H: Hashable](*its: SupportsIteration[H]) -> AsyncGenerator[H]: '''Given multiple (async) iterables, yield every item that is only seen in exactly one of the iterables.'''
def aderangements[T](it: SupportsIteration[T], r: int|None=...) -> AsyncGenerator[T]: '''Successive derangements of the elements in ``it`` of size ``r``, or all sizes if not passed. Derangements are permutations with no fixed points.'''
def aintersperse[T](e: T, it: SupportsIteration[T], n: int=...) -> AsyncGenerator[T]: '''Yield ``e``, then the next ``n`` items in ``it``, and repeat until ``it`` is exhausted.'''
def ainterleave_stopearly[T](*it: SupportsIteration[T]) -> AsyncGenerator[T]: '''Yield the items from the iterables in a round-robin fashion until at least one is exhausted.'''
def aspy[T](it: SupportsIteration[T], n: int=...) -> tuple[AsyncGenerator[T], AsyncGenerator[T]]: '''Return an async generator containing the first ``n`` items, and another containing all the original items.'''
def ainterleave_evenly[T](its: SupportsIteration[SupportsIteration[T]], lengths: SupportsIteration[int]|None=...) -> AsyncGenerator[T]: '''Interleave items of the iterables evenly according to the lengths if passed, and determined by calling the :meth:`~object.__len__` method on the iterables if present otherwise.'''
def ainterleave_randomly[T](its: SupportsIteration[SupportsIteration[T]]) -> AsyncGenerator[T]: '''Interleave items of the iterables randomly, skipping exhausted iterables.'''
def acollapse(it: SupportsIteration[object], base_typ: tuple[type, ...]|type=..., levels: int|None=...) -> AsyncGenerator[Any]: '''Flatten the (async) iterable ``it`` by at most ``levels`` levels, without collapsing objects of types specified in ``base_typ``.'''
async def afirsttrue[T](it: SupportsIteration[T], default: T|None=..., pred: Callable[[T], object]=...) -> T: '''Return the first item in the (async) iterable ``it``'''
def aappend[T](val: T, it: SupportsIteration[T]) -> AsyncGenerator[T]: '''Append ``val`` to the (async) iterable ``it``.'''
def aprepend[T](val: T, it: SupportsIteration[T]) -> AsyncGenerator[T]: '''Prepend ``val`` to the (async) iterable ``it``.'''
def arandomproduct[T](*its: SupportsIteration[T], n: int=...) -> AsyncGenerator[T]: '''Draw ``n`` items from each of the input iterables ``its`` at random. '''
def arandomcombination[T](it: SupportsIteration[T], r: int) -> AsyncGenerator[T]: '''Draw ``r`` items at random from the input iterable ``it``, without replacement.'''
def arandom_combination_with_replacement[T](it: SupportsIteration[T], r: int) -> AsyncGenerator[T]: '''Draw ``r`` items at random from the input iterable ``it``, with replacement.'''
def arandom_permutation[T](it: SupportsIteration[T], r: int|None=...) -> AsyncGenerator[T]: '''Choose a random permutation of the elements in ``it`` of size ``r``, or all sizes if not passed.'''
async def afirst[T](it: SupportsIteration[T], default: T=...) -> T: '''Return the first item in the (async) iterable ``it``, or ``default`` if passed and ``it`` is empty.'''
async def alast[T](it: SupportsIteration[T], default: T=...) -> T: '''Return the last item in the (async) iterable ``it``, or ``default`` if passed and ``it`` is empty.'''
async def anth_or_last[T](it: SupportsIteration[T], n: int, default: T=...) -> T: '''Return the ``n``-th item in the (async) iterable ``it``, or the last item if out of bounds, or ``default`` if passed and ``it`` is empty.'''
def abefore_and_after[T](pred: Callable[[T], object], it: SupportsIteration[T]) -> tuple[AsyncGenerator[T], AsyncGenerator[T]]: ''':func:`atakewhile`, but return all remaining items in the second async generator (after the first is consumed).'''
def anthcombination[T](it: SupportsIteration[T], r: int, idx: int) -> AsyncGenerator[T]: '''Return the ``idx``-th combination of ``r`` elements from the input iterable ``it``, in lexicographic order.'''
def asubslices[T](it: SupportsIteration[T]) -> AsyncGenerator[tuple[T, ...]]: ''':func:`asubstrings`, but yield all subslices containing the first item first in ascending order of length, then all subslices containing the second item but not the first, and so on.'''
def arepeatfunc[T, *Ts](f: Callable[[*Ts], Awaitable[T]], times: int|None=..., *a: *Ts) -> AsyncGenerator[T]: '''Call the async function ``f`` with arguments ``a`` repeatedly for ``times`` times, or indefinitely if ``times`` is not passed, and yield the results awaited.'''
def apolynomial_from_roots[X: (int, float, complex)](roots: SupportsIteration[X]) -> AsyncGenerator[X]: '''Generate the coefficients of a polynomial given its roots in order of descending powers.'''
def atranspose[T](mat: SupportsIteration[SupportsIteration[T]]) -> AsyncGenerator[tuple[T, ...]]: '''Compute the transpose of a matrix.'''
def aflatten_tensor(tensor: SupportsIteration[object], base_typ: tuple[type, ...]|type=...) -> AsyncGenerator[Any]: ''':func:`acollapse`, but using a different, more memory-efficient strategy that does not support the `levels` parameter.'''
def apolynomial_derivative[X: (int, float, complex)](coeff: SupportsIteration[X]) -> AsyncGenerator[X]: '''Compute the coefficients of the derivative of a polynomial. Both input and output iterables are in order of descending powers.'''
async def apolynomial_eval[X: (int, float, complex)](coeff: SupportsIteration[X], x: X) -> X: '''Evaluate a polynomial at ``x`` given its coefficients in order of descending powers.'''
@overload
def areshape[T](mat: SupportsIteration[SupportsIteration[T]], shape: int) -> AsyncGenerator[list[T]]: ...
@overload
def areshape(mat: SupportsIteration[object], shape: SupportsIteration[int]) -> AsyncGenerator[list[Any]]: '''Change the shape of a tensor according to ``shape``. For an integer ``shape``, the matrix must be 2D and ``shape`` is the number of output columns.'''
def afactor(n: int) -> AsyncGenerator[int]: '''Generate the prime factors of ``n`` asynchronously. Do not rely on the resultant order.'''
def arunning_median[N: (int, float)](it: SupportsIteration[N], *, maxlen: SupportsIndex|None=...) -> AsyncGenerator[N]: '''Yield the median of all the items seen from ``it`` within a window of size ``maxlen``, then advance it.'''
async def arandom_derangement[T](it: SupportsIteration[T]) -> tuple[T, ...]: '''Generate a random derangement of items in the (async) iterable ``it``.'''
def amatmul[X: (int, float, complex)](M: SupportsIteration[SupportsIteration[X]], N: SupportsIteration[SupportsIteration[X]]) -> AsyncGenerator[tuple[X, ...]]: '''Matrix multiplication of ``M`` and ``N``. O(n^3) time, since this library does not specialize in these operations.'''
def mat_vec_mul(M: SupportsIteration[SupportsIteration[int]], V: SupportsIteration[int]) -> AsyncGenerator[int]: '''Multiplication of a matrix ``M`` and a vector ``V``. O(n^2).'''
async def vecs_eq[T](u: SupportsIteration[T], v: SupportsIteration[T], cmpeq: Callable[[T, T], object]=..., *, strict: bool=...) -> bool: '''Whether the vectors ``u`` and ``v`` are equal according to ``cmpeq`` called on each pair of items from iterating through them in parallel. If ``strict`` is ``False`` (default ``True``), may return ``True`` even for differently-sized vectors.'''
async def afreivalds(A: SupportsIteration[SupportsIteration[int]], B: SupportsIteration[SupportsIteration[int]], C: SupportsIteration[SupportsIteration[int]], k: int=...) -> bool: '''The probabilistic Freivalds algorithm to determine if the matrix product of ``A`` and ``B`` equals ``C``. O(kn^2) time, with a false positive rate of at most 2^(-k) and no false negatives.'''
async def basic_collect[T](it: SupportsIteration[T], n: int) -> list[T]: '''Return a list of the first ``n`` items in the (async) iterable ``it``, signalling no error if there are not enough items.'''
def asubstrings[T](it: SupportsIteration[T]) -> AsyncGenerator[tuple[T, ...]]: '''Yield all the contiguous subsequences of the (async) iterable ``it`` as tuples, in increasing order of length.'''
@overload
def asubstr_indices[S: (str, bytes, bytearray)](seq: S, reverse: bool=...) -> AsyncGenerator[tuple[S, int, int]]: ...
@overload
def asubstr_indices[T](seq: SupportsSlicing[T], reverse: bool=...) -> AsyncGenerator[tuple[Iterable[T], int, int]]: '''Yield tuples of the form `(substr, start, end)`, where `substr` is a contiguous subsequence of `seq` starting at index `start` and ending at index `end-1` (such that its length is `end-start`).'''
def iter_task[I: SupportsIteration[object]](it: I, summaryf: Callable[[I], Awaitable[Any]]=...) -> Task[float]: '''Return a task that calls `summaryf` on the passed (async) iterable and returns the time taken to run it. By default, `summaryf` consumes `it` fully.'''
def agetitems_from_indices[T](it: SupportsIteration[T], indices: SupportsIteration[SupportsIndex], setatend: Future[float]|None=..., finish: bool=...) -> list[Future[T]]:
    '''| Take an (async) iterable and an (async) iterable of integers interpreted as indices, and immediately returns a list of futures.
    | Their eventual results represent the items of that iterable at the corresponding index.
    | Also begin consumption of the iterable in the background.
    | Exceptions will be set in the futures that are not done if results are encountered during iteration or if the index is out of bounds.
    | Pass in a :class:`~asyncio.Future` for the ``setatend`` parameter, which cancels the background consumption of the async iterable once
    | it is done and cancels the undone futures.

    .. attention:: Negative indices would consume the whole iterable at once if not already consumed.
    .. warning:: Do not set the result of any returned future; instead, if the result is no longer relevant, cancel the future.
    .. note:: The consumption stops as soon as all the required results are pushed into the respective futures.'''
def aintersend[T, R](i1: AsyncGenerator[T, R], i2: AsyncGenerator[R, T]) -> AsyncGenerator[tuple[T, R]]: '''Feed ``i1`` and ``i2`` into each other and yield tuples of the form ``(yielded_from_i1, yielded_from_i2)``.'''
def asendstream[T, R](i1: AsyncGenerator[T, R], i2: SupportsIteration[R]) -> AsyncGenerator[T]: '''Feed ``i2`` into ``i1`` and yield the results.'''
@overload
def acat[T](first: T) -> AsyncGenerator[T, T]: ...
@overload
def acat[T](first: None=...) -> AsyncGenerator[T|None, T|None]: '''An async generator that yields the sent value, starting with ``first`` (default ``None``).'''
def aforever() -> AsyncGenerator[None]: '''An async generator that yields ``None`` forever. Equivalent to ``arepeat(None)``.'''
def aloops(n: int) -> AsyncGenerator[None]: '''Yield ``None`` ``n`` times. Equivalent to ``base.take(aforever(), n)`` and ``arepeat(None, n)``, but without creating intermediate integers.'''
async def aguessmax[T](it: SupportsIteration[T], estlen: int, *, key: Callable[[T], SupportsRichComparison]=..., default: T=..., finish_event: EventProt|None=...) -> T: '''Optimal solution to the secretary problem, using ``key`` to guess the maximum item, which is the candidate chosen, with 36.8% accuracy by consuming 36.8% of the (async) iterable.'''
async def aguessmin[T](it: SupportsIteration[T], estlen: int, *, key: Callable[[T], SupportsRichComparison]=..., default: T=..., finish_event: EventProt|None=...) -> T: '''Optimal solution to the secretary problem, using ``key`` to guess the minimum item, which is the candidate chosen, with 36.8% accuracy by consuming 36.8% of the (async) iterable.'''
def apowers_of_two(*, init: int=..., init_shift: int=..., shift: int=...) -> AsyncGenerator[int]: '''Optimized version of :func:`apowers` using bit shift operations for powers of two, four, eight, etc. Yield ``init<<init_shift``, ``init<<init_shift+shift``, ``init<<init_shift+2*shift``, ...'''
def areversed[T](it: SupportsIteration[T]|Reversible[T], /) -> AsyncGenerator[T]: '''Reverse an (async) iterable, calling its :meth:`~object.__reversed__` method if present, falling back to consuming all the items and yielding them in reverse order.'''
async def to_list[T](it: SupportsIteration[T], /) -> list[T]: '''Collect all items of an async iterable into a list. Faster than :func:`base.collect`.'''
async def aisprime(n: int) -> bool: '''Probabilistically test for primality of ``n``. O(log^3 n), with false-positive rate below 2^(-128) for integers above 10^24.'''
def adft(xarr: SupportsIteration[complex], /) -> AsyncGenerator[complex]: '''The discrete Fourier transform. O(n^2), since this library does not specialize in these operations.'''
def aidft(Xarr: SupportsIteration[complex], /) -> AsyncGenerator[complex]: '''The inverse discrete Fourier transform. O(n^2) just like :func:`adft`.'''
def apowers[X: (int, float, complex)](base: X, start: X=...) -> AsyncGenerator[X]:
    '''Yield ``start``, ``start*base``, ``start*base*base``, ...

    .. version-changed:: 0.9.9

      When it is found that the base is a perfect power of two, this will delegate to :func:`apowers_of_two` as an optimization.'''
def arunlength_encode[T](it: SupportsIteration[T], /) -> AsyncGenerator[tuple[T, int]]: '''Compress an (async) iterable into an async generator of pairs with run-length encoding. Items in the result are in the form ``(item, count)``, where ``item`` is an item from the input iterable and ``count`` is the number of times it is repeated consecutively.'''
def arunlength_decode[T](it: SupportsIteration[tuple[T, int]], /) -> AsyncGenerator[T]: '''Inverse of the above.'''
@overload
async def aargmin[T](it: SupportsIteration[T], key: Callable[[T], SupportsRichComparison], default: int=...) -> int: ...
@overload
async def aargmin[C: SupportsRichComparison](it: SupportsIteration[C], *, default: int=...) -> int: '''Return the index of the first occurrence of the minimum element in the (async) iterable ``it`` according to ``key``, or ``default`` if empty.'''
@overload
async def aargmax[T](it: SupportsIteration[T], key: Callable[[T], SupportsRichComparison], default: int=...) -> int: ...
@overload
async def aargmax[C: SupportsRichComparison](it: SupportsIteration[C], *, default: int=...) -> int: '''Return the index of the first occurrence of the maximum element in the (async) iterable ``it`` according to ``key``, or ``default`` if empty.'''
def arunningmean[X: (int|float, complex)](it: SupportsIteration[X]) -> AsyncGenerator[X]: '''Repeatedly yield the mean of the items in the iterable so far, and advance the iterable.'''
@overload
def apowersetofsets[H: Hashable](it: SupportsIteration[H], *, frozen: Literal[True]=...) -> AsyncGenerator[frozenset[H]]: ...
@overload
def apowersetofsets[H: Hashable](it: SupportsIteration[H], *, frozen: Literal[False]) -> AsyncGenerator[set[H]]: '''Yield all the subsets of the items in the (async) iterable of hashable objects after consuming it at once and removing duplicates, as :class:`frozenset`'s if ``frozen`` is ``True`` (the default) and :class:`set`'s otherwise.'''
def aserialize[T](it: SupportsIteration[T]) -> AsyncGenerator[T]: '''Protect an (async) iterable from being consumed by many parties concurrently by applying an async lock.'''
@overload
def aonline_sorter[T](it: SupportsIteration[T], *, key: Callable[[T], SupportsRichComparison], reverse: bool=..., slow: bool=...) -> AsyncGenerator[T, T|None]: ...
@overload
def aonline_sorter[C: SupportsRichComparison](it: SupportsIteration[C], *, reverse: bool=..., slow: bool=...) -> AsyncGenerator[C, C|None]:
    '''| Sort items from an (async) iterable and those sent in on the fly in the async generator interface (i.e. by awaiting
    | the return value of :meth:`~types.AsyncGeneratorType.asend`), according to ``key`` and ``reverse``.
    | Does not work well with items that are ``None``.
    | Evaluates the truthiness of the ``slow`` parameter every time a new item is received, and if it is ``True``, offloads the evaluation of the
    | ``key`` for that item to an executor, such that the :meth:`__bool__` method on ``slow`` may reflect the state of the program but can also be
    | a plain boolean.

    .. note:: Uses a stable variant of heap sort internally, which is O(n log n) time and O(n) space.

    .. version-changed:: 0.9.9

      The ``it`` parameter is now required because an async generator can only be primed asynchronously, and a non-``None`` value cannot be sent in
      to start the async generator, causing the resultant generator to always be empty. If ``it`` itself is empty, the generator will also be empty.
'''
