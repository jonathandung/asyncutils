import asyncio, os
from asyncutils.signals import wait_for_signal
from signal import Signals
from pytest import mark, raises, fixture
async def kill(sig):
    await asyncio.sleep(0.1)
    os.kill(os.getpid(), sig)
async def processor(sig): return sig.value
async def bad_processor(sig): return 1/0
@mark.asyncio
@mark.skipif(W := __import__('sys').platform == 'win32', reason='difficult to test signal handling on windows')
@mark.parametrize('res', range(1, 9))
async def test_signal(res):
    asyncio.create_task(kill(sig := Signals(res)))
    assert res == await wait_for_signal(processor, sig, timeout=0.2)
class Log(BaseException): ...
def raise_(msg, exc_info=False): raise Log(msg)
def ignore(*_): ...
@fixture(scope='module')
def mock_logger(): return type(__import__('sys').implementation)(warning=raise_, error=raise_, info=ignore, debug=ignore)
@mark.asyncio
async def test_signal_raise(mock_logger):
    f = __import__('functools').partial(wait_for_signal, processor, loop=asyncio.get_running_loop(), logger=mock_logger)
    with raises(Log, match='invalid signal .*: .*'): await f(None)
    if not W:
        with raises(Log, match=r'(insufficient permissions for signal .*: .*)|(error registering signal handler: sig \d+ cannot be caught)'): await f(19, timeout=0.1)
        with raises(Log, match='wait_for_signal processor .* encountered expected ZeroDivisionError for signal SIGINT'):
            asyncio.create_task(kill(s := Signals.SIGINT))
            await wait_for_signal(bad_processor, s, timeout=0.2, possible_errors=(ZeroDivisionError,), logger=mock_logger)
    with raises(Log, match='wait_for_signal timed out'): await f(Signals.SIGILL, timeout=0.1)
    with raises(TimeoutError): await f(Signals.SIGFPE, timeout=0.1, raise_on_timeout=True)