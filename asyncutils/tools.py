from asyncutils._internal.helpers import fullname as _
from asyncutils._internal.parsed import p
from asyncutils._internal.patch import patch_function_signatures as f
from asyncutils._internal.unparsed import l
from asyncutils._internal.submodules import tools_all as __all__
import shlex as s
get_cmd_help = p.format_help
def loadf(p, e='json', /, l=l, _=_):
    if (f := getattr(p, '__fspath__', None)) is None or isinstance(p := f(), (str, bytes)): return l(p.decode() if isinstance(p, bytes) else p, e if isinstance(p, int) else None)
    raise TypeError(f'tools.loadf: __fspath__ method returned {_(p)} instead of str or bytes')
def json_to_argv(p, /, *, d='.', D=(('quiet', 'q'), ('basic_repl', 'b'), ('load_all', 'p'), ('debug', 'd'), ('pdb', 'P'))):
    f, l = (R := []).append, (p := loadf(p).pop)('logging_to', s := 'STDERR')
    if p('no_log', False) or l == 'NULL': f('-n')
    elif l != s:
        f('-l')
        if l != 'MAKE': f(l)
    if s := p('executor', l := 'thread') != l: f('-c' if d in s else '-e'); f(s)
    if isinstance(l := p('max_memerrs', None), int): f('-m'); f(str(l))
    if (s := p('seed', None)) is not None: f('-s'); f(repr(s))
    if (r := f'-{"".join(c for k, c in D if p(k, False))}{("Q"*-l if (l := p("V", 0)-p("Q", 0)) < 0 else "V"*l)}') != '-':
        if R: R[0] = r+R[0][1:]
        else: f(r)
    return R
def json_to_argstr(p, /, *, join=s.join): return join(json_to_argv(p))
def argv_to_json(a, p, /, *, dump=__import__('json').dump, _=p.parse_args):
    with open(p, 'w') as f: dump(_(a).__dict__, f)
def argstr_to_json(a, p, /, *, split=s.split, **k): argv_to_json(split(a), p, **k)
def get_cfg_json_format(_=('',)): return __import__('importlib.resources', fromlist=_).files('asyncutils').joinpath('format.json5').read_text()
def print_cfg_json_format(file=None): print(get_cfg_json_format(), file=file, flush=True)
def print_cmd_help(file=None): print(get_cmd_help(), file=file, flush=True)
f((loadf, "path, ext='json', /"), (json_to_argv, 'path, /'), (json_to_argstr, 'path, /, *, join={}'), (argv_to_json, 'argv, path, /, *, dump={}'), (argstr_to_json, 'argstr, path, /, *, dump={0}, split={0}'), (get_cfg_json_format, ''))
del p, s, _, l, f