import sys as S, logging as L
from ._internal.submodules import config_all as __all__
from ._internal import log, patch as P
from atexit import register
if S._xoptions.get('asyncutils_run_as_main'): from ._internal.parsed import p; N = p.parse_args(); del p
else: from ._internal.unparsed import N
def f(e, _=('',), f=frozenset(('thread', 'process', 'interpreter')), c='.', s=(s := S.stderr)):
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
max_memerrs, silent, basic_repl, loaded_all, e, Executor, get_past_logs, m, M, b = N.max_memerrs, bool(S.flags.quiet) or N.quiet, N.basic_repl, N.load_all, N.seed, f(N.executor), lambda: '', 'x', False, __import__('os').name == 'posix'
if isinstance(e, str):
    try: e = int(e, 0)
    except ValueError: ...
if isinstance(logging_to := N.log_to, str):
    try: logging_to = int(N.log_to, 0)
    except ValueError:
        if (logging_to.startswith("b'") and logging_to.endswith("'")) or (logging_to.startswith('b"') and logging_to.endswith('"')): logging_to = logging_to[2:-1].encode(errors='replace')
match logging_to:
    case 'NULL': log.disabled = True
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
log.addHandler(_ := L.StreamHandler(s))
_.setFormatter(L.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
(set_logger_level := lambda level, h=_: log.setLevel(level) or h.setLevel(level))(10*min(max(3-N.V+N.Q, 1), 5))
get_past_logs.handler = _
log.debug('hi')
__import__('atexit').register(lambda s=s, d=log.debug: None if s.closed else d('bye') or s.flush() or s.close())
class debugging:
    __slots__ = 'orig_level', 'orig_name'
    @property
    def level(self): return log.level
    def __init__(self): self.orig_level = self.orig_name = None
    def __enter__(self, _s=set_logger_level, _m=L._levelToName.__getitem__):
        if self.orig_level is None:
            self.orig_name, self.orig_level = _m(l := log.level), l; _s(10)
            if l != 10: log.debug('debugging: debug mode entered')
        else: log.warning('debugging: context manager already entered')
        return self
    def __exit__(self, /, *_, _s=set_logger_level):
        if (l := self.orig_level) is None: return log.warning('debugging: context manager not entered')
        if l != log.level == 10: log.debug('debugging: exiting debug mode'); _s(l)
        else: log.warning(f'debugging: user already exited debug mode; original level was {self.orig_name}')
        self.orig_name = self.orig_level = None
    def __repr__(self): return f'<asyncutils debug mode context manager at {id(self):#x}>'
    P.patch_method_signatures((__enter__, ''), (__exit__, 'exc_typ, exc_val, exc_tb, /'))
class sentinel_base:
    _can_instantiate, __slots__ = False, ('__name',)
    def __new__(cls, name=None, _=__import__('keyword').iskeyword):
        cls._assert_can_instantiate()
        if name is None: return super().__new__(cls)
        if _(name) or not all(p.isidentifier() and not _(p) for p in name.split('.', 1)): raise ValueError('invalid name')
        if (o := (c := cls._cache).get(name)) is None:
            (o := super().__new__(cls)).__name = name
            with cls._lock: c[name] = o
        return o
    @property
    def name(self): return self.__name
    @classmethod
    def _assert_can_instantiate(cls):
        if not cls._can_instantiate: raise TypeError(f'cannot instantiate {cls.__qualname__!r}') from None
    def __repr__(self): return f'<{type(self).__qualname__} {self.__name!r} at {id(self):#x}>'
    def __str__(self): return getattr(self, 'name', '<unbound>')+(' <private>' if self.is_private else '')
    def __set_name__(self, owner, name, /):
        if getattr(self, '__name', None) is None: self._assert_can_instantiate(); self.__name = n = f'{owner.__qualname__}.{name}'; self._cache[n] = self
        else: raise NameError(f'cannot bind named {type(self).__qualname__} to class')
    def __reduce__(self):
        try: return type(self), (self.__name,)
        except AttributeError: raise TypeError(f'cannot pickle unbound instance of {type(self).__qualname__}') from None
    def __init_subclass__(cls, lock_impl=__import__('_thread').allocate_lock):
        if getattr(cls, '__slots__', True): raise TypeError('slots should be empty for sentinel classes')
        cls._cache, cls._lock, cls._can_instantiate = {}, lock_impl(), True
    @property
    def is_private(self): return getattr(self, '__name', '').split('.', 1)[-1].startswith('_')
    @property
    def bound_to(self):
        if len(l := getattr(self, '__name', '').split('.', 1)) == 2: return l[0]
    P.patch_classmethod_signatures((__new__, 'name=None'), (__init_subclass__, 'lock_impl={}'))
class _sentinel(sentinel_base):
    __slots__ = ()
    def __init_subclass__(cls): raise TypeError('cannot subclass _sentinel')
    def __reduce__(self): return f'asyncutils.config.{self.name}'
_NO_DEFAULT, RAISE, SYNC_AWAIT = map(_sentinel, ('_NO_DEFAULT', 'RAISE', 'SYNC_AWAIT'))
debug, _sentinel._can_instantiate = debugging(), False
def r(name, /): raise AttributeError(f"module 'asyncutils.config' has no attribute {name!r}")
def __getattr__(name, /, _=e, r=r):
    if name != '_randinst': r(name)
    global _randinst; _randinst, __getattr__.__code__ = __import__('random').Random(_), r.__code__; return _randinst
P.patch_function_signatures((__getattr__, 'name, /'), (set_logger_level, 'level'))
del _, e, L, M, N, S, f, m, r, s, b, register, P, _sentinel # noqa: F821