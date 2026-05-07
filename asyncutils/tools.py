from asyncutils import _internal as I
import asyncutils as A, shlex as s
get_cmd_help, __all__ = I.parsed.p.format_help, I.submodules.tools_all
def loadf(p, e=None, /, l=I.unparsed.l, _=I.helpers.fullname):
    if not ((f := getattr(p, '__fspath__', None)) is None or isinstance(p := f(), (str, bytes))): raise TypeError(f'tools.loadf: __fspath__ method returned {_(p)} instead of str or bytes')
    if not (isinstance(p, int) or e is None): raise TypeError('did not expect extension')
    if e == '': raise ValueError('empty extension')
    return l(p.decode() if isinstance(p, bytes) else p, e)
def json_to_argv(p, /, d='.', D=(('quiet', 'q'), ('basic_repl', 'b'), ('load_all', 'p'), ('debug', 'd'), ('pdb', 'P')), g=A.raise_exc, *, strict=True):
    f, l = (R := []).append, (p := (m := loadf(p)).pop)('logging_to', s := 'STDERR')
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
    if strict and m: g(ValueError, 'unknown keys in config file', notes=m)
    return R
def json_to_argstr(p, /, *, join=s.join, strict=True): return join(json_to_argv(p, strict=strict))
def argv_to_json(a, p, /, *, dump=__import__('json').dump, _=I.parsed.p.parse_args):
    with open(p, 'w') as f: dump(_(a).__dict__, f)
def argstr_to_json(a, p, /, *, split=s.split, **k): argv_to_json(split(a), p, **k)
def find_help_url(o=None, /, _=frozenset((None, 'asyncutils', A)), g=I.initialize.Module, h=I.helpers, m=frozenset(('__hexversion__', '__version__', 'console_preloaded_submodules', 'preloaded_submodules', 'time_since_boot')), M=A.submodules_map):
    if o in _: return 'https://asyncutils.readthedocs.io/en/stable/index.html'
    if isinstance(o, str):
        if (o := o.removeprefix('asyncutils.')) == '__init__': return 'https://asyncutils.readthedocs.io/en/stable/top-level.html'
        s, _, o = o.partition('.')
        if s in m: s, o = 'asyncutils', s
        elif _: o = getattr(g(s), o)
        else: o = g(s)
    if isinstance(o, (classmethod, staticmethod)): o = o.__func__
    elif isinstance(o, property): o = o.fget
    if h.ismodule(o): s, o = o.__name__, None
    elif callable(o): s, o = o.__module__, o.__qualname__
    elif not isinstance(o, str): raise TypeError(f'tools.find_help_url: expected a string, module or callable; got {h.fullname(o)}')
    s = s.removeprefix('asyncutils.'); return (f'https://asyncutils.readthedocs.io/en/stable/api/asyncutils/{o}/index.html' if o in M else 'https://asyncutils.readthedocs.io/en/stable/top-level.html') if s == 'asyncutils' else f'https://asyncutils.readthedocs.io/en/stable/api/asyncutils/{s}/index.html#{f"module-asyncutils.{s}" if o is None else f"asyncutils.{s}.{o}"}'
def open_help(o=None, /): return __import__('webbrowser').open(find_help_url(o))
def get_cfg_json_format(_=('',)): return __import__('importlib.resources', fromlist=_).files('asyncutils').joinpath('format.json5').read_text()
def print_cfg_json_format(file=None, *, flush=True): print(get_cfg_json_format(), file=file, flush=flush)
def print_cmd_help(file=None, *, flush=True): print(get_cmd_help(), file=file, flush=flush)
I.patch.patch_function_signatures((find_help_url, 'o=None, /'), (loadf, "path, ext='json', /"), (json_to_argv, 'path, /'), (json_to_argstr, 'path, /, *, join={}'), (argv_to_json, 'argv, path, /, *, dump={}'), (argstr_to_json, 'argstr, path, /, *, dump={0}, split={0}'), (get_cfg_json_format, ''))
del A, I, s