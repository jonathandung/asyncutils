'''This submodule automatically reads the config from the file whose path is specified by AUTILSCFGPATH.
Values will be overwritten by command-line arguments when this module runs as a script.'''
from .protocols import Bag
from typing import Final
N: Final[Bag]
'''The configuration as a memory-efficient namespace-like object.'''