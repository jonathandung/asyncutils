import sys, typing as t
if sys.version_info >= (3, 14): from functools import Placeholder as Placeholder
else: Placeholder: t.Final[object]
from functools import partial as partial
apargs: dict[str, t.Any]