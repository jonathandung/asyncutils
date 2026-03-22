__all__ = 'run',
def run():
    __import__('sys')._xoptions['asyncutils_run_as_main'] = True; from ._internal import initialize; from . import base, console; del initialize
    with base.event_loop.from_flags(0) as g: return console.AsyncUtilsConsole(g).run(suppress_asyncio_warnings=True, suppress_unawaited_coroutine_warnings=True)