from .compat import pargs as j
from .. import __version__ as V
from ..constants import POSSIBLE_EXECUTORS as C
import argparse as A
i, b, d, e, f, g, j, p = '--', 'store_const', 'executor', 'Equivalent to "-e %s".', 'store_true', 'count', 'ETYP', A.ArgumentParser(prog='python [-m] asyncutils', description='''A versatile, feature-rich library of async tools integrated into the asyncio framework, aiming to make asynchronous programming easier for everyone.
Has CLI and colored REPL support for quick development.
On both conda and pip as py-asyncutils.''', add_help=False, argument_default=A.SUPPRESS, fromfile_prefix_chars='@', formatter_class=A.RawTextHelpFormatter, epilog='''Use @<filename> to insert command-line arguments from the file of that name at the exact position of this parameter.
The file should have one argument per line; this format differs from that described below.

Use the AUTILSCFGPATH environment variable to specify a path to a .json or .jsonl file containing the default configuration.
Other json formats are not currently supported; see the possible keys in format.json5, which can be accessed using tools.get_cfg_json_format().

Note that the API of this module is probably incompatible with full-fledged third-party async frameworks such as curio, anyio, trio, or tornado.''', **j)
(a := (h := lambda f=p.add_mutually_exclusive_group: f().add_argument)())('-l', '--log-to', nargs='?', const='MAKE', metavar='FILE', help='''This module uses a logger, so that post-mortem debugging can be done by inspecting the log file created.
When FILE is passed (interpreted as an integer file descriptor if possible), the logging output goes to a file with that name.
Passing 'NULL' for FILE is equivalent to specifying the --no-log option.
Most of the logging output is created in debug mode only, to prevent cluttering of the stream.
If FILE is 'MEMORY', logs are stored in memory and returned and voided whenever get_past_logs is called.
If FILE is 'MAKE' or no filename is passed but the option specified, an attempt is made to create a file of format 'asyncutils_log<number>.log' in the
current working directory for logging, for number from 1 to 4096. (If you have more than 4096 log files, you should probably clean them up.)
If FILE is 'STDOUT', logs to stdout.
If FILE is 'STDERR', logs to stderr (also the default behaviour and fallback if the above steps fail).''')
a('-n', '--no-log', action=b, const='NULL', dest='log_to', help='''Disable logging completely.
A disabled logger is still created to make subsequent logging.getLogger calls by other parties return it.
Thus, this option cannot avoid the cost of importing logging early on.''')
(a := h())('-e', '--executor', choices=C, metavar=j, help='''Chooses a PEP 3148 executor class to use when necessary depending on the value of ETYP:
thread: Use concurrent.futures.thread.ThreadPoolExecutor. This is the default and will be used if the third-party options are passed but not installed.
process: Use concurrent.futures.process.ProcessPoolExecutor. Use with care, since this depends on CPU architecture.
interpreter: Use concurrent.futures.interpreter.InterpreterPoolExecutor. Experimental; may throw various errors relating to unshareable objects.
The below options are third-party.
loky_noreuse: Use a new loky.process_executor.ProcessPoolExecutor every time.
loky: Reuse a loky.process_executor.ProcessPoolExecutor if possible.
dask: Use dask.distributed.Client. May have API incompatibilities.
ipython: Use ipyparallel.ViewExecutor.
elib_flux_cluster: Use executorlib.executor.flux.FluxClusterExecutor.
elib_flux_job: Use executorlib.executor.flux.FluxJobExecutor.
elib_slurm_cluster: Use executorlib.executor.slurm.SlurmClusterExecutor.
elib_slurm_job: Use executorlib.executor.slurm.SlurmJobExecutor.
elib_single_node: Use executorlib.executor.single.SingleNodeExecutor.
pebble_thread: Use pebble.pool.thread.ThreadPool.
pebble_process: Use pebble.pool.process.ProcessPool.
More options may be added in the future.''')
a('-c', '--custom-executor', dest='executor', metavar=j, help='Use a custom executor not included in the above options by specifying the name of an implementation.\nPassing "package.submodule.Implementation", for example, will execute "from package.submodule import Implementation as Executor".')
for _ in C: a(i+_.replace('_', '-'), action=b, const=_, dest=d, help=e%_)
(a := (h := lambda t, d, f=p.add_argument_group: f(t, d).add_argument)('verbosity', 'Adjust the amount of output of this program.'))('-Q', action=g, default=0, help='Produce less logging output. Additive.')
a('-V', action=g, default=0, help='Produce more logging output. Additive.')
(a := h('repl', 'Configure the behaviour of the Read-Eval-Print Loop of this module.'))('-q', '--quiet', action=f, help='Do not display the banner and exit message in the REPL; the -q flag can be passed to the python command directly to achieve the same effect.')
a('-b', '--basic-repl', action=f, help='Do not use the console with colors and enhanced functionality from _pyrepl. Use only if you have experienced a bug with the colored console.')
a('-m', '--max-memerrs', type=int, metavar='M', help='''The REPL will exit on the M+1-th MemoryError to prevent consuming too many computer resources.
M defaults to 3.
Set to a negative value to disable the threshold completely.''')
(a := h('testing', 'Options to more conveniently test this module.'))('-p', '--load-all', action=f, help='Preload all submodules of this module. Useful for testing, but incurs noticeable performance penalty.')
a('-s', '--seed', help='Seed the random instance used internally by this module with SEED, which will be interpreted as an integer if possible.')
a('-d', '--debug', action=f, help='Enable debug mode to produce more logging output by entering the global debug context manager. Different from -VV, since the verbosity flags take effect when the context manager is manually exited.')
(a := h('metadata', 'Get information about this installation of asyncutils.'))('-v', '--version', action='version', version=V.representation, help='Print the current version number of asyncutils and exit. Useful for checking if the installation succeeded.')
a('-?', '-h', '--help', action='help', help='Print this help message and exit.')
del a, b, C, d, e, f, g, h, i, j, A, V