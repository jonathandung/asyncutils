from ._internal.helpers import Bag
from collections.abc import Iterable
from typing import Any
__all__ = 'bug', 'run'
def bug(args: Bag[Any]) -> None:
    '''
    | Open a new issue in the `GitHub issue tracker <https://github.com/jonathandung/asyncutils/issues>`__.
    | Called by :func:`run` under the appropriate ``argv``.
    | If calling manually, pass an object with the following attributes.

    - ``title`` (:class:`str`): The title of the bug report.
    - ``src_url`` (:class:`str`): The link to the source if you can find it.
    - ``open`` (optional): If ``None``, use the default browser to open the link. If a :class:`str`, use that as the name of the browser to open the link, or a filesystem path or command pointing to the browser if the name is not registered.
    '''
def run(argv: Iterable[str]|None=...) -> int|None:
    '''
    | Run this module's REPL (or the bug reporting command) and return the integer return code.
    | If passed, ``argv`` should be a non-string iterable of strings representing the command-line arguments, and it should not have the executable name as the first item.
    | Otherwise, :data:`sys.argv` is used, as per standard :mod:`argparse` behaviour.
    | An attempt will be made to parse all arguments and the program will exit entirely on an unrecognized option.
    | If an error somehow escapes the console and the ``pdb`` option is enabled, ``None`` will be returned after calling the post-mortem debugger on its traceback.

    Execute ``asyncutils -?``, or call :func:`~asyncutils.tools.get_cmd_help`, to see detailed command-line usage.

    .. warning::
      If you call this function manually, a daemon thread is spun up to execute the code in the console, which may still be kept alive by some internal mechanisms after the function returns.
      Worse still, if you call this function within another console, its standard input may completely cease to work.
    '''
