import asyncio, os
from asyncutils.signals import wait_for_signal
from asyncutils.base import event_loop
from signal import Signals
from pytest import mark, raises, fixture
async def kill(sig):
    await asyncio.sleep(0.05)
    os.kill(os.getpid(), sig)
async def processor(sig): return sig.value
async def bad_processor(sig): return 1/0
@mark.asyncio
@mark.skipif(W := __import__('sys').platform == 'win32', reason='difficult to test signal handling on windows')
@mark.parametrize('res', range(1, 9))
async def test_signal(res):
    asyncio.create_task(kill(sig := Signals(res)))
    assert res == await wait_for_signal(processor, sig, timeout=0.1)
class Log(BaseException): ...
def raise_(msg, exc_info=False): raise Log(msg)
def ignore(*_): ...
@fixture(scope='module')
def mock_logger(): return type(__import__('sys').implementation)(warning=raise_, error=raise_, info=ignore, debug=ignore)
@fixture(scope='module')
def wait_partial(mock_logger): return __import__('functools').partial(wait_for_signal, processor, logger=mock_logger)
@fixture
def run_in_loop():
    with event_loop() as l: yield l.run_until_complete
def test_signal_log(wait_partial, run_in_loop):
    with raises(Log, match='invalid signal None: .*'): run_in_loop(wait_partial(None))
    with raises(Log, match='wait_for_signal timed out'): run_in_loop(wait_partial(Signals.SIGILL, timeout=0.05))
@mark.skipif(W, reason='these tests are only for unix')
def test_signal_log_unix(mock_logger, wait_partial, run_in_loop):
    with raises(Log, match=r'(insufficient permissions for signal .*: .*)|(error registering signal handler: sig \d+ cannot be caught)'): run_in_loop(wait_partial(19, timeout=0.1))
    with raises(Log, match='wait_for_signal processor .* encountered expected ZeroDivisionError for signal (SIGINT|2)'):
        run_in_loop.__self__.create_task(kill(s := Signals.SIGINT))
        run_in_loop(wait_for_signal(bad_processor, s, timeout=0.1, possible_errors=(ZeroDivisionError,), logger=mock_logger))
@mark.asyncio
async def test_signal_raise(wait_partial):
    with raises(TimeoutError): await wait_partial(Signals.SIGFPE, timeout=0.05, raise_on_timeout=True)