def __dir__(_=(__all__ := ('run',))): return _
def run():
    import sys as S; S._xoptions['asyncutils_run_as_main'] = True; S.audit('asyncutils.cli.run'); import asyncutils._internal.initialize
    with asyncutils.event_loop.from_flags(0) as g: return asyncutils.AsyncUtilsConsole(g).run(suppress_asyncio_warnings=True, suppress_unawaited_coroutine_warnings=True, always_run_interactive=len(A := S.orig_argv) == 2 and A[0] == S.executable and A[1].endswith(('/bin/autils.exe', '/bin/asyncutils.exe', r'\Scripts\asyncutils.exe', r'\Scripts\autils.exe'))) # noqa: PLR2004