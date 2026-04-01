import logging as L, sys as S
from ._internal import log as l, patch as P
from ._internal.submodules import config_all as __all__
from ._internal.unparsed import N
if S._xoptions.get('asyncutils_run_as_main'): from ._internal.parsed import p; N.update(p.parse_args().__dict__); del p
def f(e, _=('',), f=frozenset(('thread', 'process', 'interpreter')), c='.', s=(s := S.stderr)):
    if not isinstance(e, str): raise TypeError('executor name should be a string')
    d, c, w = e.rpartition(c)
    if c:
        try: return getattr(__import__(d, fromlist=_), w)
        except ImportError: ...
    else:
        d = 'loky'
        if e in f: return getattr(__import__('concurrent.futures.'+e, fromlist=_), e.title()+'PoolExecutor')
        elif e == 'dask':
            try: return __import__('distributed.client', fromlist=_).Client
            except ImportError: d = 'dask.distributed'
        elif e == 'loky_noreuse':
            try: return __import__('loky.process_executor', fromlist=_).ProcessPoolExecutor
            except ImportError: ...
        elif e == d:
            try: (r := __import__('loky.reusable_executor', fromlist=_)._ReusablePoolExecutor).__new__ = lambda cls, *a, **k: cls.get_reusable_executor(*a, **k)[0]; return r
            except ImportError: ...
        elif e == 'ipython': return __import__('ipyparallel.client.view', fromlist=_).ViewExecutor
        else:
            d, *a = e.split('_')
            if d == 'elib':
                try: a, e = a; return getattr(__import__('executorlib.executor.'+a, fromlist=_), f'{a.title()}{e.title()}Executor')
                except ImportError: d = 'executorlib'
            elif d == 'pebble':
                try: a = a[0]; return getattr(__import__('pebble.pool.'+a, fromlist=_), a.title()+'Pool')
                except ImportError: ...
            else: raise ValueError('invalid custom executor: '+e)
    s.write(f'Error importing {d} (maybe not installed); falling back to ThreadPoolExecutor\n'); return __import__('concurrent.futures.thread', fromlist=_).ThreadPoolExecutor
def c(*a): from .exceptions import FaultyConfig; raise FaultyConfig(*a)
def k(e, a=False, N=N, c=c):
    if isinstance(x := N[e], str):
        try: return int(x, 0)
        except ValueError:
            if a: c(e, str, int)
    return x
def g(e, a=False, t=(str, int, bytes), c=c, k=k):
    if isinstance(x := k(e), str):
        if x.startswith("b'") and x.endswith("'") or x.startswith('b"') and x.endswith('"'):
            try: x = x[2:-1].encode()
            except UnicodeEncodeError: ...
    if isinstance(x, t) or a and (x is None or isinstance(x, float)): return x
    c(e, type(x), t)
max_memerrs, e, Executor, get_past_logs, m, M, b = k('max_memerrs'), g('seed', True), f(N.executor), lambda: '', 'x', False, __import__('os').name == 'posix' # type: ignore[no-redef]
silent, basic_repl, loaded_all = map(bool, (S.flags.quiet or N.quiet, N.basic_repl, N.load_all))
match logging_to := g('log_to'):
    case 'NULL': l.disabled = True
    case 'MAKE':
        T = 'asyncutils_log%d.log'
        for h in range(1, 0x1000):
            try: logging_to = (s := open(T%h, m)).name; break
            except PermissionError as M: s.write(f'ERROR: insufficient permissions: {M}\n'); M = True; break
            except AttributeError: raise SystemError('python opened a file with no `name` attribute') from None
            except Exception: ...
        else: M = True
        del T, h
    case 'MEMORY':
        s = (j := __import__('_io').StringIO)()
        def get_past_logs(j=j):
            if r := (H := get_past_logs.handler).stream.getvalue(): H.setStream(j())
            return r
        del j
    case 'STDOUT': s = S.stdout
    case 'STDERR': ...
    case 1 if b: s, logging_to = S.stdout, 'STDOUT'
    case 2 if b: logging_to = 'STDERR'
    case str()|int()|bytes():
        M = True
        try: logging_to = getattr(s := open(logging_to, m), 'name', logging_to); M = False
        except PermissionError as b: s.write(f'ERROR: insufficient permissions: {b}\n')
        except FileExistsError: s.write('ERROR: log file already exists\n')
        except OSError as b: s.write(f'ERROR: {b}\n')
        except Exception as b: s.write(f'ERROR: unexpected error opening log file: {b}\n')
if M: s.write('Failed to create log file; falling back to stderr\n')
l.addHandler(_ := L.StreamHandler(s))
_.setFormatter(L.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
(set_logger_level := lambda level, h=_, l=l: l.setLevel(level) or h.setLevel(level))(10*min(max(3-N.V+N.Q, 1), 5))
get_past_logs.handler = _
l.debug('hi')
__import__('atexit').register(lambda s=s, d=l.debug: None if s.closed else d('bye') or s.flush() or s.close())
class debugging:
    __slots__ = 'orig_level', 'orig_name'
    @property
    def level(self, _=l): return _.level
    def __init__(self): self.orig_level = self.orig_name = None
    def __enter__(self, _s=set_logger_level, _m=L._levelToName.__getitem__, _l=l):
        if self.orig_level is None:
            self.orig_name, self.orig_level = _m(l := _l.level), l; _s(10)
            if l != 10: _l.debug('debugging: debug mode entered')
        else: _l.warning('debugging: context manager already entered')
        return self
    def __exit__(self, /, *_, _s=set_logger_level, _l=l):
        if (l := self.orig_level) is None: return _l.warning('debugging: context manager not entered')
        if l != _l.level == 10: _l.debug('debugging: exiting debug mode'); _s(l)
        else: _l.warning(f'debugging: user already exited debug mode; original level was {self.orig_name}')
        self.orig_name = self.orig_level = None
    def __repr__(self): return f'<asyncutils debug mode context manager at {id(self):#x}>'
    P.patch_method_signatures((__enter__, ''), (__exit__, 'exc_typ, exc_val, exc_tb, /'))
debug = debugging()
def r(name, /): raise AttributeError(f"module 'asyncutils.config' has no attribute {name!r}")
def __getattr__(name, /, _=e, r=r):
    if name != '_randinst': r(name)
    global _randinst; _randinst, __getattr__.__code__ = __import__('random').Random(_), r.__code__; return _randinst
P.patch_function_signatures((__getattr__, 'name, /'), (set_logger_level, 'level'))
del _, e, L, M, N, S, f, m, r, s, b, P, g, k, c, l # noqa: F821