# ruff: noqa: BLE001,SIM115
from asyncutils._internal import log as l, patch as P, initialize as I
from asyncutils._internal.submodules import config_all as __all__
from asyncutils._internal.unparsed import N, c
import logging as L, sys as S
def __dir__(_=__all__): return _
class FaultyConfig(BaseException):
    def __init__(self, k, w, c, /): self.key, self.wrong, self.correct = k, w, c; super().__init__(f'asyncutils: configuration for key {k!r} from AUTILSCFGPATH is faulty: expected {', '.join(c) if isinstance(c, tuple) else c.__name__}, got {w.__name__}')
def f(e, _=__import__('_functools').partial(__import__, fromlist=('',)), f=frozenset(('thread', 'process', 'interpreter')), c='.', S=S): # noqa: B008,C901,PLR0911,PLR0912 # pragma: no cover
    if not isinstance(e, str): raise TypeError('asyncutils: executor name should be a string')
    d, c, w = e.rpartition(c)
    if c:
        try: return getattr(_(d), w)
        except ImportError: ...
    else:
        d = 'loky'
        if e in f: return getattr(_('concurrent.futures.'+e), e.title()+'PoolExecutor')
        if e == 'dask':
            try: return _('distributed.client').Client
            except ImportError: d = 'dask.distributed'
        elif e == 'deadpool':
            try: return __import__(e).DeadPool
            except ImportError: ...
        elif e == 'loky_no_reuse':
            try: return _('loky.process_executor').ProcessPoolExecutor
            except ImportError: ...
        elif e == d:
            try: (r := _('loky.reusable_executor')._ReusablePoolExecutor).__new__ = lambda cls, *a, **k: cls.get_reusable_executor(*a, **k)[0]; return r
            except ImportError: ...
        elif e == 'ipython': return _('ipyparallel.client.view').ViewExecutor
        else:
            d, *a = e.split('_')
            if d == 'elib':
                try: a, e = a; return getattr(_('executorlib.executor.'+a), f'{a.title()}{e.title()}Executor')
                except ImportError: d = 'executorlib'
            elif d == 'pebble':
                try: a = a[0]; return getattr(_('pebble.pool.'+a), a.title()+'Pool')
                except ImportError: ...
            else: raise FaultyConfig('executor', e, _('asyncutils.constants').POSSIBLE_EXECUTORS)
    S.stderr.write(f'Error importing {d} (maybe not installed); falling back to ThreadPoolExecutor\n'); return _('concurrent.futures.thread').ThreadPoolExecutor
def k(e, a=False, N=N):
    if isinstance(x := N[e], str):
        try: return int(x, 0)
        except ValueError:
            if a: raise FaultyConfig(e, x, int)
    return x
def g(e, a=False, t=(str, int, bytes), _=k):
    if isinstance(x := _(e), str) and ((x.startswith("b'") and x.endswith("'")) or (x.startswith('b"') and x.endswith('"'))):
        try: x = x.encode()[2:-1] # noqa: SIM105
        except UnicodeEncodeError: ...
    if isinstance(x, t) or (a and (x is None or isinstance(x, float))): return x
    raise FaultyConfig(e, x, t)
max_memory_errors, e, Executor, get_past_logs, m, M, o, s, _ = k('max_memory_errors'), g('seed', True), f(N.executor), str, 'a', False, __import__('os').name == 'posix', S.stderr, L.StreamHandler()
silent, basic_repl, loaded_all, pdb = map(N.__getitem__, ('quiet', 'basic_repl', 'load_all', 'pdb'))
match logging_to := g('log_to'):
    case 'NULL': l.disabled = True
    case 'MAKE':
        T, m, h = 'asyncutils_log%d.log', 'x', 0
        for h in range(1, 0x1001):
            try: logging_to = (s := open(T%h, m)).name; break
            except PermissionError as M: s.write(f'ERROR: insufficient permissions: {M}\n'); M = True; break
            except AttributeError: raise SystemError("asyncutils: Python opened a file with no 'name' attribute when finding log file") from None
            except Exception: ...
        else: M = True
        del T, h
    case 'MEMORY':
        from _io import StringIO as J
        def get_past_logs(j=J, _=_):
            if r := _.stream.getvalue(): _.setStream(j()) # ty: ignore[unresolved-attribute]
            return r
        get_past_logs.__text_signature__, s = '()', J(); del J # ty: ignore[unresolved-attribute]
    case 'STDOUT': s = S.stdout
    case 'STDERR': ...
    case 1 if o: s, logging_to = S.stdout, 'STDOUT'
    case 2 if o: logging_to = 'STDERR'
    case str()|int()|bytes():
        try: M = True; logging_to = getattr(s := open(logging_to, m), 'name', logging_to); M = False
        except PermissionError as b: s.write(f'ERROR: insufficient permissions: {b}\n')
        except OSError as b: s.write(f'ERROR: {b}\n')
        except Exception as b: s.write(f'ERROR: unexpected error opening log file: {b}\n')
if M: s.write('ERROR: Failed to create log file; falling back to stderr\n')
l.addHandler(_)
_.setStream(s)
_.setFormatter(L.Formatter('%(asctime)s - asyncutils - %(levelname)s - %(message)s'))
(set_logger_level := lambda level, h=_, l=l: l.setLevel(level) or h.setLevel(level))(10*min(max(3-N.V+N.Q, 1), 5))
class Debugging:
    __slots__ = 'orig_level', 'orig_name'
    @property
    def level(self, _=l): return _.level # noqa: PLR0206
    @property
    def entered(self): return self.orig_level is not None
    def __init__(self): self.orig_level = self.orig_name = None
    def __enter__(self, _s=set_logger_level, _m=L._levelToName.__getitem__, _l=l, _d=10):
        if self.entered: _l.warning('config.Debugging: context manager already entered')
        else:
            self.orig_name, self.orig_level = _m(l := _l.level), l; _s(_d)
            if l != _d: _l.debug('config.Debugging: debug mode entered')
        return self
    def __exit__(self, /, *_, _s=set_logger_level, _l=l, _L=10):
        if not self.entered: return _l.warning('config.Debugging: context manager not entered')
        if (l := self.orig_level) != _l.level == _L: _l.debug('config.Debugging: exiting debug mode'); _s(l)
        else: _l.warning('config.Debugging: user already exited debug mode; original level was %s', self.orig_name)
        self.orig_name = self.orig_level = None
    def __repr__(self): return f'<asyncutils debug mode context manager (entered: {self.entered}) at {id(self):#x}>'
    P.patch_method_signatures((__enter__, ''), (__exit__, P.exit_sig))
debug = Debugging()
I.p = d = l.debug # ty: ignore[invalid-assignment]
if N.debug:
    debug.__enter__(); d('python %s', S.version) # noqa: PLC2801
    if silent: from asyncutils import __version__ as V; d(V.representation); d('platform: %s', S.platform)
    if c: d('config file path: %s', c)
__import__('atexit').register(lambda s=s, _=d: None if s.closed else _('bye') or s.flush() or s.close())
p = (A := I.A).pop
while A: d(*p())
def r(n, /): raise AttributeError(f"module 'asyncutils.config' has no attribute {n!r}")
def __getattr__(n, /, _=e, r=r):
    if n != '_randinst': r(n)
    global _randinst; _randinst, __getattr__.__code__ = __import__('random').Random(_), r.__code__; return _randinst # ty: ignore[unresolved-global]
P.patch_function_signatures((__getattr__, 'name, /'), (set_logger_level, 'level'), (__dir__, ''))
if loaded_all:
    i = I.Module.load
    for _ in I.s.values(): i(_) # ty: ignore[invalid-argument-type]
    l.debug('all submodules loaded in %.2f milliseconds', __import__('asyncutils').time_since_boot())
del _, e, L, M, N, S, f, m, r, s, o, P, g, k, l, c, d, I
