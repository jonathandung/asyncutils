from collections.abc import Iterable
__all__ = 'run',
def run(argv: Iterable[str]|None=...) -> int|None:
    '''| Run this module's REPL and return the integer return code.
    | If passed, ``argv`` should be a non-string iterable of strings representing the command-line arguments, and it should not have the executable name as the first item.
    | Otherwise, :data:`sys.argv` is used, as per standard :mod:`argparse` behaviour.
    | An attempt will be made to parse all arguments and the program will exit entirely on an unrecognized option.
    | If an error somehow escapes the console and the `pdb` option is enabled, ``None`` will be returned after calling the post-mortem debugger on its traceback.

    Execute ``asyncutils -?``, or call :func:`~asyncutils.tools.get_cmd_help`, to see detailed command-line usage.

    .. warning::
      If you call this function manually, a daemon thread is spun up to execute the code in the console, which may still be kept alive by some internal mechanisms after the function returns.
      Worse still, if you call this function within another console, its standard input may completely cease to work.
    '''
