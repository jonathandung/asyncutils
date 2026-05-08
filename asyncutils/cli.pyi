from _collections_abc import Iterable
__all__ = 'run',
def run(argv: Iterable[str]|None=...) -> int:
    '''| Run this module's REPL with `argv` as command-line arguments, and return the integer return code.
    | See :func:`tools.get_cmd_help()` for detailed usage.
    | If an error somehow escapes the console and the `pdb` option is enabled, `1` will be returned after calling the post-mortem debugger on its traceback.

    .. attention:: The function will parse any command-line arguments in :data:`sys.argv` if `argv` is not passed.'''