from ._internal import log
from ._internal.patch import patch_function_signatures as f
from ._internal.submodules import signals_all as __all__
from .base import event_loop
from .constants import _NO_DEFAULT
from .exceptions import CRITICAL, Critical, IgnoreErrors
from .util import safe_cancel
from asyncio.tasks import wait_for
from signal import Signals, getsignal, signal
async def wait_for_signal(p, /, *S, timeout=None, raise_on_timeout=False, loop=None, possible_errors=(Exception,), default_on_processor_failure=_NO_DEFAULT, sigs=(Signals.SIGINT, Signals.SIGTERM), logger=log, _i=IgnoreErrors(TypeError), _c=Signals, _s=signal, _g=getsignal): # noqa: PLR0912,PLR0915
    import sys; sys.audit('asyncutils.signals.wait_for_signal', S := (*S, *sigs)); c, x = None, 0
    if loop is None: loop = (c := event_loop.from_flags(0)).__enter__()
    a, h = (F := loop.create_future()).add_done_callback, lambda s, _=None, F=F: F.done() or F.set_result(s)
    if sys.platform == 'win32': # pragma: no cover
        logger.info('wait_for_signal has limited functionality on windows')
        for s in S:
            try: o = _s(s := _c(s), h)
            except ValueError as e: logger.warning('invalid signal %s: %s', s, e)
            except OSError as e: logger.warning('OS-level error for signal %s: %s', s.name, e)
            else: a(lambda _, s=s, o=o: _s(s, o)); x += 1; logger.debug('wait_for_signal: registered handler for signal %s', s.name)
    else:
        for s in S:
            try: o = _g(s := _c(s))
            except ValueError as e: logger.warning('invalid signal %s: %s', s, e); continue
            try: loop.add_signal_handler(s, h, s)
            except NotImplementedError: break
            except PermissionError as e: logger.warning('insufficient permissions for signal %s: %s', s.name, e)
            except OSError as e: logger.warning('OS-level error for signal %s: %s', s.name, e)
            except RuntimeError as e: logger.warning('error registering signal handler: %s', e)
            else: a(lambda _, s=s, o=o: loop.remove_signal_handler(s) and _s(s, o)); x += 1; logger.debug('wait_for_signal: registered handler for signal %s', s.name)
    try:
        if x: logger.info('signal handler registered successfully for total of %d signals', x); del x
        else: raise RuntimeError('failed to register signal handler')
        try: s = await wait_for(F, timeout)
        except TimeoutError:
            if raise_on_timeout: raise
            return logger.warning('wait_for_signal timed out')
        logger.info('signal received: %s', s.name)
        try:
            r = p(s)
            with _i: r = await r
        except possible_errors as e: logger.exception('wait_for_signal processor %r encountered expected %s for signal %s', p, type(e).__qualname__, s); return None if default_on_processor_failure is _NO_DEFAULT else default_on_processor_failure
        except CRITICAL: raise Critical
        except BaseException as e: raise RuntimeError('wait_for_signal: unexpected %s in processor %r for signal %s: %s', type(e).__qualname__, p, s, e) from None # noqa: BLE001
        return s
    finally:
        await safe_cancel(F)
        if c: c.__exit__(*sys.exc_info()) # type: ignore[arg-type]
f((wait_for_signal, 'processor, /, *signals, timeout=None, raise_on_timeout=False, loop=None, possible_errors={0}, default_on_processor_failure={0}, logger={0}'))
del signal, getsignal, Signals, f