'''Defines interfaces and type aliases used in this module's stubs to facilitate lightweight type annotations, inline or otherwise.
Pseudo-stable (deprecation periods will span at least 2 minor versions).
This is a fake module in the sense that the names in this stub are all `None` at runtime, so do not inherit from its 'protocols'.'''
from ..constants import sentinel_base
from ..exceptions import ForbiddenOperation
from ..mixins import LoopContextMixin
import sys
from _collections_abc import AsyncGenerator, AsyncIterable, Awaitable, Buffer, Callable, Coroutine, Generator, Iterable, Iterator
from asyncio.events import AbstractEventLoop
from asyncio.futures import Future
from concurrent.futures import Future as SyncFuture
from contextlib import _AsyncGeneratorContextManager
from io import TextIOWrapper, _WrappedBuffer
from mmap import mmap
from types import FunctionType, TracebackType
from typing import IO, Any, Concatenate, Literal, NamedTuple, NewType, Protocol, Self, SupportsIndex, SupportsInt, final, overload, type_check_only
@type_check_only
class SupportsLT(Protocol):
    '''An object that implements the < operator.'''
    def __lt__(self, other: Self, /) -> bool: ...
@type_check_only
class SupportsGT(Protocol):
    '''An object that implements the > operator.'''
    def __gt__(self, other: Self, /) -> bool: ...
@type_check_only
class AsyncContextManager[T](Protocol):
    '''An asynchronous context manager. Basically :class:`contextlib.AbstractAsyncContextManager` with proper overloads, as a protocol.'''
    async def __aenter__(self) -> T: ...
    @overload
    async def __aexit__(self, exc_typ: ValidExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> bool|None: ...
    @overload
    async def __aexit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> bool|None: ...
@type_check_only
class AsyncLockLike[T](AsyncContextManager[T], Protocol):
    '''An object that behaves like an asynchronous lock.'''
    async def acquire(self) -> bool|None: ...
    def release(self) -> Awaitable[None]|None: ...
    def locked(self) -> bool: ...
@type_check_only
class FutWrapType(Protocol):
    def __call__(self, future: Future[Any]|SyncFuture[Any], *, loop: AbstractEventLoop|None) -> Future[Any]: ...
@type_check_only
class GenericSized[T](Protocol):
    ''':class:`typing.Sized` is not generic, so here is a generic version of it.'''
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[T]: ...
@type_check_only
class SupportsSlicing[T](GenericSized[T], Protocol):
    '''Protocol for iterables with size, and index and slice access.'''
    @overload
    def __getitem__(self, idx: ValidSlice, /) -> Self: ...
    @overload
    def __getitem__(self, idx: SupportsIndex, /) -> T: ...
    def __len__(self) -> int: ...
    def __reversed__(self) -> Iterator[T]: '''The requirements for this protocol makes its conformants automatically reversible.'''
@type_check_only
class CanClearAndCopy[T](Protocol):
    '''An iterable that supports clearing and shallow copying.'''
    def copy(self) -> Self: ...
    def clear(self) -> None: ...
    def __iter__(self) -> Iterator[T]: ...
@type_check_only
class PathLike[T](Protocol):
    '''An object that represents a path. Basically :class:`os.PathLike`, but a Protocol.'''
    def __fspath__(self) -> T: ...
@type_check_only
class SupportsPop[T](Protocol):
    '''Types with a `pop` method.'''
    def pop(self) -> T: ...
@type_check_only
class SupportsPopLeft[T](Protocol):
    '''Types with a `popleft` method.'''
    def popleft(self) -> T: ...
@type_check_only
class GeneratorCoroutine[Y, S, R](Generator[Y, S, R], Coroutine[Y, S, R]):
    '''Objects such as those returned by :dec:`types.coroutine`-decorated generator functions.'''
    def send(self, val: S, /) -> Y: ...
    @overload # type: ignore[override]
    def throw(self, typ: ValidExcType, val: BaseException|None=..., tb: TracebackType|None=..., /) -> Y: ...
    @overload
    def throw(self, val: BaseException, /) -> Y: ...
    def close(self) -> None: ...
    def __await__(self) -> Generator[Any, None, R]: ...
@type_check_only
class PartialInterfaceMeta(type):
    '''Metaclass for 'partial interfaces', described below.'''
    def __getattr__(cls, name: str, /) -> Any: ...
@type_check_only
class PartialInterface(metaclass=PartialInterfaceMeta):
    '''Base class for partial interfaces.
    If it is only known that a class implements an interface, type checkers might throw errors on unrecognized attributes that may actually exist on the object or class.
    This is a simplistic fix that asks type checkers to assume those attributes always exist and make no attempt to infer their types.'''
    def __init__(self, *a: Any, **k: Any): ...
    def __getattr__(self, name: str, /) -> Any: ...
@type_check_only
class DumpType(Protocol):
    '''Represents the type of simple json-dumping functions accepted by tools.argv_to_json and tools.argstr_to_json.'''
    def __call__(self, dct: dict[str, Any], file: TextIOWrapper[_WrappedBuffer], /) -> None: ...
@type_check_only
class CanWriteAndFlush[T](Protocol):
    '''A writable and flushable 'stream'.'''
    def flush(self) -> None: ...
    def write(self, s: T, /) -> int|None: ...
@type_check_only
class SigPatcher(Protocol):
    '''Type of functions with a specific signature in the semi-public API of this module, used to alter function signatures.'''
    def __call__(self, *to_patch: tuple[FunctionType, str]) -> None: ...
@type_check_only
class Middleware(Protocol):
    '''Represents a middleware accepted by :class:`channels.EventBus`.
    To facilitate O(1) removal of middlewares and order preservation, it is unfortunately impossible to add the same middleware into the pipe twice.
    Therefore, it is suggested that a lightweight wrapper lambda around a function containing the main logic be used.'''
    def __call__(self, event_type: str, data: Any, /) -> Any: ...
    def __hash__(self) -> int: ...
@type_check_only
class SupportsMatMul(Protocol):
    '''A class that supports matrix multiplication.'''
    def __matmul__(self, other: Self) -> Self: ...
@type_check_only
class Q[R, T](Protocol):
    '''A base protocol representing password-protected queues.'''
    exc: type[ForbiddenOperation]
    async def get(self) -> T: '''Asynchronously get an item from the queue; if the queue is empty, wait until an item is available.'''
    async def put(self, item: T) -> None: '''Asynchronously put an item into the queue; if the queue is full, wait until a free slot is available.'''
    def get_nowait(self) -> T: '''Get an item from the queue immediately; raise :exc:`asyncio.QueueEmpty` if impossible.'''
    def put_nowait(self, item: T) -> None: '''Put an item into the queue immediately; raise :exc:`asyncio.QueueFull` if impossible.'''
    def qsize(self) -> int: '''Number of items in the queue.'''
    def task_done(self) -> None: '''Mark the completion of a task gotten from the queue to :meth:`join`.'''
    @property
    def maxsize(self) -> int: '''Maximum number of items allowed in the queue at any moment.'''
    def cancel_extend(self, msg: Any=...) -> bool: '''Cancel the current extend operation with a message which will be the argument for the CancelledError seen by the extender if any, returning success, and return False otherwise.'''
    def empty(self) -> bool: '''Check if the queue is empty.'''
    def full(self) -> bool: '''Check if the queue is full.'''
    async def join(self) -> None: '''Wait until :meth:`task_done` has been called for each item put into the queue.'''
    def shutdown(self, immediate: bool=...) -> None: '''Shut down the queue. This functionality was introduced to :class:`asyncio.queues.Queue` in python 3.13, so a backport to 3.12 is required.'''
    def change_get_password(self, old_pwd: R, new_pwd: R) -> bool: '''Attempts to change the get password of the password-protected queue to new_pwd; returns success.'''
    def change_put_password(self, old_pwd: R, new_pwd: R) -> bool: '''Attempts to change the put password of the password-protected queue to new_pwd; returns success.'''
@type_check_only
class G[R, T](Q[R, T], Protocol):
    '''Queues for which `get` is protected by a password.'''
    async def get(self, pwd: R) -> T: # type: ignore[override]
        '''Removes and returns an item from the password-protected queue, if the password provided was correct; raises :exc:`WrongPassword` otherwise.
        If the queue is empty, waits until an item is available.'''
    def get_nowait(self, pwd: R) -> T: # type: ignore[override]
        '''Removes and returns an item from the password-protected queue, if the password provided was correct; raises :exc:`WrongPassword` otherwise.
        If the queue is empty, raises :exc:`asyncio.QueueEmpty`.'''
@type_check_only
class P[R, T](Q[R, T], Protocol):
    '''Queues for which `put` is protected by a password.'''
    async def put(self, item: T, pwd: R) -> None: # type: ignore[override]
        '''Puts an item into the password-protected queue, if the password provided was correct; raises :exc:`WrongPassword` otherwise.
        If the queue is full, waits until a free slot is available.'''
    def put_nowait(self, item: T, pwd: R) -> None: # type: ignore[override]
        '''Puts an item into the password-protected queue, if the password provided was correct; raises :exc:`WrongPassword` otherwise.
        If the queue is full, raises :exc:`asyncio.QueueFull`.'''
@type_check_only
class B[R, V, T](G[R, T], P[V, T], Protocol): '''Queues for which both `get` and `put` are protected by passwords, which may or may not be the same.'''
@type_check_only
class RWLockRV[T, **P](Protocol):
    '''The return type of the :meth:`reader` and :meth:`writer` methods of :class:`locks.RWLock`.'''
    def __call__(self, *a: P.args, **k: P.kwargs) -> Coroutine[Any, Any, T]: ...
    def reader(self, f: Callable[P, Awaitable[T]], /) -> Self: ...
    def writer(self, f: Callable[P, Awaitable[T]], /) -> Self: ...
@type_check_only
class EveryMethodRVRV[T, R](Protocol):
    '''Return type of :class:`EveryMethodRV`.'''
    async def __call__(self, _: T, /, *a: Any, **k: Any) -> R|None: ...
@type_check_only
class EveryMethodFT[T, R](Protocol):
    '''The type of functions taken by :class:`EveryMethodRV`.'''
    def __call__(self, _: T, /, *a: Any, **k: Any) -> Awaitable[R]: ...
@type_check_only
class DecoratorFactoryRV(Protocol):
    def __call__[T, **P](self, f: Callable[P, Awaitable[T]], /) -> Callable[P, Coroutine[Any, Any, T]]: ...
@type_check_only
class EveryRV[T](Protocol):
    def __call__[**P](self, f: Callable[P, Awaitable[T]], /) -> Callable[P, Coroutine[Any, Any, T|None]]: ...
@type_check_only
class SubscriptionRV(Protocol):
    def __call__(self, strict: bool=...) -> None: ...
@type_check_only
class StateSnapshot(NamedTuple):
    '''Type of snapshots of the current state of a :class:`channels.Rendezvous` object as returned by its :meth:`state_snapshot` method.'''
    num_getters: int
    '''Current number of slots waiting for values.'''
    num_putters: int
    '''Current number of values waiting for slots.'''
    num_ops: int
    '''`num_getters+num_putters`'''
    idle: bool
    '''`num_getters == num_putters == 0`'''
@type_check_only
class BenchmarkResult(NamedTuple):
    '''The return type of :func:`func.benchmark`.'''
    min: float
    '''The minimum execution time among all non-warmup calls.'''
    max: float
    '''The maximum execution time among all non-warmup calls.'''
    total: float
    '''The total execution time.'''
    avg: float
    '''`total/iterations`.'''
    iterations: int
    '''The `times` constructor parameter.'''
@type_check_only
class MemoryMappedFile(LoopContextMixin):
    '''The type of async memory-mapped files as opened by :class:`io.MemoryMappedIOManager`. Calls itself :class:`asyncutils.io.File`.'''
    if sys.platform != 'win32':
        def madvise(self, option: int, start: int=..., length: int|None=...) -> None: ...
    async def read(self, offset: int=..., size: int=...) -> bytes: ...
    async def write(self, data: bytes, offset: int=...) -> None: ...
    async def readline(self, offset: int=..., size: int|None=..., incl_newline: bool=...) -> bytes: ...
    async def readlines(self, hint: int=...) -> list[bytes]: ...
    async def flush(self, offset: int=..., size: int|None=..., /) -> None: ...
    async def move(self, dest: int, src: int, count: int) -> None: ...
    async def __setup__(self) -> None: ...
    async def __cleanup__(self) -> None: ...
    async def seek(self, pos: int, whence: Seek=...) -> None: ...
    def __new__(cls, file: IO[bytes], /) -> Self: ...
    def __iter__(self) -> Iterator[bytes]: ...
    @property
    def mmap(self) -> mmap: ...
    @property
    def closed(self) -> bool: ...
    @property
    def open_files(self) -> OpenFiles: ...
    def fileno(self) -> int: ...
    def sync(self) -> None: ...
    def close(self) -> None: ...
    async def aclose(self) -> None: ...
    def read_byte(self) -> int: ...
    def write_byte(self, b: int, /) -> None: ...
    def resize(self, newsize: int) -> None: ...
    def find(self, sub: bytes, start: int|None=..., end: int|None=...) -> int: ...
    def rfind(self, sub: bytes, start: int|None=..., end: int|None=...) -> int: ...
    def tell(self) -> int: ...
    def size(self) -> int: ...
    def isatty(self) -> bool: ...
    def readable(self) -> Literal[True]: ...
    def writable(self) -> Literal[True]: ...
    def seekable(self) -> Literal[True]: ...
    async def writelines(self, lines: Iterable[bytes], /, *, sep: bytes=...) -> None: ...
    async def read_str(self, offset: int=..., size: int=..., encoding: str=..., errors: str=...) -> str: ...
    async def write_str(self, text: str, offset: int=..., encoding: str=..., errors: str=...) -> None: ...
    async def smart_write(self, data: str|bytes, offset: int=...) -> None: ...
    async def copy_range(self, src_offset: int, dest_offset: int, size: int) -> bool: ...
    async def fill(self, pattern: bytes, offset: int=..., count: int=...) -> None: ...
    async def compare(self, other: Self, /, size: int=..., offset_self: int=..., offset_other: int=...) -> bool: ...
    async def hamming_dist(self, other: Self, /, size: int=..., offset_self: int=..., offset_other: int=...) -> int: ...
    async def read_until(self, delim: bytes, offset: int=..., maxsize: int=...) -> tuple[bytes, int]: ...
    async def insert(self, data: bytes, offset: int) -> None: ...
    async def delete(self, offset: int, size: int) -> None: ...
    async def replace(self, old: bytes, new: bytes, offset: int=..., count: int=...) -> int: ...
    def search_lazy(self, pattern: bytes, offset: int=..., max_results: int=...) -> AsyncGenerator[int]: ...
    def search_lazy_nonoverlapping(self, pattern: bytes, offset: int=..., max_results: int=...) -> AsyncGenerator[int]: ...
    async def search(self, pattern: bytes, offset: int=..., max_results: int=...) -> list[int]: ...
    async def search_nonoverlapping(self, pattern: bytes, offset: int=..., max_result: int=...) -> list[int]: ...
    async def compact(self) -> None: ...
@type_check_only
class Bag(dict[str, Any]): # noqa: FURB189
    '''A thin dictionary subclass that supports attribute access.'''
    def __getattr__(self, key: str, /) -> Any: ...
    def __setattr__(self, key: str, value: Any, /) -> None: ...
    def __delattr__(self, key: str, /) -> None: ...
@type_check_only
class AUnzipConsumer[T]:
    '''The type of each consumer in the tuple return value of :func:`iters.aunzip`.'''
    def __aiter__(self) -> Self: ...
    async def __anext__(self) -> T: ...
    def close(self) -> None: '''Shut down the underlying queue, such that this consumer no longer receives the values at its position.'''
@type_check_only
class ToSyncFromLoopRV(Protocol):
    '''The signature of the return value of :func:`util.to_sync_from_loop`.'''
    def __call__[R, **P](self, f: Callable[P, Awaitable[R]], /, timeout: float|None=...) -> Callable[P, R]: ...
@type_check_only
class TransientBlockFromLoopRV(Protocol):
    '''The signature of the return value of :func:`util.transient_block_from_loop`.'''
    def __call__[T, **P](self, f: Callable[P, T], /, *a: P.args, **k: P.kwargs) -> Future[T]: ...
@type_check_only
class Sentinel(sentinel_base):
    '''Common type of sentinels for this module, internal or public.'''
    def __reduce__(self) -> str: '''These sentinels are accessible in the top level of the :mod:`asyncutils.constants` namespace.''' # type: ignore[override]
@final
@type_check_only
class NoDefaultType(Sentinel): ...
@final
@type_check_only
class RaiseType(Sentinel): ...
@final
@type_check_only
class SyncAwaitType(Sentinel): ...
@final
@type_check_only
class WildcardType:
    '''Type of :const:`channels.EventBus.WILDCARD`.'''
    def __bool__(self) -> Literal[False]: ...
type IntCompatible = str|SupportsInt|SupportsIndex|Buffer
'''Objects accepted by the :class:`int` constructor.'''
type SupportsIteration[T] = Iterable[T]|AsyncIterable[T]
'''Objects that support (async) iteration.'''
type SupportsRichComparison = SupportsLT|SupportsGT
'''Objects implementing the < or > operator.'''
type ValidExcType = type[BaseException]
'''The type of exc_typ in `__exit__` and `__aexit__` methods.'''
type Exceptable = ValidExcType|tuple[ValidExcType, ...]
'''Objects that may follow an except statement.'''
type Openable = int|str|bytes|PathLike[str]|PathLike[bytes]
'''Anything that can normally be passed to the built-in :func:`open` function.'''
type ValidSlice = slice[SupportsIndex|None, SupportsIndex|None, SupportsIndex|None]
'''A slice with start, stop and step being integers or None, representing a slice that typical sequences supporting slicing should accept.'''
type Timer = Callable[[], float]
'''Type of functions that return the current time under some specification, such as :func:`time.monotonic`, :func:`time.process_time` and :func:`time.perf_counter`.'''
type All = tuple[str, ...]
'''Type of the `__all__` attributes of the submodules of :mod:`asyncutils`.'''
type Submodule = Literal['altlocks', 'base', 'buckets', 'caches', 'channels', 'cli', 'compete', 'config', 'console', 'constants', 'context', 'events', 'exceptions', 'func', 'futures', 'io', 'iterclasses', 'iters', 'locks', 'misc', 'mixins', 'networking', 'pools', 'processors', 'properties', 'queues', 'signals', 'tools', 'util', 'version']
'''Type of strings representing asyncutils submodule names.'''
type Executor = Literal['thread', 'process', 'interpreter', 'loky_noreuse', 'loky', 'dask', 'ipython', 'elib_flux_cluster', 'elib_flux_job', 'elib_slurm_cluster', 'elib_slurm_job', 'elib_single_node', 'pebble_thread', 'pebble_process']
'''Type of strings representing executors that can be passed to -e/--executor.'''
type HashAlgorithm = Literal['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'blake2b', 'blake2s', 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512', 'shake_128', 'shake_256']
'''Names of algorithms used for calculating checksums. The default is blake2s, which is fast and somewhat secure with a low probability of collision.'''
type OpenRV = _AsyncGeneratorContextManager[MemoryMappedFile, None]
'''The type of the return values of the `open`, `create` and `create_sparsef` methods of `io.MemoryMappedIOManager`.'''
type OpenFiles = dict[tuple[TextIOWrapper[_WrappedBuffer], Literal['r+b', 'w+b', 'x+b']], MemoryMappedFile]
'''The type of the `open_files` property of :class:`io.MemoryMappedIOManager`.'''
type SpecificSubscriber = Callable[[Any], Awaitable[object]]
'''The type of subscribers for :class:`channels.EventBus`.'''
type WildcardSubscriber = Callable[[str, Any], Awaitable[object]]
'''The type of wildcard subscribers for :class:`channels.EventBus`.'''
if sys.platform == 'win32':
    type Seek = Literal[0, 1, 2]
    '''Possible values of the `whence` parameter for :meth:`io.MemoryMappedIOManager.seek`, as follows:
    * 0: SEEK_SET
    * 1: SEEK_CUR
    * 2: SEEK_END'''
else:
    type Seek = Literal[0, 1, 2, 3, 4]
    '''Possible values of the `whence` parameter for :meth:`io.MemoryMappedIOManager.seek`, as follows:
    * 0: SEEK_SET
    * 1: SEEK_CUR
    * 2: SEEK_END
    * 3: SEEK_DATA
    * 4: SEEK_HOLE'''
type EveryMethodRV[R, T] = Callable[[EveryMethodFT[T, R]], EveryMethodRVRV[T, R]]
'''Return type of :func:`func.everymethod`.'''
type Observer[**P] = Callable[Concatenate[Any, P], Awaitable[Any]]
'''The type of :class:`channels.Observable` observers.'''
ExceptionWrapper = NewType('ExceptionWrapper', object)
'''The return type of :func:`exceptions.wrap_exc`.'''