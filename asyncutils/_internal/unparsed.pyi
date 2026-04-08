'''This submodule automatically reads the config from the file whose path is specified by `AUTILSCFGPATH`.
Values will be overwritten by command-line arguments when this module runs as a script.'''
from typing import Final, Any
class _(dict[str, Any]):
    '''A thin dictionary subclass that supports attribute access.'''
    def __getattr__(self, key: str, /) -> Any: ...
    def __setattr__(self, key: str, value: Any, /) -> None: ...
    def __delattr__(self, key: str, /) -> None: ...
N: Final[_]
'''The configuration as a memory-efficient namespace-like object.'''