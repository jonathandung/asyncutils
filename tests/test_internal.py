# type: ignore
from asyncutils import _internal as mod
from pytest import raises, fail
def test_helpers():
    helpers = mod.helpers
    for _ in helpers.filter_out(None, True, False): assert isinstance(_, bool)
    assert helpers.check_methods('', 'lower', 'casefold')
    with raises(AttributeError): helpers.copy_and_clear(())
    class _: ...
    assert helpers.subscriptable(_) is _
    _ = _[None]()
    _.foo = lambda: None
    assert not helpers.check_methods(_, 'foo')
def test_submods_lazy_loading():
    module = mod.initialize.Module
    if 'asyncutils.cli' in __import__('sys').modules: fail('module `asyncutils.cli` is somehow already loaded in test environment')
    assert isinstance(m := module('cli'), module) and m is module('cli')
    assert (a := m.__all__) is m.__dir__()
    assert a[0] == 'run'
    with raises(AttributeError, match="module 'asyncutils' has no attribute 'foo'"): module('foo')
    with raises(TypeError, match='cannot subclass module'): type('', (module,), {})
    with raises(AttributeError, match="module 'asyncutils.cli' has no attribute 'foo'"): m.foo
    assert isinstance(m, module)
    import pickle
    assert pickle.loads(pickle.dumps(m)) is m
    assert (t := type(M := m.load())) is type(module('config')) and t.__module__ == 'builtins' and t.__name__ == t.__qualname__ == 'module'
    assert m.run is M.run
def test_others(cfgjson, monkeypatch):
    assert type(mod.log).__module__ == 'logging'
    assert mod.types.All is mod.types.foo is mod.running_console._get_() is mod.running_console._unset_() is None
    assert mod.submodules.cli_all == ('run',)
    monkeypatch.setenv('AUTILSCFGPATH', cfgjson)
    N = __import__('importlib').reload(mod.unparsed).N
    assert N.load_all and N.V == 2
def test_patch():
    patch = mod.patch
    patch.patch_function_signatures((f := lambda _: None, 'foo'))
    assert f.__text_signature__ == '(foo)'
    patch.patch_method_signatures((f, 'bar'))
    assert f.__text_signature__ == '($self, bar)'
    patch.patch_classmethod_signatures((f, ''))
    assert f.__text_signature__ == '($cls)'