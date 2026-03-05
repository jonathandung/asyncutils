import sys
from signal import signal, getsignal, Signals
from asyncio.tasks import wait_for
from ._internal.helpers import pkgpref
from ._internal.patch import patch_function_signatures as f
from .config import _NO_DEFAULT
from .exceptions import Critical, IgnoreErrors, CRITICAL
from .base import event_loop
from .util import safe_cancel
from ._internal import log
from ._internal.submodules import signals_all as __all__
async def wait_for_signal(p, /, *S, timeout=None, raise_on_timeout=False, loop=None, possible_errors=(Exception,), default_on_processor_failure=_NO_DEFAULT, logger=log, _i=IgnoreErrors(TypeError), _c=Signals, _d=(Signals.SIGINT, Signals.SIGTERM), _s=signal, _g=getsignal):
    sys.audit(f'{pkgpref}signals.wait_for_signal', S := tuple(map(_c, S)) or _d); c, x = None, 0
    if loop is None: loop = (c := event_loop.from_flags(0)).__enter__()
    a = (F := loop.create_future()).add_done_callback
    def hdlr(s, f=None, F=F):
        if not F.done(): F.set_result(s)
    if sys.platform == 'win32':
        logger.info('wait_for_signal has limited functionality on windows')
        for s in S:
            try: o = _s(s, hdlr)
            except ValueError as e: logger.warning(f'invalid signal {s}: {e}')
            except PermissionError as e: logger.warning(f'insufficient permissions for signal {s}: {e}')
            except OSError as e: logger.warning(f'OS-level error for signal {s}: {e}')
            else: a(lambda _, s=s, o=o: _s(s, o)); x += 1; logger.debug(f'wait_for_signal: registered handler for signal {s}')
    else:
        for s in S:
            try: o = _g(s)
            except ValueError as e: logger.warning(f'invalid signal: {e}'); continue
            try: loop.add_signal_handler(s, hdlr, s)
            except NotImplementedError: break
            except RuntimeError as e: logger.warning(f'error registering signal handler: {e}')
            else: a(lambda _: loop.remove_signal_handler(s) and _s(s, o)); x += 1; logger.debug(f'wait_for_signal: registered for signal {s}')
    try:
        if x: logger.info(f'signal handler registered successfully for total of {x} signals'); del x
        else: raise RuntimeError('signal handler could not be registered')
        try: s = await wait_for(F, timeout)
        except TimeoutError:
            if raise_on_timeout: raise
            logger.warning(f'wait_for_signal timed out; signals: {S}')
        logger.info(f'signal received: {s}')
        try: s = p(s)
        except possible_errors as e:
            logger.error(f'wait_for_signal processor {p!r} encountered {type(e).__name__} for signal {s}', exc_info=True)
            return None if default_on_processor_failure is _NO_DEFAULT else default_on_processor_failure
        except CRITICAL: raise Critical
        except BaseException as e: raise RuntimeError(f'wait_for_signal: unexpected {type(e).__name__} in processor {p!r} for signal {s}: {e}') from None
        with _i: s = await s
        return s
    finally:
        await safe_cancel(F)
        if c: c.__exit__(*sys.exc_info()) # type: ignore
f((wait_for_signal, 'processor, /, *signals, timeout=None, raise_on_timeout=False, loop=None, possible_errors={0}, default_on_processor_failure={0}, logger={0}'))
del signal, getsignal, Signals, f