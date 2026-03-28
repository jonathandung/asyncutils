'''This submodule automatically reads the config from the file whose path is specified by AUTILSCFGPATH.
Keys will be overridden by command-line arguments when this module runs as a script.'''
from .protocols import Bag
N: Bag
'''The configuration as a memory-efficient namespace-like object.'''