'''Asynchronous descriptors, mimicking :class:`property` and optionally applying a lock.'''
from abc import ABC, abstractmethod
from asyncio import Task
from collections.abc import Awaitable, Callable
from types import CoroutineType
from typing import Any, Concatenate, Self, final, overload
__all__ = 'AsyncPropertyBase', 'ConcurrentAsyncProperty', 'LazyAsyncProperty', 'coercedmethod'
class AsyncPropertyBase[T, R](ABC):
    '''A property with asynchronous getters, setters and deleters.'''
    @overload
    def __new__(cls, *, doc: str|None=..., strict: bool=..., hide: bool=...) -> Callable[[Callable[[R], Awaitable[T]]], Self]: ...
    @overload
    def __new__(cls, fget: Callable[[R], Awaitable[T]]|None, fset: Callable[[R, T], Awaitable[None]]|None=..., fdel: Callable[[R], Awaitable[None]]|None=..., *, doc: str|None=..., strict: bool=..., hide: bool=...) -> Self:
        '''| Create a new async property with getter `fget`, setter `fset` and deleter `fdel`.
        | If the getter is not provided, return a partial decorator instead. In that overload, none of the accessors are to be passed.
        | ``doc``, if passed, will be the docstring of the property in the form of the :attr:`__doc__` attribute. Otherwise, an attempt is made to
        | find it on the getter.
        | ``strict`` defaults to ``True``, and controls whether performing an operation that invokes an unset accessor is allowed. If ``strict`` is
        | ``False``, setters and deleters are also allowed to return something other than ``None``.
        | If the property has no getter (only possible with explicit `fget=None` and at least one of `fset` and `fdel` passed, which is rare),
        | accessing the attribute on instances would return the property itself if `strict=False` and raise an :exc:`AttributeError` otherwise.
        | If `hide` is ``True`` (default ``False``), accessing the attribute on the class it is defined in would raise as if the property didn't exist.'''
    @overload
    def __get__(self, instance: R, owner: type[R]|None=..., /) -> Self|T: ...
    @overload
    def __get__(self, instance: None, owner: type, /) -> Self: ...
    def __set__(self, instance: R, value: T, /) -> None: ...
    def __delete__(self, instance: R, /) -> None: ...
    def __set_name__(self, typ: type[R], name: str, /) -> None: ...
    def __getattr__(self, name: str, /) -> Any: '''Find the attribute on the getter if it exists.'''
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
    __doc__: str|None
    '''The docstring for this property, or ``None`` if it doesn't exist.'''
    __name__: str
    '''The name of this property, determined by the function it decorates.'''
    __module__: str|None
    '''The module this property is defined in, determined by the function it decorates.'''
class LazyAsyncProperty[T, R](AsyncPropertyBase[T, R]):
    '''Queue set and delete operations, and complete them in order only when a get is called.'''
    def _inner_helper[X](self, aw: Awaitable[X], /) -> CoroutineType[Any, Any, X]: ...
    @property
    def __doc__(self) -> str|None: '''The docstring for this property, or ``None`` if it doesn't exist.'''
    @property
    def __name__(self) -> str: '''The name of this property, determined by the function it decorates.'''
class ConcurrentAsyncProperty[T, R](AsyncPropertyBase[T, R]):
    '''| Allow set and delete operations to run concurrently once the operations are called, without any guarantee on the order of
    | execution.
    | The setters and deleters can be implemented acquire a writer lock and the getter the corresponding reader lock from
    | :mod:`~asyncutils.rwlocks` with its lock policies that provide fluent decorator interfaces. Note, however, that the accessor
    | decorators must be outermost because they turn callables into properties.'''
    def _inner_helper[X](self, aw: Awaitable[X], /) -> Task[X]: '''Return a task for the awaitable returned by the setter or deleter.'''
    @property
    def __doc__(self) -> str|None: '''The docstring for this property, or ``None`` if it doesn't exist.'''
    @property
    def __name__(self) -> str: '''The name of this property, determined by the function it decorates.'''
@final
class coercedmethod[T, R, **P]: # noqa: N801
    '''Interpret any callable as a regular function in a class body so that access on instance returns something like a bound method.'''
    def __init__(self, func: Callable[Concatenate[R, P], T], /): ...
    def __getattr__(self, name: str, /) -> Any: ...
    def __set_name__(self, owner: type[R], name: str, /) -> None: ...
    def __get__(self, instance: R, owner: type[R]|None=..., /) -> Callable[P, T]: '''Return the 'bound method'. The descriptor itself is hidden and cannot be accessed on the class it is defined in, only instances of.'''
