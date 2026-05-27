import asyncio, sys, os
from signal import Signals
from pytest import fixture, mark, raises, warns
from asyncutils import WarningToError
from asyncutils.signals import wait_for_signal
from tests.conftest import mk
async def kill(sig):
    await asyncio.sleep(0.05)
    os.kill(os.getpid(), sig)
async def processor(sig): return sig.value
async def bad_processor(sig): return 1/0
@(dec := mark.skipif(win := sys.platform == 'win32', reason='difficult to test signal handling on Windows'))
@mk
@mark.parametrize('res', range(1, 8, 3))
async def test_signal(res):
    _ = asyncio.create_task(kill(sig := Signals(res)))
    assert res == await wait_for_signal(processor, sig, timeout=0.05)
class Log(BaseException): ...
def raise_(msg, *a, exc_info=False): raise Log(msg%a)
def ignore(*_): ...
@fixture(scope='module')
def wait_partial(): return __import__('_functools').partial(wait_for_signal, processor, logger=type(sys.implementation)(warning=raise_, error=raise_, exception=raise_, info=ignore, debug=ignore))
@dec
@mk
async def test_signal_log(wait_partial):
    with raises(Log, match=r'signals\.wait_for_signal: invalid signal None'): await wait_partial(None)
    with raises(Log, match=r'signals\.wait_for_signal: timed out'): await wait_partial(4, timeout=0.05)
    with raises(Log, match=r'signals\.wait_for_signal: timed out' if sys.platform == 'darwin' else r'signals\.wait_for_signal: (insufficient permissions|error registering signal handler) for signal SIGSTOP'): await wait_partial(19, timeout=0.05)
@mk
async def test_signal_raise(wait_partial):
    with raises(TimeoutError), warns(RuntimeWarning, match=r'signals\.wait_for_signal has limited functionality on Windows') if win else WarningToError(): await wait_partial(Signals.SIGFPE, timeout=0.05, raise_on_timeout=True)