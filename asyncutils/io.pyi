'''Provides asynchronous file-like interfaces to the following: coupled reader and writer, write-one-end-and-read-the-other pipes,
and memory maps. Does not depend on `aiofiles` or any such library.'''
from ._internal.protocols import HashAlgorithm, MemoryMappedFile, Openable, OpenFiles, OpenRV
from .config import Executor
from .mixins import LoopContextMixin
from _collections_abc import Callable, Iterable, Mapping
from contextlib import _AsyncGeneratorContextManager
from mmap import mmap
from typing import IO, Any, Literal
from weakref import WeakSet
__all__ = 'AsyncReadWriteCouple', 'MemoryMappedIOManager', 'double_ended_binary_pipe', 'double_ended_text_pipe'
def double_ended_text_pipe(pipe_impl: Callable[[], tuple[int, int]]=...) -> tuple[AsyncReadWriteCouple[str, str], AsyncReadWriteCouple[str, str]]:
    '''Return a tuple of two `AsyncReadWriteCouple`s, such that each can read what the other writes. Two os-level pipes must be created.
    Pass a function that returns a tuple of two integer file descriptors for `pipe_impl` (default os.pipe) to customize this behaviour.'''
def double_ended_binary_pipe(pipe_impl: Callable[[], tuple[int, int]]=...) -> tuple[AsyncReadWriteCouple[bytes, bytes], AsyncReadWriteCouple[bytes, bytes]]: ...
class AsyncReadWriteCouple[T: (str, bytes), R: (str, bytes)](LoopContextMixin):
    '''An asynchronous file-like interface to a readable and writable object, which really just delegates its methods to the underlying reader and writer.
    The methods are made truly async using an executor and event loop, the type of which is determined from the module configuration.'''
    @property
    def reader(self) -> IO[T]: '''The underlying reader.'''
    @property
    def writer(self) -> IO[R]: '''The underlying writer.'''
    def __init__(self, reader: IO[T], writer: IO[R], /): ...
    def __getattr__(self, name: str, /) -> Any: ...
    async def aclose(self) -> None: '''Close the reader and writer asynchronously and shut down the underlying executor. It is safe to close a file multiple times, but no other methods should be called after closing.'''
    async def flush(self) -> None: '''Asynchronously flush the writer.'''
    async def read(self, n: int=..., /) -> T: '''Read `n` characters from the reader.'''
    async def readline(self, limit: int=..., /) -> T: '''Read a line, of length at most `limit`, from the reader.'''
    async def readlines(self, hint: int=..., /) -> list[T]: '''Collect lines of the file into a list until at least `hint` characters are read (if available), and a line boundary is encountered.'''
    async def truncate(self, size: int|None=..., /) -> int: '''Truncate the file at `size` (or the current position if not passed), and return the new file size.'''
    async def write(self, s: R, /) -> int: '''Write `s` into the writer, returning the number of characters written.'''
    async def writelines(self, lines: Iterable[R], /) -> None: '''Write the lines from the iterable into the writer without adding newline as separators.'''
    def fileno(self) -> int: '''Raise OSError.'''
    def isatty(self) -> bool: '''Whether at least one of the reader or the writer is connected to a terminal.'''
    def readable(self) -> bool: '''Whether the reader can be read from.'''
    def seek(self, offset: int, whence: int=..., /) -> int: '''Raise OSError.'''
    def seekable(self) -> bool: '''Whether both streams support random access.'''
    def tell(self) -> int: '''Raise OSError.'''
    def writable(self) -> bool: '''Whether the writer can be written into.'''
    @property
    def closed(self) -> bool: '''Whether the file has been closed.'''
    __cleanup__ = aclose
class MemoryMappedIOManager(LoopContextMixin):
    '''An asynchronous object-oriented manager interface to memory-mapped I/O, that optimizes batch operations using an event loop.
    You probably only need one instance of this.
    In the docstrings below, `mgr` will be an instance of this class.'''
    def __init__(self, executor: Executor|None=...): ...
    @property
    def open_mmaps(self) -> WeakSet[mmap]: '''Instance of `weakref.WeakSet` containing the maps managed by this manager.'''
    @property
    def currently_open(self) -> int: '''Number of currently open memory maps.'''
    @property
    def open_paths(self) -> dict[Openable, Literal['r+b', 'w+b', 'x+b']]: '''Dictionary mapping file paths as passed to `mgr.open`, `mgr.create` or `mgr.create_sparsef` to the mode the file was opened with.'''
    @property
    def open_files(self) -> OpenFiles: '''Dictionary mapping tuples of the form `(file, mode)` to the managed file objects.'''
    @open_files.deleter
    def open_files(self) -> None: '''Clear the dictionary of open files.'''
    def open(self, path: Openable, init_size: int=...) -> OpenRV: '''An async context manager that opens a file at `path` for memory-mapped reading and writing on entry and closes it on exit. The file must exist and is not truncated.'''
    def create(self, path: Openable, init_size: int=..., *, exclusive: bool=...) -> OpenRV: '''An async context manager that opens a file at `path` for memory-mapped writing and reading on entry and closes it on exit. The file is truncated to the beginning, and must not exist if `exclusive` is `True` (the default behaviour).'''
    def create_sparsef(self, path: Openable, total_size: int, chunks: Mapping[int, bytes|str]) -> OpenRV: '''An async context manager that creates a file of size `total_size` at `path`, with `chunks` mapping offsets to the data to be written there. Though it is technically undefined behaviour to have overlapping chunks, the implementation overwrites data from old chunks with that from new ones.'''
    def prefetch_files(self, *paths: Openable, init_size: int=...) -> _AsyncGeneratorContextManager[list[MemoryMappedFile], None]: '''Prefetch existing files at `paths` for memory-mapped I/O into memory at once, closing them simultaneously on exit.'''
    async def __cleanup__(self) -> None: ...
    async def copy_file(self, srcp: Openable, destp: Openable) -> None: ...
    async def checksum(self, path: Openable, alg: HashAlgorithm=...) -> str: ...
    async def approx_memory_usage(self) -> int: ...
    async def bulk_read(self, file_offsets: Mapping[Openable, Iterable[tuple[int, int]]]) -> dict[Openable, list[bytes]]: ...
    async def bulk_write(self, file_data: Mapping[Openable, Iterable[tuple[bytes, int]]]) -> None: ...
    async def bulk_checksum(self, paths: Iterable[Openable], alg: HashAlgorithm=...) -> dict[Openable, str]: ...
    async def bulk_copy(self, pairs: Iterable[tuple[Openable, Openable]]) -> None: ...
    async def bulk_resize(self, sizes: Mapping[Openable, int]) -> None: ...
    async def compact_files(self, paths: Iterable[Openable]) -> None: ...
    async def find_in_files(self, pattern: bytes, paths: Mapping[Openable, int], max_per_file: int=..., *, allow_overlapping: bool=...) -> dict[Openable, list[int]]: ...