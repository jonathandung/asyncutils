'''Defines interfaces and type aliases used in this module's stubs. Pseudo-stable (deprecation periods will span at least 2 minor versions).
This is a fake module in the sense that the names in this stub are all None at runtime, so do not inherit from its 'protocols'.
This facilitates lightweight inline type annotations.'''
from _collections_abc import Awaitable, Iterator, Iterable, AsyncIterable, Callable, Generator, Coroutine, Buffer
from io import TextIOWrapper, _WrappedBuffer
from types import TracebackType, FunctionType
from typing import Protocol, Self, SupportsIndex, SupportsInt, Any, Literal, overload, type_check_only, final
from ..constants import sentinel_base
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
    '''An asynchronous context manager. Basically `contextlib.AbstractAsyncContextManager` with proper overloads, as a protocol.'''
    async def __aenter__(self) -> T: ...
    @overload
    async def __aexit__(self, exc_typ: ValidExcType, exc_val: BaseException, exc_tb: TracebackType|None, /) -> bool|None: ...
    @overload
    async def __aexit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> bool|None: ...
@type_check_only
class AsyncLockLike(AsyncContextManager, Protocol):
    '''An object that behaves like an asynchronous lock.'''
    async def acquire(self) -> bool|None: ...
    def release(self) -> None|Awaitable[None]: ...
    def locked(self) -> bool: ...
@type_check_only
class GenericSized[T](Protocol):
    '''`typing.Sized` is not generic, so here is a generic version of it.'''
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[T]: ...
@type_check_only
class SupportsSlicing[T](GenericSized[T], Protocol):
    '''Protocol for iterables with size, and index and slice access.'''
    @overload
    def __getitem__(self, idx: ValidSlice, /) -> GenericSized[T]: ...
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
    '''An object that represents a path. Basically os.PathLike, but a Protocol.'''
    def __fspath__(self) -> T: ...
@type_check_only
class SupportsPop[T](Protocol):
    def pop(self) -> T: ...
@type_check_only
class SupportsPopLeft[T](Protocol):
    def popleft(self) -> T: ...
@type_check_only
class GeneratorCoroutine[Y, S, R](Generator[Y, S, R], Coroutine[Y, S, R]):
    '''Objects such as those returned by `types.coroutine`-decorated generator functions.'''
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
    If it is only known that a class implements an interface (e.g. the PEP 3148 Future interface), type checkers might throw errors on unrecognized attributes
    that may actually exist on the object/class. This is a simplistic fix that assumes those attributes always exist, with type Any.'''
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
    '''Represents a middleware accepted by `channels.EventBus`.
    To facilitate O(1) removal of middlewares and order preservation, it is unfortunately impossible to add the same middleware into the pipe twice.
    Therefore, it is suggested that a lightweight wrapper lambda around a function containing the main logic be used.'''
    def __call__(self, event_type: str, data: Any, /) -> Any: ...
    def __hash__(self) -> int: ...
@type_check_only
class Bag(dict[str, Any]):
    '''A thin dictionary subclass that supports attribute access.'''
    def __getattr__(self, key: str, /) -> Any: ...
    def __setattr__(self, key: str, value: Any, /) -> None: ...
    def __delattr__(self, key: str, /) -> None: ...
@final
@type_check_only
class Sentinel(sentinel_base):
    '''Common type of sentinels for this module, internal or public.'''
    @property
    def bound_to(self) -> None: ...
    def __reduce__(self) -> str: '''These sentinels are accessible in the top level of the asyncutils.constants namespace.'''
type IntCompatible = str|SupportsInt|SupportsIndex|Buffer
'''Objects accepted by the int constructor.'''
type SupportsIteration[T] = Iterable[T]|AsyncIterable[T]
'''Objects that support (async) iteration.'''
type SupportsRichComparison = SupportsLT|SupportsGT
type ValidExcType = type[BaseException]
'''The type of exc_typ in __exit__ and __aexit__ methods.'''
type Exceptable = ValidExcType|tuple[ValidExcType, ...]
'''Objects that may follow an except statement.'''
type Openable = int|str|bytes|PathLike[str]|PathLike[bytes]
'''Anything that can normally be passed to the built-in open function.'''
type ValidSlice = slice[SupportsIndex|None, SupportsIndex|None, SupportsIndex|None]
'''A slice with start, stop and step being integers or None, representing a slice that typical sequences supporting slicing should accept.'''
type Timer = Callable[[], float]
'''Type of functions that return the current time under some specification, such as time.monotonic, time.process_time and time.perf_counter.'''
type All = tuple[str, ...]
'''Type of the __all__ attributes of asyncutils' submodules.'''
type Submodule = Literal['altlocks', 'base', 'buckets', 'caches', 'channels', 'cli', 'compete', 'config', 'console', 'constants', 'context', 'events', 'exceptions', 'func', 'futures', 'io', 'iterclasses', 'iters', 'locks', 'misc', 'mixins', 'networking', 'pools', 'processors', 'properties', 'queues', 'signals', 'tools', 'util', 'version']
'''Type of strings representing asyncutils submodule names.'''
type Executor = Literal['thread', 'process', 'interpreter', 'loky_noreuse', 'loky', 'dask', 'ipython', 'elib_flux_cluster', 'elib_flux_job', 'elib_slurm_cluster', 'elib_slurm_job', 'elib_single_node', 'pebble_thread', 'pebble_process']
'''Type of strings representing executors that can be passed to -e/--executor.'''