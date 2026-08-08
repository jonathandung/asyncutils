from asyncutils.constants import POSSIBLE_EXECUTORS as c
from asyncutils._internal.compat import j
import argparse as A
j.update(add_help=False, fromfile_prefix_chars='@', formatter_class=A.RawTextHelpFormatter)
i, b, d, e, f, g, J, p = '--', 'store_const', 'executor', 'Equivalent to "-e %s".', 'store_true', 'count', 'ETYP', A.ArgumentParser(prog='asyncutils', argument_default=A.SUPPRESS, description='''Copyright (c) 2026 Jonathan Dung. All rights reserved.

A versatile, feature-rich library of async tools integrated into the asyncio framework, aiming to make asynchronous programming easier for everyone.
Has CLI and coloured REPL support for quick development.
On both conda and pip as py-asyncutils.''', epilog='''Use @<filename> to insert command-line arguments from the file of that name at the exact position of this parameter.
The file should have one argument per line; this format differs from that described below.

Use the AUTILSCFGPATH environment variable to specify a path to a file of a supported type containing the default configuration.
See the possible keys in format.json5, which can be accessed using tools.get_cfg_json_format().

Note that the inner workings of this library is tightly coupled with the ever-evolving asyncio framework.
As such, it is probably incompatible with full-fledged third-party async frameworks such as curio, anyio, trio, and tornado.''', **j)
(a := (h := lambda f=p.add_mutually_exclusive_group: f().add_argument)())('-l', '--log-to', nargs='?', const='MAKE', metavar='FILE', help='''This module uses a logger, so that post-mortem debugging can be done by inspecting the log file created.
When FILE, interpreted as a file descriptor if an integer, is passed, the logging output goes to a file with that name.
Passing 'NULL' for FILE is equivalent to specifying the --no-log option.
If FILE is 'MEMORY', logs are stored in memory and returned and voided whenever get_past_logs is called.
If FILE is 'MAKE' or no filename is passed but the option specified, an attempt is made to create a file of format 'asyncutils_log<n>.log' in the
current working directory for logging, for integer n from 1 to 4096 inclusive. You are advised to clean up old log files periodically.
Log file rotation is not currently supported, and the program is unlikely to produce a large enough volume of logs to warrant it anyway.
If FILE is 'STDOUT', log to standard output.
If FILE is 'STDERR', log to standard error. This is also the default behaviour and fallback if the above steps fail.''')
a('-n', '--no-log', action=b, const='NULL', dest='log_to', help='''Disable logging completely.
A disabled logger is still created to make subsequent logging.getLogger calls return it.
Thus, this option cannot avoid the cost of importing logging and instantiating the logger early on.''')
(a := h())('-e', '--executor', choices=c, metavar=J, help='''Choose an executor class to use when necessary depending on the value of ETYP as follows:
thread: Use concurrent.futures.thread.ThreadPoolExecutor. This is the default and will be used if the third-party options are passed but not installed.
The below options are experimental.
process: Use concurrent.futures.process.ProcessPoolExecutor. Use with care, since this depends on CPU architecture.
interpreter: Use concurrent.futures.interpreter.InterpreterPoolExecutor. May throw various errors relating to unshareable objects.
The below options are third-party.
loky_no_reuse: Use a new loky.process_executor.ProcessPoolExecutor every time.
loky: Reuse a loky.process_executor.ProcessPoolExecutor if possible.
dask: Use dask.distributed.Client, the API of which just so happens to be a superset of that of the concurrent.futures executors.
ipython: Use ipyparallel.ViewExecutor.
elib_flux_cluster: Use executorlib.executor.flux.FluxClusterExecutor.
elib_flux_job: Use executorlib.executor.flux.FluxJobExecutor.
elib_slurm_cluster: Use executorlib.executor.slurm.SlurmClusterExecutor.
elib_slurm_job: Use executorlib.executor.slurm.SlurmJobExecutor.
elib_single_node: Use executorlib.executor.single.SingleNodeExecutor.
pebble_thread: Use pebble.pool.thread.ThreadPool.
pebble_process: Use pebble.pool.process.ProcessPool.
deadpool: Use deadpool.Deadpool.''')
a('-c', '--custom-executor', dest='executor', metavar=J, help='Use a custom executor not included in the above options by specifying the name of an implementation.\nPassing "package.submodule.Implementation", for example, will execute "from package.submodule import Implementation as Executor".')
for _ in c: a(i+_.replace('_', '-'), action=b, const=_, dest=d, help=e%_)
(a := (h := lambda t, d, f=p.add_argument_group: f(t, d).add_argument)('verbosity', 'Adjust the amount of output of this program.'))('-Q', action=g, default=0, help='Produce less logging output. Additive.')
a('-V', action=g, default=0, help='Produce more logging output. Additive.')
(a := h('repl', 'Configure the behaviour of the Read-Eval-Print Loop of this module.'))('-q', '--quiet', action=f, help='Do not display the banner and exit message in the REPL; the -q flag can be passed to the python command directly to achieve the same effect.')
a('-b', '--basic-repl', action=f, help='Do not use the console with colours and enhanced functionality from _pyrepl. Use only if you have experienced a bug with the coloured console.')
a('-m', '--max-memory_errors', type=int, metavar='M', help='''The REPL will exit on the (M+1)-th MemoryError to prevent consuming too many computer resources.
M defaults to 3.
Set to a negative value to disable the threshold completely.''')
(a := h('testing', 'Options to more conveniently test this module.'))('-p', '--load-all', action=f, help='Preload all submodules of this module. Useful for testing, but incurs noticeable performance penalty.')
a('-s', '--seed', help='Seed the random instance used internally by this module with SEED, which will be interpreted as an integer if possible.')
a('-d', '--debug', action=f, help='Enable debug mode to produce more logging output by entering the global debug context manager. Different from -VV, since\nthe verbosity flags take effect again when the context manager is manually exited.')
a('-P', '--pdb', action=f, help='Intended for developers of this library only; open the pdb debugger interface when the exit code of the console is greater than zero,\nor an uncaught error occurs in the console execution logic itself.')
(a := h('metadata', 'Get basic information about this installation of asyncutils.'))('-v', '--version', action='version', version=__import__('asyncutils').__version__.representation, help='Print the current version number of asyncutils, in the form as specified by __version__.representation, and exit.\nUseful for checking if the installation succeeded.')
t = '-?', '-h', '--help'
a(*t, action='help', help='Print this help message and exit.')
s = p.add_subparsers(dest='command').add_parser('bug', help='Streamline the process of opening a bug report on GitHub.', description='This command will print a link to open a new issue on GitHub with pre-filled information detected from the environment to stdout\nand exit, or if --open is passed, the link is opened directly using the webbrowser module.', epilog='Some text area fields cannot be filled here, since they expect longer responses and cannot be crammed into a link, which has\nhard character limits.', **j)
(a := s.add_mutually_exclusive_group().add_argument)('-v', '--verbose', action=f, help='Emit more output.')
a('-q', '--quiet', action=f, help='Emit less output.')
(a := s.add_argument)('title', nargs='?', default='', help='The title of the bug report. If not specified, the title will be left blank.')
a('-u', '--src-url', default='', help='The permalink to the source file the bug primarily concerns. Must be a proper URL that passes urllib.parse.urlsplit validation.')
a('-l', '--log-path', nargs='?', const='', help='The filesystem path to the logs to include in the report.')
a('-t', '--traceback-path', nargs='?', const='', help='The filesystem path to the traceback.')
a('-n', '--no-prefill-env', action=f, help='Do not fill the context section of the bug report with the values of environment variables that may affect ``asyncutils``.')
a('-e', '--ensure-filled', action=f, help='Ensure that all fillable fields are filled and fail if not.')
a('-P', '--pastebin', action=f, help='Create a public paste.rs paste for each field with long content.')
a('-p', '--print-on-fail', action=f, help='Print the link to the console and exit with code 1 if opening it in a browser fails.')
a('-i', '--interactive', action=f, help='Prompt the user to enter missing fields interactively. Will also prompt for log and traceback if ')
a('-o', '--open', nargs='?', const=None, default=NotImplemented, metavar='BROWSER', help='Open the link in a browser instead of printing it to the console.')
a(*t, action='help', help='Print this help message and exit.')
del a, b, c, d, e, f, g, h, i, j, s, t, J, A
