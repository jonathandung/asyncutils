import asyncio, sys, os
from signal import Signals
from pytest import fixture, mark, raises
from asyncutils.signals import wait_for_signal
async def kill(sig):
    await asyncio.sleep(0.05)
    os.kill(os.getpid(), sig)
async def processor(sig): return sig.value
async def bad_processor(sig): return 1/0
@mark.skipif(W := sys.platform == 'win32', reason='difficult to test signal handling on windows')
@mark.parametrize('res', range(1, 8, 3))
async def test_signal(res):
    _ = asyncio.create_task(kill(sig := Signals(res)))
    assert res == await wait_for_signal(processor, sig, timeout=0.1)
class Log(BaseException): ...
def raise_(msg, *a, exc_info=False): raise Log(msg%a)
def ignore(*_): ...
@fixture(scope='module')
def mock_logger(): return type(sys.implementation)(warning=raise_, error=raise_, exception=raise_, info=ignore, debug=ignore) # type: ignore
@fixture(scope='module')
def wait_partial(mock_logger): return __import__('_functools').partial(wait_for_signal, processor, logger=mock_logger)
@mark.skipif(sys.platform != 'linux', reason='these tests are only for linux')
async def test_signal_log(wait_partial):
    with raises(Log, match='invalid signal None: .*'): await wait_partial(None)
    with raises(Log, match='wait_for_signal timed out'): await wait_partial(Signals.SIGILL, timeout=0.05)
    with raises(Log, match=r'(insufficient permissions for signal .*: .*)|(error registering signal handler: sig \d+ cannot be caught)'): await wait_partial(19, timeout=0.1)
async def test_signal_raise(wait_partial):
    with raises(TimeoutError): await wait_partial(Signals.SIGFPE, timeout=0.05, raise_on_timeout=True)