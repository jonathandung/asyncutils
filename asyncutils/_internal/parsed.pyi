'''The submodule imported when parsing of command-line arguments is required.'''
import argparse as a, typing as t
p: t.Final[a.ArgumentParser]
'''The :class:`argparse.ArgumentParser` instance shared by :mod:`asyncutils`.'''
