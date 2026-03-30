from . import config as C, __version__ as V
from ._internal import patch as P, running_console as R
import sys as S
from os import getenv as g
from ._internal.submodules import console_all as __all__
try: from _pyrepl.console import InteractiveColoredConsole as B
except ImportError: from code import InteractiveConsole as B; C.basic_repl = True # type: ignore
_f, _s = ('',), object()
class ConsoleBase(B): # type: ignore
    LOCALS_HANDLERS, interrupt_hooks, memerr_hooks, default_local_exit, disallow_subclass_msg, _unsubclassable = __import__('collections').ChainMap(), (), (lambda self, f=S._clear_internal_caches, g=__import__('gc').collect, d=__import__('logging').getLogger('asyncutils').debug: f() or self.write('MemoryError\n') or d(f'Emergency garbage collection after MemoryError: {g()} objects collected in total'),), False, 'cannot subclass %r', False
    match '1' if C.basic_repl else g('PYTHON_BASIC_REPL', '0'):
        case '1': CAN_USE_PYREPL = False
        case str() as s:
            if s != '0': S.stderr.write(f'WARNING: unknown value associated with environment variable PYTHON_BASIC_REPL: {s!r}\n')
            from _pyrepl.main import CAN_USE_PYREPL
    def __init__(self, loop, mod=None, modname=None, *, context_factory=__import__('_contextvars').copy_context, _f=_f, _s=_s, _m='cannot %s event loop within REPL'):
        S.audit(f'{(t := type(self)).__module__}.{t.__qualname__}', loop)
        if t is __class__: raise TypeError('cannot instantiate asyncutils.console.ConsoleBase; please subclass instead')
        if modname is None: modname = self.NAME
        if mod is None: mod = __import__(modname, fromlist=_f)
        def stop(p=None, /, _o=loop.stop, *, asap=False):
            if p is _s: _o() if asap else loop.call_soon_threadsafe(_o)
            else: raise RuntimeError(_m%'stop')
        def close(p=None, /, _o=loop.close):
            if p is _s: _o()
            else: raise RuntimeError(_m%'close')
        loop.stop, loop.close, self._internal_is_running, self.memory_errors, self._loop, self.context, self.retcode, self._fut, (d := dict(__name__='__main__', __doc__='A console with top-level await support.', __package__=__package__, __loader__=__loader__, __spec__=__spec__, __builtins__=__builtins__, __file__=__file__))[modname] = stop, close, False, 0, loop, context_factory(), 0, None, mod; super().__init__(d, '<stdin>', local_exit=self.default_local_exit); self.compile.compiler.flags |= 0x2000
        if callable(h := self.LOCALS_HANDLERS.get(modname)): h(d)
    def refresh(self):
        if not ((F := self._fut) is None or F.done()): F.cancel()
    def __callback(self, fut, code, /, *, makef=type(refresh), corocheck=__import__('asyncio.coroutines', fromlist=_f).iscoroutine, futchain=__import__('asyncio.futures', fromlist=_f)._chain_future):
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
        getattr(self._loop, 'call_soon'+'_threadsafe'*threadsafe)(self.__callback, F := futimpl(), code, context=self.context)
        try: return F.result()
        except SystemExit as e: self.set_return_code(e)
        except BaseException as e:
            if not isinstance(e, dont_show_traceback): self.showtraceback()
            return self.STATEMENT_FAILED
    def interact(self, banner=None, *, ps1='>>> ', _f=_f, _s=_s, _q=C.silent, _o=type('', (), {'write': lambda *_: None, 'flush': lambda _, /: None})(), _g=g):
        x, p = False, None; self.write_special(self.BANNER if banner is None else banner)
        try:
            if p := _g('PYTHONSTARTUP'):
                with __import__('tokenize').open(p) as f:
                    if _q: S.stdout, _o = _o, S.stdout
                    S.audit('cpython.run_startup', p); exec(compile(f.read(), p, 'exec'), self.locals)
                    if _q: S.stdout = _o
            if (p := getattr(S, 'ps1', None)) is None: p, x = ps1, True
            if self.CAN_USE_PYREPL: self._interact_hook(f'{(t := __import__('_colorize').get_theme().syntax).prompt}{p}{(r := t.reset)}'.lstrip(), t.keyword, r, t.builtin); __import__('_pyrepl.simple_interact', fromlist=_f).run_multiline_interactive_console(self)
            else: self._interact_hook(p, '', '', ''); super().interact('', '')
        finally: self._loop.stop(_s); S.ps1 = ps1 if x else getattr(S, 'ps1', ps1) if p is None else p
    def _interact_hook(self, ps1, kcolor, reset, fcolor): n, S.ps1 = self.NAME, ps1; self.write_special(f'{ps1}{kcolor}import{reset} {n}\n{ps1}{kcolor}from{reset} {n} {kcolor}import{reset} *\n')
    def prehook(self, max_memerrs): self._max_memerrs, self._internal_is_running = 3 if max_memerrs is None else max_memerrs, True
    def posthook(self): self._internal_is_running = False
    def write_special(self, msg): self.write(msg)
    def interrupt(self, _f=_f, _m='\nKeyboardInterrupt\n'):
        if not self.CAN_USE_PYREPL: self.write(_m)
        elif (x := __import__('_pyrepl.simple_interact', fromlist=_f)._get_reader().threading_hook): x.add('')
        self.refresh()
    def memoryerror(self):
        if (m := self.memory_errors) == self._max_memerrs: self.write_special(f'Exceeded MemoryError threshold: {m}\n'); return self.set_return_code(1)
        self.memory_errors = m+1
        for _ in self.memerr_hooks: _(self)
        self.refresh()
    def set_return_code(self, e, /, _s=_s): self.retcode = e if isinstance(e, int) else e.code; self._loop.stop(_s)
    def __init_subclass__(cls, *, name=None, native_handler=None, default_local_exit=True, disallow_subclass_msg=None, other_handlers=None, additional_interrupt_hooks=(), additional_memerr_hooks=(), template='%(name)s REPL (version %(version)s) running on {}\nType "help", "copyright", "credits" or "license" for more information, "clear" to clear the terminal, and "exit" or "quit" to exit.\n%(description)s\n'.format(S.platform), **k):
        if cls._unsubclassable: raise TypeError(cls.disallow_subclass_msg%cls.__qualname__)
        if name is None: name = cls.__qualname__.lower().removesuffix('console')
        if other_handlers is None: other_handlers = {}
        k['name'] = cls.NAME = name; (f := k.setdefault)('version', 'unknown'); f('description', 'Enjoy!'); cls.BANNER, cls.LOCALS_HANDLERS, cls.interrupt_hooks, cls.memerr_hooks, cls.default_local_exit, cls._unsubclassable, other_handlers[name] = template%k, cls.LOCALS_HANDLERS.new_child(other_handlers), (*cls.interrupt_hooks, *additional_interrupt_hooks), (*cls.memerr_hooks, *additional_memerr_hooks), default_local_exit, disallow_subclass_msg is not None, native_handler
        if disallow_subclass_msg: cls.disallow_subclass_msg = disallow_subclass_msg
    def __repr__(self): return f'{type(self).__qualname__}({self._loop!r}, local_exit={self.local_exit})'
    @property
    def is_running(self): return self._internal_is_running
    def run(self, *, exitmsg='Thank you for using %s!\nExiting REPL...\n', threadname='<%s REPL thread>', max_memerrs=None, always_run_interactive=bool(S.flags.inspect), always_install_completer=False, suppress_asyncio_warnings=False, suppress_unawaited_coroutine_warnings=False):
        self.prehook(max_memerrs); S.audit(f'{type(self).__qualname__}.run', self); l = self._loop
        if always_run_interactive or S.stdin.isatty():
            S.audit('cpython.run_stdin'); __import__('threading').Thread(name=threadname%(n := self.NAME), target=self.interact, daemon=True).start(); w = S.stderr.write
            if callable(h := getattr(S, i := '__interactivehook__', None)):
                S.audit('cpython.run_interactivehook', h)
                try: h()
                except: w(f'Error running {self!r}\nFailed calling sys.__interactivehook__\n'); __import__('traceback').print_exc()
                if always_install_completer or (h.__module__ == 'site' and h.__name__ == 'register_readline'):
                    try: __import__('readline').set_completer(__import__('rlcompleter').Completer(self.locals).complete)
                    except ImportError: ...
            elif h is not None: w('Removing sys.__interactivehook__ because it is not callable\n'); delattr(S, i)
            while True:
                try: l.run_forever(); break
                except KeyboardInterrupt: self.interrupt()
                except MemoryError: self.memoryerror()
        else: self.write_special(self.BANNER); self.runcode(compile((l := S.stdin).read(), getattr(l, 'name', '<stdin>'), 'exec'))
        try: self.posthook()
        except BaseException as e: w(f'{type(e).__qualname__} occurred in posthook of {self!r}: {e}\n')
        if suppress_asyncio_warnings: P.patch_asyncio_warnings()
        if suppress_unawaited_coroutine_warnings: P.patch_unawaited_coroutine_warnings()
        self.write_special(exitmsg%n); return self.retcode
    P.patch_method_signatures((interrupt, ''), (set_return_code, 'e, /'), (__init__, 'loop, mod=None, modname=None, *, context_factory={}'), (__callback, 'fut, code, /, *, makef={0}, corocheck={0}, futchain={0}'), (interact, "banner=None, *, ps1='>>> '"))
class AsyncUtilsConsole(ConsoleBase, version=V, description='asyncutils is a multi-purpose and efficient asynchronous utilties library.\nYou can use await statements directly instead of asyncio.run for quick testing.\nAll the submodules of asyncutils are also loaded into the namespace.\nDo not use functions such as sync_await in this REPL, they are bound to cause deadlocks.', native_handler=lambda d, /, v=V, _=_f: d.update(m := __import__('asyncutils._internal.initialize', fromlist=_).s) or setattr(f := lambda m=m, /: m.update({k: v if (g := getattr(v, 'load', None)) is None else g() for k, v in m.items()}), '__qualname__', l := 'load_all') or setattr(f, '__name__', l) or d.update(__version__=v, load_all=f), default_local_exit=True, disallow_subclass_msg='cannot subclass %s; subclass asyncutils.console.ConsoleBase instead'):
    def __repr__(self): return f'<{'running' if self.is_running else 'idle'} asyncutils console at {id(self):#x}>'
    @property
    def is_running(self, _m='User tampered with console-internal state!\n'):
        if not self._loop.is_running(): self._internal_is_running = False; return False
        if self._internal_is_running^(b := R._get_() is self):
            if b: self._internal_is_running = True
            else: self.set_return_code(1)
            S.stderr.write(_m); return False
        return b
    def _interact_hook(self, ps1, kcolor, reset, fcolor):
        super()._interact_hook(ps1, kcolor, reset, fcolor)
        if R._should_write_load_all_(): self.write_special(f'{ps1}{fcolor}load_all{reset}()\n')
    def write_special(self, msg, _=C.silent):
        if not _: self.write(msg)
    def prehook(self, max_memerrs, _m=C.max_memerrs, _r='this console is already running', _a='another console is running'):
        if self._internal_is_running: raise RuntimeError(_r)
        if (r := R._get_()) is None: R._set_(self)
        else: raise RuntimeError(_r if r is self else _a)
        super().prehook(_m if max_memerrs is None else max_memerrs)
    def posthook(self, _m='WARNING: user tampered with asyncutils module state\n'):
        if R._unset_() is not self: S.stderr.write(_m); del S.modules[__name__]
        super().posthook()
    def showtraceback(self, _skip_frames=3, _suf=('asyncutils\\console.py', 'asyncutils/console.py'), _fln=30, _mn=S.intern('__callback')):
        t, v, b = S.exc_info()
        try:
            for _ in range(_skip_frames):
                if b is None or (n := b.tb_next) is None: break
                b = n.tb_next if (c := n.tb_frame.f_code).co_filename.endswith(_suf) and c.co_firstlineno == _fln and c.co_name == _mn else n
            if b is not None: self._showtraceback(t, v, b, '')
        finally: t = v = b = None
    P.patch_method_signatures((showtraceback, ''), (posthook, ''), (prehook, 'max_memerrs'), (write_special, 'msg'))
del _f, _s, g, C, V, B