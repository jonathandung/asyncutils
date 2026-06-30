'''| Defines interfaces and type aliases used in this module's stubs to facilitate lightweight type annotations, inline or otherwise.
| To avoid confusion with builtin modules, this module is named ``prots``, which may be less than descriptive, but it is what it is.
| Neither this module nor any of its symbols exist at runtime.
| Thus, we export nothing intentionally and prompt type checkers to emit errors when symbols here are used with ``from asyncutils._internal.prots import *``.

.. note:: In the generated documentation, the instances of ``tyx`` represent `the ty_extensions module <https://github.com/astral-sh/ruff/blob/main/crates/ty_python_semantic/resources/mdtest/ty_extensions.md>`__. It is only available when ty is type checking the library.
.. tip:: For inline type annotations, wrap the imports in ``if TYPE_CHECKING:`` blocks.
.. tip::

  Besides, run ``from __future__ import annotations`` on the top of the file for Python 3.13 or below, so that the annotations need not be quoted
  even prior to the implementation of :pep:`563`, which introduced deferred annotation evaluation.
'''
from ..config import FaultyConfig
from ..constants import SentinelBase
from ..exceptions import ForbiddenOperation
from ..mixins import LoopContextMixin
import sys, ty_extensions as tyx
from collections.abc import AsyncIterable, Awaitable, Buffer, Callable, Coroutine, Generator, Hashable, Iterable, Iterator
from asyncio import AbstractEventLoop, Future
from concurrent.futures import Future as SyncFuture
from contextlib import AbstractContextManager, AbstractAsyncContextManager
from contextvars import Context
from io import TextIOWrapper
from types import AsyncGeneratorType, CodeType, CoroutineType, FrameType, FunctionType, TracebackType
from typing import Any, Concatenate, Literal, NamedTuple, NewType, Protocol, Self, SupportsIndex, SupportsInt, final, overload, type_check_only
from typing_extensions import TypeIs
@type_check_only
class Reader[T](Protocol):
    ''':class:`io.Reader` is not used due to version compatibility issues.'''
    def read(self, size: int=..., /) -> T: ...
@type_check_only
class Writer[T](Protocol):
    ''':class:`io.Writer` is not used due to version compatibility issues.'''
    def write(self, data: T, /) -> int: ...
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
    '''A protocol version of :class:`~contextlib.AbstractAsyncContextManager` with proper overloads.'''
    async def __aenter__(self) -> T: ...
    @overload
    async def __aexit__(self, exc_typ: ExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> bool|None: ...
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
    '''The signature of the functions accepted for the ``futwrap`` parameter in :func:`~asyncutils.compete.convert_to_coro_iter`.'''
    def __call__[T](self, future: Future[T]|SyncFuture[T], *, loop: AbstractEventLoop|None) -> Future[T]: ...
@type_check_only
class GenericSized[T](Protocol):
    '''A generic version of :class:`~typing.Sized`.'''
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
@type_check_only
class CanClearAndCopy[T](Protocol):
    '''An iterable that supports clearing and shallow copying.'''
    def copy(self) -> Self: ...
    def clear(self) -> None: ...
    def __iter__(self) -> Iterator[T]: ...
@type_check_only
class PathLike[T](Protocol):
    '''An object that represents a path. Basically :class:`os.PathLike`, but a :class:`~typing.Protocol`.'''
    def __fspath__(self) -> T: ...
@type_check_only
class SupportsPop[T](Protocol):
    '''Types with a :meth:`~list.pop` method.'''
    def pop(self) -> T: ...
@type_check_only
class SupportsPopLeft[T](Protocol):
    '''Types with a :meth:`~collections.deque.popleft` method.'''
    def popleft(self) -> T: ...
@type_check_only
class GeneratorCoroutine[T, S, R](Generator[T, S, R], Coroutine[T, S, R]):
    '''Objects such as those returned by :func:`types.coroutine`-decorated generator functions.'''
    def send(self, val: S, /) -> T: ...
    @overload
    def throw(self, typ: ExcType, val: object=..., tb: TracebackType|None=..., /) -> T: ...
    @overload
    def throw(self, exc: BaseException, val: None=..., tb: TracebackType|None=..., /) -> T: ...
    def close(self) -> R|None: ... # ty: ignore[invalid-method-override]
    @property
    def gi_code(self) -> CodeType: ...
    @property
    def gi_frame(self) -> FrameType|None: ...
    @property
    def gi_running(self) -> bool: ...
    @property
    def gi_yieldfrom(self) -> Iterator[T] | None: ... # cspell:disable-line
    @property
    def gi_suspended(self) -> bool: ...
    @property
    def __name__(self) -> str: ...
    @property
    def __qualname__(self) -> str: ...
    def __await__(self) -> Generator[Any, None, R]: ...
@type_check_only
class PartialInterfaceMeta(type):
    '''Metaclass for partial interfaces, as described and justified in :class:`PartialInterface`.'''
    def __getattr__(cls, name: str, /) -> Any: ... # noqa: ANN401
@type_check_only
class PartialInterface(metaclass=PartialInterfaceMeta):
    '''| Base class for partial interfaces.
    | If it is only known that a class implements an interface, static code analysis tools might emit diagnostics on unrecognized attributes that may actually exist on the object or class.
    | This is a simplistic fix that asks type checkers to assume those attributes always exist and make no attempt to infer their types.
    '''
    def __init__(self, *a: object, **k: object): ...
    def __getattr__(self, name: str, /) -> Any: ... # noqa: ANN401
@type_check_only
class DumpType(Protocol):
    '''Encapsulates the signature of simple json-dumping functions accepted by :func:`~asyncutils.tools.argv_to_json` and :func:`~asyncutils.tools.argstr_to_json`.'''
    def __call__(self, dct: dict[str, Any], file: TextIOWrapper, /) -> None: '''``dict[str, Any]`` is used here because the callable needs only handle strict instances of :class:`dict`.'''
@type_check_only
class CanWriteAndFlush[T](Protocol):
    '''A writable and flushable 'stream', supposedly used for I/O.'''
    def flush(self) -> None: ...
    def write(self, s: T, /) -> int|None: ...
@type_check_only
class FuncWrapper[T](Protocol):
    '''Intermediate protocol to build the recursive definition of :type:`Wrapper`.'''
    @property
    def __wrapped__(self) -> T: ...
@type_check_only
class FuncProxy[T](Protocol):
    '''Same as above.'''
    @property
    def __func__(self) -> T: ...
type Proxy[T] = FuncProxy[T]|FuncWrapper[T]
'''A supposed callable object having a :attr:`FuncWrapper.__wrapped__` or :attr:`~method.__func__` attribute pointing to the callable it wraps.'''
type Wrapper = FunctionType|Proxy[FunctionType|Wrapper]
'''A function or wrapper of any depth thereof.'''
type SigPatcherArg = tuple[Wrapper, str]
'''The type of a positional argument passed to a signature-patching function in :mod:`~asyncutils._internal.patch`.'''
type Middleware = Callable[[str, Any], Any]
'''Represents a middleware accepted by :class:`~asyncutils.channels.EventBus`.'''
type NonGroupExc = tyx.Intersection[BaseException, tyx.Not[BaseExceptionGroup]]
'''Exceptions that are not exception groups.'''
type NotNone = tyx.Not[None]
'''The complement of ``None``.'''
@type_check_only
class SupportsMatMul(Protocol):
    '''Objects that implement matrix multiplication to return an instance of its own type.'''
    def __matmul__(self, other: Self, /) -> Self: ...
@type_check_only
class QProtBase[R, V](Protocol):
    '''A base protocol representing password-protected queues.'''
    exc: type[ForbiddenOperation]
    '''Convenience alias for :exc:`~asyncutils.exceptions.ForbiddenOperation`.'''
    def qsize(self) -> int: '''Return the number of items in the queue.'''
    def task_done(self) -> None: '''Mark the completion of a task gotten from the queue to :meth:`join`.'''
    @property
    def maxsize(self) -> int: '''Maximum number of items allowed in the queue at any moment.'''
    def cancel_extend(self, msg: object=...) -> bool:
        '''| Cancel the currently running task to put in the initial items to the queue asynchronously, optionally with a message, which will
        | be the argument for the :exc:`~asyncio.CancelledError` seen by the extender if any.
        | Return ``False`` if the task is already done or cancelled, or there was no task to begin with.
        '''
    def empty(self) -> bool: '''Check if the queue is empty.'''
    def full(self) -> bool: '''Check if the queue is full.'''
    async def join(self) -> None: '''Wait until :meth:`task_done` has been called for each item put into the queue.'''
    def shutdown(self, immediate: bool=...) -> None: '''Shut down the queue. If ``immediate`` is ``True``, pending gets raise immediately even if the queue is not empty.'''
    def change_get_password(self, opw: R, npw: R) -> bool: '''Attempt to change the get password of the password-protected queue to ``npw`` given the old password ``opw`` and return success. Always returns ``False`` if the queue does not protect gets or is empty and has been shut down.'''
    def change_put_password(self, opw: V, npw: V) -> bool: '''Attempt to change the put password of the password-protected queue to ``npw`` given the old password ``opw`` and return success. Always returns ``False`` if the queue does not protect puts or has been shut down.'''
@type_check_only
class GetProtectedQProtocol[R, T](QProtBase[R, Any], Protocol):
    '''Queues for which :meth:`~asyncio.Queue.get` and :meth:`~asyncio.Queue.get_nowait` are protected by a password.'''
    async def get(self, pwd: R, /) -> T: '''Remove and return an item from the password-protected queue, if the password provided was correct; raise :exc:`~asyncutils.exceptions.WrongPassword` otherwise. If the queue is empty, wait until an item is available.'''
    async def put(self, item: T) -> None: '''Put ``item`` into the queue; if the queue is full, asynchronously wait until a free slot is available.'''
    def get_nowait(self, pwd: R, /) -> T: '''Remove and return an item from the password-protected queue, if the password provided was correct; raise :exc:`~asyncutils.exceptions.WrongPassword` otherwise. If the queue is empty, raise :exc:`~asyncio.QueueEmpty`.'''
    def put_nowait(self, item: T) -> None: '''Put ``item`` into the queue immediately; raise :exc:`~asyncio.QueueFull` if impossible.'''
@type_check_only
class PutProtectedQProtocol[V, T](QProtBase[Any, V], Protocol):
    '''Queues for which :meth:`~asyncio.Queue.put` and :meth:`~asyncio.Queue.put_nowait` are protected by a password.'''
    async def get(self) -> T: '''Asynchronously get an item from the queue; if the queue is empty, wait until an item is available.'''
    def get_nowait(self) -> T: '''Get an item from the queue immediately; raise :exc:`~asyncio.QueueEmpty` if impossible.'''
    async def put(self, item: T, pwd: V, /) -> None: '''Put ``item`` into the password-protected queue, if ``pwd`` is the correct password; raise :exc:`~asyncutils.exceptions.WrongPassword` otherwise. If the queue is full, wait until a free slot is available.'''
    def put_nowait(self, item: T, pwd: V, /) -> None: '''Put ``item`` into the password-protected queue, if ``pwd`` is the correct password; raise :exc:`~asyncutils.exceptions.WrongPassword` otherwise. If the queue is full, raise :exc:`~asyncio.QueueFull`.'''
@type_check_only
class GetAndPutProtectedQProtocol[R, V, T](QProtBase[R, V], Protocol):
    '''Queues for which all mutating operations are protected by passwords. There is no requirement as to whether they are the same or different.'''
    async def get(self, pwd: R, /) -> T: '''Remove and return an item from the password-protected queue, if the password provided was correct; raise :exc:`~asyncutils.exceptions.WrongPassword` otherwise. If the queue is empty, wait until an item is available.'''
    def get_nowait(self, pwd: R, /) -> T: '''Remove and return an item from the password-protected queue, if the password provided was correct; raise :exc:`~asyncutils.exceptions.WrongPassword` otherwise. If the queue is empty, raise :exc:`~asyncio.QueueEmpty`.'''
    async def put(self, item: T, pwd: V, /) -> None: '''Put ``item`` into the password-protected queue, if ``pwd`` is the correct password; raise :exc:`~asyncutils.exceptions.WrongPassword` otherwise. If the queue is full, wait until a free slot is available.'''
    def put_nowait(self, item: T, pwd: V, /) -> None: '''Put ``item`` into the password-protected queue, if ``pwd`` is the correct password; raise :exc:`~asyncutils.exceptions.WrongPassword` otherwise. If the queue is full, raise :exc:`~asyncio.QueueFull`.'''
@type_check_only
class RWLockRV[T, **P](Protocol):
    '''The return type of the :meth:`~asyncutils.rwlocks.RWLock.reader` and :meth:`~asyncutils.rwlocks.RWLock.writer` methods of :class:`~asyncutils.rwlocks.RWLock` and subclasses thereof.'''
    def __call__(self, *a: P.args, **k: P.kwargs) -> CoroutineType[Any, Any, T]: ...
    def reader(self, f: Callable[P, Awaitable[T]], /) -> Self: '''Mark another function as a reader and return an object with :meth:`reader` and :meth:`writer` methods.'''
    def writer(self, f: Callable[P, Awaitable[T]], /) -> Self: '''Mark another function as a writer and return an object with :meth:`reader` and :meth:`writer` methods.'''
@type_check_only
class EveryMethodFT[T, R](Protocol):
    '''The type of functions taken by :class:`EveryMethodRV`.'''
    def __call__(self, self_: T, /, *a: object, **k: object) -> Awaitable[R]: ...
@type_check_only
class DecoratorFactoryRV(Protocol):
    '''The return type of various decorator factories in :mod:`~asyncutils.func`, including :func:`~asyncutils.func.debounce`, :func:`~asyncutils.func.throttle` and :func:`~asyncutils.func.debounce`.'''
    def __call__[T, **P](self, f: Callable[P, Awaitable[T]], /) -> Callable[P, CoroutineType[Any, Any, T]]: ...
@type_check_only
class EveryRV[T](Protocol):
    '''The return type of :func:`~asyncutils.func.every`.'''
    def __call__[**P](self, f: Callable[P, Awaitable[T]], /) -> Callable[P, CoroutineType[Any, Any, T|None]]: ...
@type_check_only
class SubscriptionRV(Protocol):
    '''Return type of the :meth:`~asyncutils.channels.Observable.subscribe`, :meth:`~asyncutils.channels.Observable.subscribe_nowait` and :meth:`~asyncutils.channels.Observable.ntimes` methods of :class:`~asyncutils.channels.Observable`.'''
    def __call__(self, strict: bool=...) -> None: ...
@type_check_only
class StateSnapshot(NamedTuple):
    '''Type of snapshots of the current state of a :class:`~asyncutils.channels.Rendezvous` object as returned by its :meth:`~asyncutils.channels.Rendezvous.state_snapshot` method.'''
    num_getters: int
    '''Current number of slots waiting for values.'''
    num_putters: int
    '''Current number of values waiting for slots.'''
    num_ops: int
    '''``ss.num_ops == ss.num_getters+ss.num_putters``'''
    idle: bool
    '''``ss.idle == (ss.num_getters == ss.num_putters == 0)``'''
@type_check_only
class BenchmarkResult(NamedTuple):
    '''The return type of :func:`~asyncutils.func.benchmark`.'''
    min: float
    '''The minimum execution time among all non-warmup calls.'''
    max: float
    '''The maximum execution time among all non-warmup calls.'''
    total: float
    '''The total execution time.'''
    avg: float
    '''``br.avg == br.total/br.iterations``.'''
    iterations: int
    '''The ``times`` constructor parameter.'''
@type_check_only
class MemoryMappedFile(LoopContextMixin):
    '''The type of async memory-mapped files as opened and returned by :class:`~asyncutils.iotools.MemoryMappedIOManager`.'''
    if sys.platform != 'win32':
        def madvise(self, option: int, start: int=..., length: int|None=...) -> None: '''Advise the kernel about how to handle the memory map by making the ``madvise`` system call.'''
    async def read(self, offset: int=..., size: int=...) -> bytes: '''Read ``size`` bytes from the file at ``offset``. A negative ``size`` reads until the end of the file.'''
    async def write(self, data: bytes, offset: int=...) -> None: '''Write ``data`` into the file at ``offset``.'''
    async def readline(self, offset: int=..., size: int|None=..., include_newline: bool=...) -> bytes: '''Read a line from the file at ``offset``, up to a maximum of ``size`` bytes if ``size`` is not ``None``, and return it, optionally including the newline character.'''
    async def readlines(self, hint: int=...) -> list[bytes]: '''Read lines from the file until the total size of the lines read reaches or exceeds ``hint`` if ``hint`` is non-negative, and return a list of the lines read.'''
    async def flush(self, offset: int=..., size: int|None=..., /) -> None: '''Flush the file, or a portion of it if ``offset`` and ``size`` are specified. If ``size`` is ``None``, flush until the end of the file.'''
    async def move(self, dest: int, src: int, count: int) -> None: '''Move ``count`` bytes of data within the file starting from ``src`` to ``dest``.'''
    async def __setup__(self) -> None: ...
    async def __cleanup__(self) -> None: ...
    async def seek(self, pos: int, whence: Seek=...) -> None: '''Move the file pointer to ``pos`` according to ``whence``.'''
    def __iter__(self) -> Iterator[bytes]: '''Return an iterator over the lines of the file.'''
    def __aiter__(self) -> AsyncGeneratorType[bytes]: '''Return an asynchronous iterator over the lines of the file.'''
    @property
    def closed(self) -> bool: '''Whether the file and memory map have been closed.'''
    @property
    def open_files(self) -> OpenFiles: '''A dictionary mapping tuples of the form ``(file, mode)`` to the file objects underlying this memory-mapped file.'''
    def fileno(self) -> int: '''Return the file descriptor of the underlying file.'''
    def sync(self) -> None: '''Force the file to be written to disk, in addition to flushing the memory map.'''
    def close(self) -> None: '''Close the memory-mapped file and the underlying file. It is safe to call this method multiple times, but no other methods should be called after closing.'''
    async def aclose(self) -> None: '''Close the memory-mapped file and the underlying file concurrently in async. It is safe to call this method multiple times, but no other methods should be called after closing.'''
    def read_byte(self) -> int: '''Read one byte from the file at the current file pointer, advance the pointer and return the byte as an integer >=0, <256.'''
    def write_byte(self, b: int, /) -> None: '''Write a byte to the file at the current file pointer and advance the pointer.'''
    def resize(self, new_size: int) -> None: '''Resize the file to ``new_size`` bytes. If the file is extended, the added bytes are zero-filled.'''
    def find(self, sub: bytes, start: int|None=..., end: int|None=...) -> int: '''Return the lowest index in the file where the bytes ``sub`` is found, such that ``sub`` is contained in the slice ``file[start:end]``. Return -1 if ``sub`` is not found.'''
    def rfind(self, sub: bytes, start: int|None=..., end: int|None=...) -> int: '''Return the highest index in the file where the bytes ``sub`` is found, such that ``sub`` is contained in the slice ``file[start:end]``. Return -1 if ``sub`` is not found.'''
    def tell(self) -> int: '''Return the current file pointer position.'''
    def size(self) -> int: '''Return the size of the file in bytes.'''
    def isatty(self) -> bool: '''Return whether the file is connected to a TTY device.'''
    def readable(self) -> Literal[True]: '''Return ``True`` unconditionally.'''
    def writable(self) -> Literal[True]: '''Return ``True`` unconditionally.'''
    def seekable(self) -> Literal[True]: '''Return ``True`` unconditionally.'''
    async def writelines(self, lines: Iterable[bytes], /, *, sep: bytes=..., minimize_writes: bool=...) -> None: '''Write each line in ``lines``, followed by ``sep``, into the file. If ``minimize_writes`` is ``True`` (default :const:`~asyncutils.context.Context.MEMORY_MAPPED_IO_MANAGER_DEFAULT_MINIMIZE_WRITES`), write all the lines in one call.'''
    async def read_str(self, offset: int=..., size: int=..., encoding: str=..., errors: str=...) -> str: '''Version of :meth:`read` returning a string instead, decoded with the specified ``encoding`` and ``errors``.'''
    async def write_str(self, text: str, offset: int=..., encoding: str=..., errors: str=...) -> None: '''Write a string to the file at the specified offset, encoded with the specified ``encoding`` and ``errors``.'''
    @overload
    async def smart_write(self, data: str, offset: int=..., encoding: str=..., errors: str=...) -> None: ...
    @overload
    async def smart_write(self, data: bytes, offset: int=...) -> None: '''Write data to the file at the specified offset, automatically encoding strings.'''
    async def copy_range(self, src_offset: int, dest_offset: int, size: int) -> bool: '''Copy a range of bytes from one location to another in the file.'''
    async def fill(self, pattern: bytes, offset: int=..., count: int=...) -> None: '''Fill a range of the file with a repeating pattern of bytes.'''
    async def compare(self, other: Self, /, size: int=..., offset_self: int=..., offset_other: int=...) -> bool: '''Compare a range of bytes in this file with a range in another file.'''
    async def hamming_dist(self, other: Self, /, size: int=..., offset_self: int=..., offset_other: int=...) -> int: '''Calculate the Hamming distance in bits between a range of bytes in this file and a range in another file.'''
    async def hamming_dist_bytes(self, other: Self, /, size: int=..., offset_self: int=..., offset_other: int=...) -> int: '''Calculate the Hamming distance in bytes between a range of bytes in this file and a range in another file.'''
    async def read_until(self, delim: bytes, offset: int=..., maxsize: int=...) -> tuple[bytes, int]: '''Read bytes from the file until the delimiter is found or the maximum size is reached.'''
    async def insert(self, data: bytes, offset: int) -> None: '''Insert data into the file at the specified offset.'''
    async def delete(self, offset: int, size: int) -> None: '''Delete a range of bytes from the file.'''
    async def replace(self, old: bytes, new: bytes, offset: int=..., count: int=...) -> int: '''Replace occurrences of a pattern in the file with a new pattern.'''
    def search_lazy(self, pattern: bytes, offset: int=...) -> AsyncGeneratorType[int]: '''Search for a pattern in the file starting from the specified offset, yielding the offsets of each occurrence found as they are found.'''
    def search_lazy_non_overlapping(self, pattern: bytes, offset: int=...) -> AsyncGeneratorType[int]: '''Version of :meth:`search_lazy` that ensures the offsets returned do not overlap using a greedy approach.'''
    async def search(self, pattern: bytes, offset: int=..., max_results: int=...) -> list[int]: '''Return a list of the offsets of the first ``max_results`` occurrences of ``pattern`` in the file starting from ``offset``.'''
    async def search_non_overlapping(self, pattern: bytes, offset: int=..., max_results: int=...) -> list[int]: '''Version of :meth:`search` that ensures the offsets returned do not overlap using a greedy approach.'''
    async def compact(self) -> int: '''Reduce the size of the file by stripping all contiguous null bytes at the end, and return the number of bytes removed.'''
@type_check_only
class AUnzipConsumer[T]:
    '''The type of each consumer in the tuple return value of :func:`~asyncutils.iters.aunzip`.'''
    def __aiter__(self) -> Self: ...
    async def __anext__(self) -> T: ...
    def close(self) -> None: '''Shut down the underlying queue, such that this consumer no longer receives the values at its position.'''
@type_check_only
class ToSyncFromLoopRV(Protocol):
    '''The signature of the return value of :func:`~asyncutils.util.to_sync_from_loop`.'''
    def __call__[R, **P](self, f: Callable[P, Awaitable[R]], /, timeout: float|None=...) -> Callable[P, R]: ...
@type_check_only
class TransientBlockFromLoopRV(Protocol):
    '''The signature of the return value of :func:`~asyncutils.util.transient_block_from_loop`.'''
    def __call__[T, **P](self, f: Callable[P, T], /, *a: P.args, **k: P.kwargs) -> Future[T]: ...
@type_check_only
class NullContextType:
    '''The type of :const:`~asyncutils.util.anullcontext`; that is, a simple async-only version of :func:`contextlib.nullcontext` that does not depend on :mod:`contextlib`.

    .. note:: This does not support the ``enter_result`` argument of the original.
    '''
    async def __aenter__(self) -> None: ...
    @overload
    async def __aexit__(self, exc_typ: ExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> None: ...
    @overload
    async def __aexit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> None: ...
@type_check_only
class RaiseType(SentinelBase):
    '''The type of :const:`~asyncutils.constants.RAISE`.'''
    def __reduce__(self) -> Literal['RAISE']: ... # ty: ignore[invalid-method-override]
    def is_(self, other: object, /) -> TypeIs[Self]: '''Not actually redefined, but this allows for effective type narrowing.'''
@final
@type_check_only
class WildcardType:
    '''Type of :const:`~asyncutils.channels.EventBus.WILDCARD`.'''
    def __bool__(self) -> Literal[False]: ...
@type_check_only
class EventProtocol(Protocol):
    '''Protocol for event objects.'''
    def is_set(self) -> bool: '''Return whether the event is set.'''
    def set(self) -> None: '''Set the event, allowing any waiters to proceed.'''
    def clear(self) -> None: '''Clear the event, causing future waiters to block until it is set again.'''
    async def wait(self) -> Any: '''Asynchronously wait until the event is set.''' # noqa: ANN401
@type_check_only
class FutProtocol[T](Protocol):
    '''The barest of protocol for future-like objects such that the class is accepted at runtime by :func:`~asyncutils.util.done_fut`. Does not require the object to be awaitable, for instance.'''
    def set_result(self, result: T, /) -> None: '''Set a result on the future, making it available to any waiters.'''
    def set_exception(self, exc: BaseException, /) -> None: '''Set an exception on the future, causing it to be raised by any waiters.'''
    def result(self) -> T: '''Return the result or raise the exception set on the future.'''
    def exception(self) -> BaseException|None: '''Return the exception set on the future if any.'''
@type_check_only
class IncompleteFut[T](FutProtocol[T], PartialInterface): '''Since the type system does not allow modelling a type variable to have an upper bound parametrized by another type variable, this is necessary to type the return type of :func:`~asyncutils.util.done_fut` while losing much type information.'''
@type_check_only
class StrictDualContextFactory(Protocol):
    '''Protocol for the return type of the strict decorator factory overload of :func:`~asyncutils.util.dualcontextmanager`.'''
    @overload
    def __call__[T, **P](self, gfunc: Callable[P, Iterable[T]], /) -> Callable[P, AbstractContextManager[T]]: ...
    @overload
    def __call__[T, **P](self, agfunc: Callable[P, AsyncIterable[T]], /) -> Callable[P, AbstractAsyncContextManager[T]]: ...
@type_check_only
class TaskFactory[T](Protocol):
    def __call__(self, loop: AbstractEventLoop, coro: Coroutine[Any, Any, T], *, name: str|None=..., context: Context|None=..., **k: object) -> T: ...
type IntCompatible = str|SupportsInt|SupportsIndex|Buffer
'''Objects accepted by the :class:`int` constructor.'''
type SupportsIteration[T] = Iterable[T]|AsyncIterable[T]
'''Objects that support (async) iteration.'''
type SupportsRichComparison = SupportsLT|SupportsGT
'''Objects implementing one of the operators < and >.'''
type ExcType = type[BaseException]
'''The type of ``exc_typ`` in :meth:`~object.__exit__` and :meth:`~object.__aexit__` methods.'''
type CanExcept = ExcType|tuple[ExcType, ...]
'''The type of objects that may follow an except statement.'''
type Openable = int|str|bytes|PathLike[str]|PathLike[bytes]
'''Anything that can normally be passed to :func:`open`.'''
type ValidSlice = slice[SupportsIndex|None, SupportsIndex|None, SupportsIndex|None]
'''A slice with start, stop and step being integers or ``None``, representing a slice that typical sequences supporting slicing should accept.'''
type Timer = Callable[[], tyx.JustFloat]
'''Type of functions that return the current time under some specification, such as :func:`time.monotonic`, :func:`time.process_time` and :func:`time.perf_counter`.'''
type All = tuple[str, ...]
'''Type of the :attr:`~module.__all__` attributes of the submodules of :mod:`asyncutils`.'''
type Submodule = Literal['altlocks', 'base', 'buckets', 'channels', 'cli', 'compete', 'config', 'console', 'constants', 'context', 'events', 'exceptions', 'func', 'futures', 'iotools', 'iterclasses', 'iters', 'locks', 'locksmiths', 'misc', 'mixins', 'networking', 'pools', 'processors', 'properties', 'queues', 'rwlocks', 'signals', 'tools', 'util', 'version']
'''Type of strings representing :mod:`asyncutils` submodule names.'''
type Executor = Literal['thread', 'process', 'interpreter', 'loky', 'loky_no_reuse', 'dask', 'ipython', 'elib_flux_cluster', 'elib_flux_job', 'elib_slurm_cluster', 'elib_slurm_job', 'elib_single_node', 'pebble_thread', 'pebble_process', 'deadpool']
'''Type of strings representing executors that can be passed to -e/--executor.'''
type HashAlgorithm = Literal['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'blake2b', 'blake2s', 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512', 'shake_128', 'shake_256']
'''Names of algorithms used for calculating checksums. The default is :const:`~asyncutils.context.Context.MEMORY_MAPPED_IO_MANAGER_DEFAULT_CHECKSUM_ALG`. The BLAKE2 family of algorithms, fast and somewhat secure with a low probability of collision, is the default choice.'''
type OpenRV = AbstractAsyncContextManager[MemoryMappedFile, None]
'''The type of the return values of the :meth:`~asyncutils.iotools.MemoryMappedIOManager.open`, :meth:`~asyncutils.iotools.MemoryMappedIOManager.create` and :meth:`~asyncutils.iotools.MemoryMappedIOManager.create_sparse_file` methods of :class:`~asyncutils.iotools.MemoryMappedIOManager`.'''
type DualContextManager[T] = tyx.Intersection[AbstractContextManager[T, bool], AbstractAsyncContextManager[T, bool]]
'''Return type of :func:`~asyncutils.util.dualcontextmanager`.'''
type OpenFiles = dict[tuple[TextIOWrapper, Literal['r+b', 'w+b', 'x+b']], MemoryMappedFile]
'''The type of the :attr:`~asyncutils.iotools.MemoryMappedIOManager.open_files` property of :class:`~asyncutils.iotools.MemoryMappedIOManager`.'''
type AndHashable[T] = tyx.Intersection[T, Hashable]
'''Most useful on duck-typed classes when specific functions require hashability.'''
type CanCallAndHash[**P] = AndHashable[Callable[P, Awaitable[object]]]
'''A hashable callable returning an awaitable.'''
type SpecificSubscriber = CanCallAndHash[[Any]]
'''The type of subscribers for :class:`~asyncutils.channels.EventBus`.'''
type WildcardSubscriber = CanCallAndHash[[str, Any]]
'''The type of wildcard subscribers for :class:`~asyncutils.channels.EventBus`.'''
if sys.platform == 'win32':
    type Seek = Literal[0, 1, 2]
    '''Possible values of the ``whence`` parameter for :meth:`MemoryMappedFile.seek`, as follows:

    * 0: :data:`~os.SEEK_SET`
    * 1: :data:`~os.SEEK_CUR`
    * 2: :data:`~os.SEEK_END`'''
else:
    type Seek = Literal[0, 1, 2, 3, 4]
    '''Possible values of the ``whence`` parameter for :meth:`MemoryMappedFile.seek`, as follows:

    * 0: :data:`~os.SEEK_SET`
    * 1: :data:`~os.SEEK_CUR`
    * 2: :data:`~os.SEEK_END`
    * 3: :data:`~os.SEEK_DATA`
    * 4: :data:`~os.SEEK_HOLE`'''
type EveryMethodRV[R, T] = Callable[[EveryMethodFT[T, R]], Callable[Concatenate[T, ...], CoroutineType[Any, Any, R|None]]]
'''Return type of :func:`~asyncutils.func.everymethod`.'''
type Observer[**P] = Callable[Concatenate[Any, P], Awaitable[Any]]
'''The type of :class:`~asyncutils.channels.Observable` observers.'''
type RWLockCM = AbstractAsyncContextManager[None, None]
'''The type of the context managers returned by the :meth:`~asyncutils.rwlocks.RWLock.reader` and :meth:`~asyncutils.rwlocks.RWLock.writer` methods of :class:`~asyncutils.rwlocks.RWLock` and subclasses thereof.'''
ExceptionWrapper = NewType('ExceptionWrapper', object)
'''The return type of :func:`~asyncutils.exceptions.wrap_exc`.'''
Mark1 = NewType('Mark1', FaultyConfig)
'''For better type checking. Unstable.'''
Mark2 = NewType('Mark2', FaultyConfig)
'''For better type checking. Unstable.'''
