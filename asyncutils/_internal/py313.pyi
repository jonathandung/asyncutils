'''Backport of functools.partial that supports placeholders to python 3.13 or under.'''
from typing import Final, Any
from functools import partial as partial
__all__ = 'Placeholder', 'apargs', 'partial'
apargs: dict[str, Any]
Placeholder: Final[object]