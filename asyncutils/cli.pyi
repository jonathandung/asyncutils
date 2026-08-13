from ._internal.prots import BugArgs
from collections.abc import Callable, Iterable
__all__ = 'bug', 'run'
def bug(args: BugArgs, paste_backend: Callable[[bytes], bytes|str]=...) -> None:
    '''
    | Open a new issue in the `GitHub issue tracker <https://github.com/jonathandung/asyncutils/issues>`__.
    | Called by :func:`run` under the appropriate ``argv``.
    | If calling manually, pass a callable taking a bytestring and returning a link from a pastebin service as a string or the bytestring itself depending on the length for ``paste_backend`` if desired,
    | and an object with the following attributes for ``args``.

    - ``title`` (:class:`str`): The title of the bug report.
    - ``src_url`` (:class:`str`): The link to the source if you can find it.
    - ``ensure_filled`` (:class:`bool`): If ``True``, raise an exception if any of the required fields are empty.
    - ``interactive`` (:class:`bool`): If ``True``, prompt the user to pre-fill any empty fields in the console. Assumes standard input is a TTY.
    - ``verbose`` (:class:`bool`): If ``True``, print more information to the console (both stdout and stderr); mutually exclusive with ``quiet``.
    - ``quiet`` (:class:`bool`): If ``True``, only print essential information to the console; mutually exclusive with ``verbose``.
    - ``pastebin`` (:class:`bool`): If ``True``, upload the logs and traceback, to `paste.rs <https://paste.rs>`__ using :mod:`urllib.request` by default, to avoid an absurdly long link.
    - ``log_path`` (:class:`str`): The path to the file containing the debug logs, most likely created by :mod:`asyncutils` with name ``asyncutils_log<n>.log`` for some integer ``n``.
    - ``traceback_path`` (:class:`str`): The path to the file containing the traceback in text.
    - ``no_prefill_env`` (:class:`bool`): If ``True``, do not pre-fill the environment variables in the issue body.
    - ``print_on_fail`` (:class:`bool`): If ``True``, print the link to the console if opening the link in a browser fails and exit with code 1.
    - ``open``: If ``None``, try the default browsers sequentially to open the link. If a :class:`str`, use that as the name of the browser to open the link, or a filesystem path or command pointing to the browser if the name is not registered.
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
