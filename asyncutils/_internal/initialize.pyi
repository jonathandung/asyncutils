'''A special module used to set up the :mod:`asyncutils` module namespace.

.. danger:: Modifying the module's contents or reloading it at runtime may break the module.'''
from .prots import All, Submodule
from types import ModuleType
from typing import Any, Final, Self, final, overload
@final
class Module:
    '''The actual type of submodule proxies, implemented as transparently as possible. Only user-facing methods have docstrings here.'''
    @overload
    def __new__(cls, name: Submodule, /) -> Self|ModuleType: ...
    @overload
    def __new__(cls, name: str, /) -> Any: ...
    def __getattr__(self, name: str, /) -> Any: '''Check if the name is public and exit early without importing the module if not, unless the name is a double-underscored attribute, in which case the module will be loaded even if it doesn't exist.'''
    def __setattr__(self, name: str, value: object, /) -> None:
        '''.. version-changed:: 0.9.4
          Loading is triggered by any attribute assignment. Previously, it failed with an :exc:`AttributeError`.
'''
    def __delattr__(self, name: str, /) -> None:
        '''.. version-changed:: 0.9.6
          Loading is triggered by any attribute deletion. Previously, it failed with an :exc:`AttributeError`.
'''
    def __reduce__(self) -> tuple[type[Self], tuple[str]]: '''Support for pickling.'''
    def load(self) -> ModuleType: '''Load the submodule and replace the dummy object with the actual submodule in :data:`~asyncutils.submodules_map`. Triggered on attribute access or an explicit call.'''
    @property
    def __all__(self) -> All: '''A tuple of the names that go into the global namespace when `from asyncutils.submod import *` is executed in alphabetical order.'''
    def __dir__(self) -> All: '''Return :attr:`__all__`, as opposed to also the default behaviour of returning the dunder attributes each module has.'''
a: Final[tuple[Submodule, ...]]
s: Final[dict[Submodule, Module|ModuleType]]
S: Final[list[str]]
A: Final[list[str]]
def l(*a: object) -> None: ...
