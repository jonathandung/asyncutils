'''asyncutils is a feature-rich asynchronous utilities library with CLI and REPL support.'''
__all__ = 'altlocks', 'base', 'buckets', 'caches', 'channels', 'cli', 'compete', 'config', 'console', 'constants', 'context', 'events', 'exceptions', 'func', 'futures', 'io', 'iterclasses', 'iters', 'locks', 'misc', 'mixins', 'networking', 'pools', 'processors', 'properties', 'queues', 'signals', 'tools', 'util', 'version'
from .altlocks import *
from .base import *
from .buckets import *
from .caches import *
from .channels import *
from .cli import *
from .compete import *
from .config import *
from .console import *
from .constants import *
from .context import *
from .events import *
from .exceptions import *
from .func import *
from .futures import *
from .io import *
from .iterclasses import *
from .iters import *
from .locks import *
from .misc import *
from .mixins import *
from .networking import *
from .pools import *
from .processors import *
from .properties import *
from .queues import *
from .signals import *
from .tools import *
from .util import *
from .version import *
from types import ModuleType
from typing import Final
from ._internal.protocols import Submodule, All
def __dir__() -> All: ...
__version__: Final[VersionInfo]
'''The current asyncutils version as a string with magical properties for working with versions (refer to the IDE autocomplete for its methods).'''
__hexversion__: Final[int]
'''0x12070e -> version 18.7.14'''
preloaded_submodules: Final[frozenset[str]]
'''A `frozenset` containing all submodules that are inevitably preloaded on module startup, which also loads `asyncio`.
This avoids attribute access later on randomly triggering the asyncio import, which would take 160 ms.'''
submodules_map: Final[dict[Submodule, ModuleType]]
'''A dictionary mapping submodule names to the corresponding submodule objects.'''