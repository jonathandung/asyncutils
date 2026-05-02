'''This submodule automatically reads the config from the file whose path is specified by `AUTILSCFGPATH`.
Values will be overwritten by command-line arguments when this module runs as a script.'''
from .types import Bag
from typing import Any, Final, overload
N: Final[Bag]
'''The frozen part of the configuration as a light namespace-like object.'''
C: Final[dict[str, Any]]
'''The contextual portion of the configuration as a flat :class:`dict` mapping upper-case keys to values.'''
D: Final[dict[str, str]]
'''A :class:`dict` mapping file extensions to module names for loading config files.'''
@overload
def l(path: int, ext: str, /) -> dict[str, Any]: ...
@overload
def l(path: str, ext: str|None=..., /) -> dict[str, Any]: '''Load a config file from the given string path or file descriptor (in which case the file extension is should be passed but defaults to json), from which the file extension and thus appropriate parser is determined.'''
c: Final[str]
'''The path to the config file used, or an empty string if no config file was read.'''