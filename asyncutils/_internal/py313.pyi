'''Backport of functools.partial that supports placeholders to python 3.13 or under.'''
from functools import partial as partial
from typing import Any, Final
__all__ = 'Placeholder', 'apargs', 'partial'
apargs: dict[str, Any]
Placeholder: Final[object]