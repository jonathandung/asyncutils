import asyncutils as A, signal as B, sys as M
from asyncutils.constants import _NO_DEFAULT
from asyncutils._internal import log, helpers as H
from asyncutils._internal.running_console import getc
from asyncutils._internal.submodules import signals_all as __all__
from asyncio.tasks import wait_for
async def wait_for_signal(p, /, *S, timeout=None, raise_on_timeout=False, loop=None, possible_errors=(Exception,), default_on_processor_failure=_NO_DEFAULT, sigs=None, logger=log): # noqa: PLR0912,PLR0915
    if loop is None: loop = H.get_loop_and_set()
    P, x, a, h = (S := {*S, *(A.getcontext().WAIT_FOR_SIGNAL_DEFAULT_SIGNALS if sigs is None else sigs)}).pop, 0, (F := loop.create_future()).add_done_callback, lambda s, _=None, F=F: F.done() or F.set_result(B.Signals(s)); M.audit('asyncutils.signals.wait_for_signal', S)
    if M.platform == 'win32':
        if getc() is None: __import__('_warnings').warn('signals.wait_for_signal has limited functionality on windows', RuntimeWarning, 2)
        while S:
            s = P()
            try: o = B.signal(s := B.Signals(s), h)
            except ValueError: logger.exception('signals.wait_for_signal: invalid signal %r', s)
            except OSError: logger.exception('signals.wait_for_signal: OS-level error for signal %s', s.name) # ty: ignore[unresolved-attribute]
            else: a(lambda _, s=s, o=o: B.signal(s, o)); x += 1; logger.debug('signals.wait_for_signal: registered handler for signal %s', s.name)
    else:
        while S:
            s = P()
            try: o = B.getsignal(s := B.Signals(s))
            except ValueError: logger.exception('signals.wait_for_signal: invalid signal %r', s); continue
            try: loop.add_signal_handler(s, h, s)
            except NotImplementedError: break
            except PermissionError: logger.exception('signals.wait_for_signal: insufficient permissions for signal %s', s.name)
            except OSError: logger.exception('signals.wait_for_signal: OS-level error for signal %s', s.name)
            except RuntimeError: logger.exception('signals.wait_for_signal: error registering signal handler for signal %s', s.name)
            else: a(lambda _, s=s, o=o: loop.remove_signal_handler(s) and B.signal(s, o)); x += 1; logger.debug('signals.wait_for_signal: registered handler for signal %s', s.name)
    try:
        if x: logger.info('signals.wait_for_signal: signal handler registered successfully for total of %d signals', x); del x
        else: raise RuntimeError('asyncutils.signals.wait_for_signal: failed to register signal handler')
        try: s = await wait_for(F, timeout)
        except TimeoutError:
            if raise_on_timeout: raise
            return logger.warning('signals.wait_for_signal: timed out')
        logger.info('signals.wait_for_signal: signal received: %s', s.name)
        try:
            r = p(s)
            with A.ignore_typeerrs: r = await r
        except possible_errors: logger.exception('signals.wait_for_signal processor %r encountered expected error for signal %s', p, s); return None if default_on_processor_failure is _NO_DEFAULT else default_on_processor_failure
        except A.CRITICAL: raise A.Critical
        except BaseException as e: raise RuntimeError(f'asyncutils.signals.wait_for_signal: unexpected {H.fullname(e)} in processor {p!r} for signal {s.name}') from e
        return r
    finally: await A.safe_cancel(F)
wait_for_signal.__text_signature__ = '(processor, /, *signals, sigs=None, timeout=None, raise_on_timeout=False, loop=None, possible_errors={0}, default_on_processor_failure={0}, logger={0})' # ty: ignore[unresolved-attribute]