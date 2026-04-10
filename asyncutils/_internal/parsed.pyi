'''Sub-module imported when parsing of command-line arguments is required.'''
import argparse
import typing
p: typing.Final[argparse.ArgumentParser]
'''The ArgumentParser instance shared by asyncutils.'''