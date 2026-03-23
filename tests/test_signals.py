import asyncio, os
from asyncutils.signals import wait_for_signal
from asyncutils._internal import log
from signal import Signals
from pytest import mark, raises
async def kill(sig):
    await asyncio.sleep(0.1)
    os.kill(os.getpid(), sig)
async def processor(sig): return sig.value
@mark.asyncio
@mark.skipif(W := __import__('sys').platform == 'win32', reason='difficult to test signal handling on windows')
@mark.parametrize('res', (15, 11, 7))
async def test_signal(res):
    asyncio.create_task(kill(sig := Signals(res)))
    assert res == await wait_for_signal(processor, sig, timeout=0.2)
class Log(BaseException): ...
def raise_(msg): raise Log(msg)
@mark.asyncio
async def test_signal_raise(monkeypatch):
    f = __import__('functools').partial(wait_for_signal, processor, loop=asyncio.get_running_loop())
    with raises(RuntimeError, match='failed to register signal handler'): await f(-1)
    monkeypatch.setattr(log, 'warning', raise_)
    with raises(Log, match='invalid signal .*: .*'): await f(None)
    if not W:
        with raises(Log, match=r'(insufficient permissions for signal .*: .*)|(error registering signal handler: sig \d+ cannot be caught)'): await f(Signals.SIGSTOP, timeout=0.1)
    with raises(Log, match='wait_for_signal timed out'): await f(Signals.SIGILL, timeout=0.1)
    with raises(TimeoutError): await f(Signals.SIGABRT, timeout=0.1, raise_on_timeout=True)