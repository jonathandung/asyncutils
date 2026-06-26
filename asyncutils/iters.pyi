'''| Functional and composable interface to get async generators from (async) iterables. Many of the algorithms here are taken from :mod:`more_itertools`, but some are unique to async.
| However, since they must support both sync and async iterables, they are much less efficient than their sync counterparts.
'''
from ._internal.prots import EventProtocol, Exceptable, NotNone, RaiseType, SupportsIteration, SupportsMatMul, SupportsRichComparison, SupportsSlicing, AUnzipConsumer
from asyncio import AbstractEventLoop, Future, Task
from collections.abc import AsyncIterable, AsyncGenerator, Awaitable, Callable, Hashable, Iterable, Mapping, MutableSequence, Reversible
from types import AsyncGeneratorType
from typing import Any, Concatenate, Literal, Never, SupportsIndex, overload
from typing_extensions import deprecated
__all__ = 'aaccumulate', 'aadjacent', 'aall', 'aallequal', 'aany', 'aappend', 'aargmax', 'aargmin', 'aawgenf2agenf', 'abefore_and_after', 'abfs', 'abrent', 'ac3merge', 'acanonical', 'acat', 'acollapse', 'acombinations', 'acombinations_with_replacement', 'acompress', 'aconsume', 'aconvolve', 'acount', 'acount_cycle', 'acountdown', 'acycle', 'aderangements', 'adfs', 'adft', 'adifference', 'adistinct_permutations', 'adouble_starmap', 'adropwhile', 'aevery', 'aeveryother', 'afactor', 'afilter', 'afilterfalse', 'afirst', 'afirstfalse', 'afirsttrue', 'aflatten', 'aflatten_tensor', 'aforever', 'afreivalds', 'agather', 'agetitems_from_indices', 'agives', 'agroupby', 'agroupby_transform', 'agrouper', 'aguessmax', 'aguessmin', 'ahamming_dist', 'aidft', 'ailen', 'ainterleave_evenly', 'ainterleave_randomly', 'ainterleave_stopearly', 'aintersend', 'aintersperse', 'aisempty', 'aislice', 'aisprime', 'aiter_idx', 'aiterate', 'aiterexcept', 'alast', 'aloops', 'amap', 'amapif', 'amatmul', 'amatprod', 'amax', 'amerge_sorted_by', 'amin', 'aminmax', 'aminmax_keyed', 'amultifilter', 'amultifilterfalse', 'amultimapif', 'amultistarfilter', 'amultistarfilterfalse', 'ancycles', 'anth', 'anth_combination', 'anth_or_last', 'aonline_sorter', 'aouter_product', 'apadded', 'apadnone', 'apairwise', 'apartition', 'apermutations', 'apolynomial_derivative', 'apolynomial_eval', 'apolynomial_from_roots', 'apowers', 'apowers_of_two', 'apowerset', 'apowerset_of_sets', 'aprepend', 'aprod', 'aproduct', 'aquantify', 'arandom_combination', 'arandom_combination_with_replacement', 'arandom_derangement', 'arandom_permutation', 'arandom_product', 'arange', 'arepeat', 'arepeat_each', 'arepeat_func', 'arepeat_last', 'areshape', 'areversed', 'aroundrobin', 'aroundrobin2', 'arunlength_decode', 'arunlength_encode', 'arunning_mean', 'arunning_median', 'asample_weighted', 'asamplel', 'asattolo', 'asendstream', 'aserialize', 'aside_effect', 'asieve', 'asliced', 'asorted', 'asplitat', 'aspy', 'asquaresum', 'astarfilter', 'astarfilterfalse', 'astarmap', 'astarmap_with_kwds', 'asubslices', 'asubstr_indices', 'asubstrings', 'asum', 'asumprod', 'atabulate', 'atail', 'atakeuntil', 'atakeuntil_inclusive', 'atakewhile', 'atakewhile_inclusive', 'atranspose', 'atriplewise', 'aunique', 'aunique_everseen', 'aunique_justseen', 'aunique_to_each', 'aunzip', 'azip', 'aziplongest', 'basic_collect', 'batch', 'batch2', 'batch_process', 'buffer', 'empty_agen', 'fmap', 'fmap_parallel', 'fmap_sequential', 'iter_task', 'map_on_map', 'mat_vec_mul', 'merge', 'tee', 'to_list', 'to_set', 'to_tuple', 'vecs_eq', 'window'
def agives[T](x: T, /) -> AsyncGeneratorType[T]: '''Yield the given value, then return.'''
def empty_agen() -> AsyncGeneratorType[Never]: '''Return an async generator that yields nothing. Due to async generator finalization issues, this is not a constant like :const:`~asyncutils.base.yield_to_event_loop`.'''
def aawgenf2agenf[T, **P](f: Callable[P, AsyncIterable[T]], /) -> Callable[P, AsyncGeneratorType[T]]: '''Convert a function that returns an awaitable resolving to an async iterable into one returning an async generator.'''
async def fmap[T, **P](fs: SupportsIteration[Callable[P, Awaitable[T]]], /, *a: P.args, **k: P.kwargs) -> list[T]: '''Return a list of the results of calling each async function in the first argument (an (async) iterable of functions), with the provided arguments.'''
def fmap_sequential[T, **P](fs: SupportsIteration[Callable[P, Awaitable[T]]], /, *a: P.args, **k: P.kwargs) -> AsyncGeneratorType[T]: '''Like :func:`fmap`, but only call a function after the last completes and the result is gotten.'''
def fmap_parallel[T, **P](fs: SupportsIteration[Callable[P, Awaitable[T]]], /, *a: P.args, **k: P.kwargs) -> AsyncGeneratorType[T]: '''Like :func:`fmap_sequential`, but starts background tasks for each call.'''
async def agather[T](it_of_its: SupportsIteration[Awaitable[T]], return_exceptions: bool=...) -> list[T]: '''Wrap :func:`asyncio.gather` to accept (async) iterables as the first argument, so that unpacking is not needed.'''
@overload
def map_on_map[T, R, V](outer: Callable[[R], V], inner: Callable[[T], SupportsIteration[R]], it: SupportsIteration[T], *, inner_await: Literal[False]=..., outer_await: Literal[False]=...) -> AsyncGeneratorType[tuple[V, ...]]: ...
@overload
def map_on_map[T, R, V](outer: Callable[[R], Awaitable[V]], inner: Callable[[T], SupportsIteration[R]], it: SupportsIteration[T], *, inner_await: Literal[False]=..., outer_await: Literal[True]) -> AsyncGeneratorType[tuple[V, ...]]: ...
@overload
def map_on_map[T, R, V](outer: Callable[[R], V], inner: Callable[[T], Awaitable[SupportsIteration[R]]], it: SupportsIteration[T], *, inner_await: Literal[True], outer_await: Literal[False]=...) -> AsyncGeneratorType[tuple[V, ...]]: ...
@overload
def map_on_map[T, R, V](outer: Callable[[R], Awaitable[V]], inner: Callable[[T], Awaitable[SupportsIteration[R]]], it: SupportsIteration[T], *, inner_await: Literal[True], outer_await: Literal[True]) -> AsyncGeneratorType[tuple[V, ...]]: '''Apply a transformation on an (async) iterable on top of another.'''
@overload
def tee[T](it: SupportsIteration[T], n: Literal[1]) -> tuple[AsyncGeneratorType[T]]: ...
@overload
def tee[T](it: SupportsIteration[T], n: Literal[2]=..., *, maxqsize: int=..., put_exc: bool=..., loop: AbstractEventLoop|None=...) -> tuple[AsyncGeneratorType[T], AsyncGeneratorType[T]]: ...
@overload
def tee[T](it: SupportsIteration[T], n: Literal[3], *, maxqsize: int=..., put_exc: bool=..., loop: AbstractEventLoop|None=...) -> tuple[AsyncGeneratorType[T], AsyncGeneratorType[T], AsyncGeneratorType[T]]: ...
@overload
def tee[T](it: SupportsIteration[T], n: Literal[4], *, maxqsize: int=..., put_exc: bool=..., loop: AbstractEventLoop|None=...) -> tuple[AsyncGeneratorType[T], AsyncGeneratorType[T], AsyncGeneratorType[T], AsyncGeneratorType[T]]: ...
@overload
def tee[T](it: SupportsIteration[T], n: Literal[5], *, maxqsize: int=..., put_exc: bool=..., loop: AbstractEventLoop|None=...) -> tuple[AsyncGeneratorType[T], AsyncGeneratorType[T], AsyncGeneratorType[T], AsyncGeneratorType[T], AsyncGeneratorType[T]]: ...
@overload
def tee[T](it: SupportsIteration[T], n: Literal[6], *, maxqsize: int=..., put_exc: bool=..., loop: AbstractEventLoop|None=...) -> tuple[AsyncGeneratorType[T], AsyncGeneratorType[T], AsyncGeneratorType[T], AsyncGeneratorType[T], AsyncGeneratorType[T], AsyncGeneratorType[T]]: ...
@overload
def tee[T](it: SupportsIteration[T], n: int, *, maxqsize: int=..., put_exc: bool=..., loop: AbstractEventLoop|None=...) -> tuple[AsyncGeneratorType[T], ...]:
    '''| Create ``n`` independent async generators from a single (async) iterable ``it`` that yield the same items, caching items in a queue when needed.
    | A background task is spawned to consume the iterable.
    | Unlike :func:`itertools.tee`, the returned iterators are plain async generators, and the flattening step with a linked list as specified in the :mod:`itertools` docs is not done.
    | ``maxqsize`` (default :const:`~asyncutils.context.Context.TEE_DEFAULT_MAX_QSIZE`) specifies how many unproduced items can be consumed from the source ahead of the slowest consumer(s) before the background task and the faster consumers start blocking to wait for them. 0 or below indicates an unbounded queue.
    | If ``put_exc`` is ``True`` (default :const:`~asyncutils.context.Context.TEE_DEFAULT_PUT_EXC`), an exception raised by the source iterable will be propagated as late as possible; that is, only when the caller gets to that point. Slower consumers are not immediately affected.
    | Otherwise, the exception is raised in the background task used to consume the iterable, and :exc:`~asyncio.QueueShutDown` will be propagated to callers waiting on consumers.
    '''
def adouble_starmap[T](f: Callable[..., T], it: SupportsIteration[Mapping[str, Any]], /) -> AsyncGeneratorType[T]: '''Like :func:`amap`, but the iterables should yield mappings that are unpacked as arguments to the function.'''
def astarmap_with_kwds[T](f: Callable[..., T], it: SupportsIteration[tuple[Iterable[Any], Mapping[str, Any]]], /) -> AsyncGeneratorType[T]: '''Like :func:`amap`, but the iterable should yield tuples of the form ``(args, kwargs)``, where ``args`` is an iterable of positional arguments and ``kwargs`` is a mapping of keyword arguments.'''
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
    | This function operates lazily, consuming items from the async iterable only when needed, in batches of size ``put_batch`` (default :const:`~asyncutils.context.Context.AUNZIP_DEFAULT_PUT_BATCH`) and caching other items in queues of capacity ``maxqsize`` (default :const:`~asyncutils.context.Context.AUNZIP_DEFAULT_MAX_QSIZE`).

    .. warning:: This function may require significant auxiliary space.
    '''
def merge[T](*I: SupportsIteration[T], reverse: bool=..., maxqsize: int=...) -> AsyncGeneratorType[T]:
    '''| Merge items from the (async) iterables into a single async generator, according to the order in which they come.
    | If ``reverse`` is ``True``, the order is reversed, but the returned generator only starts when all items are available.
    | ``maxqsize`` (default :const:`~asyncutils.context.Context.MERGE_DEFAULT_MAX_QSIZE`) controls the maximum number of items the consumer can fall behind the producers before the producers cease to be advanced.

    .. caution:: If ``maxqsize`` is smaller than the total number of items in the sources in reverse mode, a deadlock will occur.
    '''
def aflatten[T](it: SupportsIteration[SupportsIteration[T]]) -> AsyncGeneratorType[T]: '''Flatten one level of nesting using :class:`~asyncutils.iterclasses.AChain` and return an async iterator over it.'''
def batch[T](it: SupportsIteration[T], n: int, *, item_timeout: float|None=..., strict: bool=...) -> AsyncGeneratorType[list[T]]: '''More flexible but slightly slower implementation of :func:`batch2`, supporting timeouts waiting for each item, that raises :exc:`ValueError` instead of :class:`~asyncutils.exceptions.ItemsExhausted` in the case of the length of the iterable being indivisible by the batch size.'''
@overload
def batch2[T](it: SupportsIteration[T], n: int, strict: Literal[True]) -> AsyncGeneratorType[list[T]]: ...
@overload
def batch2[T](it: SupportsIteration[T], n: int|None, strict: Literal[False]=...) -> AsyncGeneratorType[list[T]]: '''Batch an (async) iterable into an async generator of lists. If ``strict=True`` is specified, raise :class:`~asyncutils.exceptions.ItemsExhausted` on the last batch if it is discovered then that the iterable does not have enough items for a complete batch.'''
def aevery[T](it: SupportsIteration[T], n: int, *, skip_first: bool=...) -> AsyncGeneratorType[T]: '''Yield every ``n``-th item from an (async) iterable, optionally skipping the first item.'''
def aeveryother[T](it: SupportsIteration[T], *, skip_first: bool=...) -> AsyncGeneratorType[T]: '''Yield every other item from an (async) iterable, optionally skipping the first item.'''
@overload
def aside_effect[T](f: Callable[[list[T]], object], it: SupportsIteration[T], /, *, size: int, before: Callable[[], object]|None=..., after: Callable[[], object]|None=...) -> AsyncGeneratorType[T]: ...
@overload
def aside_effect[T](f: Callable[[T], object], it: SupportsIteration[T], /, *, size: None=..., before: Callable[[], object]|None=..., after: Callable[[], object]|None=...) -> AsyncGeneratorType[T]:
    '''| Apply a side effect function ``f`` to each item in an (async) iterable ``it`` and yield the items unchanged in an async generator.
    | If ``size`` is specified, the side effect function is applied to batches of that size instead of individual items, but the items are still yielded separately.
    | The ``before`` and ``after`` functions are called before and after the iteration, respectively, but ``after`` is not called if ``before`` fails.
    '''
def asliced[T: SupportsSlicing[Any]](seq: T, n: int, strict: bool=...) -> AsyncGeneratorType[T]:
    '''| Slice a slicable object ``seq`` (so named because these are usually sequences) and yield slices of the size ``n``, which should be of the same type as ``seq``, from the start to the end.
    | If ``strict`` is ``True``, raise :exc:`ValueError` if the length of any slice is less than ``n`` (should only happen for the last slice unless the :meth:`~object.__getitem__` method is misimplemented).
    '''
def buffer[T](it: SupportsIteration[T], maxsize: int=..., *, timeout_get: float|None=..., timeout_put: float|None=..., cooldown: float=...) -> AsyncGeneratorType[T]:
    '''| Buffer the given (async) iterable in an async generator, with an async queue as buffer of capacity ``maxsize`` (default unbounded) and optional timeouts for getting and putting items into the buffer.
    | ``cooldown`` specifies how long to wait after hitting a get timeout before trying again; whereas when a put timeout is reached, the async generator finishes.
    '''
def asplitat[T](it: SupportsIteration[T], pred: Callable[[T], object], maxsplit: int=..., keep_sep: bool=...) -> AsyncGeneratorType[list[T]]: '''Split an async iterator at each item satisfying ``pred``, with ``keep_sep`` dictating whether the separator is to be included as the last item of each list.'''
def batch_process[T, R](items: SupportsIteration[T], size: int, processor: Callable[[list[T]], Awaitable[R]]) -> AsyncGeneratorType[R]: '''Apply ``processor`` to each batch of size ``size`` in ``items`` and yield the results awaited.'''
def window[T](it: SupportsIteration[T], size: int, step: int=...) -> AsyncGeneratorType[tuple[T, ...], tuple[int, int]|None]: '''Window an async iterable into an async generator of tuples of the specified size and step. You can send in a tuple ``(size, step)`` to change the behaviour of the iterator.'''
async def aall(it: SupportsIteration[object]) -> bool: '''Async version of :func:`all`.'''
async def aany(it: SupportsIteration[object]) -> bool: '''Async version of :func:`any`.'''
@overload
async def amax[T: SupportsRichComparison](it: SupportsIteration[T], *, default: T=...) -> T: ...
@overload
async def amax[T: SupportsRichComparison](arg1: T, arg2: T, /, *args: T, default: T=...) -> T: ...
@overload
async def amax[T](it: SupportsIteration[T], *, key: Callable[[T], SupportsRichComparison], default: T=...) -> T: ...
@overload
async def amax[T](arg1: T, arg2: T, /, *args: T, key: Callable[[T], SupportsRichComparison], default: T=...) -> T: '''Async version of :func:`max`.'''
@overload
async def amin[T: SupportsRichComparison](it: SupportsIteration[T], *, default: T=...) -> T: ...
@overload
async def amin[T: SupportsRichComparison](arg1: T, arg2: T, /, *args: T, default: T=...) -> T: ...
@overload
async def amin[T](it: SupportsIteration[T], *, key: Callable[[T], SupportsRichComparison], default: T=...) -> T: ...
@overload
async def amin[T](arg1: T, arg2: T, /, *args: T, key: Callable[[T], SupportsRichComparison], default: T=...) -> T: '''Async version of :func:`min`.'''
@overload
def azip[T](i1: SupportsIteration[T], /) -> AsyncGeneratorType[tuple[T]]: ...
@overload
def azip[T, R](i1: SupportsIteration[T], i2: SupportsIteration[R], /) -> AsyncGeneratorType[tuple[T, R]]: ...
@overload
def azip[T, R](i1: SupportsIteration[T], i2: SupportsIteration[R], /, *, strict: Literal[True]) -> AsyncGeneratorType[tuple[T, R]]: ...
@overload
def azip[T, R, V](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], /) -> AsyncGeneratorType[tuple[T, R, V]]: ...
@overload
def azip[T, R, V](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], /, *, strict: Literal[True]) -> AsyncGeneratorType[tuple[T, R, V]]: ...
@overload
def azip[T, R, V, U](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], /) -> AsyncGeneratorType[tuple[T, R, V, U]]: ...
@overload
def azip[T, R, V, U](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], /, *, strict: Literal[True]) -> AsyncGeneratorType[tuple[T, R, V, U]]: ...
@overload
def azip[T, R, V, U, S](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], i5: SupportsIteration[S], /) -> AsyncGeneratorType[tuple[T, R, V, U, S]]: ...
@overload
def azip[T, R, V, U, S](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], i5: SupportsIteration[S], /, *, strict: Literal[True]) -> AsyncGeneratorType[tuple[T, R, V, U, S]]: ...
@overload
def azip[T](*its: SupportsIteration[T], strict: bool=...) -> AsyncGeneratorType[tuple[T, ...]]: '''Async version of :class:`zip` that is not a class.'''
@overload
def amap[T, R](f: Callable[[T], Awaitable[R]], it: SupportsIteration[T], /, *, await_: Literal[True], strict: Literal[False]=...) -> AsyncGeneratorType[R]: ...
@overload
def amap[T, R](f: Callable[[T], R], it: SupportsIteration[T], /, *, await_: Literal[False]=..., strict: Literal[False]=...) -> AsyncGeneratorType[R]: ...
@overload
def amap[T, S, R](f: Callable[[T, S], Awaitable[R]], i1: SupportsIteration[T], i2: SupportsIteration[S], /, *, await_: Literal[True], strict: bool=...) -> AsyncGeneratorType[R]: ...
@overload
def amap[T, S, R](f: Callable[[T, S], R], i1: SupportsIteration[T], i2: SupportsIteration[S], /, *, await_: Literal[False]=..., strict: bool=...) -> AsyncGeneratorType[R]: ...
@overload
def amap[T, S, V, R](f: Callable[[T, S, V], Awaitable[R]], i1: SupportsIteration[T], i2: SupportsIteration[S], i3: SupportsIteration[V], /, *, await_: Literal[True], strict: bool=...) -> AsyncGeneratorType[R]: ...
@overload
def amap[T, S, V, R](f: Callable[[T, S, V], R], i1: SupportsIteration[T], i2: SupportsIteration[S], i3: SupportsIteration[V], /, *, await_: Literal[False]=..., strict: bool=...) -> AsyncGeneratorType[R]: ...
@overload
def amap[T, S, V, U, R](f: Callable[[T, S, V, U], Awaitable[R]], i1: SupportsIteration[T], i2: SupportsIteration[S], i3: SupportsIteration[V], i4: SupportsIteration[U], /, *, await_: Literal[True], strict: bool=...) -> AsyncGeneratorType[R]: ...
@overload
def amap[T, S, V, U, R](f: Callable[[T, S, V, U], R], i1: SupportsIteration[T], i2: SupportsIteration[S], i3: SupportsIteration[V], i4: SupportsIteration[U], /, *, await_: Literal[False]=..., strict: bool=...) -> AsyncGeneratorType[R]: ...
@overload
def amap[T, R](f: Callable[[*tuple[T, ...]], Awaitable[R]], /, *its: SupportsIteration[T], await_: Literal[True], strict: bool=...) -> AsyncGeneratorType[R]: ...
@overload
def amap[T, R](f: Callable[[*tuple[T, ...]], R], /, *its: SupportsIteration[T], await_: Literal[False]=..., strict: bool=...) -> AsyncGeneratorType[R]: ...
@overload
def amap[R](f: Callable[..., Awaitable[R]], /, *its: SupportsIteration[object], await_: Literal[True], strict: bool=...) -> AsyncGeneratorType[R]: ...
@overload
def amap[R](f: Callable[..., R], /, *its: SupportsIteration[object], await_: Literal[False]=..., strict: bool=...) -> AsyncGeneratorType[R]: '''Async version of :class:`map` that is not a class, with ``await_`` dictating whether the return value of the function is to be awaited before yielding.'''
def afilter[T](f: Callable[[T], object]|None, it: SupportsIteration[T]) -> AsyncGeneratorType[T]: '''Async version of :class:`filter` that is not a class.'''
@overload
def amapif[T, R](f: Callable[[T], R], pred: Callable[[T], object]|None, it: SupportsIteration[T], /, await_: Literal[False]=...) -> AsyncGeneratorType[R]: ...
@overload
def amapif[T, R](f: Callable[[T], Awaitable[R]], pred: Callable[[T], object]|None, it: SupportsIteration[T], /, await_: Literal[True]) -> AsyncGeneratorType[R]: '''Essentially the restriction of :func:`amultimapif` to one (async) iterable, which allows for more flexibility.'''
@overload
def amultimapif[T, R](f: Callable[[T], R], pred: Callable[[tuple[T]], object], it: SupportsIteration[T], /, *, await_: Literal[False]=...) -> AsyncGeneratorType[R]: ...
@overload
def amultimapif[T, R](f: Callable[[T], Awaitable[R]], pred: Callable[[tuple[T]], object], it: SupportsIteration[T], /, *, await_: Literal[True]) -> AsyncGeneratorType[R]: ...
@overload
def amultimapif[T, V, R](f: Callable[[T, V], R], pred: Callable[[tuple[T, V]], object], i1: SupportsIteration[T], i2: SupportsIteration[V], /, *, await_: Literal[False]=...) -> AsyncGeneratorType[R]: ...
@overload
def amultimapif[T, V, R](f: Callable[[T, V], Awaitable[R]], pred: Callable[[tuple[T, V]], object], i1: SupportsIteration[T], i2: SupportsIteration[V], /, *, await_: Literal[True]) -> AsyncGeneratorType[R]: ...
@overload
def amultimapif[T, V, S, R](f: Callable[[T, V, S], R], pred: Callable[[tuple[T, V, S]], object], i1: SupportsIteration[T], i2: SupportsIteration[V], i3: SupportsIteration[S], /, *, await_: Literal[False]=...) -> AsyncGeneratorType[R]: ...
@overload
def amultimapif[T, V, S, R](f: Callable[[T, V, S], Awaitable[R]], pred: Callable[[tuple[T, V, S]], object], i1: SupportsIteration[T], i2: SupportsIteration[V], i3: SupportsIteration[S], /, *, await_: Literal[True]) -> AsyncGeneratorType[R]: ...
@overload
def amultimapif[T, V, S, U, R](f: Callable[[T, V, S, U], R], pred: Callable[[tuple[T, V, S, U]], object], i1: SupportsIteration[T], i2: SupportsIteration[V], i3: SupportsIteration[S], i4: SupportsIteration[U], /, *, await_: Literal[False]=...) -> AsyncGeneratorType[R]: ...
@overload
def amultimapif[T, V, S, U, R](f: Callable[[T, V, S, U], Awaitable[R]], pred: Callable[[tuple[T, V, S, U]], object], i1: SupportsIteration[T], i2: SupportsIteration[V], i3: SupportsIteration[S], i4: SupportsIteration[U], /, *, await_: Literal[True]) -> AsyncGeneratorType[R]: ...
@overload
def amultimapif[*Ts, R](f: Callable[[*Ts], R], pred: Callable[[tuple[*Ts]], object], /, *its: SupportsIteration[object], await_: Literal[False]=...) -> AsyncGeneratorType[R]: ...
@overload
def amultimapif[*Ts, R](f: Callable[[*Ts], Awaitable[R]], pred: Callable[[tuple[*Ts]], object], /, *its: SupportsIteration[object], await_: Literal[True]) -> AsyncGeneratorType[R]: '''Composition of :func:`astarmap`, :func:`afilter` and :func:`azip`.'''
@overload
def arange(stop: int, /) -> AsyncGeneratorType[int]: ...
@overload
def arange(start: int, stop: int, /) -> AsyncGeneratorType[int]: ...
@overload
def arange(start: int, stop: int, step: int, /) -> AsyncGeneratorType[int]: '''Async version of :class:`range` that is not a class.'''
@overload
def acount(start: int=..., step: int=...) -> AsyncGeneratorType[int]: ...
@overload
def acount(start: float, step: int=...) -> AsyncGeneratorType[float]: ...
@overload
def acount(start: float, step: float) -> AsyncGeneratorType[float]: ...
@overload
def acount(*, step: float) -> AsyncGeneratorType[float]: '''Async version of :func:`itertools.count` that is not a class.'''
def acycle[T](it: SupportsIteration[T]) -> AsyncGeneratorType[T]: '''Async version of :func:`itertools.cycle` that is not a class.'''
def arepeat[T](elem: T, n: int=...) -> AsyncGeneratorType[T]: '''Async version of :func:`itertools.repeat` that is not a class.'''
def aaccumulate[T](it: SupportsIteration[T], func: Callable[[T, T], T]=..., *, initial: T|None=...) -> AsyncGeneratorType[T]: '''Async version of :func:`itertools.accumulate` that is not a class.'''
def acompress[T](data: SupportsIteration[T], selectors: SupportsIteration[object]) -> AsyncGeneratorType[T]: '''Async version of :func:`itertools.compress` that is not a class.'''
def adropwhile[T](pred: Callable[[T], object], it: SupportsIteration[T], *, skip_first: bool=...) -> AsyncGeneratorType[T]:
    '''| Async version of :func:`itertools.dropwhile` that is not a class.
    | If ``skip_first`` is ``True``, drop the first item that fails the predicate as well.
    '''
def afilterfalse[T](f: Callable[[T], object]|None, it: SupportsIteration[T]) -> AsyncGeneratorType[T]: '''Async version of :func:`itertools.filterfalse` that is not a class.'''
async def asattolo[T](it: SupportsIteration[T], /) -> list[T]: '''Return a list representing a random full-length permutation of the items in ``it``.'''
@overload
def agroupby[T](it: SupportsIteration[T], key: Callable[[T], T]=...) -> AsyncGeneratorType[tuple[T, AsyncGeneratorType[T]]]: ...
@overload
def agroupby[T, R](it: SupportsIteration[T], key: Callable[[T], R]) -> AsyncGeneratorType[tuple[R, AsyncGeneratorType[T]]]: '''Async version of :func:`itertools.groupby` that is not a class.'''
@overload
def aislice[T](it: SupportsIteration[T], stop: SupportsIndex|None=..., /) -> AsyncGeneratorType[T]: ...
@overload
def aislice[T](it: SupportsIteration[T], start: SupportsIndex|None, stop: SupportsIndex|None, step: SupportsIndex|None=..., /) -> AsyncGeneratorType[T]: '''Async version of :func:`itertools.islice` that is not a class.'''
def aiter_idx[T](it: SupportsIteration[T], value: T, start: int=..., stop: int|None=...) -> AsyncGeneratorType[int]: '''Yield the indices at which ``value`` occurs in ``it`` within ``start`` and ``stop``.'''
def asieve(n: int) -> AsyncGeneratorType[int]: '''Yield prime numbers strictly smaller than ``n`` in order in an async generator.'''
def apairwise[T](it: SupportsIteration[T]) -> AsyncGeneratorType[tuple[T, T]]: '''Async version of :func:`itertools.pairwise` that is not a class.'''
def atriplewise[T](it: SupportsIteration[T]) -> AsyncGeneratorType[tuple[T, T, T]]: '''Yield overlapping triples of items from an (async) iterable.'''
@overload
def aproduct[T](i1: SupportsIteration[T], /, *, repeat: Literal[1]=...) -> AsyncGeneratorType[tuple[T]]: ...
@overload
def aproduct[T](i1: SupportsIteration[T], /, *, repeat: int) -> AsyncGeneratorType[tuple[T, ...]]: ...
@overload
def aproduct[T, R](i1: SupportsIteration[T], i2: SupportsIteration[R], /, *, repeat: Literal[1]=...) -> AsyncGeneratorType[tuple[T, R]]: ...
@overload
def aproduct[T, R](i1: SupportsIteration[T], i2: SupportsIteration[R], /, *, repeat: int) -> AsyncGeneratorType[tuple[T | R, ...]]: ...
@overload
def aproduct[T, R, V](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], /, *, repeat: Literal[1]=...) -> AsyncGeneratorType[tuple[T, R, V]]: ...
@overload
def aproduct[T, R, V](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], /, *, repeat: int) -> AsyncGeneratorType[tuple[T | R | V, ...]]: ...
@overload
def aproduct[T, R, V, U](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], /, *, repeat: Literal[1]=...) -> AsyncGeneratorType[tuple[T, R, V, U]]: ...
@overload
def aproduct[T, R, V, U](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], /, *, repeat: int) -> AsyncGeneratorType[tuple[T | R | V | U, ...]]: ...
@overload
def aproduct[T, R, V, U, S](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], i5: SupportsIteration[S], /, *, repeat: Literal[1]=...) -> AsyncGeneratorType[tuple[T, R, V, U, S]]: ...
@overload
def aproduct[T, R, V, U, S](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], i5: SupportsIteration[S], /, *, repeat: int) -> AsyncGeneratorType[tuple[T | R | V | U | S, ...]]: ...
@overload
def aproduct(i1: SupportsIteration[object], i2: SupportsIteration[object], i3: SupportsIteration[object], i4: SupportsIteration[object], i5: SupportsIteration[object], /, *its: SupportsIteration[object], repeat: int=...) -> AsyncGeneratorType[tuple[Any, ...]]: ...
@overload
def aproduct[T](*its: SupportsIteration[T], repeat: int=...) -> AsyncGeneratorType[tuple[T, ...]]: '''Async version of :func:`itertools.product` that is not a class.'''
@overload
def astarmap[*Ts, R](f: Callable[[*Ts], R], it: SupportsIteration[tuple[*Ts]], /, await_: Literal[False]=...) -> AsyncGeneratorType[R]: ...
@overload
def astarmap[*Ts, R](f: Callable[[*Ts], Awaitable[R]], it: SupportsIteration[tuple[*Ts]], /, await_: Literal[True]) -> AsyncGeneratorType[R]: '''Async version of :func:`itertools.starmap` that is not a class. ``await_`` specifies whether to await the return value of the transformation function.'''
def atakewhile[T](pred: Callable[[T], object]|None, it: SupportsIteration[T]) -> AsyncGeneratorType[T]: '''Async version of :func:`itertools.takewhile` that is not a class.'''
def atakeuntil[T](pred: Callable[[T], object]|None, it: SupportsIteration[T]) -> AsyncGeneratorType[T]: '''Take items from the iterable while the predicate called on the item does not hold.'''
def atakewhile_inclusive[T](pred: Callable[[T], object]|None, it: SupportsIteration[T]) -> AsyncGeneratorType[T]: ''':func:`atakewhile`, but yielding the first falsy item last.'''
def atakeuntil_inclusive[T](pred: Callable[[T], object]|None, it: SupportsIteration[T]) -> AsyncGeneratorType[T]: ''':func:`atakeuntil`, but yielding the first truthy item last.'''
def ac3merge[T](seqs: SupportsIteration[MutableSequence[T]]) -> AsyncGeneratorType[T]: '''Async version of ``functools._c3_merge`` that doesn't assume the input is an synchronous iterable of mutable sequences of classes.'''
async def asquaresum[T: (int, float, complex)](it: SupportsIteration[T]) -> T: '''Return the sum of squares of items in an (async) iterable of numbers as a number of the same type.'''
@overload
def aziplongest[T](i1: SupportsIteration[T], /) -> AsyncGeneratorType[tuple[T]]: ...
@overload
def aziplongest[T, R](i1: SupportsIteration[T], i2: SupportsIteration[R], /, *, fillvalue: object=...) -> AsyncGeneratorType[tuple[T, R]]: ...
@overload
def aziplongest[T, R, V](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], /, *, fillvalue: object=...) -> AsyncGeneratorType[tuple[T, R, V]]: ...
@overload
def aziplongest[T, R, V, U](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], /, *, fillvalue: object=...) -> AsyncGeneratorType[tuple[T, R, V, U]]: ...
@overload
def aziplongest[T, R, V, U, S](i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], i5: SupportsIteration[S], /, *, fillvalue: object=...) -> AsyncGeneratorType[tuple[T, R, V, U, S]]: ...
@overload
def aziplongest[T](*its: SupportsIteration[T], fillvalue: T=...) -> AsyncGeneratorType[tuple[T, ...]]: '''Async version of :func:`itertools.zip_longest` that is not a class. The first overload does not accept ``fillvalue``, because passing it with only one iterable does not make sense.'''
async def asumprod[T: (int, float, complex)](p: SupportsIteration[T], q: SupportsIteration[T], /) -> T: '''Return the sum of products of items in two iterables of numbers as a number of the same type. Not as precise as :func:`math.sumprod` for floating-point numbers, but supports async iterables.'''
def aconvolve[T: (int, float, complex)](signal: SupportsIteration[T], kernel: SupportsIteration[T]) -> AsyncGeneratorType[T]: '''Polynomial multiplication with coefficients from the two iterables. The first iterable is advanced on demand, meaning it may be infinite, but the second iterable is exhausted immediately, storing all its items in memory.'''
@overload
def atabulate[T](f: Callable[[int], T], start: int=..., step: int=..., /, *, await_: Literal[False]=...) -> AsyncGeneratorType[T]: ...
@overload
def atabulate[T](f: Callable[[int], Awaitable[T]], start: int=..., step: int=..., /, *, await_: Literal[True]) -> AsyncGeneratorType[T]: '''Composition of :func:`amap` and :func:`acount`.'''
async def asum[T: (int, float, complex)](it: SupportsIteration[T], start: T=...) -> T: '''Return the sum of the items in the (async) iterable, preceded by ``start`` if passed.'''
async def aprod[T: (int, float, complex)](it: SupportsIteration[T], start: T=...) -> T: '''Return the product of the items in the (async) iterable, preceded by ``start`` if passed.'''
async def amatprod[T: SupportsMatMul](it: SupportsIteration[T], start: T) -> T: '''Return the product of the matrices in the (async) iterable, preceded by ``start`` if passed.'''
def acountdown(n: int, step: int=..., *, include_zero: bool=...) -> AsyncGeneratorType[int]: '''Count down from ``n`` to zero, excluding zero if it is to appear and ``include_zero`` is ``False`` (the default), by a step size of ``step``.'''
def atail[T](n: int, it: SupportsIteration[T], /) -> AsyncGeneratorType[T]: '''Yield the last ``n`` items from the (async) iterable ``it``.'''
def abfs[T: Hashable](start: T, neighbours: Callable[[T], SupportsIteration[T]], *, include_start: bool=...) -> AsyncGeneratorType[T]: '''Breadth-first search on a start node ``start``, given a function ``neighbours`` that returns an (async) iterable of neighbours to be traversed in order. If ``include_start`` is ``True``, the start node is yielded first.'''
def adfs[T: Hashable](start: T, neighbours: Callable[[T], SupportsIteration[T]], *, include_start: bool=...) -> AsyncGeneratorType[T]: '''Depth-first search on a start node ``start``, given a function ``neighbours`` that returns an (async) iterable of neighbours to be traversed in order. If ``include_start`` is ``True``, the start node is yielded first.'''
async def abrent[T](next_node: Callable[[T], Awaitable[T]], start: T, /) -> tuple[T, int, int]:
    '''| Brent's algorithm for cycle detection, assuming that a cycle is indeed present, given a function ``next_node`` returning the next node from the previous.
    | Return a tuple ``(node, la, mu)``, where ``node`` is the first node involved in a cycle, ``mu`` its index (the least number of times ``next_node`` was applied to get ``node``), and ``la`` the cycle length.

    .. note:: ``next_node`` should be deterministic. Also, if there is no cycle, the algorithm hangs indefinitely.
    '''
async def ahamming_dist[T](a: SupportsIteration[T], b: SupportsIteration[T], /, cmpeq: Callable[[T, T], object]=...) -> int: '''Return the Hamming distance between two (async) iterables, using ``cmpeq`` to check for equality if passed.'''
@overload
def amerge_sorted_by[T: SupportsRichComparison](its: SupportsIteration[SupportsIteration[T]], *, key: Callable[[T], T]=..., await_: Literal[False]=..., reverse: bool=...) -> AsyncGeneratorType[T]: ...
@overload
def amerge_sorted_by[T](its: SupportsIteration[SupportsIteration[T]], *, key: Callable[[T], SupportsRichComparison], await_: Literal[False]=..., reverse: bool=...) -> AsyncGeneratorType[T]: ...
@overload
def amerge_sorted_by[T](its: SupportsIteration[SupportsIteration[T]], *, key: Callable[[T], Awaitable[SupportsRichComparison]], await_: Literal[True], reverse: bool=...) -> AsyncGeneratorType[T]: '''Async version of :func:`heapq.merge`.'''
@overload
def amultifilter[T](pred: Callable[[tuple[T]], object], it: SupportsIteration[T], /, *, strict: bool=...) -> AsyncGeneratorType[tuple[T]]: ...
@overload
def amultifilter[T, R](pred: Callable[[tuple[T, R]], object], i1: SupportsIteration[T], i2: SupportsIteration[R], /, *, strict: bool=...) -> AsyncGeneratorType[tuple[T, R]]: ...
@overload
def amultifilter[T, R, V](pred: Callable[[tuple[T, R, V]], object], i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], /, *, strict: bool=...) -> AsyncGeneratorType[tuple[T, R, V]]: ...
@overload
def amultifilter[T, R, V, U](pred: Callable[[tuple[T, R, V, U]], object], i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], /, *, strict: bool=...) -> AsyncGeneratorType[tuple[T, R, V, U]]: ...
@overload
def amultifilter[T, R, V, U, S](pred: Callable[[tuple[T, R, V, U, S]], object], i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], i5: SupportsIteration[S], /, *, strict: bool=...) -> AsyncGeneratorType[tuple[T, R, V, U, S]]: ...
@overload
def amultifilter[T](pred: Callable[[tuple[T, ...]], object], /, *its: SupportsIteration[T], strict: bool=...) -> AsyncGeneratorType[tuple[T, ...]]: ...
@overload
def amultifilter(pred: Callable[[tuple[Any, ...]], object], i1: SupportsIteration[object], i2: SupportsIteration[object], i3: SupportsIteration[object], i4: SupportsIteration[object], i5: SupportsIteration[object], /, *its: SupportsIteration[object], strict: bool=...) -> AsyncGeneratorType[tuple[Any, ...]]: '''Composition of :func:`afilter` and :func:`azip`.'''
@overload
def amultifilterfalse[T](pred: Callable[[tuple[T]], object], it: SupportsIteration[T], /, *, strict: bool=...) -> AsyncGeneratorType[tuple[T]]: ...
@overload
def amultifilterfalse[T, R](pred: Callable[[tuple[T, R]], object], i1: SupportsIteration[T], i2: SupportsIteration[R], /, *, strict: bool=...) -> AsyncGeneratorType[tuple[T, R]]: ...
@overload
def amultifilterfalse[T, R, V](pred: Callable[[tuple[T, R, V]], object], i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], /, *, strict: bool=...) -> AsyncGeneratorType[tuple[T, R, V]]: ...
@overload
def amultifilterfalse[T, R, V, U](pred: Callable[[tuple[T, R, V, U]], object], i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], /, *, strict: bool=...) -> AsyncGeneratorType[tuple[T, R, V, U]]: ...
@overload
def amultifilterfalse[T, R, V, U, S](pred: Callable[[tuple[T, R, V, U, S]], object], i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], i5: SupportsIteration[S], /, *, strict: bool=...) -> AsyncGeneratorType[tuple[T, R, V, U, S]]: ...
@overload
def amultifilterfalse[T](pred: Callable[[tuple[T, ...]], object], /, *its: SupportsIteration[T], strict: bool=...) -> AsyncGeneratorType[tuple[T, ...]]: ...
@overload
def amultifilterfalse(pred: Callable[[tuple[Any, ...]], object], i1: SupportsIteration[object], i2: SupportsIteration[object], i3: SupportsIteration[object], i4: SupportsIteration[object], i5: SupportsIteration[object], /, *its: SupportsIteration[object], strict: bool=...) -> AsyncGeneratorType[tuple[Any, ...]]: '''Composition of :func:`afilterfalse` and :func:`azip`.'''
@overload
def amultistarfilter[T](pred: Callable[[T], object], it: SupportsIteration[T], /, *, strict: bool=...) -> AsyncGeneratorType[tuple[T]]: ...
@overload
def amultistarfilter[T, R](pred: Callable[[T, R], object], i1: SupportsIteration[T], i2: SupportsIteration[R], /, *, strict: bool=...) -> AsyncGeneratorType[tuple[T, R]]: ...
@overload
def amultistarfilter[T, R, V](pred: Callable[[T, R, V], object], i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], /, *, strict: bool=...) -> AsyncGeneratorType[tuple[T, R, V]]: ...
@overload
def amultistarfilter[T, R, V, U](pred: Callable[[T, R, V, U], object], i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], /, *, strict: bool=...) -> AsyncGeneratorType[tuple[T, R, V, U]]: ...
@overload
def amultistarfilter[T, R, V, U, S](pred: Callable[[T, R, V, U, S], object], i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], i5: SupportsIteration[S], /, *, strict: bool=...) -> AsyncGeneratorType[tuple[T, R, V, U, S]]: ...
@overload
def amultistarfilter[T](pred: Callable[[*tuple[T, ...]], object], /, *its: SupportsIteration[T], strict: bool=...) -> AsyncGeneratorType[tuple[T, ...]]: ...
@overload
def amultistarfilter(pred: Callable[[*tuple[Any, ...]], object], i1: SupportsIteration[object], i2: SupportsIteration[object], i3: SupportsIteration[object], i4: SupportsIteration[object], i5: SupportsIteration[object], /, *its: SupportsIteration[object], strict: bool=...) -> AsyncGeneratorType[tuple[Any, ...]]: '''Composition of :func:`astarfilter` and :func:`azip`.'''
@overload
def amultistarfilterfalse[T](pred: Callable[[T], object], it: SupportsIteration[T], /, *, strict: bool=...) -> AsyncGeneratorType[tuple[T]]: ...
@overload
def amultistarfilterfalse[T, R](pred: Callable[[T, R], object], i1: SupportsIteration[T], i2: SupportsIteration[R], /, *, strict: bool=...) -> AsyncGeneratorType[tuple[T, R]]: ...
@overload
def amultistarfilterfalse[T, R, V](pred: Callable[[T, R, V], object], i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], /, *, strict: bool=...) -> AsyncGeneratorType[tuple[T, R, V]]: ...
@overload
def amultistarfilterfalse[T, R, V, U](pred: Callable[[T, R, V, U], object], i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], /, *, strict: bool=...) -> AsyncGeneratorType[tuple[T, R, V, U]]: ...
@overload
def amultistarfilterfalse[T, R, V, U, S](pred: Callable[[T, R, V, U, S], object], i1: SupportsIteration[T], i2: SupportsIteration[R], i3: SupportsIteration[V], i4: SupportsIteration[U], i5: SupportsIteration[S], /, *, strict: bool=...) -> AsyncGeneratorType[tuple[T, R, V, U, S]]: ...
@overload
def amultistarfilterfalse[T](pred: Callable[[*tuple[T, ...]], object], /, *its: SupportsIteration[T], strict: bool=...) -> AsyncGeneratorType[tuple[T, ...]]: ...
@overload
def amultistarfilterfalse(pred: Callable[[*tuple[Any, ...]], object], i1: SupportsIteration[object], i2: SupportsIteration[object], i3: SupportsIteration[object], i4: SupportsIteration[object], i5: SupportsIteration[object], /, *its: SupportsIteration[object], strict: bool=...) -> AsyncGeneratorType[tuple[Any, ...]]: '''Composition of :func:`astarfilterfalse` and :func:`azip`.'''
async def asample_weighted[T](it: SupportsIteration[tuple[T, float]], k: int, *, rrange: Callable[[int], int]=..., rand: Callable[[], float]=...) -> list[T]: '''Choose ``k`` items from an (async) iterable of ``(item, weight)`` pairs, where the probability of each item being chosen is proportional to its weight. ``rrange`` and ``rand`` should be the :func:`~random.randrange` and :func:`~random.random` methods of a random device respectively. This is the A-Chao with Jumps reservoir sampling algorithm.'''
async def asamplel[T](it: SupportsIteration[T], k: int, *, rrange: Callable[[int], int]=..., rand: Callable[[], float]=...) -> list[T]: '''Chooses ``k`` items from an (async) iterable of items, where each item is chosen with equal probability. ``rrange`` and ``rand`` should be the :func:`~random.randrange` and :func:`~random.random` methods of a random device respectively. This is Algorithm L.'''
def astarfilter[T](pred: Callable[[*tuple[T, ...]], object], it: SupportsIteration[SupportsIteration[T]]) -> AsyncGeneratorType[tuple[T, ...]]: '''Filter an (async) iterable of tuples of items, yielding only those tuples for which the predicate returns a truthy value when called on the tuple unpacked.'''
def astarfilterfalse[T](pred: Callable[[*tuple[T, ...]], object], it: SupportsIteration[SupportsIteration[T]]) -> AsyncGeneratorType[tuple[T, ...]]: '''Filter an (async) iterable of tuples of items, yielding only those tuples for which the predicate returns a falsy value when called on the tuple unpacked.'''
async def to_tuple[T](it: SupportsIteration[T], /) -> tuple[T, ...]: '''Convert the output of :func:`to_list` into a tuple.'''
@overload
async def to_set[T: Hashable](it: SupportsIteration[T], /, frozen: Literal[False]=...) -> set[T]: ...
@overload
async def to_set[T: Hashable](it: SupportsIteration[T], /, frozen: Literal[True]) -> frozenset[T]: '''Convert the output of :func:`to_list` into a set or frozenset depending on the ``frozen`` parameter (``False`` by default).'''
async def aconsume[T](it: SupportsIteration[T], n: int|None=...) -> None: '''Advance the (async) iterable ``it`` by ``n`` steps, using a function-scoped executor created on demand where appropriate. If you want the item at the final position, use :func:`anth` instead.'''
async def anth[T](it: SupportsIteration[T], n: int, default: T=...) -> T: '''Return the ``n``-th item of the (async) iterable ``it``, or ``default`` if passed and there is no such item.'''
async def aallequal[T](it: SupportsIteration[T], key: Callable[[T], object]=..., strict: bool=...) -> bool: '''Whether all items in the (async) iterable are equal to each other according to the ``key`` function. Check for identity rather than equality if ``strict`` is ``True``.'''
def acombinations[T](it: SupportsIteration[T], r: int) -> AsyncGeneratorType[tuple[T, ...]]: '''Async version of :func:`itertools.combinations` that is not a class.'''
def acombinations_with_replacement[T](it: SupportsIteration[T], r: int) -> AsyncGeneratorType[tuple[T, ...]]: '''Async version of :func:`itertools.combinations_with_replacement` that is not a class.'''
def apermutations[T](it: SupportsIteration[T], r: int|None=...) -> AsyncGeneratorType[tuple[T, ...]]: '''Async version of :func:`itertools.permutations` that is not a class.'''
def apowerset[T](it: SupportsIteration[T]) -> AsyncGeneratorType[tuple[T, ...]]: '''Yield all the subsets of the (async) iterable ``it`` (by index!) as tuples, starting with the empty tuple.'''
async def aquantify[T](it: SupportsIteration[T], pred: Callable[[T], object]=...) -> int: '''Return the number of items in the (async) iterable for which the predicate is true.'''
def apadded[T](it: SupportsIteration[T], fillvalue: T, n: int|None=...) -> AsyncGeneratorType[T]: '''Yield the items in the (async) iterable ``it``, followed by ``fillvalue`` repeatedly, such that the iterable is fully consumed and the result has length at least ``n`` if passed.'''
def apadnone[T](it: SupportsIteration[T], n: int|None=...) -> AsyncGeneratorType[T|None]: '''Yield the items in the (async) iterable ``it``, followed by ``None`` repeatedly, such that the iterable is fully consumed and the result has length at least ``n`` if passed.'''
def agrouper[T](it: SupportsIteration[T], n: int, fillvalue: T|RaiseType=...) -> AsyncGeneratorType[tuple[T | None, ...]]:
    '''| Collect items of the (async) iterable ``it`` into tuples of length ``n`` each.
    | If ``fillvalue`` is :const:`~asyncutils.constants.RAISE`, raise :exc:`ValueError` if the last group is not of length ``n``.
    | Otherwise, pad the last group with ``fillvalue`` to length ``n`` if needed. No padding is done if not passed.
    '''
def aroundrobin[T](*its: SupportsIteration[T]) -> AsyncGeneratorType[T]: '''Yield items from the given (async) iterables in round-robin order, skipping exhausted iterables. Prefer over :func:`aroundrobin2` for less iterables.'''
def aroundrobin2[T](*its: SupportsIteration[T]) -> AsyncGeneratorType[T]: '''Yield items from the given (async) iterables in round-robin order, skipping exhausted iterables. Prefer over :func:`aroundrobin` for more iterables.'''
def aunique_everseen[T](it: SupportsIteration[T], key: Callable[[T], object]=...) -> AsyncGeneratorType[T]: '''Yield items from the (async) iterable ``it``, without yielding items already previously yielded.'''
def aunique_justseen[T](it: SupportsIteration[T], key: Callable[[T], object]=...) -> AsyncGeneratorType[T]: '''Yield items from the (async) iterable ``it``, without yielding consecutive duplicate items.'''
def aunique[T](it: SupportsIteration[T], key: Callable[[T], SupportsRichComparison]|None=..., reverse: bool=...) -> AsyncGeneratorType[T]: '''Yield unique elements from ``it`` in sorted order, according to ``key``, which should not be too expensive. If ``reverse`` is ``True``, yield in descending order.'''
def ancycles[T](it: SupportsIteration[T], n: int) -> AsyncGeneratorType[T]: '''Yield the items in the (async) iterable ``it`` over and over for a total of ``n`` cycles.'''
def apartition[T](pred: Callable[[T], object]|None, it: SupportsIteration[T]) -> tuple[AsyncGeneratorType[T], AsyncGeneratorType[T]]: '''Return a tuple ``(fgen, tgen)``. ``tgen`` is an async generator yielding the items in ``it`` passing the predicate, and ``fgen`` the others.'''
def aiterexcept[T](f: Callable[[], Awaitable[T]], exc: Exceptable, first: Callable[[], Awaitable[T]]=...) -> AsyncGeneratorType[T]: '''Yield the awaited output of ``first``, then ``f`` called with no arguments repeatedly until an exception present in ``exc`` occurs.'''
async def ailen(it: SupportsIteration[object]) -> int: '''Return the length of the (async) iterable ``it``, consuming it entirely.'''
def aiterate[T](f: Callable[[T], Awaitable[T]], start: T) -> AsyncGeneratorType[T]: '''Yield ``start``, then the awaited output of ``f`` called on the previous output repeatedly.'''
@overload
def asorted[T: SupportsRichComparison](it: SupportsIteration[T], *, reverse: bool=...) -> list[T]: ...
@overload
def asorted[T](it: SupportsIteration[T], *, key: Callable[[T], SupportsRichComparison], reverse: bool=...) -> list[T]: '''Async version of :func:`sorted`. O(n log n) time and O(n) space, but nowhere near as optimized as the builtin version.'''
def acanonical[T](it: SupportsIteration[T]) -> list[T]: '''Return a canonicalized ordering of the items in ``it``, which may change across different Python invocations or sessions.'''
def adistinct_permutations[T](it: SupportsIteration[T], r: int|None=...) -> AsyncGeneratorType[tuple[T, ...]]: '''Successive distinct permutations of the elements in ``it`` of size ``r``, or all sizes if not passed.'''
async def aisempty(it: SupportsIteration[object]) -> bool:
    '''Return whether the (async) iterable ``it`` is empty.

    .. note::
      This advances the iterable on success and discards the item.
      If the item is needed, call :func:`afirst` instead and catch :exc:`StopAsyncIteration` or pass a default value.
    '''
def aunique_to_each[T: Hashable](*its: SupportsIteration[T]) -> AsyncGeneratorType[T]: '''Given multiple (async) iterables, yield every item that is only seen in exactly one of the iterables.'''
def aderangements[T](it: SupportsIteration[T], r: int|None=...) -> AsyncGeneratorType[T]: '''Successive derangements of the elements in ``it`` of size ``r``, or all sizes if not passed. Derangements are permutations with no fixed points.'''
def aintersperse[T](e: T, it: SupportsIteration[T], n: int=...) -> AsyncGeneratorType[T]: '''Yield ``e``, then the next ``n`` items in ``it``, and repeat until ``it`` is exhausted.'''
def ainterleave_stopearly[T](*it: SupportsIteration[T]) -> AsyncGeneratorType[T]: '''Yield the items from the iterables in a round-robin fashion until at least one is exhausted.'''
def aspy[T](it: SupportsIteration[T], n: int=...) -> tuple[AsyncGeneratorType[T], AsyncGeneratorType[T]]: '''Return an async generator containing the first ``n`` items, and another containing all the original items.'''
def ainterleave_evenly[T](its: SupportsIteration[SupportsIteration[T]], lengths: SupportsIteration[int]|None=...) -> AsyncGeneratorType[T]: '''Interleave items of the iterables evenly according to the lengths if passed, and determined by calling the :meth:`~object.__len__` method on the iterables if present otherwise.'''
def ainterleave_randomly[T](its: SupportsIteration[SupportsIteration[T]]) -> AsyncGeneratorType[T]: '''Interleave items of the iterables randomly, skipping exhausted iterables.'''
def acollapse(it: SupportsIteration[object], base_typ: tuple[type, ...]|type=..., levels: int|None=...) -> AsyncGeneratorType[Any]: '''Flatten the (async) iterable ``it`` by at most ``levels`` levels, without collapsing objects of types specified in ``base_typ``.'''
async def afirsttrue[T](it: SupportsIteration[T], default: T|None=..., pred: Callable[[T], object]=...) -> T: '''Return the first item in the (async) iterable ``it`` that satisfies the predicate, or ``default`` if passed and there is no such item, and raise :exc:`StopAsyncIteration` otherwise.'''
async def afirstfalse[T](it: SupportsIteration[T], default: T|None=..., pred: Callable[[T], object]=...) -> T: '''Return the first item in the (async) iterable ``it`` that fails the predicate, or ``default`` if passed and there is no such item, and raise :exc:`StopAsyncIteration` otherwise.'''
def aappend[T](val: T, it: SupportsIteration[T]) -> AsyncGeneratorType[T]: '''Append ``val`` to the (async) iterable ``it``.'''
def aprepend[T](val: T, it: SupportsIteration[T]) -> AsyncGeneratorType[T]: '''Prepend ``val`` to the (async) iterable ``it``.'''
def awrap[T](it: SupportsIteration[T], start: T, end: T) -> AsyncGeneratorType[T]: '''Wrap the (async) iterable ``it`` by yielding ``start`` first, then the items in ``it``, then ``end``.'''
def arandom_product[T](*its: SupportsIteration[T], n: int=...) -> AsyncGeneratorType[T]: '''Draw ``n`` items from each of the input iterables ``its`` at random.'''
def arandom_combination[T](it: SupportsIteration[T], r: int) -> AsyncGeneratorType[T]: '''Draw ``r`` items at random from the input iterable ``it``, without replacement.'''
def arandom_combination_with_replacement[T](it: SupportsIteration[T], r: int) -> AsyncGeneratorType[T]: '''Draw ``r`` items at random from the input iterable ``it``, with replacement.'''
def arandom_permutation[T](it: SupportsIteration[T], r: int|None=...) -> AsyncGeneratorType[T]: '''Choose a random permutation of the elements in ``it`` of size ``r``, or all sizes if not passed.'''
async def afirst[T](it: SupportsIteration[T], default: T=...) -> T: '''Return the first item in the (async) iterable ``it``, or ``default`` if passed and ``it`` is empty.'''
async def alast[T](it: SupportsIteration[T], default: T=...) -> T: '''Return the last item in the (async) iterable ``it``, or ``default`` if passed and ``it`` is empty.'''
async def anth_or_last[T](it: SupportsIteration[T], n: int, default: T=...) -> T: '''Return the ``n``-th item in the (async) iterable ``it``, or the last item if out of bounds, or ``default`` if passed and ``it`` is empty.'''
def abefore_and_after[T](pred: Callable[[T], object], it: SupportsIteration[T]) -> tuple[AsyncGeneratorType[T], AsyncGeneratorType[T]]: ''':func:`atakewhile`, but return all remaining items in the second async generator (after the first is consumed).'''
def anth_combination[T](it: SupportsIteration[T], r: int, idx: int) -> AsyncGeneratorType[T]: '''Return the ``idx``-th combination of ``r`` elements from the input iterable ``it``, in lexicographic order.'''
def asubslices[T](it: SupportsIteration[T]) -> AsyncGeneratorType[tuple[T, ...]]: ''':func:`asubstrings`, but yield all subslices containing the first item first in ascending order of length, then all subslices containing the second item but not the first, and so on.'''
def arepeat_func[T, *Ts](f: Callable[[*Ts], Awaitable[T]], times: int|None=..., *a: *Ts) -> AsyncGeneratorType[T]: '''Call the async function ``f`` with arguments ``a`` repeatedly for ``times`` times, or indefinitely if ``times`` is not passed, and yield the results awaited.'''
def apolynomial_from_roots[T: (int, float, complex)](roots: SupportsIteration[T]) -> AsyncGeneratorType[T]: '''Generate the coefficients of a polynomial given its roots in order of descending powers.'''
def atranspose[T](mat: SupportsIteration[SupportsIteration[T]]) -> AsyncGeneratorType[tuple[T, ...]]: '''Compute the transpose of a matrix.'''
def aflatten_tensor(tensor: SupportsIteration[object], base_typ: tuple[type, ...]|type=...) -> AsyncGeneratorType[Any]: ''':func:`acollapse`, but using a different, more memory-efficient strategy that does not support the ``levels`` parameter.'''
def apolynomial_derivative[T: (int, float, complex)](coeff: SupportsIteration[T]) -> AsyncGeneratorType[T]: '''Compute the coefficients of the derivative of a polynomial. Both input and output iterables are in order of descending powers.'''
async def apolynomial_eval[T: (int, float, complex)](coeff: SupportsIteration[T], x: T) -> T: '''Evaluate a polynomial at ``x`` given its coefficients in order of descending powers.'''
@overload
def areshape[T](mat: SupportsIteration[SupportsIteration[T]], shape: int) -> AsyncGeneratorType[list[T]]: ...
@overload
def areshape(mat: SupportsIteration[object], shape: SupportsIteration[int]) -> AsyncGeneratorType[list[Any]]: '''Change the shape of a tensor according to ``shape``. For an integer ``shape``, the matrix must be 2D and ``shape`` is the number of output columns.'''
def afactor(n: int) -> AsyncGeneratorType[int]: '''Generate the prime factors of ``n`` asynchronously. Do not rely on the resultant order.'''
def arunning_median[N: (int, float)](it: SupportsIteration[N], *, maxlen: SupportsIndex|None=...) -> AsyncGeneratorType[N]: '''Yield the median of all the items seen from ``it`` within a window of size ``maxlen``, then advance it.'''
async def arandom_derangement[T](it: SupportsIteration[T]) -> tuple[T, ...]: '''Generate a random derangement of items in the (async) iterable ``it``.'''
def amatmul[T: (int, float, complex)](M: SupportsIteration[SupportsIteration[T]], N: SupportsIteration[SupportsIteration[T]]) -> AsyncGeneratorType[tuple[T, ...]]: '''Matrix multiplication of ``M`` and ``N``. O(n^3) time, since this library does not specialize in these operations.'''
def mat_vec_mul(M: SupportsIteration[SupportsIteration[int]], V: SupportsIteration[int]) -> AsyncGeneratorType[int]: '''Multiplication of a matrix ``M`` and a vector ``V``. O(n^2).'''
async def vecs_eq[T](u: SupportsIteration[T], v: SupportsIteration[T], cmpeq: Callable[[T, T], object]=..., *, strict: bool=...) -> bool: '''Whether the vectors ``u`` and ``v`` are equal according to ``cmpeq`` called on each pair of items from iterating through them in parallel. If ``strict`` is ``False`` (default ``True``), may return ``True`` even for differently-sized vectors.'''
async def afreivalds(A: SupportsIteration[SupportsIteration[int]], B: SupportsIteration[SupportsIteration[int]], C: SupportsIteration[SupportsIteration[int]], k: int=...) -> bool: '''Determine if the matrix product of ``A`` and ``B`` equals ``C``. This is the probabilistic Freivalds algorithm. O(kn^2) time, with a false positive rate of at most 2^(-k) and no false negatives.'''
async def basic_collect[T](it: SupportsIteration[T], n: int) -> list[T]: '''Return a list of the first ``n`` items in the (async) iterable ``it``, signalling no error if there are not enough items.'''
def asubstrings[T](it: SupportsIteration[T]) -> AsyncGeneratorType[tuple[T, ...]]: '''Yield all the contiguous subsequences of the (async) iterable ``it`` as tuples, in increasing order of length.'''
@overload
def asubstr_indices[S: (str, bytes, bytearray)](seq: S, reverse: bool=...) -> AsyncGeneratorType[tuple[S, int, int]]: ...
@overload
def asubstr_indices[T](seq: SupportsSlicing[T], reverse: bool=...) -> AsyncGeneratorType[tuple[Iterable[T], int, int]]: '''Yield tuples of the form ``(substr, start, end)``, where ``substr`` is a contiguous subsequence of ``seq`` starting at index ``start`` and ending at index ``end-1`` (such that its length is ``end-start``).'''
def iter_task[T: SupportsIteration[object]](it: T, summaryf: Callable[[T], Awaitable[Any]]=...) -> Task[float]: '''Return a task that calls ``summaryf`` on the passed (async) iterable and returns the time taken to run it. By default, ``summaryf`` consumes ``it`` fully.'''
def agetitems_from_indices[T](it: SupportsIteration[T], indices: SupportsIteration[SupportsIndex], setatend: Future[float]|None=..., finish: bool=...) -> list[Future[T]]:
    '''| Take an (async) iterable and an (async) iterable of integers interpreted as indices, and immediately returns a list of futures.
    | Their eventual results represent the items of that iterable at the corresponding index.
    | Also begin consumption of the iterable in the background.
    | Exceptions will be set in the futures that are not done if results are encountered during iteration or if the index is out of bounds.
    | Pass in a :class:`~asyncio.Future` for the ``setatend`` parameter, which cancels the background consumption of the async iterable once it is done and cancels the undone futures.

    .. attention:: Negative indices would consume the whole iterable at once if not already consumed.
    .. warning:: Do not set the result of any returned future; instead, if the result is no longer relevant, cancel the future.
    .. note:: The consumption stops as soon as all the required results are pushed into the respective futures.
    '''
def aintersend[T, R](i1: AsyncGenerator[T, R], i2: AsyncGenerator[R, T]) -> AsyncGeneratorType[tuple[T, R]]: '''Feed ``i1`` and ``i2`` into each other and yield tuples of the form ``(yielded_from_i1, yielded_from_i2)``.'''
def asendstream[T, R](i1: AsyncGenerator[T, R], i2: SupportsIteration[R]) -> AsyncGeneratorType[T]: '''Feed ``i2`` into ``i1`` and yield the results.'''
@overload
def acat[T](first: T) -> AsyncGeneratorType[T, T]: ...
@overload
def acat[T](first: None=...) -> AsyncGeneratorType[T|None, T|None]: '''Yield the sent value, starting with ``first`` (default ``None``).'''
def aforever() -> AsyncGeneratorType[None]: '''Yield ``None`` forever. Equivalent to ``arepeat(None)``.'''
def aloops(n: int) -> AsyncGeneratorType[None]: '''Yield ``None`` ``n`` times. Equivalent to ``base.take(aforever(), n)`` and ``arepeat(None, n)``, but without creating intermediate integers.'''
async def aguessmax[T](it: SupportsIteration[T], estlen: int, *, key: Callable[[T], SupportsRichComparison]=..., default: T=..., finish_event: EventProtocol|None=...) -> T: '''Optimal solution to the secretary problem, using ``key`` to guess the maximum item, which is the candidate chosen, with 36.8% accuracy, by finding the maximum among the first 36.8% of the (async) iterable and then returning the first item greater than that afterwards, in O(1) space. `This video <https://www.youtube.com/watch?v=XIOoCKO-ybQ>`__ proves that the approach used is best.'''
async def aguessmin[T](it: SupportsIteration[T], estlen: int, *, key: Callable[[T], SupportsRichComparison]=..., default: T=..., finish_event: EventProtocol|None=...) -> T: '''Like :func:`aguessmax`, but guesses the minimum item instead.'''
def apowers_of_two(*, init: int=..., init_shift: int=..., shift: int=...) -> AsyncGeneratorType[int]: '''Optimized version of :func:`apowers` using bit shift operations for powers of two, four, eight, etc. Yield ``init<<init_shift``, ``init<<init_shift+shift``, ``init<<init_shift+2*shift``, ...'''
def areversed[T](it: SupportsIteration[T]|Reversible[T], /) -> AsyncGeneratorType[T]: '''Reverse an (async) iterable, calling its :meth:`~object.__reversed__` method if present, falling back to consuming all the items and yielding them in reverse order.'''
async def to_list[T](it: SupportsIteration[T], /) -> list[T]: '''Collect all items of an async iterable into a list. Faster than :func:`~asyncutils.base.collect`.'''
async def aisprime(n: int) -> bool: '''Probabilistically test for primality of ``n``. O(log^3 n), with false-positive rate below 2^(-128) for integers above 10^24.'''
def adft(xarr: SupportsIteration[complex], /) -> AsyncGeneratorType[complex]: '''The discrete Fourier transform. O(n^2), since this library does not specialize in these operations.''' # noqa: D401
def aidft(Xarr: SupportsIteration[complex], /) -> AsyncGeneratorType[complex]: '''The inverse discrete Fourier transform. O(n^2) just like :func:`adft`.''' # noqa: D401
def apowers[T: (int, float, complex)](base: T, start: T=...) -> AsyncGeneratorType[T]:
    '''Yield ``start``, ``start*base``, ``start*base*base``, ...

    .. note:: When it is found that the base is a perfect power of two, this will delegate to :func:`apowers_of_two` as an optimization.
    '''
def arunlength_encode[T](it: SupportsIteration[T], /) -> AsyncGeneratorType[tuple[T, int]]: '''Compress an (async) iterable into an async generator of pairs with run-length encoding. Items in the result are in the form ``(item, count)``, where ``item`` is an item from the input iterable and ``count`` is the number of times it is repeated consecutively.'''
def arunlength_decode[T](it: SupportsIteration[tuple[T, int]], /) -> AsyncGeneratorType[T]: '''Inverse of the above.'''
@overload
async def aargmin[T](it: SupportsIteration[T], key: Callable[[T], SupportsRichComparison], default: int=...) -> int: ...
@overload
async def aargmin[T: SupportsRichComparison](it: SupportsIteration[T], *, default: int=...) -> int: '''Return the index of the first occurrence of the minimum element in the (async) iterable ``it`` according to ``key``, or ``default`` if empty.'''
@overload
async def aargmax[T](it: SupportsIteration[T], key: Callable[[T], SupportsRichComparison], default: int=...) -> int: ...
@overload
async def aargmax[T: SupportsRichComparison](it: SupportsIteration[T], *, default: int=...) -> int: '''Return the index of the first occurrence of the maximum element in the (async) iterable ``it`` according to ``key``, or ``default`` if empty.'''
def arunning_mean[T: (int, float, complex)](it: SupportsIteration[T]) -> AsyncGeneratorType[T]: '''Repeatedly yield the mean of the items in the iterable so far, and advance the iterable.'''
@overload
def apowerset_of_sets[T: Hashable](it: SupportsIteration[T], *, frozen: Literal[True]=...) -> AsyncGeneratorType[frozenset[T]]: ...
@overload
def apowerset_of_sets[T: Hashable](it: SupportsIteration[T], *, frozen: Literal[False]) -> AsyncGeneratorType[set[T]]: '''Yield all the subsets of the items in the (async) iterable of hashable objects after consuming it at once and removing duplicates, as :class:`frozenset`'s if ``frozen`` is ``True`` (the default) and :class:`set`'s otherwise.'''
def aserialize[T](it: SupportsIteration[T]) -> AsyncGeneratorType[T]: '''Protect an (async) iterable from being consumed by many parties concurrently by applying an async lock.'''
@overload
def aonline_sorter[T: NotNone](it: SupportsIteration[T], *, key: Callable[[T], SupportsRichComparison], reverse: bool=..., slow: Any=...) -> AsyncGeneratorType[T, T|None]: ... # noqa: ANN401
@overload
def aonline_sorter[T: SupportsRichComparison](it: SupportsIteration[T], *, reverse: bool=..., slow: Any=...) -> AsyncGeneratorType[T, T|None]: # noqa: ANN401
    '''| Sort items from an (async) iterable and those sent in on the fly in the async generator interface (i.e. by awaiting the return value of ``asend``), according to ``key`` and ``reverse``.
    | Does not work well with items that are ``None``, because for an async generator ``agen``, ``agen.asend(None)`` and ``anext(agen)`` are indistinguishable.
    | Evaluates the truthiness of the ``slow`` parameter every time a new item is received, and if it is ``True``, offloads the evaluation of the ``key`` for that item to an executor, such that the :meth:`~object.__bool__` method on ``slow`` may reflect the state of the program but can also be a plain boolean.
    | If ``it`` is empty, the generator will also be empty.
    | In the second overload in the stub, since ``None`` is not assignable to :class:`~asyncutils._internal.prots.SupportsRichComparison`, there is no need to intersect the upper bound with :class:`~asyncutils._internal.prots.NotNone`.

    .. note:: Uses a stable variant of heap sort internally, which is O(n log n) time and O(n) space.
    '''
@overload
def aadjacent[T](pred: Callable[[T], object]|None, it: SupportsIteration[T], dist: int=..., *, await_pred: Literal[False]=...) -> AsyncGeneratorType[tuple[bool, T]]: ...
@overload
def aadjacent[T](pred: Callable[[T], Awaitable[object]], it: SupportsIteration[T], dist: int=..., *, await_pred: Literal[True]) -> AsyncGeneratorType[tuple[bool, T]]: ...
def acount_cycle[T](it: SupportsIteration[T], n: int|None=...) -> AsyncGeneratorType[tuple[int, T]]: ...
@overload
def agroupby_transform[T](it: SupportsIteration[T], *, vf: None=..., rf: None=..., await_kf: Literal[False]=..., await_vf: Literal[False]=..., await_rf: Literal[False]=...) -> AsyncGeneratorType[tuple[T, AsyncGeneratorType[T]]]: ...
@overload
def agroupby_transform[T, R](it: SupportsIteration[T], kf: Callable[[T], R], vf: None=..., rf: None=..., *, await_kf: Literal[False]=..., await_vf: Literal[False]=..., await_rf: Literal[False]=...) -> AsyncGeneratorType[tuple[R, AsyncGeneratorType[T]]]: ...
@overload
def agroupby_transform[T, S](it: SupportsIteration[T], *, vf: None=..., rf: Callable[[AsyncGeneratorType[T]], S], await_kf: Literal[False]=..., await_vf: Literal[False]=..., await_rf: Literal[False]=...) -> AsyncGeneratorType[tuple[T, S]]: ...
@overload
def agroupby_transform[T, S](it: SupportsIteration[T], *, vf: None=..., rf: Callable[[AsyncGeneratorType[T]], Awaitable[S]], await_kf: Literal[False]=..., await_vf: Literal[False]=..., await_rf: Literal[True]) -> AsyncGeneratorType[tuple[T, S]]: ...
@overload
def agroupby_transform[T, R, S](it: SupportsIteration[T], kf: Callable[[T], R], *, rf: Callable[[AsyncGeneratorType[T]], S], await_kf: Literal[False]=..., await_vf: Literal[False]=..., await_rf: Literal[False]=...) -> AsyncGeneratorType[tuple[R, S]]: ...
@overload
def agroupby_transform[T, R, S](it: SupportsIteration[T], kf: Callable[[T], R], vf: None, rf: Callable[[AsyncGeneratorType[T]], S], *, await_kf: Literal[False]=..., await_vf: Literal[False]=..., await_rf: Literal[False]=...) -> AsyncGeneratorType[tuple[R, S]]: ...
@overload
def agroupby_transform[T, R, S](it: SupportsIteration[T], kf: Callable[[T], R], *, rf: Callable[[AsyncGeneratorType[T]], Awaitable[S]], await_kf: Literal[False]=..., await_vf: Literal[False]=..., await_rf: Literal[True]) -> AsyncGeneratorType[tuple[R, S]]: ...
@overload
def agroupby_transform[T, R, S](it: SupportsIteration[T], kf: Callable[[T], R], vf: None, rf: Callable[[AsyncGeneratorType[T]], Awaitable[S]], *, await_kf: Literal[False]=..., await_vf: Literal[False]=..., await_rf: Literal[True]) -> AsyncGeneratorType[tuple[R, S]]: ...
@overload
def agroupby_transform[T, R](it: SupportsIteration[T], kf: Callable[[T], Awaitable[R]], vf: None=..., rf: None=..., *, await_kf: Literal[True], await_vf: Literal[False]=..., await_rf: Literal[False]=...) -> AsyncGeneratorType[tuple[R, AsyncGeneratorType[T]]]: ...
@overload
def agroupby_transform[T, R, S](it: SupportsIteration[T], kf: Callable[[T], Awaitable[R]], *, rf: Callable[[AsyncGeneratorType[T]], S], await_kf: Literal[True], await_vf: Literal[False]=..., await_rf: Literal[False]=...) -> AsyncGeneratorType[tuple[R, S]]: ...
@overload
def agroupby_transform[T, R, S](it: SupportsIteration[T], kf: Callable[[T], Awaitable[R]], vf: None, rf: Callable[[AsyncGeneratorType[T]], S], *, await_kf: Literal[True], await_vf: Literal[False]=..., await_rf: Literal[False]=...) -> AsyncGeneratorType[tuple[R, S]]: ...
@overload
def agroupby_transform[T, R, S](it: SupportsIteration[T], kf: Callable[[T], Awaitable[R]], *, rf: Callable[[AsyncGeneratorType[T]], Awaitable[S]], await_kf: Literal[True], await_vf: Literal[False]=..., await_rf: Literal[True]) -> AsyncGeneratorType[tuple[R, S]]: ...
@overload
def agroupby_transform[T, R, S](it: SupportsIteration[T], kf: Callable[[T], Awaitable[R]], vf: None, rf: Callable[[AsyncGeneratorType[T]], Awaitable[S]], *, await_kf: Literal[True], await_vf: Literal[False]=..., await_rf: Literal[True]) -> AsyncGeneratorType[tuple[R, S]]: ...
@overload
def agroupby_transform[T, R, V](it: SupportsIteration[T], kf: Callable[[T], Awaitable[R]], vf: Callable[[T], V], rf: None=..., *, await_kf: Literal[True], await_vf: Literal[False]=..., await_rf: Literal[False]=...) -> AsyncGeneratorType[tuple[R, AsyncGeneratorType[V]]]: ...
@overload
def agroupby_transform[T, R, S, V](it: SupportsIteration[T], kf: Callable[[T], Awaitable[R]], vf: Callable[[T], V], rf: Callable[[AsyncGeneratorType[V]], S], *, await_kf: Literal[True], await_vf: Literal[False]=..., await_rf: Literal[False]=...) -> AsyncGeneratorType[tuple[R, S]]: ...
@overload
def agroupby_transform[T, R, S, V](it: SupportsIteration[T], kf: Callable[[T], Awaitable[R]], vf: Callable[[T], V], rf: Callable[[AsyncGeneratorType[V]], Awaitable[S]], *, await_kf: Literal[True], await_vf: Literal[False]=..., await_rf: Literal[True]) -> AsyncGeneratorType[tuple[R, S]]: ...
@overload
def agroupby_transform[T, R, V](it: SupportsIteration[T], kf: Callable[[T], Awaitable[R]], vf: Callable[[T], Awaitable[V]], rf: None=..., *, await_kf: Literal[True], await_vf: Literal[True], await_rf: Literal[False]=...) -> AsyncGeneratorType[tuple[R, AsyncGeneratorType[V]]]: ...
@overload
def agroupby_transform[T, R, S, V](it: SupportsIteration[T], kf: Callable[[T], Awaitable[R]], vf: Callable[[T], Awaitable[V]], rf: Callable[[AsyncGeneratorType[V]], S], *, await_kf: Literal[True], await_vf: Literal[True], await_rf: Literal[False]=...) -> AsyncGeneratorType[tuple[R, S]]: ...
@overload
def agroupby_transform[T, R, S, V](it: SupportsIteration[T], kf: Callable[[T], Awaitable[R]], vf: Callable[[T], Awaitable[V]], rf: Callable[[AsyncGeneratorType[V]], Awaitable[S]], *, await_kf: Literal[True], await_vf: Literal[True], await_rf: Literal[True]) -> AsyncGeneratorType[tuple[R, S]]: ...
def arepeat_each[T](it: SupportsIteration[T], n: int) -> AsyncGeneratorType[T]: ...
def arepeat_last[T](it: SupportsIteration[T], default: T=...) -> AsyncGeneratorType[T]: ...
@overload
def adifference[T, R](it: SupportsIteration[T], func: Callable[[T, T], R], *, yield_initial: Literal[False], await_func: Literal[False]=...) -> AsyncGeneratorType[R]: ...
@overload
def adifference[T, R](it: SupportsIteration[T], func: Callable[[T, T], Awaitable[R]], *, yield_initial: Literal[False], await_func: Literal[True]) -> AsyncGeneratorType[R]: ...
@overload
def adifference[T](it: SupportsIteration[T], *, yield_initial: bool=..., await_func: Literal[False]=...) -> AsyncGeneratorType[T]: ...
@overload
def adifference[T](it: SupportsIteration[T], func: Callable[[T, T], Awaitable[T]], *, yield_initial: Literal[True], await_func: Literal[True]) -> AsyncGeneratorType[T]: ...
@overload
@deprecated('This overload is pointless and will be removed in version 2.0. If you are starring an iterable and want to handle the case where the iterable is empty, simply pass the iterable as the only argument.')
async def aminmax[R](*, default: R) -> R: ...
@overload
async def aminmax[T: SupportsRichComparison](it: SupportsIteration[T], /) -> tuple[T, T]: ...
@overload
async def aminmax[T: SupportsRichComparison, R](it: SupportsIteration[T], /, *, default: R) -> tuple[T, T]|R: ...
@overload
async def aminmax[T: SupportsRichComparison](a: T, b: T, /, *items: T) -> tuple[T, T]: ...
@overload
async def aminmax[T: SupportsRichComparison, R](a: T, b: T, /, *items: T, default: R) -> tuple[T, T]|R: '''Return a tuple of the smallest item and the largest item in the iterable or among the positional arguments by making a single pass. If the iterable is empty, return ``default``. O(1) space and O(n) time.'''
@overload
@deprecated('This overload is pointless and will be removed in version 2.0. If you are starring an iterable and want to handle the case where the iterable is empty, simply pass the iterable as the only argument.')
async def aminmax_keyed[R](*, key: Callable[[Any], object], default: R) -> R: ...
@overload
async def aminmax_keyed[T](it: SupportsIteration[T], /, *, key: Callable[[T], SupportsRichComparison]) -> tuple[T, T]: ...
@overload
async def aminmax_keyed[T, R](it: SupportsIteration[T], /, *, key: Callable[[T], SupportsRichComparison], default: R) -> tuple[T, T]|R: ...
@overload
async def aminmax_keyed[T](a: T, b: T, /, *items: T, key: Callable[[T], SupportsRichComparison]) -> tuple[T, T]: ...
@overload
async def aminmax_keyed[T, R](a: T, b: T, /, *items: T, key: Callable[[T], SupportsRichComparison], default: R) -> tuple[T, T]|R: '''Like :func:`aminmax`, but performs comparisons according to the return value of ``key``.'''
def aouter_product[T, R, V, **P](f: Callable[Concatenate[T, R, P], Awaitable[V]], xs: SupportsIteration[T], ys: SupportsIteration[R], /, *a: P.args, **k: P.kwargs) -> AsyncGeneratorType[list[V]]: ...
