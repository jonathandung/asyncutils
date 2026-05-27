'''Asynchronous descriptors, mimicking :class:`property` and optionally applying a lock.'''
from ._internal.types import AsyncLockLike
from _collections_abc import Awaitable, Callable, Hashable
from asyncio.locks import Lock
from typing import Any, Concatenate, Self, final, overload
__all__ = 'AsyncLockProperty', 'AsyncProperty', 'coercedmethod'
class AsyncProperty[T, R]:
    '''| A property with asynchronous getters, setters and deleters running synchronously via event loop scheduling. Would fail in the console,
    | since :func:`util.sync_await` is called internally, which would deadlock in that context.'''
    @overload
    def __new__(cls, *, doc: str|None=..., strict: bool=..., hide: bool=...) -> Callable[[Callable[[R], Awaitable[T]]], Self]: ...
    @overload
    def __new__(cls, fget: Callable[[R], Awaitable[T]]|None, fset: Callable[[R, T], Awaitable[None]]|None=..., fdel: Callable[[R], Awaitable[None]]|None=..., *, doc: str|None=..., strict: bool=..., hide: bool=...) -> Self:
        '''| Create a new async property with getter `fget`, setter `fset` and deleter `fdel`.
        | If the getter is not provided, return a partial decorator instead. In that overload, none of the accessors are to be passed.
        | `doc`, if passed, will be the docstring of the property in the form of the :attr:`__doc__` attribute. Otherwise, an attempt is made to
        | find it on the getter.
        | `strict` defaults to `True`, and controls whether performing an operation that invokes an unset accessor is allowed.
        | If the property has no getter (only possible with explicit `fget=None` and at least one of `fset` and `fdel` passed, which is rare),
        | accessing the attribute on instances would return the property itself if `strict=False` and raise an :exc:`AttributeError` otherwise.
        | If `hide` is `True` (default `False`), accessing the attribute on the class it is defined in would raise as if the property didn't exist.'''
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
    @property
    def fget(self) -> Callable[[R], Awaitable[T]]|None: '''The getter function for this property, or `None` if it doesn't exist.'''
    @property
    def fset(self) -> Callable[[R, T], Awaitable[None]]|None: '''The setter function for this property, or `None` if it doesn't exist.'''
    @property
    def fdel(self) -> Callable[[R], Awaitable[None]]|None: '''The deleter function for this property, or `None` if it doesn't exist.'''
    @property
    def __doc__(self) -> str|None: '''The docstring for this property, or `None` if it doesn't exist.'''
    @property
    def __name__(self) -> str: '''The name of this property, determined by the function it decorates.'''
class AsyncLockProperty[T, R: Hashable](AsyncProperty[T, R]):
    '''A property that applies an async lock to its getters, setters and deleters.

    .. tip::
      If you wish to apply a readers-writer lock from :mod:`rwlocks` to the property, decorate the getter of an ordinary :class:`AsyncProperty`
      with :meth:`~rwlocks.RWLock.reader` and the setter and deleter with :class:`~rwlocks.RWLock.writer` on a lock of choice. Because attribute
      access delegates to the getter, a `writer` attribute is also on the getter after decoration. In this case, the property should be the
      outermost (topmost) decorator, since it turns an async function into a property.
'''
    @overload
    @staticmethod
    def _new_lock[L: AsyncLockLike[Any]](_: R, *, lock_impl: type[L]) -> L: ...
    @overload
    @staticmethod
    def _new_lock(_: R) -> Lock: '''Default way to create a new lock for the given object. The implementation should not cache the locks for each instance, since that is done by this class already.'''
    @overload
    def __new__(cls, *, doc: str|None=..., strict: bool=..., hide: bool=..., lock_getter: Callable[[R], AsyncLockLike[Any]]|None=...) -> Callable[[Callable[[R], Awaitable[T]]], Self]: ...
    @overload
    def __new__(cls, fget: Callable[[R], Awaitable[T]]|None, fset: Callable[[R, T], Awaitable[None]]|None=..., fdel: Callable[[R], Awaitable[None]]|None=..., *, doc: str|None=..., strict: bool=..., hide: bool=..., lock_getter: Callable[[R], AsyncLockLike[Any]]|None=...) -> Self: ...
    def get_lock(self, obj: R) -> AsyncLockLike[Any]: '''Get the lock for the given object, applying a cache that unfortunately requires the object to be hashable and weakly referencable.'''
    @property
    def __doc__(self) -> str|None: '''The docstring for this property, or `None` if it doesn't exist.'''
    @property
    def __name__(self) -> str: '''The name of this property, determined by the function it decorates.'''
@final
class coercedmethod[T, R, **P]: # noqa: N801
    '''Interpret any callable as a regular function in a class body so that access on instance returns something like a bound method.'''
    def __init__(self, func: Callable[Concatenate[R, P], T], /): ...
    def __getattr__(self, name: str, /) -> Any: ...
    def __set_name__(self, owner: type[R], name: str, /) -> None: ...
    def __get__(self, instance: R, owner: type[R]|None=..., /) -> Callable[P, T]: '''Return the 'bound method'. The descriptor itself is hidden and cannot be accessed on the class it is defined in, only instances of.'''