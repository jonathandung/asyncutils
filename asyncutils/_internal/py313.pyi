'''Backport of :class:`functools.partial` that supports placeholders to python 3.13 or under.'''
import sys
if sys.version_info < (3, 14):
    from functools import partial
    from typing import Any, Final
    __all__ = 'Placeholder', 'pargs', 'partial'
    pargs: dict[str, Any]
    Placeholder: Final[object]