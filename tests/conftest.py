@(dec := __import__('pytest').fixture(scope='session'))
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
def contents(): return '{"load_all": true, "V": 2}'