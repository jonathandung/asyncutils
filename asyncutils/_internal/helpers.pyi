'''Miscellaneous helper routines for :mod:`asyncutils` submodules that are not meant to be called by the user.'''
from .prots import CanClearAndCopy
from ..config import Executor
from asyncio import AbstractEventLoop, Future, Task
from collections.abc import Awaitable, Callable, Iterable
from ty_extensions import Not
from types import GeneratorType, ModuleType
from typing import Any, overload
from typing_extensions import TypeIs
def filter_out(*a: object, s: object=...) -> GeneratorType[Any]: '''Yield items in the positional arguments not identical to the sentinel ``s``, or ``None`` by default.'''
def get_loop_and_set() -> AbstractEventLoop: '''Return the running event loop. If there is none, create and set one first.'''
def check_methods(obj: object, /, *meth: str) -> bool: '''Re-implement :func:`!collections.abc._check_methods`.'''
def copy_and_clear[T: CanClearAndCopy[Any]](l: T) -> T: '''Copy the given object, clear it, and return the copy.'''
def ismodule(o: object, /) -> TypeIs[ModuleType]: '''Whether the given object is a module, or an :mod:`asyncutils`-internal submodule object.'''
def subscriptable[T: type](cls: T, /) -> T: '''Add a :meth:`~object.__class_getitem__` method to the given class, raising :exc:`TypeError` if it is already present.'''
def check(candidate: object, against: object, /) -> bool: '''Check if two objects are equal without calling the :meth:`~object.__eq__` method of the candidate, such that it cannot falsely claim equality.'''
def create_executor(obj: object, /, save: bool=...) -> Executor: '''Return an :class:`~asyncutils.config.Executor` instance for the given object, creating one if necessary, and saving it on the object as the ``executor`` attribute if ``save=False`` was not passed.'''
@overload
def coerce_callable[T: Callable[..., Any]](f: T, /) -> T: ...
@overload
def coerce_callable[T: Not[Callable[..., Any]]](o: T, /) -> type[T]: '''Return the callable itself if the argument is callable, and return its type otherwise.'''
def fullname(f: object, /, remove_prefix: bool=...) -> str: '''Return the fully-qualified name of the given object, including its module, optionally removing the ``'asyncutils'`` prefix.'''
async def simple_wrap[T](aw: Awaitable[T], /) -> T: '''Return a coroutine wrapping the given awaitable. Use :func:`~asyncutils.util.wrap_in_coro` instead for better error handling.'''
class LoopMixinBase:
    '''The base class for :class:`~asyncutils.mixins.LoopContextMixin`.'''
    @property
    def loop(self) -> AbstractEventLoop: '''The underlying event loop.'''
    def make[T](self, aw: Awaitable[T], /) -> Task[T]: '''Create a :class:`~asyncio.Task` for the given awaitable that runs in the underlying loop.'''
    def make_fut(self) -> Future[Any]: '''Create a :class:`~asyncio.Future` attached to the underlying loop.'''
    def make_multiple[T](self, aws: Iterable[Awaitable[T]], /) -> GeneratorType[Task[T]]: '''Return an iterator over instances of :class:`~asyncio.Task` created for each coroutine in C, in that order.'''
class Bag(dict[str, Any]): # noqa: FURB189
    '''A thin dictionary subclass that supports attribute access, setting and deleting.'''
    def __getattr__(self, key: str, /) -> Any: ... # noqa: ANN401
    def __setattr__(self, key: str, value: object, /) -> None: ...
    def __delattr__(self, key: str, /) -> None: ...
