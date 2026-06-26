'''Asynchronous descriptors, mimicking :class:`property` and optionally applying a lock.'''
from ._internal.prots import AsyncContextManager
from .rwlocks import RWLock
from abc import ABC, abstractmethod
from asyncio import Task
from collections.abc import Awaitable, Callable
from enum import IntFlag
from typing import Any, Concatenate, Self, overload
__all__ = 'AsyncPropertyBase', 'ConcurrentAsyncProperty', 'Deleters', 'LazyAsyncProperty', 'RWLockedAsyncProperty'
class Deleters(IntFlag):
    '''Integer flags configuring a fallback deleter for async properties.'''
    DEFAULT = 0
    '''The default deleter.'''
    CANNOT_SET_AFTER_DELETE = 1
    '''This flag is only meaningful if :const:`NO_DELETER` is not set. Setting this flag means the setter will not be allowed to run after the deleter has been executed on an instance.'''
    SILENT = 1
    '''This flag is only meaningful if :const:`NO_DELETER` is also set. Deletion will essentially become a no-op in that case, as opposed to the default behaviour which raises :exc:`AttributeError`.'''
    CAN_DELETE_AGAIN = 2
    '''If this flag is set, the deleter can be called multiple times on the same instance without raising :exc:`AttributeError`.'''
    NO_DELETER = 4
    '''If this flag is set, the attribute still exists on the object after deletion, just like there was no deleter, if :const:`SILENT` is set.'''
class AsyncPropertyBase[T, R](ABC):
    '''A property with asynchronous getters, setters and deleters.'''
    @overload
    def __new__(cls, *, doc: str|None=..., strict: bool=..., hide: bool=..., mutable: bool=..., assert_modifiers_return_none: bool=...) -> Callable[[Callable[[R], Awaitable[T]]], Self]: ...
    @overload
    def __new__(cls, fget: Callable[[R], Awaitable[T]]|None, fset: Callable[[R, T], Awaitable[None]|None]|None=..., fdel: Callable[[R], Awaitable[None]|None]|Deleters=..., *, doc: str|None=..., strict: bool=..., hide: bool=..., mutable: bool=..., assert_modifiers_return_none: bool=...) -> Self:
        '''| Create a new async property with getter ``fget``, setter ``fset`` and deleter ``fdel``.
        | ``fget`` must return an awaitable resolving to the value of the property and take only the instance as argument.
        | ``fset`` must return either ``None`` or an awaitable resolving to ``None``, and take the instance and value as arguments.
        | ``fdel`` can be a callable taking the instance as an argument and resolving to ``None`` or an awaitable thereof, or a member of :class:`Deleters` to configure a basic deleter that disallows gets after deletion on the instance in question.
        | If the getter is not provided, return a partial decorator instead. In that overload, none of the accessors are to be passed.
        | ``doc``, if passed, will be the docstring of the property in the form of the :attr:`__doc__` attribute. Otherwise, an attempt is made to find it on the getter.
        | ``strict`` defaults to ``True``, and controls whether performing an operation that invokes an unset accessor is allowed. If it is ``False``, setters and deleters are also allowed to return something other than ``None``, and accessing the attribute on instances would return the property itself for getter-less properties where normally an :exc:`AttributeError` would have been raised.
        | If ``hide`` is ``True`` (default ``False``), accessing the attribute on the class it is defined in would raise :exc:`AttributeError` as if the property didn't exist.
        | Subclasses must define :meth:`wrap_aw`, and are allowed to override :meth:`_init` and :meth:`_repr_accessor`. Nothing else is customizable.
        '''
    @overload
    async def __get__(self, instance: R, owner: type[R]|None=..., /) -> T: ...
    @overload
    async def __get__(self, instance: None, owner: type, /) -> Self: '''Call the getter and return a coroutine resolving to its result.'''
    def __set__(self, instance: R, value: T, /) -> None: '''Note that the setter is to be called with the instance and value as arguments.'''
    def __delete__(self, instance: R, /) -> None: '''Note that the deleter is to be called with the instance as the only argument.'''
    def __set_name__(self, owner: type[R], name: str, /) -> None: '''Bind the property to the class.'''
    def __getattr__(self, name: str, /) -> Any: '''Find the attribute on the getter if it exists.''' # noqa: ANN401
    def __reduce__(self) -> str: '''Return the qualified name of this property for pickling. Hidden properties cannot be pickled.'''
    def getter(self, fget: Callable[[R], Awaitable[T]], /) -> Self: '''Return another async property with the given function as the getter.'''
    def setter(self, fset: Callable[[R, T], Awaitable[None]|None], /) -> Self: '''Return another async property with the given function as the setter.'''
    def deleter(self, fdel: Callable[[R], Awaitable[None]|None]|Deleters, /) -> Self: '''Return another async property with the given function as the deleter.'''
    @staticmethod
    def _repr_accessor(accessor: Callable[Concatenate[R, ...], Awaitable[T|None]|None]|Deleters|None, /) -> str: '''Return a string representing an accessor. Called by the implementation of :meth:`~object.__repr__`.'''
    def _init(self, fget: Callable[[R], Awaitable[T]], /, fset: Callable[[R, T], Awaitable[None]|None]|None=..., fdel: Callable[[R], Awaitable[None]|None]|Deleters=..., *, doc: str|None=..., strict: bool=..., hide: bool=..., mutable: bool=..., assert_modifiers_return_none: bool=...) -> None: '''Set the necessary attributes on the property; called at construction.'''
    @abstractmethod
    def wrap_aw[S](self, aw: Awaitable[S], /) -> Awaitable[S]: '''Return an awaitable resolving to the result of an awaitable, limited to those returned by the setter or deleter. This can be a coroutine, a future, a task or anything else, and affects the strategy used to handle assignments and deletions which must return synchronously but run in the background.'''
    @property
    def fget(self) -> Callable[[R], Awaitable[T]]|None: '''The getter function for this property, or ``None`` if it doesn't exist.'''
    @property
    def fset(self) -> Callable[[R, T], Awaitable[None]|None]|None: '''The setter function for this property, or ``None`` if it doesn't exist.'''
    @property
    def fdel(self) -> Callable[[R], Awaitable[None]|None]|Deleters: '''The deleter for this property.'''
    def __init_subclass__(cls, /, *, lock_factory: Callable[[], AsyncContextManager[Any]]=..., **k: object) -> None: '''``lock_factory``, a callable that returns a new per-instance async context manager, is required for immediate subclasses.'''
    __doc__: str|None
    '''The docstring for this property, or ``None`` if it doesn't exist.'''
    __name__: str
    '''The name of this property, determined by the function it decorates.'''
    __module__: str|None
    '''The module this property is defined in, determined by the function it decorates.'''
class LazyAsyncProperty[T, R](AsyncPropertyBase[T, R]):
    '''A property that queues set and delete operations.'''
    @overload
    def __new__(cls, *, doc: str|None=..., strict: bool=..., hide: bool=..., mutable: bool=..., assert_modifiers_return_none: bool=...) -> Callable[[Callable[[R], Awaitable[T]]], Self]: ...
    @overload
    def __new__(cls, fget: Callable[[R], Awaitable[T]]|None, fset: Callable[[R, T], Awaitable[None]|None]|None=..., fdel: Callable[[R], Awaitable[None]|None]|Deleters=..., *, doc: str|None=..., strict: bool=..., hide: bool=..., mutable: bool=..., assert_modifiers_return_none: bool=...) -> Self: '''Operations are completed only when a get is called, strictly in order.'''
    async def wrap_aw[S](self, aw: Awaitable[S], /) -> S: '''Wrap the awaitable in a coroutine, run lazily.'''
    __doc__: str|None
    '''The docstring for this property, or ``None`` if it doesn't exist.'''
    __name__: str
    '''The name of this property, determined by the function it decorates.'''
    __module__: str|None
    '''The module this property is defined in, determined by the function it decorates.'''
class ConcurrentAsyncProperty[T, R](AsyncPropertyBase[T, R]):
    '''Allows set and delete operations to run concurrently once the operations are called, without any guarantee on the order of execution.'''
    @overload
    def __new__(cls, *, doc: str|None=..., strict: bool=..., hide: bool=..., mutable: bool=..., assert_modifiers_return_none: bool=...) -> Callable[[Callable[[R], Awaitable[T]]], Self]: ...
    @overload
    def __new__(cls, fget: Callable[[R], Awaitable[T]]|None, fset: Callable[[R, T], Awaitable[None]|None]|None=..., fdel: Callable[[R], Awaitable[None]|None]|Deleters=..., *, doc: str|None=..., strict: bool=..., hide: bool=..., mutable: bool=..., assert_modifiers_return_none: bool=...) -> Self:
        '''| The setters and deleters can be implemented acquire a writer lock and the getter the corresponding reader lock from :mod:`~asyncutils.rwlocks` with its lock policies that provide fluent decorator interfaces.
        | Note, however, that the accessor decorators must be outermost because they turn callables into properties.
        '''
    def wrap_aw[S](self, aw: Awaitable[S], /) -> Task[S]: '''Return a task for the awaitable returned by the setter or deleter.'''
    __doc__: str|None
    '''The docstring for this property, or ``None`` if it doesn't exist.'''
    __name__: str
    '''The name of this property, determined by the function it decorates.'''
    __module__: str|None
    '''The module this property is defined in, determined by the function it decorates.'''
class RWLockedAsyncProperty[T, R](ConcurrentAsyncProperty[T, R]):
    '''Apply a reader-writer lock to the property. Naturally, setters and deleters are writers and getters are readers.'''
    __doc__: str|None
    '''The docstring for this property, or ``None`` if it doesn't exist.'''
    __name__: str
    '''The name of this property, determined by the function it decorates.'''
    __module__: str|None
    '''The module this property is defined in, determined by the function it decorates.'''
    @overload
    def __new__(cls, *, policy: type[RWLock]=..., doc: str|None=..., strict: bool=..., hide: bool=..., mutable: bool=..., assert_modifiers_return_none: bool=...) -> Callable[[Callable[[R], Awaitable[T]]], Self]: ...
    @overload
    def __new__(cls, fget: Callable[[R], Awaitable[T]]|None, fset: Callable[[R, T], Awaitable[None]|None]|None=..., fdel: Callable[[R], Awaitable[None]|None]|Deleters=..., *, policy: type[RWLock]=..., doc: str|None=..., strict: bool=..., hide: bool=..., mutable: bool=..., assert_modifiers_return_none: bool=...) -> Self: '''``policy`` is the class used to create the readers-writer lock for the property. It must subclass :class:`~asyncutils.rwlocks.RWLock`.'''
    def _init(self, f: Callable[[R], Awaitable[T]], /, fset: Callable[[R, T], Awaitable[None]|None]|None=..., fdel: Callable[[R], Awaitable[None]|None]|Deleters=..., *, policy: type[RWLock]=..., doc: str|None=..., strict: bool=..., hide: bool=..., mutable: bool=..., assert_modifiers_return_none: bool=...) -> None: ...
    @staticmethod
    def _repr_accessor(v: Callable[..., Awaitable[T|None]|None]|Deleters|None, /) -> str: ...
