from _collections_abc import Sequence, Callable
from ._internal.protocols import Openable, DumpType, CanWriteAndFlush
__all__ = 'json_to_argv', 'json_to_argstr', 'argv_to_json', 'argstr_json', 'get_cfg_json_format', 'print_cfg_json_format'
def json_to_argv(path: Openable, /, *, json: str=..., json5: str=..., jsonc: str=..., hjson: str=...) -> list[str]:
    '''Returns a list of strings representing the command-line arguments for this module from the path to the corresponding
    .json file, with as little items as possible.
    Use the `json`, `json5`, `jsonc` and `hjson` parameters to specify the module name of a module to be used to parse a json with
    that file extension, which default to the builtin json module, pyjson5, hjson-py and commentjson respectively.
    The modules should have a `load` function that takes the json path and returns a dict of its contents.'''
def json_to_argstr(path: Openable, /, *, json: str=..., json5: str=..., jsonc: str=..., hjson: str=..., join: Callable[[list[str]], str]=...) -> str: '''Essentially the output of json_to_argv but joined into a shell-escaped string.'''
def argv_to_json(argv: Sequence[str], path: Openable, /, *, dump: DumpType=...) -> None: '''Writes the sequence of strings, parsed as command-line arguments for this module, into `path` with .json format.'''
def argstr_to_json(argstr: str, path: Openable, /, *, dump: DumpType=..., split: Callable[[str], Sequence[str]]=...) -> None: '''Parses the shell-escaped string representing the command-line arguments for this module and writes it into a .json path.'''
def get_cfg_json_format() -> str: '''Get the format of .json configs this module takes, as a string.'''
def print_cfg_json_format(file: CanWriteAndFlush[str]=...) -> None: '''Prints the above format into the specified file (default stdout).'''
def get_cmd_help() -> str: '''Get the command line help as a string containing ANSI colour escape sequences. It would therefore be more useful to call `print_cmd_help` instead.'''
def print_cmd_help(file: CanWriteAndFlush[str]=...) -> None: '''Prints the above help into the specified file (default stdout).'''