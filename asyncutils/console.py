# ruff: noqa: BLE001,PLR2004
from asyncutils import __version__ as V, config as C, exceptions as E
from asyncutils._internal import patch as P, running_console as R, log
from asyncutils._internal.helpers import fullname
from asyncutils._internal.submodules import console_all as __all__
import abc, sys as S
from asyncio import iscoroutine
from asyncio.futures import _chain_future
from itertools import repeat
from os import getenv as g
try: from _pyrepl.console import InteractiveColoredConsole as B # ty: ignore[unresolved-import]
except ImportError: from code import InteractiveConsole as B; C.basic_repl = True
_s = object()
_f = '',
class ConsoleBase(B, metaclass=abc.ABCMeta):
    LOCALS_HANDLERS, interrupt_hooks, memory_error_hooks, disallow_subclass_msg = __import__('collections').ChainMap(), (), (lambda self, f=getattr(S, '_clear_internal_caches' if S.version_info >= (3, 13) else '_clear_type_cache', None), g=__import__('gc').collect, d=log.debug: (f and f()) or self.write('MemoryError\n') or d('Emergency garbage collection after MemoryError: %s objects collected in total', g()),), 'cannot subclass %s'; default_local_exit = _unsubclassable = False
    if C.basic_repl: CAN_USE_PYREPL = False # pragma: no cover
    else: from _pyrepl.main import CAN_USE_PYREPL # ty: ignore[unresolved-import]
    def __init__(self, loop, mod=None, modname=None, *, context_factory=__import__('contextvars').copy_context, _f=_f, _s=_s, _m='cannot %s event loop within REPL', g=globals().get, _={'__cached__': 'cached', '__file__': 'origin', '__package__': 'parent', '__loader__': 'submodule_search_locations'}, _r=E.raise_exc): # noqa: B006
        S.audit(fullname(type(self)), loop)
        if modname is None: modname = self.NAME
        if mod is None: mod = __import__(modname, fromlist=_f if '.' in modname else ())
        def stop(p=None, /, _=loop.stop, *, asap=False):
            if p is _s: _() if asap else loop.call_soon_threadsafe(_)
            else: raise RuntimeError(_m%'stop')
        def close(p=None, /, _=loop.close):
            if p is _s: _()
            else: raise RuntimeError(_m%'close')
        loop.stop, loop.close, self._internal_is_running, self.memory_errors, self._loop, self.context, self.exc, self._fut, (d := {})[modname] = stop, close, False, 0, loop, context_factory(), None, None, mod; super().__init__(d, '<stdin>', **({'local_exit': self.default_local_exit} if (H := S.hexversion) > 0x30d00a0 else {})); self.compile.compiler.flags |= 0x2000; d.update(__name__='__main__', __doc__='A console with top-level await support, much like the asyncio REPL, and some preloaded names.', __spec__=__spec__, __annotations__={}, __builtins__=__builtins__)
        if H > 0x30e00a0: d['__annotate__'] = g('__annotate__') # cover: off
        if H < 0x30f00a1:
            for k in _: d[k] = g(k)
        elif H < 0x30f00f0:
            for k, v in _.items(): d[k] = getattr(__spec__, v) # cover: on
        if callable(h := self.LOCALS_HANDLERS.get(modname)): h(d)
        elif h is not None: raise TypeError(f'asyncutils.console.ConsoleBase: locals handler for module {modname!r} should be callable, not {fullname(h)!r}')
    def refresh(self):
        if not ((F := self._fut) is None or F.done()): F.cancel()
    def __callback(self, F, C, /, *, c=type(refresh), v=iscoroutine, l=_chain_future):
        try: r = c(C, self.locals)()
        except SystemExit as e: return self.set_return_code(e)
        except BaseException as e:
            if isinstance(e, KeyboardInterrupt): self.interrupt()
            elif isinstance(e, MemoryError): self.memory_error()
            return F.set_exception(e)
        if not v(r): return F.set_result(r)
        try: l(_ := self._loop.create_task(r, context=self.context), F); self._fut = _
        except BaseException as e: F.set_exception(e)
    def showtraceback(self):
        if (t := S.exc_info())[2] is not None: self._showtraceback(*t, '')
    def runcode(self, code, *, futimpl=__import__('concurrent.futures', fromlist=_f).Future, no_traceback=(KeyboardInterrupt, MemoryError, SyntaxError), threadsafe=True):
        getattr(self._loop, 'call_soon_threadsafe' if threadsafe else 'call_soon')(self.__callback, F := futimpl(), code, context=self.context)
        try: return F.result()
        except SystemExit as e: self.set_return_code(e)
        except BaseException as e:
            if not isinstance(e, no_traceback): self.showtraceback()
            return getattr(self, 'STATEMENT_FAILED', None)
    def interact(self, banner=None, *, ps1='>>> ', _f=_f, _s=_s, _q=C.silent, _o=type('', (), {'write': lambda *_: None, 'flush': lambda _, /: None})(), p=g('PYTHONSTARTUP')): # noqa: B008
        x = False; self.write_special(self.BANNER if banner is None else banner)
        if p and not S.flags.ignore_environment: # pragma: no cover
            with __import__('tokenize').open(p) as f:
                if _q: S.stdout, _o = _o, S.stdout
                S.audit('cpython.run_startup', p); exec(compile(f.read(), p, 'exec'), self.locals) # noqa: S102
                if _q: S.stdout = _o
        if (p := getattr(S, 'ps1', None)) is None: p, x = ps1, True
        self._interact_hook(*((f'{(t := __import__('_colorize').get_theme().syntax).prompt}{p}{(r := t.reset)}', t.keyword, r, t.builtin) if (c := self.CAN_USE_PYREPL) and S.version_info >= (3, 14) else (p, '', '', '')))
        try: __import__('_pyrepl.simple_interact', fromlist=_f).run_multiline_interactive_console(self) if c else super().interact('', '')
        finally: self._loop.stop(_s); S.ps1 = ps1 if x else getattr(S, 'ps1', ps1) if p is None else p
    def _interact_hook(self, ps1, kcolour, reset, fcolour): n, S.ps1 = self.NAME, ps1; self.write_special(f'{ps1}{kcolour}import{reset} {n}\n{ps1}{kcolour}from{reset} {n} {kcolour}import{reset} *\n') # noqa: ARG002
    @abc.abstractmethod
    def before_run(self, max_memory_errors): self._max_memory_errors, self._internal_is_running = 3 if max_memory_errors is None else max_memory_errors, True
    def after_run(self): self._internal_is_running = False
    def write_special(self, msg): self.write(msg)
    def interrupt(self, _=_f, m='\nKeyboardInterrupt\n'):
        if not self.CAN_USE_PYREPL: self.write(m)
        elif callable(f := getattr(__import__('_pyrepl.readline', fromlist=_)._get_reader().threading_hook, 'add', None)): f('')
        self.refresh()
    def memory_error(self):
        if (m := self.memory_errors) == self._max_memory_errors: return self.set_return_code(f'ERROR: Exceeded MemoryError threshold: {m}\n')
        self.memory_errors = m+1
        for _ in self.memory_error_hooks: _(self)
        self.refresh()
    def set_return_code(self, e, /, _=_s): self.exc = e if isinstance(e, SystemExit) else SystemExit(*(e.args if isinstance(e, BaseException) else (e,))); self._loop.stop(_)
    def __init_subclass__(cls, *, name=None, native_handler=None, default_local_exit=True, disallow_subclass_msg=None, other_handlers=None, additional_interrupt_hooks=(), additional_memory_error_hooks=(), template=f'%(name)s REPL (version %(version)s) running on {S.platform}\nType "help", "copyright", "credits" or "license" for more information, "clear" to clear the terminal, and "exit" or "quit" to exit.\n%(description)s\n', **k):
        if cls._unsubclassable: raise TypeError(cls.disallow_subclass_msg%fullname(cls))
        if name is None: name = cls.__qualname__.casefold().removesuffix('console')
        if other_handlers is None: other_handlers = {}
        k['name'] = cls.NAME = name; (f := k.setdefault)('version', 'unknown'); f('description', 'Enjoy!'); cls.BANNER, cls.LOCALS_HANDLERS, cls.interrupt_hooks, cls.memory_error_hooks, cls.default_local_exit, cls._unsubclassable, other_handlers[name] = template%k, cls.LOCALS_HANDLERS.new_child(other_handlers), (*cls.interrupt_hooks, *additional_interrupt_hooks), (*cls.memory_error_hooks, *additional_memory_error_hooks), default_local_exit, disallow_subclass_msg is not None, native_handler
        if disallow_subclass_msg: cls.disallow_subclass_msg = disallow_subclass_msg
    def __repr__(self): return f'{fullname(self)}({self._loop!r}, local_exit={self.local_exit})'
    @property
    def is_running(self): return self._internal_is_running
    def run(self, *, exit_message='Thank you for using %s!\nExiting REPL...\n', thread_name='<%s REPL thread>', max_memory_errors=None, always_run_interactive=bool(S.flags.inspect), always_install_completer=False, suppress_asyncio_warnings=False, suppress_unawaited_coroutine_warnings=False, _=frozenset(('win32', 'cygwin', 'android', 'ios', 'wasi'))):
        self.before_run(max_memory_errors); S.audit(f'{fullname(self)}.run', id(self)); l, w, n = self._loop, S.stderr.write, self.NAME
        if always_run_interactive or S.stdin.isatty():
            S.audit('cpython.run_stdin'); __import__('threading').Thread(name=thread_name%n, target=self.interact, daemon=True).start()
            if callable(h := getattr(S, i := '__interactivehook__', None)): # pragma: no cover
                S.audit('cpython.run_interactivehook', h)
                try: h()
                except: w(f'Error running {self!r}!\nFailed calling sys.__interactivehook__\n'); __import__('traceback').print_exc() # noqa: E722
                if always_install_completer or (S.platform not in _ and h.__module__ == 'site' and h.__name__ == h.__qualname__ == 'register_readline'):
                    try: __import__('readline').set_completer(__import__('rlcompleter').Completer(self.locals).complete) # ty: ignore[possibly-missing-attribute]
                    except ImportError: w('Failed to install readline completer\n')
            elif h is not None: w('Removing sys.__interactivehook__ since it is not callable\n'); delattr(S, i)
            while True:
                try: l.run_forever(); break
                except KeyboardInterrupt: self.interrupt()
                except MemoryError: self.memory_error()
        else: self.write_special(self.BANNER); self.runcode(compile((l := S.stdin).read(), getattr(l, 'name', '<stdin>'), 'exec'))
        try: self.after_run()
        except SystemExit: raise
        except BaseException as e: w(f'{fullname(e)} occurred in after_run of {self!r}: {e}\n')
        finally:
            if suppress_asyncio_warnings: P.patch_aio_logs()
            if suppress_unawaited_coroutine_warnings: P.patch_unawaited_coroutine_warnings()
            self.write_special(exit_message%n)
        return 0 if (e := self.exc) is None else e.code
    P.patch_method_signatures((run, '*, exit_message=None, thread_name=None, max_memory_errors=None, always_run_interactive=None, always_install_completer=False, suppress_asyncio_warnings=False, suppress_unawaited_coroutine_warnings=False'), (interrupt, ''), (set_return_code, 'e, /'), (__init__, 'loop, mod=None, modname=None, *, context_factory={}'), (interact, "banner=None, *, ps1='>>> '")); P.patch_classmethod_signatures((__init_subclass__, '*, name=None, native_handler=None, default_local_exit=True, disallow_subclass_msg=None, other_handlers=None, additional_interrupt_hooks=(), additional_memory_error_hooks=(), template={}, version=None, description=None, **k'))
def _(d, /):
    def load_all(_=d):
        for k, v in _.items(): _[k] = v if (g := getattr(v, 'load', None)) is None else g()
    load_all.__qualname__, load_all.__module__, load_all.__text_signature__ = load_all.__name__, 'asyncutils', '()'; return load_all # ty: ignore[unresolved-attribute]
class AsyncUtilsConsole(ConsoleBase, version=V, description='asyncutils is a multi-purpose and efficient asynchronous utilities library.\nYou can use await statements directly instead of asyncio.run for quick testing.\nAll the submodules of asyncutils are also loaded into the namespace.', native_handler=lambda d, /, v=V, _=_f, r=_: (u := d.update)(m := __import__('asyncutils._internal.initialize', fromlist=_).s) or u(__version__=v, load_all=r(m)), default_local_exit=True, disallow_subclass_msg='cannot subclass %s; subclass asyncutils.console.ConsoleBase instead'):
    def __repr__(self): return f'<{'running' if self.is_running else 'idle'} asyncutils console at {id(self):#x}>'
    @property
    def is_running(self):
        if not self._loop.is_running(): self._internal_is_running = False; return False
        if self._internal_is_running == (b := R.getc() is self): return b
        if b: self._internal_is_running = True
        else: self.set_return_code(1)
        S.stderr.write('User tampered with console-internal state!\n'); return False
    def _interact_hook(self, ps1, kcolour, reset, fcolour):
        super()._interact_hook(ps1, kcolour, reset, fcolour)
        if R.should_write_load_all(): self.write_special(f'{ps1}{fcolour}load_all{reset}()\n')
    def write_special(self, msg, _=C.silent):
        if not _: self.write(msg)
    def before_run(self, max_memory_errors, _=C.max_memory_errors, _r='this console is already running', _a='another console is running'):
        if self._internal_is_running: raise RuntimeError(_r)
        if r := R.getc(): raise RuntimeError(_r if r is self else _a)
        R.setc(self); super().before_run(_ if max_memory_errors is None else max_memory_errors) # ty: ignore[invalid-argument-type]
    def after_run(self, _m='WARNING: user tampered with asyncutils module state\n', _=C.pdb, _e=E.StateCorrupted('console-internal', 'console.exc was set to a non-SystemExit exception')):
        if R.unsetc() is not self: S.stderr.write(_m); del S.modules[__name__]
        if _ and isinstance(e := self.exc, BaseException):
            if not isinstance(e, SystemExit): raise _e
            if (t := e.__traceback__) is None: raise e
            __import__('pdb').post_mortem(t)
        super().after_run()
    def showtraceback(self, s=3, a=('asyncutils\\console.py', 'asyncutils/console.py'), f=39, m=S.intern('__callback')):
        t, v, b = S.exc_info()
        if b is None: return
        for _ in repeat(None, s):
            if (b := b.tb_next) is None: return
        if (c := b.tb_frame.f_code).co_filename.endswith(a) and c.co_firstlineno == f and c.co_name == m and (b := b.tb_next) is None: return # cspell:disable-line
        self._showtraceback(t, v, b, '')
    P.patch_method_signatures((showtraceback, ''), (after_run, ''), (before_run, 'max_memory_errors'), (write_special, 'msg'))
del _f, _s, g, C, V, B, _, iscoroutine, E, log
