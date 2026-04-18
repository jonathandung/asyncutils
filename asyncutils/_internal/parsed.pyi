'''Submodule imported when parsing of command-line arguments is required.'''
import argparse
import typing
p: typing.Final[argparse.ArgumentParser]
'''The :class:`argparse.ArgumentParser` instance shared by :mod:`asyncutils`.'''