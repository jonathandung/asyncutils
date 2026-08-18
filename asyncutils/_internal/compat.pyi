'''Compatibility shims for Python 3.12 - 3.15.'''
from collections.abc import Iterable
from functools import partial
from sys import version_info as v
from typing import Any, Final
from .prots import SupportsRichComparison
__all__ = 'D', 'Placeholder', 'heapify', 'heappop', 'heappush', 'heappushpop', 'heapreplace', 'j', 'partial', 's'
D: Final[dict[str, Any]]
j: Final[dict[str, Any]]
if v < (3, 14): from .py313 import * # ruff: ignore[undefined-local-with-import-star]
else:
    from functools import Placeholder
    def heapify[C: SupportsRichComparison](heap: list[C], /) -> None: ...
    def heappop[C: SupportsRichComparison](heap: list[C], /) -> C: ...
    def heappush[C: SupportsRichComparison](heap: list[C], item: C, /) -> None: ...
    def heappushpop[C: SupportsRichComparison](heap: list[C], item: C, /) -> C: ...
    def heapreplace[C: SupportsRichComparison](heap: list[C], item: C, /) -> C: ...
s: Final[frozenset[type[Iterable[Any]]]]
