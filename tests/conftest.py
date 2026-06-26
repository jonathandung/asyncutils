import asyncutils, pytest
@(dec := pytest.fixture(scope='session'))
def config_json_file(contents):
    with __import__('tempfile').NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as f: f.write(contents)
    yield f
@dec
def config_json(config_json_file, contents):
    n = config_json_file.name
    try:
        yield n; import json as J
        with open(n, encoding='utf-8') as f: assert J.load(f).items() >= J.loads(contents).items()
    finally: __import__('os').unlink(n)
@dec
def contents(): return '{"load_all": true, "V": 2, "max_memory_errors": 5}'
def pytest_configure(config):
    global mk # noqa: PLW0603
    mk = pytest.mark.asyncio_cooperative if config.pluginmanager.hasplugin('asyncio-cooperative') else pytest.mark.asyncio
    asyncutils._internal.patch.patch_aio_logs()
