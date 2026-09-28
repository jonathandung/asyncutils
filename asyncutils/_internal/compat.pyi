'''Compatibility shims for different Python versions.'''
from collections.abc import Iterable
from functools import partial as partial
from sys import version_info as v
from typing import Any, Final
from .prots import SupportsRichComparison
D: Final[dict[str, Any]]
j: Final[dict[str, Any]]
if v < (3, 14): from .py313 import * # ruff: ignore[undefined-local-with-import-star]
else:
    from functools import Placeholder as Placeholder
    def heapify[C: SupportsRichComparison](heap: list[C], /) -> None: ...
    def heappop[C: SupportsRichComparison](heap: list[C], /) -> C: ...
    def heappush[C: SupportsRichComparison](heap: list[C], item: C, /) -> None: ...
    def heappushpop[C: SupportsRichComparison](heap: list[C], item: C, /) -> C: ...
    def heapreplace[C: SupportsRichComparison](heap: list[C], item: C, /) -> C: ...
s: Final[frozenset[type[Iterable[Any]]]]
