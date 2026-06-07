from collections.abc import Iterable
__all__ = 'run',
def run(argv: Iterable[str]|None=...) -> int|None:
    '''| Run this module's REPL and return the integer return code.
    | If passed, ``argv`` should be a non-string iterable of strings representing the command-line arguments, and it should not include the
    | executable name as the first item. Otherwise, :data:`sys.argv` is used.
    | An attempt will be made to parse all arguments and the program will exit entirely on an unrecognized option.
    | See :func:`tools.get_cmd_help()` for detailed usage.
    | If an error somehow escapes the console and the `pdb` option is enabled, ``None`` will be returned after calling the post-mortem
    | debugger on its traceback.

    .. important::
      If you call this function manually, since a daemon thread was spun up to execute the code in the console, it may still be kept alive by
      some internal mechanisms. Worse still, if you run this function within another console, its standard input may completely cease to work.
      In a nutshell, if you are calling this in a console, it is recommended that you input no code afterwards.
'''
