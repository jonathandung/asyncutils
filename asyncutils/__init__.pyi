'''asyncutils is a feature-rich asynchronous utilities library with CLI and REPL support.'''
__all__ = 'altlocks', 'base', 'buckets', 'caches', 'channels', 'cli', 'compete', 'config', 'console', 'constants', 'events', 'exceptions', 'func', 'futures', 'io', 'iterclasses', 'iters', 'locks', 'misc', 'mixins', 'networking', 'pools', 'processors', 'properties', 'queues', 'signals', 'tools', 'util', 'version'
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
from typing import Final
from types import ModuleType
__version__: Final[VersionInfo]
__hexversion__: Final[int]
'''0x123456 -> version 12.34.56'''
__git_version__: Final[str]
'''The git commit hash.'''
preloaded_submodules: Final[frozenset[str]]
'''A frozenset containing all submodules that are inevitably preloaded on module startup, which also loads asyncio.
This avoids attribute access later on randomly triggering the asyncio import, which would take 160 ms.'''
submodules_map: Final[dict[str, ModuleType]]
'''A dictionary mapping the submodule names to the submodule objects.'''