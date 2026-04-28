'''A special module used to set up the :mod:`asyncutils` module namespace.
Do not modify its contents or reload it at runtime.'''
from .types import All, Submodule
from types import ModuleType
from typing import Any, Final, Self, final, overload
@final
class Module:
    @overload
    def __new__(cls, name: Submodule, /) -> Self: ...
    @overload
    def __new__(cls, name: str, /) -> Any: ...
    def __getattr__(self, name: str, /) -> Any: ...
    def __reduce__(self) -> tuple[type[Self], tuple[str]]: ...
    def load(self) -> ModuleType: '''Load the submodule and replace the dummy with the actual submodule in :data:`~asyncutils.submodules_map`. Triggered on attribute access or an explicit call.'''
    @property
    def __all__(self) -> All: '''The names that go into the global namespace when `from asyncutils.submod import *` is executed.'''
    def __dir__(self) -> All: '''Return :attr:`__all__`, as opposed to also the default behaviour of returning the dunder attributes each module has.'''
a: Final[list[str]]
s: Final[dict[Submodule, Module|ModuleType]]