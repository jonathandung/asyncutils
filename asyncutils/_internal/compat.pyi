import sys, typing as t
from functools import partial as partial
if sys.version_info >= (3, 14): from functools import Placeholder as Placeholder
else: Placeholder: t.Final[object]
apargs: dict[str, t.Any]