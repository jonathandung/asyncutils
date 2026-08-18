# ruff: file-ignore[undefined-local-with-import-star] # cspell:disable
'''
A feature-rich asynchronous utilities library with CLI and REPL support.

.. autoapidata:: __hexversion__
.. autoapidata:: __version__
.. autoapidata:: all_symbols
.. autoapidata:: console_preloaded_submodules
.. autoapidata:: preloaded_submodules
.. autoapidata:: submodules_map
.. autoapifunction:: time_since_boot
''' # cspell:enable
__all__ = 'altlocks', 'base', 'buckets', 'channels', 'cli', 'compete', 'config', 'console', 'constants', 'context', 'events', 'exceptions', 'func', 'futures', 'iotools', 'iterclasses', 'iters', 'locks', 'locksmiths', 'misc', 'mixins', 'networking', 'pools', 'processors', 'properties', 'queues', 'rwlocks', 'signals', 'tools', 'util', 'version' # ruff: ignore[undefined-local-with-import-star-usage]
from ._internal.prots import Submodule
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
from .iotools import *
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
from ty_extensions import JustFloat
def time_since_boot() -> JustFloat: '''Time since the module was imported or invoked in the command line in milliseconds, as returned by :func:`time.monotonic`, as a :class:`float`.'''
__version__: Final[VersionInfo] # ruff: ignore[undefined-local-with-import-star-usage]
'''An instance of :class:`version.VersionInfo` representing the current pip/conda version of this library.

.. note:: This library adheres to `Semantic Versioning 2.0.0 <https://semver.org/spec/v2.0.0.html>`__.
'''
__hexversion__: Final[int]
'''| An integer representing the current pip/conda version of this library. Comparison operators behave as expected.
| For version 1.3.11, for instance, this would be ``0x01030b``.

.. note:: Equivalent to ``int(__version__)``.'''
all_symbols: Final[list[str]]
'''A :class:`list` of all symbols in this module, in alphabetical order. Does not include any dunder names.'''
console_preloaded_submodules: Final[frozenset[Submodule]]
'''A :class:`frozenset` of submodule names which are loaded when starting the interactive console of this module.

.. note:: This is a strict superset of :data:`preloaded_submodules`.'''
preloaded_submodules: Final[frozenset[Submodule]]
'''A :class:`frozenset` of names of submodules which are preloaded when importing the library for essential initialization.'''
submodules_map: Final[dict[Submodule, ModuleType]]
'''A :class:`dict` mapping submodule names to the corresponding submodule objects.

.. note:: For submodules that are already loaded, these are exact instances of :class:`~types.ModuleType`.
'''
