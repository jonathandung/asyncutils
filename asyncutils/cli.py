def __dir__(_=(__all__ := ('run',))): return _
def run(argv=None):
    import asyncutils as A, asyncutils._internal as I, sys as S; I.parsed.p.parse_args(argv, I.unparsed.N); I.initialize; S.audit('asyncutils.cli.run') # noqa: B018
    try:
        with A.event_loop.from_flags(0) as g: return A.AsyncUtilsConsole(g).run(suppress_asyncio_warnings=True, suppress_unawaited_coroutine_warnings=True, always_run_interactive=len(a := S.orig_argv) == 2 and a[0] == S.executable and a[1].endswith(('/bin/autils.exe', '/bin/asyncutils.exe', r'\Scripts\asyncutils.exe', r'\Scripts\autils.exe'))) # noqa: PLR2004
    except:
        if A.pdb: __import__('pdb').post_mortem(); return 1
        raise