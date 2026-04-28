__lazy_modules__ = frozenset(('asyncio.tasks',))
from asyncutils import CRITICAL, Critical, IgnoreErrors, event_loop, getcontext
from asyncutils.constants import _NO_DEFAULT
from asyncutils._internal import log
from asyncutils._internal.helpers import fullname
from asyncutils._internal.patch import patch_function_signatures as f
from asyncutils._internal.submodules import signals_all as __all__
from asyncio.tasks import wait_for
async def wait_for_signal(p, /, *S, timeout=None, raise_on_timeout=False, loop=None, possible_errors=(Exception,), default_on_processor_failure=_NO_DEFAULT, sigs=None, logger=log, _i=IgnoreErrors(TypeError)): # noqa: PLR0912,PLR0915
    import sys as M; from signal import Signals as C, signal as _s, getsignal as _g
    (S := set(S)).update(getcontext().WAIT_FOR_SIGNAL_DEFAULT_SIGNALS if sigs is None else sigs)
    M.audit('asyncutils.signals.wait_for_signal', S); c, x = None, 0
    if loop is None: loop = (c := event_loop.from_flags(0)).__enter__()
    a, h = (F := loop.create_future()).add_done_callback, lambda s, _=None, F=F: F.done() or F.set_result(C(s))
    if M.platform == 'win32':
        logger.info('signals.wait_for_signal has limited functionality on windows')
        for s in S:
            try: o = _s(s := C(s), h)
            except ValueError as e: logger.warning('signals.wait_for_signal: invalid signal %s: %s', s, e)
            except OSError as e: logger.warning('signals.wait_for_signal: OS-level error for signal %s: %s', s.name, e)
            else: a(lambda _, s=s, o=o: _s(s, o)); x += 1; logger.debug('signals.wait_for_signal: registered handler for signal %s', s.name)
    else:
        for s in S:
            try: o = _g(s := C(s))
            except ValueError as e: logger.warning('signals.wait_for_signal: invalid signal %s: %s', s, e); continue
            try: loop.add_signal_handler(s, h, s)
            except NotImplementedError: break
            except PermissionError as e: logger.warning('signals.wait_for_signal: insufficient permissions for signal %s: %s', s.name, e)
            except OSError as e: logger.warning('signals.wait_for_signal: OS-level error for signal %s: %s', s.name, e)
            except RuntimeError as e: logger.warning('signals.wait_for_signal: error registering signal handler: %s', e)
            else: a(lambda _, s=s, o=o: loop.remove_signal_handler(s) and _s(s, o)); x += 1; logger.debug('signals.wait_for_signal: registered handler for signal %s', s.name)
    try:
        if x: logger.info('signals.wait_for_signal: signal handler registered successfully for total of %d signals', x); del x
        else: raise RuntimeError('signals.wait_for_signal: failed to register signal handler')
        try: s = await wait_for(F, timeout)
        except TimeoutError:
            if raise_on_timeout: raise
            return logger.warning('signals.wait_for_signal: timed out')
        logger.info('signals.wait_for_signal: signal received: %s', s.name)
        try:
            r = p(s)
            with _i: r = await r
        except possible_errors: logger.exception('signals.wait_for_signal processor %r encountered expected error for signal %s', p, s); return None if default_on_processor_failure is _NO_DEFAULT else default_on_processor_failure
        except CRITICAL: raise Critical
        except BaseException as e: raise RuntimeError(f'signals.wait_for_signal: unexpected {fullname(e)} in processor %r for signal %s', p, s) from e
        return r
    finally:
        F.cancel()
        if c: c.__exit__(*M.exc_info()) # type: ignore[arg-type]
f((wait_for_signal, 'processor, /, *signals, timeout=None, raise_on_timeout=False, loop=None, possible_errors={0}, default_on_processor_failure={0}, logger={0}'))
del f