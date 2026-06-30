from pytest import mark, raises
from asyncio import QueueEmpty, QueueFull, create_task, new_event_loop, sleep
from asyncutils import _internal as mod
from asyncutils.console import AsyncUtilsConsole
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
def test_submodules_lazy_loading():
    with raises(AttributeError, match="module 'asyncutils._internal' has no attribute 'foo'"): mod.foo
    module = mod.initialize.Module
    with raises(AttributeError, match="module 'asyncutils' has no attribute 'foo'"): module('foo')
    with raises(TypeError, match='asyncutils: cannot subclass the type of submodule objects'): type('', (module,), {})
    assert (t := type(module('constants'))) is type(module('context'))
    assert t.__module__ == 'builtins'
    assert t.__name__ == t.__qualname__ == 'module'
def test_others(config_json, monkeypatch):
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
    assert cons.exc is None
    loop.close()
    assert mod.submodules.cli_all == ('run',)
    monkeypatch.setenv('AUTILSCFGPATH', config_json) # cspell:disable-line
    N = __import__('importlib').reload(mod.unparsed).N
    assert N.load_all
    assert N.V == 2
def test_patch():
    patch = mod.patch
    patch.patch_function_signatures((f := lambda _: None, 'foo, {}'))
    assert f.__text_signature__ == '(foo, <unrepresentable>)'
    patch.patch_method_signatures((f, patch.exit_sig))
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
    with raises(QueueFull): Q.put_nowait(-1)
    t = create_task(Q.put(2))
    assert await Q.get() == 0
    assert Q.get_nowait() == 1
    await sleep(0)
    assert t.done()
    assert await Q.get() == 2
    t = create_task(Q.get())
    Q.put_nowait(3)
    Q.task_done()
    await sleep(0)
    assert t.done()
    assert t.result() == 3
    assert Q.empty()
    with raises(QueueEmpty): Q.get_nowait()
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
    assert m.heapreplace(h, 10) == 8
    assert m.heappushpop(h, 13) == 13
    assert m.heappop(h) == 10
    assert m.heappop(h) == 5
    assert h == [3, 1]
    with raises(TypeError, match='trailing Placeholders are not allowed'): m.partial(lambda *_: None, m.Placeholder)
    sio = StringIO()
    p = m.partial(print, 'baz', m.Placeholder, 'foo', end='_bar_', file=sio)
    with raises(TypeError): p()
    p(42)
    p(1, 2)
    assert sio.getvalue() == 'baz 42 foo_bar_baz 1 foo 2_bar_'
