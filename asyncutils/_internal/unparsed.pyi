'''
Automatically read the config from the file whose path is specified by :envvar:`AUTILSCFGPATH`.

.. important:: Values will be overwritten by command-line arguments when this module runs as a script.
'''
from typing import Any, Final, overload
from .helpers import Bag
N: Final[Bag[Any]]
'''The frozen part of the configuration as a light namespace-like object.'''
C: Final[dict[str, Any]]
'''The contextual portion of the configuration as a flattened :class:`dict` mapping upper-case keys to values.'''
Z: Final[dict[str, str]]
'''A :class:`dict` mapping file extensions to module names for loading config files. Is queried by :func:`~asyncutils.tools.loadf`.'''
c: Final[str]
'''The path to the config file read, or an empty string if no config file was read.'''
z: Final[str]
'''The contents of the config file read fenced in a markdown code block, or an empty string if no config file was read. If the config file is in ``pyproject.toml`` format, this will be a synthesized JSON string containing only the :mod:`asyncutils` keys, made as compact as can be.'''
@overload
def r(path: int, ext: str, /) -> dict[str, Any]: ...
@overload
def r(path: str, ext: str|None=..., /) -> dict[str, Any]: '''Load a config file from the given string path or file descriptor (in which case the file extension should be passed but leniently defaults to json), from which the file extension and thus appropriate parsing library is determined.'''
