__all__ = 'run',
from ._internal import initialize
def run():
    __import__('sys')._xoptions['asyncutils_run_as_main'] = True; from . import base, console
    with base.event_loop.from_flags(0) as g: raise SystemExit(console.AsyncUtilsConsole(g).run(suppress_asyncio_warnings=True, suppress_unawaited_coroutine_warnings=True))
del initialize