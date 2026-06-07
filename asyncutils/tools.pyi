'''Utilities related to the command-line interface and getting metadata for package configuration.'''
from ._internal.prots import CanWriteAndFlush, DumpType, Openable
from collections.abc import Callable, Sequence
from typing import Any
__all__ = 'argstr_to_json', 'argv_to_json', 'find_help_url', 'get_cfg_json_format', 'get_cmd_help', 'json_to_argstr', 'json_to_argv', 'loadf', 'open_help', 'print_cfg_json_format', 'print_cmd_help'
def loadf(path: Openable, ext: str=..., /) -> dict[str, Any]: '''Load the file at `path`, with the specified file extension if indeducible from the file name, into a dictionary using the correct library.'''
def json_to_argv(path: Openable, /) -> list[str]:
    '''| Return a list of strings representing the command-line arguments for this module from ``path`` to the corresponding json file,
    | with as little items as possible.
    | For integer file descriptors as ``path``, the format is assumed to be plain JSON.
    | The module should have a ``load`` function that takes ``path`` and returns a dict of its contents.
    | Perfect round-trip conversion with :func:`argv_to_json` is guaranteed only with no other configuration file active.'''
def json_to_argstr(path: Openable, /, *, join: Callable[[list[str]], str]=...) -> str: '''Essentially the output of :func:`json_to_argv`, but joined into a shell-escaped string with ``join``.'''
def argv_to_json(argv: Sequence[str], path: Openable, /, *, dump: DumpType=...) -> None:
    '''| Writes the sequence of strings, parsed as command-line arguments for this module, into ``path`` in JSON format.
    | Since this function is 'environment-agnostic', it may have unintended behaviour if the arguments passed rely on current configuration,
    | which is not captured.'''
def argstr_to_json(argstr: str, path: Openable, /, *, dump: DumpType=..., split: Callable[[str], Sequence[str]]=...) -> None: '''Parses the shell-escaped string representing the command-line arguments for this module and writes it into a .json path.'''
def get_cfg_json_format() -> str:
    '''| Get the format of .json configs this module takes as a string.
    | :func:`print_cfg_json_format` is perhaps more useful.
    | If you would like a format schema for other languages, a programmatic approach would likely be unnecessary; you can just use an online
    | tool implementing a browser-based converter.'''
def print_cfg_json_format(file: CanWriteAndFlush[str]=..., *, flush: bool=...) -> None: '''Print the above format into the specified file and flush it (default :data:`~sys.stdout`).'''
def get_cmd_help() -> str:
    '''Return the command line help as a string containing ANSI color escape sequences.

    .. seealso

      :func:`print_cmd_help`
        A more useful function that prints the help to a file or the console

    .. admonition:: Implementation detail

      This is actually a bound method of the library's argument parser at runtime.'''
def print_cmd_help(file: CanWriteAndFlush[str]=..., *, flush: bool=...) -> None: '''Print the above help into the specified file (default :data:`~sys.stdout`) and flush it.'''
def find_help_url(obj: object=..., /) -> str:
    '''Get the URL of the :mod:`asyncutils` documentation page for ``obj``. See the supported calling patterns `here <https://asyncutils.readthedocs.io/en/stable/examples.html>`__.

    .. caution:: The URL returned is not guaranteed to work with strings representing non-existent, undocumented or internal symbols.'''
def open_help(obj: object=..., /) -> bool: '''Open the URL to the documentation of the specified symbol defined in :mod:`asyncutils` via the default browser, returning success.'''
