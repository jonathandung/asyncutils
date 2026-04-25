'''Utilities related to the command-line interface and getting metadata for package configuration.'''
from ._internal.types import CanWriteAndFlush, DumpType, Openable
from _collections_abc import Callable, Sequence
__all__ = 'argstr_to_json', 'argv_to_json', 'ext2modname', 'get_cfg_json_format', 'get_cmd_help', 'json_to_argstr', 'json_to_argv', 'print_cfg_json_format', 'print_cmd_help'
ext2modname: dict[str, str]
'''A dictionary mapping file extensions (without the .) to module names to use to parse files of that type as json.
The default module name for a file extension not in this registry is just the extension itself, besides .jsonl files, which should only have one line, being parsed with the standard library :mod:`json`.'''
def json_to_argv(path: Openable, /) -> list[str]:
    '''Return a list of strings representing the command-line arguments for this module from `path` to the corresponding json file, with as little items as possible.
    For integer file descriptors as `path`, the format is assumed to be plain json.
    The module, name as determined by `ext2modname`, should have a `load` function that takes `path` and returns a dict of its contents.'''
def json_to_argstr(path: Openable, /, *, join: Callable[[list[str]], str]=...) -> str: '''Essentially the output of :func:`json_to_argv`, but joined into a shell-escaped string with `join`.'''
def argv_to_json(argv: Sequence[str], path: Openable, /, *, dump: DumpType=...) -> None:
    '''Writes the sequence of strings, parsed as command-line arguments for this module, into `path` with .json format.
    Since this function is 'environment-agnostic', it may have unintended behaviour if the arguments passed rely on current configuration, which is not captured.'''
def argstr_to_json(argstr: str, path: Openable, /, *, dump: DumpType=..., split: Callable[[str], Sequence[str]]=...) -> None: '''Parses the shell-escaped string representing the command-line arguments for this module and writes it into a .json path.'''
def get_cfg_json_format() -> str: '''Get the format of .json configs this module takes as a string. :func:`print_cfg_json_format` is perhaps more useful.'''
def print_cfg_json_format(file: CanWriteAndFlush[str]=...) -> None: '''Print the above format into the specified file and flush it (default :data:`~sys.stdout`).'''
def get_cmd_help() -> str: '''Get the command line help as a string containing ANSI color escape sequences. It would therefore be more useful to call :func:`print_cmd_help` instead.'''
def print_cmd_help(file: CanWriteAndFlush[str]=...) -> None: '''Print the above help into the specified file (default :data:`~sys.stdout`) and flush it.'''