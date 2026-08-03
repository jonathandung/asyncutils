'''
| Provides asynchronous file-like interfaces to the following: coupled reader and writer, write-one-end-and-read-the-other pipes, and memory maps.
| Does not depend on `aiofiles <https://pypi.org/p/aiofiles>`__ or any such library.
| Executors of the type determined by the module configuration are used.

.. note::
  This library is not designed specifically for I/O, and the functionality in this submodule is far from comprehensive.
  See `aiostream <https://aiostream.readthedocs.io/en/stable>`__ or similar for that.
'''
from ._internal.helpers import LoopMixinBase
from ._internal.prots import ExcType, HashAlgorithm, MemoryMappedFile, OpenFiles, OpenRV, PipePairCM, StdCoupType
from .config import Executor
from _typeshed import FileDescriptorOrPath
from collections.abc import Buffer, Callable, Iterable
from contextlib import AbstractAsyncContextManager
from mmap import mmap
from types import TracebackType
from typing import Any, IO, Literal, NoReturn, Self, overload
from weakref import WeakSet
__all__ = 'AsyncReadWriteCouple', 'MemoryMappedIOManager', 'ainput', 'double_ended_binary_pipe', 'double_ended_text_pipe', 'stdcoup'
def double_ended_text_pipe(*, pipe_impl: Callable[[], tuple[int, int]]=...) -> PipePairCM[str]:
    '''
    | Return a dual context manager resolving to a tuple of two :class:`AsyncReadWriteCouple`'s in text mode, such that each can read what the other writes.
    | Two operating system level pipes are created.
    | Pass a function that returns a tuple of two integer file descriptors for ``pipe_impl`` (default :func:`os.pipe`) to customize this behaviour.
    '''
def double_ended_binary_pipe(*, pipe_impl: Callable[[], tuple[int, int]]=...) -> PipePairCM[bytes]: ''':func:`double_ended_text_pipe`, but opens the pipes in binary mode.'''
class AsyncReadWriteCouple[T: (str, bytes), R: (str, bytes)](LoopMixinBase):
    '''
    | An asynchronous file-like interface to a readable and writable object.
    | Delegates its methods to the underlying reader and writer, but makes them non-blocking by running in an executor.
    | Preferably, the executor should be a thread pool, but that is ultimately determined by the library configuration.

    .. note:: This class only wraps typical file-like objects implementing the :class:`io.IOBase` interface, not :mod:`asyncio` streams, because they have different, already async methods.
    .. seealso::

      :class:`io.BufferedRWPair`
        The standard library synchronous equivalent. Some of its methods may not be present here.
    '''
    async def __aenter__(self) -> Self: ...
    @overload
    async def __aexit__(self, exc_typ: ExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> None: ...
    @overload
    async def __aexit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> None: ...
    @property
    def reader(self) -> IO[T]: '''The underlying reader.'''
    @property
    def writer(self) -> IO[R]: '''The underlying writer.'''
    @property
    def executor(self) -> Executor: '''The underlying executor.'''
    def __init__(self, reader: IO[T], writer: IO[R], /, executor: Executor|None=..., *, find_attr_on_writer_first: bool=...): '''Initialize the couple with the given reader, writer and optionally a :pep:`3148` executor to call the file methods in, after checking that the reader is readable and the writer is writable.'''
    def __getattr__(self, name: str, /) -> Any: '''Search for the attribute on the writer first if ``find_attr_on_writer_first=True`` was passed and the reader otherwise.''' # ruff: ignore[any-type]
    async def aclose(self) -> None: '''Close the reader and writer asynchronously and shut down the underlying executor. It is safe to close a file multiple times, but no other methods should be called after closing.'''
    async def flush(self) -> None: '''Asynchronously flush the writer.'''
    async def read(self, n: int=..., /) -> T: '''Read ``n`` characters from the reader.'''
    async def read1(self, n: int=..., /) -> T: '''Call the :meth:`~io.BufferedIOBase.read1` method on the reader.'''
    async def readall(self) -> T: '''Read all characters from the reader until EOF. If the :meth:`~io.RawIOBase.readall` method is not present, call :meth:`~io.TextIOBase.read` with no arguments without handling the non-blocking case.'''
    async def readinto(self, buffer: Buffer, /) -> int:
        '''
        | Read into the writable bytes-like object ``buffer`` from the reader, returning the number of bytes read.
        | Calls the :meth:`~io.RawIOBase.readinto` method of the reader if it exists and falls back to the :meth:`~io.TextIOBase.read` method.
        | The case where the underlying implementation of :meth:`read` returns ``None`` or raises :exc:`BlockingIOError` is not considered.
        '''
    async def readinto1(self, buffer: Buffer, /) -> int: '''Call the :meth:`~io.BufferedIOBase.readinto1` method of the reader. There is no fallback implementation.'''
    async def readline(self, limit: int=..., /) -> T: '''Read a line, of length at most ``limit``, from the reader.'''
    async def readlines(self, hint: int=..., /) -> list[T]: '''Collect lines of the file into a list until at least ``hint`` characters are read (if available), and a line boundary is encountered.'''
    async def truncate(self, size: int|None=..., /) -> int: '''Truncate the file at ``size`` (or the current position if not passed), and return the new file size.'''
    async def write(self, s: R, /) -> int: '''Write ``s`` into the writer, returning the number of characters written.'''
    async def writelines(self, lines: Iterable[R], /) -> None: '''Write the lines from the iterable into the writer without adding newline as separators.'''
    def fileno(self) -> NoReturn: '''Raise :exc:`OSError` with errno :data:`~errno.EBADF`.'''
    def isatty(self) -> NoReturn: '''Raise :exc:`OSError` with errno :data:`~errno.ENOTSUP`.'''
    def readable(self) -> Literal[True]: '''Return ``True``, because prior verification has been done that the reader is readable, and that is assumed not to be invalidated.'''
    def seek(self, offset: int, whence: int=..., /) -> NoReturn: '''Raise :exc:`OSError` with errno :data:`~errno.ESPIPE`.'''
    def seekable(self) -> Literal[False]: '''Return ``False`` since the couple itself is not seekable, but the reader and writer may be..'''
    def tell(self) -> NoReturn: '''Raise :exc:`OSError` with errno :data:`~errno.ESPIPE`.'''
    def writable(self) -> Literal[True]: '''Return ``True``, because prior verification has been done that the writer is writable, and that is assumed not to be invalidated.'''
    @property
    def closed(self) -> bool: '''Whether both the reader and writer have been closed.'''
stdcoup: StdCoupType
'''Instance of :class:`AsyncReadWriteCouple` that combines standard input and output. Special-cased such that this is unusable as an async context manager.'''
async def ainput(prompt: str=..., assert_tty: bool=...) -> str: '''Asynchronously write ``prompt`` to standard output and read a line from standard input, returning it without the trailing newline. If ``assert_tty`` is ``True``, raise :exc:`OSError` if standard input is not a TTY (You need only pass this the first time you call the function).'''
class MemoryMappedIOManager(LoopMixinBase):
    '''
    An asynchronous object-oriented manager interface to memory-mapped I/O, that optimizes batch operations using an event loop.

    .. tip:: One global instance of this is most likely enough.
    '''
    def __init__(self, executor: Executor|None=...): '''Initialize the manager with the executor to be used for its operations.'''
    @property
    def open_maps(self) -> WeakSet[mmap]: '''Instance of :class:`~weakref.WeakSet` containing the maps managed by this manager.'''
    @property
    def currently_open(self) -> int: '''Number of currently open memory maps.'''
    @property
    def open_paths(self) -> dict[FileDescriptorOrPath, Literal['r+b', 'w+b', 'x+b']]: '''Dictionary mapping file paths as passed to :meth:`open`, :meth:`create` or :meth:`create_sparse_file` to the mode the file was opened with.'''
    @property
    def open_files(self) -> OpenFiles: '''Dictionary mapping tuples of the form ``(file, mode)`` to the managed file objects.'''
    def open(self, path: FileDescriptorOrPath, init_size: int=...) -> OpenRV: '''Open a file at ``path`` for memory-mapped reading and writing on entry and close it on exit. The file must exist and is not truncated.'''
    def create(self, path: FileDescriptorOrPath, init_size: int=..., *, exclusive: bool=...) -> OpenRV: '''Open a file at ``path`` for memory-mapped writing and reading on entry and close it on exit. The file is truncated to the beginning, and may exist if and only if ``exclusive=False`` is passed.'''
    def create_sparse_file(self, path: FileDescriptorOrPath, total_size: int, chunks: Iterable[tuple[int, bytes|str]]) -> OpenRV: '''Return an async context manager that creates a file of size ``total_size`` at ``path``, with ``chunks`` mapping offsets to the data to be written there. Data from old chunks is overwritten by that from new ones.'''
    def prefetch_files(self, *paths: FileDescriptorOrPath, init_size: int=...) -> AbstractAsyncContextManager[list[MemoryMappedFile], None]: '''Prefetch existing files at ``paths`` for memory-mapped I/O into memory at once, closing them simultaneously on exit.'''
    async def copy_file(self, src: FileDescriptorOrPath, dest: FileDescriptorOrPath, *, exclusive: bool=..., flush: bool=...) -> None: '''Copy the contents of the file at ``src`` into that at ``dest`` asynchronously and flush it if ``flush`` is ``True``. Uses :meth:`open` and :meth:`create` internally.'''
    async def checksum(self, path: FileDescriptorOrPath, alg: HashAlgorithm=...) -> str:
        '''
        | Compute a checksum from the file at ``path`` using the specified algorithm (default :const:`~asyncutils.context.Context.MEMORY_MAPPED_IO_MANAGER_DEFAULT_CHECKSUM_ALG`).
        | ``usedforsecurity=False`` is passed to the :func:`hashlib.new` constructor to bypass FIPS restrictions, such that broken algorithms like MD5 are always allowed if explicitly requested, seeing as though they are fast and enough to prevent accidental file corruption in simple cases.

        .. caution:: If executing cryptographic checksums, never pass MD5 or SHA1. Use the factory default (BLAKE2 family), SHA256, or similar.
        .. danger:: Calling without the ``alg`` parameter may cause a faulty algorithm to be chosen if the value in the current context dictates so.
        .. seealso::

          :data:`hashlib.algorithms_available`
            The set of supported algorithms on your system and installation.

          `The relevant FIPS specification <https://csrc.nist.gov/pubs/fips/140-2/upd2/final>`__
            For the security requirements of the algorithms.

          `The Wikipedia article <https://en.wikipedia.org/wiki/Checksum>`__
            For basic information pertaining to checksums and their use cases.
        '''
    async def approx_memory_usage(self) -> int: '''Compute the approximate memory used by the currently open memory maps in bytes.'''
    async def bulk_read[T: FileDescriptorOrPath](self, file_offsets: Iterable[tuple[T, Iterable[tuple[int, int]]]]) -> dict[T, list[bytes]]: '''Read from each file at their corresponding offsets as specified by the value in the ``file_offsets`` mapping, which should be an iterable of tuples ``(offset, size)`` or ``None`` if the whole file is to be read.'''
    async def bulk_write(self, file_data: Iterable[tuple[FileDescriptorOrPath, Iterable[tuple[bytes, int]]]]) -> None: '''Write into each file at their corresponding offsets as specified by the value in the ``file_data`` mapping, which should be an iterable of tuples ``(data, offset)``.'''
    async def bulk_checksum[T: FileDescriptorOrPath](self, paths: Iterable[T], alg: HashAlgorithm=...) -> dict[T, str]: '''Compute checksums from the files at ``paths`` using the specified algorithm, defaulting to :const:`~asyncutils.context.Context.MEMORY_MAPPED_IO_MANAGER_DEFAULT_CHECKSUM_ALG`. The same remarks from :meth:`checksum` apply here.'''
    async def bulk_copy(self, pairs: Iterable[tuple[FileDescriptorOrPath, FileDescriptorOrPath]]) -> None: '''Copy the contents of each file in the first position of the tuples in ``pairs`` into the file in the second position asynchronously. If you have a dictionary, pass in its items view.'''
    async def bulk_resize(self, sizes: Iterable[tuple[FileDescriptorOrPath, int]]) -> None: '''Resize each file at the keys of ``sizes`` to the corresponding value asynchronously.'''
    async def compact_files(self, paths: Iterable[FileDescriptorOrPath]) -> None: '''Reduce the size of each file at ``paths`` by truncating the trailing null bytes asynchronously.'''
    async def find_in_files[T: FileDescriptorOrPath](self, pattern: bytes, paths: Iterable[tuple[T, int]], max_per_file: int=..., *, allow_overlapping: bool=...) -> dict[T, list[int]]: '''Find all occurrences of ``pattern`` in the files at ``paths``, returning a mapping from each file to a list of offsets where the pattern was found.'''
    async def __aenter__(self) -> Self: ...
    @overload
    async def __aexit__(self, exc_typ: ExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> None: ...
    @overload
    async def __aexit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> None: ...
