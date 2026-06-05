'''A feature-rich asynchronous utilities library with CLI and REPL support.'''
__all__ = 'altlocks', 'base', 'buckets', 'channels', 'cli', 'compete', 'config', 'console', 'constants', 'context', 'events', 'exceptions', 'func', 'futures', 'io', 'iterclasses', 'iters', 'locks', 'locksmiths', 'misc', 'mixins', 'networking', 'pools', 'processors', 'properties', 'queues', 'rwlocks', 'signals', 'tools', 'util', 'version'
from ._internal.types import Submodule
from .altlocks import *
from .base import *
from .buckets import *
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
from .locksmiths import *
from .misc import *
from .mixins import *
from .networking import *
from .pools import *
from .processors import *
from .properties import *
from .queues import *
from .rwlocks import *
from .signals import *
from .tools import *
from .util import *
from .version import *
from types import ModuleType
from typing import Final
def __dir__() -> tuple[str, ...]: ...
def time_since_boot() -> float: ...
__version__: Final[VersionInfo]
__hexversion__: Final[int]
console_preloaded_submodules: Final[frozenset[Submodule]]
preloaded_submodules: Final[frozenset[Submodule]]
submodules_map: Final[dict[Submodule, ModuleType]]
