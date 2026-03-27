import shlex as s
from ._internal.helpers import check_methods as c
from ._internal.parsed import p
from ._internal.submodules import tools_all as __all__
ext2modname, get_cmd_help = {}, p.format_help
def json_to_argv(p, /, *, _=c, d='.'):
    if _(p, '__fspath__') and isinstance(p := p.__fspath__(), int): raise TypeError('__fspath__ should return str or bytes')
    if isinstance(p, bytes): p = p.decode()
    if isinstance(p, int): c = 'json'
    else:
        _, b, c = p.rpartition(d)
        if not b: __import__('sys').stderr.write('json_to_argv: No file extension; assuming .json\n'); c = 'json'
    with open(p) as f: f, l = (r := []).append, (p := __import__(ext2modname.get(c, c)).load(f).pop)('log_to', s := 'STDERR')
    if p('no_log', False) or l == 'NULL': f('-n')
    elif l != s:
        f('-l')
        if l != 'MAKE': f(l)
    if (s := p('executor', l := 'thread')) != l: f('-c' if d in s else '-e'); f(s)
    if (l := p('max_memerrs', 3)) != 3: f('-m'); f(str(l))
    if p('quiet', False): f('-q')
    if p('basic_repl', False): f('-b')
    if (s := p('seed', None)) is not None: f('-s'); f(repr(s))
    if p('load_all', False): f('-p')
    f(f'-{'Q'*-l if (l := p('V', 0)-p('Q', 0)) < 0 else 'V'*l}'); return r
def json_to_argstr(p, /, *, join=s.join, **k): return join(json_to_argv(p, **k))
def argv_to_json(a, p, /, *, dump=__import__('json').dump, _=p.parse_args):
    with open(p, 'w') as f: dump(_(a).__dict__, f)
def argstr_to_json(a, p, /, *, split=s.split, **k): argv_to_json(split(a), p, **k)
def get_cfg_json_format(): return (__import__('importlib.resources', fromlist=('',)).files('asyncutils')/'format.jsonc').read_text()
def print_cfg_json_format(file=None): print(get_cfg_json_format(), file=file, flush=True)
def print_cmd_help(file=None): print(get_cmd_help(), file=file, flush=True)
del p, s, c