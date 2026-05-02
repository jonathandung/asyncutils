'''Submodule imported when parsing of command-line arguments is required.'''
import argparse, typing
p: typing.Final[argparse.ArgumentParser]
'''The :class:`argparse.ArgumentParser` instance shared by :mod:`asyncutils`.'''