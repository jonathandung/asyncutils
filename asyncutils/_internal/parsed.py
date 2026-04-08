from .. import __version__ as V
from ..constants import POSSIBLE_EXECUTORS as c
from .compat import apargs as j
import argparse as A
i, b, d, e, f, g, j, p = '--', 'store_const', 'executor', 'Equivalent to "-e %s".', 'store_true', 'count', 'ETYP', A.ArgumentParser(prog='python [-m] asyncutils', description='''A versatile, feature-rich library of async tools integrated into the asyncio framework, aiming to make asynchronous programming easier for everyone.
Has CLI and coloured REPL support for quick development.
On both conda and pip as `py-asyncutils`.''', add_help=False, fromfile_prefix_chars='@', formatter_class=A.RawTextHelpFormatter, epilog='''Use @<filename> to insert command-line arguments from the file of that name at the exact position of this parameter.
The file should have one argument per line.
This format differs from that described below.

Use the AUTILSCFGPATH environment variable to specify a path to a .json or .jsonl file containing the default configuration.
Other json formats are not currently supported; see the possible keys in format.json5, which can be accessed using `tools.get_cfg_json_format()`.

Note that the API of this module is probably incompatible with full-fledged third-party async frameworks such as curio, anyio, trio, tornado, or FastAPI.''', **j)
(a := (h := lambda f=p.add_mutually_exclusive_group: f().add_argument)())('-l', '--log-to', nargs='?', const='MAKE', default='STDERR', metavar='FILE', help='''This module uses a logger, so that post-mortem debugging can be done by inspecting the log file created.
When FILE is passed (interpreted as an integer file descriptor if possible), the logging output goes to a file with that name.
Passing 'NULL' for FILE is equivalent to specifying the --no-log option.
Most of the logging output is created in debug mode only, to prevent cluttering of the stream.
If FILE is 'MEMORY', logs are stored in memory and returned and voided whenever get_past_logs is called.
If FILE is 'MAKE' or no filename is passed but the option specified, an attempt is made to create a file of format 'asyncutils_log<number>.log'
in the current directory for logging, for number from 1 to 4095.
If FILE is 'STDOUT', logs to stdout.
If FILE is 'STDERR', logs to stderr (also the default behaviour and fallback if the above steps fail).''')
a('-n', '--no-log', action=b, const='NULL', default=A.SUPPRESS, dest='log_to', help='''Disable logging completely.
A disabled logger is still created to make subsequent logging.getLogger calls by other parties return it.
Thus, this option cannot avoid the cost of importing logging early on.''')
(a := h())('-e', '--executor', choices=c, default='thread', metavar=j, help='''Chooses a PEP 3148 executor class to use when necessary depending on the value of ETYP:
thread: Use concurrent.futures.thread.ThreadPoolExecutor. This is the default.
process: Use concurrent.futures.process.ProcessPoolExecutor. Use with care, since this depends on CPU architecture.
interpreter: Use concurrent.futures.interpreter.InterpreterPoolExecutor. Experimental; may throw various errors relating to unshareable objects.
The below options are third-party; ThreadPoolExecutor will be used instead if these are passed but not installed.
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
for _ in c: a(i+_.replace('_', '-'), action=b, const=_, dest=d, help=e%_)
(a := (h := lambda t, d, f=p.add_argument_group: f(t, d).add_argument)('verbosity', 'Adjust the amount of output of this program.'))('-Q', action=g, default=0, help='Produce less logging output. Additive.')
a('-V', action=g, default=0, help='Produce more logging output. Additive.')
(a := h('repl', 'Configure the behaviour of the Read-Eval-Print Loop of this module.'))('-q', '--quiet', action=f, help='Do not display the banner and exit message in the REPL; the -q flag can be passed to the python command directly to achieve the same effect.')
a('-b', '--basic-repl', action=f, help='Do not use the console with colors and enhanced functionality from _pyrepl. Use only if you have experienced a bug with the colored console.')
a('-m', '--max-memerrs', type=int, default=3, metavar='M', help='''The REPL will exit on the M+1-th MemoryError to prevent consuming too many computer resources.
M defaults to 3.
Set to a negative value to disable the threshold completely.''')
(a := h('testing', 'Options to more conveniently test this module.'))('-p', '--load-all', action=f, help='Preload all submodules of this module. Useful for testing, but incurs noticeable performance penalty.')
a('-s', '--seed', help='Seed the random instance used internally by this module with SEED, which will be interpreted as an integer if possible.')
a('-d', '--debug', action=f, help='Enable debug mode to produce more logging output.')
(a := h('metadata', 'Get information about this installation of asyncutils.'))('-v', '--version', action='version', version=V.representation, help='Print the current version number of asyncutils and exit. Useful for checking if the installation succeeded.')
a('-?', '-h', '--help', action='help', default=A.SUPPRESS, help='Print this help message and exit.')
del a, b, c, d, e, f, g, h, i, j, A, V