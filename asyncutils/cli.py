def __dir__(_=(__all__ := ('run',))): return _
def run(argv=None):
    if isinstance(argv, str): raise TypeError('asyncutils.cli.run: parameter argv must be a non-string iterable')
    import asyncutils as A, asyncutils._internal as I, sys as S; I.parsed.p.parse_args(argv, I.unparsed.N); I.initialize; S.audit('asyncutils.cli.run') # noqa: B018
    try:
        with A.event_loop() as g: return A.AsyncUtilsConsole(g).run(suppress_asyncio_warnings=True, suppress_unawaited_coroutine_warnings=True, always_run_interactive=len(a := S.orig_argv) == 2 and a[0] == S.executable and a[1].endswith(('/bin/autils.exe', '/bin/asyncutils.exe', r'\Scripts\asyncutils.exe', r'\Scripts\autils.exe'))) # noqa: PLR2004
    except BaseException as e:
        if not A.pdb: raise
        __import__('_warnings').warn('asyncutils.cli.run: unprecedented exception with no traceback caught; cannot perform autopsy as requested', RuntimeWarning, 2) if (t := e.__traceback__) is None else __import__('pdb').post_mortem(t)