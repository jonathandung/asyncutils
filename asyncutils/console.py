from asyncutils import __version__ as V, config as C, StateCorrupted
from asyncutils._internal import patch as P, running_console as R
from asyncutils._internal.helpers import fullname
from asyncutils._internal.submodules import console_all as __all__
import sys as S
from asyncio import iscoroutine
from asyncio.futures import _chain_future # type: ignore[import-not-found]
from os import getenv as g
try: from _pyrepl.console import InteractiveColoredConsole as B
except ImportError: from code import InteractiveConsole as B; C.basic_repl = True
_s = object()
_f = '',
class ConsoleBase(B):
    LOCALS_HANDLERS, interrupt_hooks, memerr_hooks, disallow_subclass_msg = __import__('collections').ChainMap(), (), (lambda self, f=S._clear_internal_caches, g=__import__('gc').collect, d=__import__('logging').getLogger('asyncutils').debug: f() or self.write('MemoryError\n') or d('Emergency garbage collection after MemoryError: %s objects collected in total', g()),), 'cannot subclass %s'; default_local_exit = _unsubclassable = False # noqa: B008
    if C.basic_repl: CAN_USE_PYREPL = False
    else: from _pyrepl.main import CAN_USE_PYREPL
    def __init__(self, loop, mod=None, modname=None, *, context_factory=__import__('_contextvars').copy_context, _f=_f, _s=_s, _m='cannot %s event loop within REPL', g=globals().get, _={'__cached__': 'cached', '__file__': 'origin', '__package__': 'parent', '__loader__': 'submodule_search_locations'}): # noqa: B006
        if (t := type(self)) is __class__: raise TypeError('cannot instantiate asyncutils.console.ConsoleBase; subclass instead')
        S.audit(fullname(t), loop)
        if modname is None: modname = self.NAME
        if mod is None: mod = __import__(modname, fromlist=_f if '.' in modname else ())
        def stop(p=None, /, _=loop.stop, *, asap=False):
            if p is _s: _() if asap else loop.call_soon_threadsafe(_)
            else: raise RuntimeError(_m%'stop')
        def close(p=None, /, _=loop.close):
            if p is _s: _()
            else: raise RuntimeError(_m%'close')
        loop.stop, loop.close, self._internal_is_running, self.memory_errors, self._loop, self.context, self.exc, self._fut, (d := {})[modname] = stop, close, False, 0, loop, context_factory(), None, None, mod; super().__init__(d, '<stdin>', local_exit=self.default_local_exit); self.compile.compiler.flags |= 0x2000; d.update(__name__='__main__', __doc__='A console with top-level await support.', __spec__=__spec__, __annotations__={})
        if (H := S.hexversion) > 0x30e00a0: d['__annotate__'] = g('__annotate__')
        if H < 0x30f00a1:
            for k in _: d[k] = g(k)
        elif H < 0x30f00f0:
            for k, v in _.items(): d[k] = getattr(__spec__, v)
        if callable(h := self.LOCALS_HANDLERS.get(modname)): h(d)
        elif h is not None: raise TypeError(f'asyncutils.console.ConsoleBase: locals handler for module {modname!r} should be callable, not {fullname(h)!r}')
    def refresh(self):
        if not ((F := self._fut) is None or F.done()): F.cancel()
    def __callback(self, fut, code, /, *, makef=type(refresh), corocheck=iscoroutine, futchain=_chain_future):
        try: c = makef(code, self.locals)()
        except SystemExit as e: return self.set_return_code(e)
        except BaseException as e:
            if isinstance(e, KeyboardInterrupt): self.interrupt()
            elif isinstance(e, MemoryError): self.memoryerror()
            return fut.set_exception(e)
        if not corocheck(c): return fut.set_result(c)
        try: self._fut = _ = self._loop.create_task(c, context=self.context); futchain(_, fut)
        except BaseException as e: fut.set_exception(e)
    def showtraceback(self):
        t, v, b = S.exc_info()
        try:
            if b is not None: self._showtraceback(t, v, b, '')
        finally: t = v = b = None
    def runcode(self, code, *, futimpl=__import__('concurrent.futures._base', fromlist=_f).Future, dont_show_traceback=(KeyboardInterrupt, MemoryError, SyntaxError), threadsafe=True):
        getattr(self._loop, 'call_soon_threadsafe' if threadsafe else 'call_soon')(self.__callback, F := futimpl(), code, context=self.context)
        try: return F.result()
        except SystemExit as e: self.set_return_code(e)
        except BaseException as e:
            if not isinstance(e, dont_show_traceback): self.showtraceback()
            return getattr(self, 'STATEMENT_FAILED', None)
    def interact(self, banner=None, *, ps1='>>> ', _f=_f, _s=_s, _q=C.silent, _o=type('', (), {'write': lambda *_: None, 'flush': lambda _, /: None})(), p=g('PYTHONSTARTUP')): # noqa: B008
        x = False; self.write_special(self.BANNER if banner is None else banner)
        try:
            if p and not S.flags.ignore_environment:
                with __import__('tokenize').open(p) as f:
                    if _q: S.stdout, _o = _o, S.stdout
                    S.audit('cpython.run_startup', p); exec(compile(f.read(), p, 'exec'), self.locals) # noqa: S102
                    if _q: S.stdout = _o
            if (p := getattr(S, 'ps1', None)) is None: p, x = ps1, True
            if self.CAN_USE_PYREPL: self._interact_hook(f'{(t := __import__('_colorize').get_theme().syntax).prompt}{p}{(r := t.reset)}'.lstrip(), t.keyword, r, t.builtin); __import__('_pyrepl.simple_interact', fromlist=_f).run_multiline_interactive_console(self)
            else: self._interact_hook(p, '', '', ''); super().interact('', '')
        finally: self._loop.stop(_s); S.ps1 = ps1 if x else getattr(S, 'ps1', ps1) if p is None else p
    def _interact_hook(self, ps1, kcolor, reset, fcolor): n, S.ps1 = self.NAME, ps1; self.write_special(f'{ps1}{kcolor}import{reset} {n}\n{ps1}{kcolor}from{reset} {n} {kcolor}import{reset} *\n') # noqa: ARG002
    def prehook(self, max_memerrs): self._max_memerrs, self._internal_is_running = 3 if max_memerrs is None else max_memerrs, True
    def posthook(self): self._internal_is_running = False
    def write_special(self, msg): self.write(msg)
    def interrupt(self, _=_f, m='\nKeyboardInterrupt\n'):
        if not self.CAN_USE_PYREPL: self.write(m)
        elif (x := __import__('_pyrepl.simple_interact', fromlist=_)._get_reader().threading_hook): x.add('')
        self.refresh()
    def memoryerror(self):
        if (m := self.memory_errors) == self._max_memerrs: self.write_special(f'Exceeded MemoryError threshold: {m}\n'); return self.set_return_code(1)
        self.memory_errors = m+1
        for _ in self.memerr_hooks: _(self)
        self.refresh()
    def set_return_code(self, e, /, _s=_s): self.exc = e if isinstance(e, SystemExit) else SystemExit(*(e.args if isinstance(e, BaseException) else (e,))); self._loop.stop(_s)
    def __init_subclass__(cls, *, name=None, native_handler=None, default_local_exit=True, disallow_subclass_msg=None, other_handlers=None, additional_interrupt_hooks=(), additional_memerr_hooks=(), template=f'%(name)s REPL (version %(version)s) running on {S.platform}\nType "help", "copyright", "credits" or "license" for more information, "clear" to clear the terminal, and "exit" or "quit" to exit.\n%(description)s\n', **k):
        if cls._unsubclassable: raise TypeError(cls.disallow_subclass_msg%fullname(cls))
        if name is None: name = cls.__qualname__.casefold().removesuffix('console')
        if other_handlers is None: other_handlers = {}
        k['name'] = cls.NAME = name; (f := k.setdefault)('version', 'unknown'); f('description', 'Enjoy!'); cls.BANNER, cls.LOCALS_HANDLERS, cls.interrupt_hooks, cls.memerr_hooks, cls.default_local_exit, cls._unsubclassable, other_handlers[name] = template%k, cls.LOCALS_HANDLERS.new_child(other_handlers), (*cls.interrupt_hooks, *additional_interrupt_hooks), (*cls.memerr_hooks, *additional_memerr_hooks), default_local_exit, disallow_subclass_msg is not None, native_handler
        if disallow_subclass_msg: cls.disallow_subclass_msg = disallow_subclass_msg
    def __repr__(self): return f'{fullname(self)}({self._loop!r}, local_exit={self.local_exit})'
    @property
    def is_running(self): return self._internal_is_running
    def run(self, *, exitmsg='Thank you for using %s!\nExiting REPL...\n', threadname='<%s REPL thread>', max_memerrs=None, always_run_interactive=bool(S.flags.inspect), always_install_completer=False, suppress_asyncio_warnings=False, suppress_unawaited_coroutine_warnings=False, _=frozenset(('win32', 'cygwin', 'android', 'ios', 'wasi'))):
        self.prehook(max_memerrs); S.audit(f'{fullname(self)}.run', id(self)); l = self._loop
        if always_run_interactive or S.stdin.isatty():
            S.audit('cpython.run_stdin'); __import__('threading').Thread(name=threadname%(n := self.NAME), target=self.interact, daemon=True).start(); w = S.stderr.write
            if callable(h := getattr(S, i := '__interactivehook__', None)):
                S.audit('cpython.run_interactivehook', h)
                try: h()
                except: w(f'Error running {self!r}!\nFailed calling sys.__interactivehook__\n'); __import__('traceback').print_exc() # noqa: E722
                if always_install_completer or (S.platform not in _ and h.__module__ == 'site' and h.__name__ == 'register_readline'):
                    try: __import__('readline').set_completer(__import__('rlcompleter').Completer(self.locals).complete)
                    except ImportError: w('Failed to install readline completer\n')
            elif h is not None: w('Removing sys.__interactivehook__ since it is not callable\n'); delattr(S, i)
            while True:
                try: l.run_forever(); break
                except KeyboardInterrupt: self.interrupt()
                except MemoryError: self.memoryerror()
        else: self.write_special(self.BANNER); self.runcode(compile((l := S.stdin).read(), getattr(l, 'name', '<stdin>'), 'exec'))
        try: self.posthook()
        except BaseException as e: w(f'{fullname(e)} occurred in posthook of {self!r}: {e}\n')
        if suppress_asyncio_warnings: P.patch_asyncio_warnings()
        if suppress_unawaited_coroutine_warnings: P.patch_unawaited_coroutine_warnings()
        self.write_special(exitmsg%n); return self.retcode
    @property
    def retcode(self): return 0 if (e := self.exc) is None else e.code
    P.patch_method_signatures((run, '*, exitmsg=None, threadname=None, max_memerrs=None, always_run_interactive=None, always_install_completer=False, suppress_asyncio_warnings=False, suppress_unawaited_coroutine_warnings=False'), (interrupt, ''), (set_return_code, 'e, /'), (__init__, 'loop, mod=None, modname=None, *, context_factory={}'), (__callback, 'fut, code, /, *, makef={0}, corocheck={0}, futchain={0}'), (interact, "banner=None, *, ps1='>>> '")); P.patch_classmethod_signatures((__init_subclass__, '*, name=None, native_handler=None, default_local_exit=True, disallow_subclass_msg=None, other_handlers=None, additional_interrupt_hooks=(), additional_memerr_hooks=(), template={}, version=None, description=None, **k'))
def _(d, /):
    def load_all(_=d):
        for k, v in _.items(): _[k] = v if (g := getattr(v, 'load', None)) is None else g()
    load_all.__qualname__, load_all.__module__ = load_all.__name__, 'asyncutils'; P.patch_function_signatures((load_all, '')); return load_all
class AsyncUtilsConsole(ConsoleBase, version=V, description='asyncutils is a multi-purpose and efficient asynchronous utilties library.\nYou can use await statements directly instead of asyncio.run for quick testing.\nAll the submodules of asyncutils are also loaded into the namespace.\nDo not use functions such as util.sync_await in this REPL, since they are bound to cause deadlocks.', native_handler=lambda d, /, v=V, _=_f, r=_: (u := d.update)(m := __import__('asyncutils._internal.initialize', fromlist=_).s) or u(__version__=v, load_all=r(m)), default_local_exit=True, disallow_subclass_msg='cannot subclass %s; subclass asyncutils.console.ConsoleBase instead'):
    def __repr__(self): return f'<{"running" if self.is_running else "idle"} asyncutils console at {id(self):#x}>'
    @property
    def is_running(self, _='User tampered with console-internal state!\n'): # noqa: PLR0206
        if not self._loop.is_running(): self._internal_is_running = False; return False
        if self._internal_is_running == (b := R.get() is self): return b
        if b: self._internal_is_running = True
        else: self.set_return_code(_)
        S.stderr.write(_); return False
    def _interact_hook(self, ps1, kcolor, reset, fcolor):
        super()._interact_hook(ps1, kcolor, reset, fcolor)
        if R.should_write_load_all(): self.write_special(f'{ps1}{fcolor}load_all{reset}()\n')
    def write_special(self, msg, _=C.silent):
        if not _: self.write(msg)
    def prehook(self, max_memerrs, _=C.max_memerrs, _r='this console is already running', _a='another console is running'):
        if self._internal_is_running: raise RuntimeError(_r)
        if r := R.get(): raise RuntimeError(_r if r is self else _a)
        R.set(self); super().prehook(_ if max_memerrs is None else max_memerrs)
    def posthook(self, _m='WARNING: user tampered with asyncutils module state\n', _=C.pdb, _e=StateCorrupted('console-internal', "attribute 'exc' of console was set to a non-SystemExit exception")):
        if R.unset() is not self: S.stderr.write(_m); del S.modules[__name__]
        if _ and isinstance(e := self.exc, BaseException):
            if not isinstance(e, SystemExit): raise _e
            __import__('pdb').post_mortem(e.__traceback__)
        super().posthook()
    def showtraceback(self, _sf=3, _suf=('asyncutils\\console.py', 'asyncutils/console.py'), _fln=38, _mn=S.intern('__callback')):
        t, v, b = S.exc_info()
        if b is None: return
        try:
            for _ in range(_sf):
                if (b := b.tb_next) is None: break
            else:
                if (c := b.tb_frame.f_code).co_filename.endswith(_suf) and c.co_firstlineno == _fln and c.co_name == _mn: b = b.tb_next
            if b is not None: self._showtraceback(t, v, b, '')
        finally: t = v = b = None
    P.patch_method_signatures((showtraceback, ''), (posthook, ''), (prehook, 'max_memerrs'), (write_special, 'msg'))
del _f, _s, g, C, V, B, _, iscoroutine