from pytest import mark, raises
from asyncio import create_task, new_event_loop, sleep
from asyncutils import _internal as mod, AsyncUtilsConsole
from io import StringIO
from tests.conftest import mk
import sys
def test_helpers():
    helpers = mod.helpers
    for _ in helpers.filter_out(None, True, False): assert isinstance(_, bool)
    assert helpers.check_methods('', 'lower', 'casefold')
    assert helpers.check_methods(b'', '__doc__')
    assert not helpers.check_methods(int, 'bit_count')
    assert not helpers.check_methods(0, 'bit_length', 'bar')
    with raises(AttributeError): helpers.copy_and_clear(())
    class _: ...
    assert helpers.subscriptable(_) is _
    o = _[None]()
    o.foo = lambda: None
    assert not helpers.check_methods(_(), 'foo')
    assert not helpers.check_methods(o, 'foo')
def test_submods_lazy_loading():
    module = mod.initialize.Module
    with raises(AttributeError, match="module 'asyncutils' has no attribute 'foo'"): module('foo')
    with raises(TypeError, match='cannot subclass the type of asyncutils submodule objects'): type('', (module,), {})
    assert (t := type(module('constants'))) is type(module('context')) and t.__module__ == 'builtins' and t.__name__ == t.__qualname__ == 'module'
def test_others(cfgjson, monkeypatch):
    assert type(mod.log).__module__ == 'logging'
    assert mod.running_console.getc() is mod.running_console.unsetc() is None
    loop = new_event_loop()
    t = loop.close, loop.stop
    mod.running_console.setc(cons := AsyncUtilsConsole(loop))
    assert mod.running_console.unsetc() is cons
    with raises(RuntimeError, match='cannot close event loop within REPL'): loop.close()
    with raises(RuntimeError, match='cannot stop event loop within REPL'): loop.stop()
    loop.close, loop.stop = t
    cons.refresh()
    exec(cons.compile.compiler('assert 1+1 == 2', '<test>', 'exec'))
    assert cons.retcode == 0
    loop.close()
    assert mod.submodules.cli_all == ('run',)
    monkeypatch.setenv('AUTILSCFGPATH', cfgjson)
    N = __import__('importlib').reload(mod.unparsed).N
    assert N.load_all and N.V == 2
def test_patch():
    patch = mod.patch
    patch.patch_function_signatures((f := lambda _: None, 'foo, {}'))
    assert f.__text_signature__ == '(foo, <unrepresentable>)'
    patch.patch_method_signatures((f, patch.xsig))
    assert f.__text_signature__ == '($self, exc_typ, exc_val, exc_tb, /)'
    patch.patch_classmethod_signatures((f, ''))
    assert f.__text_signature__ == '($cls)'
@mark.skipif(sys.version_info >= (3, 13), reason='requires Python <3.13')
@mk
async def test_py312():
    m = mod.py312
    Q = m.Queue(2)
    await Q.put(0)
    await Q.put(1)
    assert Q.full()
    with raises(m.QueueFull): Q.put_nowait(-1)
    t = create_task(Q.put(2))
    assert await Q.get() == 0
    assert Q.get_nowait() == 1
    await sleep(0)
    assert t.done() and await Q.get() == 2
    t = create_task(Q.get())
    Q.put_nowait(3)
    Q.task_done()
    await sleep(0)
    assert t.done() and t.result() == 3 and Q.empty()
    with raises(m.QueueEmpty): Q.get_nowait()
    Q.shutdown()
    with raises(m.QueueShutDown): Q.put_nowait(-2)
    with raises(m.QueueShutDown): await Q.put(-3)
    with raises(m.QueueShutDown): Q.get_nowait()
    with raises(m.QueueShutDown): await Q.get()
    t = create_task(Q.join())
    Q.task_done()
    await sleep(0)
    assert not t.done()
    Q.task_done()
    Q.shutdown(True)
    Q.task_done()
    await sleep(0)
    assert t.done()
    with raises(ValueError, match=r'task_done\(\) called too many times'): Q.task_done()
@mark.skipif(sys.version_info >= (3, 13), reason='requires Python <3.14')
def test_py313():
    m = mod.py313
    h = [1, 5, 3]
    m.heapify(h)
    m.heappush(h, 8)
    assert m.heapreplace(h, 10) == 8 and m.heappushpop(h, 13) == 13
    assert m.heappop(h) == 10
    assert m.heappop(h) == 5
    assert m == [3, 1]
    with raises(TypeError, match='trailing Placeholders are not allowed'): m.partial(lambda *_: None, m.Placeholder)
    sio = StringIO()
    p = m.partial(print, 'baz', m.Placeholder, 'foo', end='bar', file=sio)
    with raises(TypeError): p()
    p(42)
    p(1, 2)
    assert sio.getvalue() == 'baz 42 foobarbaz 1 foo 2bar'