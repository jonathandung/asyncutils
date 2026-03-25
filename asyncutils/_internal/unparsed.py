__doc__ = '''usage: python [-m] asyncutils [-l [FILE] | -n] [-e ETYP | -c EXECUTOR | --thread | --process | --interpreter | --loky | --loky-reuse | --dask | --elib-flux-cluster | --elib-flux-job | --elib-slurm-cluster | --elib-slurm-job | --elib-single-node | --pebble-thread | --pebble-process] [-Q] [-V] [-q] [-b] [-m M] [-p] [-s SEED] [-v] [-?]

A versatile, feature-rich library of async tools integrated into the asyncio framework, aiming to make asynchronous programming easier for everyone.
Has CLI and coloured REPL support for quick development.
Install with: `python -m pip install py-asyncutils`, or `python -m pip install git+https://github.com/jonathandung/asyncutils.git#egg=asyncutils` if that fails

options:
    -l, --log-to [FILE]     This module uses a logger, so that post-mortem debugging can be done by inspecting the log file created.
                            When FILE is passed (interpreted as an integer file descriptor if possible), the logging output goes to a file with that name.
                            Passing 'NULL' for FILE is equivalent to specifying the --no-log option.
                            Most of the logging output is created in debug mode only, to prevent cluttering of the stream.
                            If FILE is 'MEMORY', logs are stored in memory, accessible via get_past_logs, which also clears the logs.
                            If FILE is 'MAKE' or no filename is passed but the option specified, an attempt is made to create a file of format 'asyncutils_log<number>.log'
                            in the current directory for logging, for number from 1 to 4095.
                            If FILE is 'STDOUT', logs to stdout.
                            If FILE is 'STDERR', logs to stderr (also the default behaviour and fallback if the above steps fail).
    -n, --no-log            Disable logging completely.
                            A disabled logger is still created to make subsequent logging.getLogger calls by other parties return it.
                            Thus, this option cannot avoid the cost of importing logging early on.
    -e, --executor ETYP     Chooses a PEP 3148 executor class to use when necessary depending on the value of ETYP:
                            thread: Use concurrent.futures.thread.ThreadPoolExecutor. This is the default.
                            process: Use concurrent.futures.process.ProcessPoolExecutor. Use with care, since this depends on CPU architecture.
                            interpreter: Use concurrent.futures.interpreter.InterpreterPoolExecutor. Experimental; may throw various errors relating to unshareable objects.
                            The below options are third-party, and will raise ImportError if not installed.
                            loky: Use loky.process_executor.ProcessPoolExecutor.
                            loky_reuse: Reuse a loky.process_executor.ProcessPoolExecutor if possible.
                            dask: Use dask.distributed.Client. May have API incompatibilities.
                            ipython: Use ipyparallel.ViewExecutor.
                            elib_flux_cluster: Use executorlib.executor.flux.FluxClusterExecutor.
                            elib_flux_job: Use executorlib.executor.flux.FluxJobExecutor.
                            elib_slurm_cluster: Use executorlib.executor.slurm.SlurmClusterExecutor.
                            elib_slurm_job: Use executorlib.executor.slurm.SlurmJobExecutor.
                            elib_single_node: Use executorlib.executor.single.SingleNodeExecutor.
                            pebble_thread: Use pebble.pool.thread.ThreadPool.
                            pebble_process: Use pebble.pool.process.ProcessPool.
                            More options may be added in the future.
    -c, --custom-executor ETYP
                            Use a custom executor not included in the above options by specifying the fully qualified name of an implementation.
                            Passing "-c package.submodule.Implementation", for example, will execute "from package.submodule import Implementation as Executor".
    --thread                Equivalent to "-e thread".
    --process               Equivalent to "-e process".
    --interpreter           Equivalent to "-e interpreter".
    --loky                  Equivalent to "-e loky".
    --loky-reuse            Equivalent to "-e loky_reuse".
    --dask                  Equivalent to "-e dask".
    --ipython               Equivalent to "-e ipython".
    --elib-flux-cluster     Equivalent to "-e elib_flux_cluster".
    --elib-flux-job         Equivalent to "-e elib_flux_job".
    --elib-slurm-cluster    Equivalent to "-e elib_slurm_cluster".
    --elib-slurm-job        Equivalent to "-e elib_slurm_job".
    --elib-single-node      Equivalent to "-e elib_single_node".
    --pebble-thread         Equivalent to "-e pebble_thread".
    --pebble-process        Equivalent to "-e pebble_process".

verbosity:
    Adjust the amount of output of this program.

    -Q                      Produce less logging output. Additive.
    -V                      Produce more logging output. Additive.

repl:
    Configure the behaviour of the Read-Eval-Print Loop of this module.

    -q, --quiet             Do not display the banner and exit message in the REPL; the -q flag can be passed to the python command directly to achieve the same effect.
    -b, --basic-repl        Do not use the console with colors and enhanced functionality from _pyrepl. Use only if you have experienced a bug with the colored console.
    -m, --max-memerrs M     The REPL will exit on the M+1-th MemoryError to prevent consuming too many computer resources.
                            M defaults to 3.
                            Set to a negative value to disable the threshold completely.

testing:
    Options to more conveniently test this module.

    -p, --load-all          Preload all submodules of this module. Useful for testing, but incurs noticeable performance penalty.
    -s, --seed SEED         Seed the random instance used internally by this module with SEED, which will be interpreted as an integer if possible.

metadata:
    Get information about this installation of asyncutils.

    -v, --version           Print the current version number of asyncutils and exit.
    -?, -h, --help          Print this help message and exit.

Use @<filename> to insert command-line arguments from the file of that name at the exact position of this parameter; the file should have one argument per line.

If using this module without exposing the command line, use the AUTILSCFGPATH environment variable to specify a path to a .json or .jsonl file.
Other json formats are not currently supported; see the possible keys in format.jsonc, which can be accessed using tools.get_cfg_json_format().

Note that the API of this module is probably incompatible with full-fledged third-party async frameworks such as curio and trio.'''
N = type('Namespace', (dict,), {'__getattr__': dict.__getitem__, '__setattr__': dict.__setitem__, '__delattr__': dict.__delitem__})(log_to='STDERR', executor='thread', Q=0, V=0, quiet=False, basic_repl=False, max_memerrs=3, load_all=False, seed=None)
if p := (E := __import__('os').environ).get(k := 'AUTILSCFGPATH', '').strip('"\''):
    import sys as S
    if not p.endswith(('.json', '.jsonl')): S.stderr.write('WARNING: AUTILSCFGPATH should point to a json file; proceeding anyway\n')
    with open(p.strip()) as f:
        S.audit('asyncutils/read_config', p)
        if (t := type(f := __import__('json').load(f))) is not dict: raise TypeError(f'incorrent json format for asyncutils configuration; top-level structure should be an object, not {t.__name__!r}')
        if isinstance(v := f.pop('next_config', p), str): E[k] = v
        elif v is None: del E[k]
        else: raise TypeError(f'key "next_config" in {p} should point to a string or null, not {v!r}; see format.jsonc')
        N.update(f)
    del S, f, v, t
del p, E, k