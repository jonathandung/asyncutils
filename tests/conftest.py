import asyncutils, pytest
@(dec := pytest.fixture(scope='session'))
def cfgjsonf(contents):
    with __import__('tempfile').NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as f: f.write(contents)
    yield f
@dec
def cfgjson(cfgjsonf, contents):
    n = cfgjsonf.name
    try:
        yield n; import json as J
        with open(n) as f: assert J.load(f).items() >= J.loads(contents).items()
    finally: __import__('os').unlink(n)
@dec
def contents(): return '{"load_all": true, "V": 2, "max_memerrs": 5}'
def pytest_configure(config):
    global mk # noqa: PLW0603
    mk = pytest.mark.asyncio_cooperative if config.pluginmanager.hasplugin('asyncio-cooperative') else pytest.mark.asyncio
    asyncutils._internal.patch.patch_aio_logs()