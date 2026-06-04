'''Asynchronous descriptors, mimicking :class:`property` and optionally applying a lock.'''
from abc import ABC, abstractmethod
from asyncio import Task
from asyncutils import RWLock
from ._internal.types import AsyncContextManager
from collections.abc import Awaitable, Callable
from types import CoroutineType
from typing import Any, Self, overload
__all__ = 'AsyncPropertyBase', 'ConcurrentAsyncProperty', 'LazyAsyncProperty'
class AsyncPropertyBase[T, R](ABC):
    '''A property with asynchronous getters, setters and deleters.'''
    @overload
    def __new__(cls, *, doc: str|None=..., strict: bool=..., hide: bool=...) -> Callable[[Callable[[R], Awaitable[T]]], Self]: ...
    @overload
    def __new__(cls, fget: Callable[[R], Awaitable[T]]|None, fset: Callable[[R, T], Awaitable[None]]|None=..., fdel: Callable[[R], Awaitable[None]]|None=..., *, doc: str|None=..., strict: bool=..., hide: bool=...) -> Self:
        '''| Create a new async property with getter ``fget``, setter ``fset`` and deleter ``fdel``.
        | If the getter is not provided, return a partial decorator instead. In that overload, none of the accessors are to be passed.
        | ``doc``, if passed, will be the docstring of the property in the form of the :attr:`__doc__` attribute. Otherwise, an attempt is made to
        | find it on the getter.
        | ``strict`` defaults to ``True``, and controls whether performing an operation that invokes an unset accessor is allowed. If it is
        | ``False``, setters and deleters are also allowed to return something other than ``None``.
        | If the property has no getter (only possible with explicit ``fget=None`` and at least one of ``fset`` and ``fdel`` passed, which is rare),
        | accessing the attribute on instances would return the property itself if ``strict=False`` and raise an :exc:`AttributeError` otherwise.
        | If ``hide`` is ``True`` (default ``False``), accessing the attribute on the class it is defined in would raise :exc:`AttributeError` as if
        | the property didn't exist.'''
    @overload
    def __get__(self, instance: R, owner: type[R]|None=..., /) -> Self|CoroutineType[Any, Any, T]: ...
    @overload
    def __get__(self, instance: None, owner: type, /) -> Self: ...
    def __set__(self, instance: R, value: T, /) -> None: ...
    def __delete__(self, instance: R, /) -> None: ...
    def __set_name__(self, typ: type[R], name: str, /) -> None: ...
    def __getattr__(self, name: str, /) -> Any: '''Find the attribute on the getter if it exists.'''
    def __reduce__(self) -> str: '''Return the qualified name of this property for pickling. Hidden properties cannot be pickled.'''
    def _setup(self, fget: Callable[[R], Awaitable[T]], /, fset: Callable[[R, T], Awaitable[None]]|None=..., fdel: Callable[[R], Awaitable[None]]|None=..., *, doc: str|None=..., strict: bool=..., hide: bool=...) -> None: '''Set the necessary attributes on the property; called by :meth:`__new__`.'''
    def getter(self, fget: Callable[[R], Awaitable[T]], /) -> Self: '''Return another async property with the given function as the getter.'''
    def setter(self, fset: Callable[[R, T], Awaitable[None]], /) -> Self: '''Return another async property with the given function as the setter.'''
    def deleter(self, fdel: Callable[[R], Awaitable[None]], /) -> Self: '''Return another async property with the given function as the deleter.'''
    @abstractmethod
    def _inner_helper[X](self, aw: Awaitable[X], /) -> Awaitable[X]: '''Return an awaitable resolving to the result of an awaitable, limited to those returned by the setter or deleter. This can be a coroutine, a future, a task or anything else, and affects the strategy used to handle assignments and deletions which must return synchronously but run in the background.'''
    @property
    def fget(self) -> Callable[[R], Awaitable[T]]|None: '''The getter function for this property, or ``None`` if it doesn't exist.'''
    @property
    def fset(self) -> Callable[[R, T], Awaitable[None]]|None: '''The setter function for this property, or ``None`` if it doesn't exist.'''
    @property
    def fdel(self) -> Callable[[R], Awaitable[None]]|None: '''The deleter function for this property, or ``None`` if it doesn't exist.'''
    def __init_subclass__(cls, /, *, lock_factory: Callable[[], AsyncContextManager[Any]]=..., **k: object) -> None: '''``lock_factory``, a callable that returns a new per-instance async context manager, is required for immediate subclasses.'''
    __doc__: str|None
    '''The docstring for this property, or ``None`` if it doesn't exist.'''
    __name__: str
    '''The name of this property, determined by the function it decorates.'''
    __module__: str|None
    '''The module this property is defined in, determined by the function it decorates.'''
class LazyAsyncProperty[T, R](AsyncPropertyBase[T, R]):
    '''Queue set and delete operations, and complete them in order only when a get is called.'''
    def _inner_helper[X](self, aw: Awaitable[X], /) -> CoroutineType[Any, Any, X]: ...
    __doc__: str|None
    '''The docstring for this property, or ``None`` if it doesn't exist.'''
    __name__: str
    '''The name of this property, determined by the function it decorates.'''
    __module__: str|None
    '''The module this property is defined in, determined by the function it decorates.'''
class ConcurrentAsyncProperty[T, R](AsyncPropertyBase[T, R]):
    '''| Allow set and delete operations to run concurrently once the operations are called, without any guarantee on the order of
    | execution.
    | The setters and deleters can be implemented acquire a writer lock and the getter the corresponding reader lock from
    | :mod:`~asyncutils.rwlocks` with its lock policies that provide fluent decorator interfaces. Note, however, that the accessor
    | decorators must be outermost because they turn callables into properties.'''
    def _inner_helper[X](self, aw: Awaitable[X], /) -> Task[X]: '''Return a task for the awaitable returned by the setter or deleter.'''
    __doc__: str|None
    '''The docstring for this property, or ``None`` if it doesn't exist.'''
    __name__: str
    '''The name of this property, determined by the function it decorates.'''
    __module__: str|None
    '''The module this property is defined in, determined by the function it decorates.'''
class RWLockedAsyncProperty[T, R](ConcurrentAsyncProperty[T, R]):
    __doc__: str|None
    '''The docstring for this property, or ``None`` if it doesn't exist.'''
    __name__: str
    '''The name of this property, determined by the function it decorates.'''
    __module__: str|None
    '''The module this property is defined in, determined by the function it decorates.'''
    @overload
    def __new__(cls, *, policy: type[RWLock]=..., doc: str|None=..., strict: bool=..., hide: bool=...) -> Callable[[Callable[[R], Awaitable[T]]], Self]: ...
    @overload
    def __new__(cls, fget: Callable[[R], Awaitable[T]]|None, fset: Callable[[R, T], Awaitable[None]]|None=..., fdel: Callable[[R], Awaitable[None]]|None=..., *, policy: type[RWLock]=..., doc: str|None=..., strict: bool=..., hide: bool=...) -> Self: ...
    def _setup(self, f: Callable[[R], Awaitable[T]], /, fset: Callable[[R, T], Awaitable[None]]|None=None, fdel: Callable[[R], Awaitable[None]]|None=None, *, policy: type[RWLock]=..., **k: Any) -> None: ...
