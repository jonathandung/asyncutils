'''A special module used to set up the :mod:`asyncutils` module namespace.

.. danger:: Modifying the module's contents or reloading it at runtime may break the module.
'''
from .prots import All, Submodule
from types import ModuleType
from typing import Any, ClassVar, Final, Self, final, overload
@final
class Module:
    dunders: ClassVar[list[str]]
    slots: frozenset[str]
    @overload
    def __new__(cls, name: Submodule, /) -> Self|ModuleType: ...
    @overload
    def __new__(cls, name: str, /) -> Any: ... # noqa: ANN401
    def __getattr__(self, name: str, /) -> Any: ... # noqa: ANN401
    def __setattr__(self, name: str, value: object, /) -> None: ...
    def __delattr__(self, name: str, /) -> None: ...
    def __reduce__(self) -> tuple[type[Self], tuple[str]]: ...
    def load(self) -> ModuleType: ...
    @property
    def __all__(self) -> All: ...
    def __dir__(self) -> All: ...
a: Final[tuple[Submodule, ...]]
s: Final[dict[Submodule, Module|ModuleType]]
S: Final[list[str]]
A: Final[list[str]]
def p(*a: object) -> None: ...
