from asyncutils._internal import patch as P
from asyncutils._internal.submodules import context_all as __all__
from asyncutils._internal.unparsed import C
_, k, all_contextual_consts = __import__('_contextvars').ContextVar('asyncutils_contextvar'), None, frozenset(C)
class Context:
    __slots__ = tuple(C); exec(f'def __new__(cls,/,*,{",".join(f"{k}={v!r}" for k, v in C.items())}):\n\t(_:=object.__new__(cls)).{"\n\t_.".join(f"{k}={k}" for k in __slots__)}\n\treturn _') # noqa: S102
    def __init_subclass__(cls, /, **_): raise TypeError('cannot subclass asyncutils.context.Context')
    def __getattribute__(self, n, /, _=frozenset(('ascurctx', 'replace_from_dct', 'replace', 'update', 'asdict', 'copy', 'pprint', 'from_dct')), u='__'): return super().__getattribute__(n if n in _ or (n.startswith(u) and n.endswith(u)) else n.upper())
    def __getitem__(self, n, /): return super().__getattribute__(n.upper())
    def __setattr__(self, n, v, /):
        if (n := n.upper()) not in all_contextual_consts: raise AttributeError(f'{type(self).__name__!r} object has no attribute {n!r}')
        if isinstance(v, list):
            if v and isinstance(v[0], list): v = map(tuple, v)
            v = tuple(v)
        super().__setattr__(n, v)
    def replace_from_dct(self, d, /, _=all_contextual_consts):
        D = self.asdict()
        for n, v in d.items():
            if (n := n.upper()) in _: D[n] = v
        return type(self)(**D)
    def update(self, d=None, _=all_contextual_consts, /, **k):
        for m in (d, k):
            if not m: continue
            for n, v in m.items():
                if (n := n.upper()) in _: setattr(self, n, v)
    def ascurctx(self): return nonreusablelocalcontext(self)
    @classmethod
    def from_dct(cls, d, /): return cls(**{k.upper(): v for k, v in d.items()})
    def asdict(self): return {k: getattr(self, k) for k in self.__slots__}
    def copy(self): return type(self)(**self.asdict())
    def replace(self, /, **k): return self.replace_from_dct(k)
    def pprint(self, file=__import__('sys').stdout, *, flush=True, pp=__import__('pprint').PrettyPrinter(sort_dicts=False, underscore_numbers=True), incl_newline=True): file.write('Context.from_dct(\n'); pp._format(self.asdict(), file, 0, 0, {}, 0); print('\n)', end='\n'*incl_newline, file=file, flush=flush) # pragma: no cover # noqa: B008
    def __str__(self, _=__import__('_io').StringIO): self.pprint(s := _(), incl_newline=False); return s.getvalue()
    def __repr__(self): return f'Context({", ".join(f"{k}={getattr(self, k)!r}" for k in self.__slots__)})'
    __copy__, __replace__, __setitem__ = copy, replace, __setattr__; P.patch_method_signatures((__str__, ''), (update, 'd=None, /, **k'), (pprint, 'file={0}, *, pp={0}, incl_newline=True'), (replace_from_dct, 'd, /'), (__getattribute__, 'name, /'))
def getcontext(_=_, d=Context()):
    try: return _.get()
    except LookupError: _.set(d); return d
def setcontext(c, /, _=_):
    if not isinstance(c, Context): raise TypeError('setcontext: ctx must be an instance of asyncutils.context.Context')
    _.set(c)
class localcontext:
    __slots__ = 'new_ctx', 'saved_ctx'
    def __init__(self, ctx=None, **k):
        if ctx is None: ctx = getcontext()
        if type(ctx) is not Context: raise TypeError('localcontext: ctx must be an instance of asyncutils.context.Context')
        self.new_ctx = ctx.replace_from_dct(k)
    def __enter__(self): self.saved_ctx = getcontext(); setcontext(c := self.new_ctx); return c
    def __exit__(self, /, *_):
        setcontext(self.saved_ctx); del self.saved_ctx
        if isinstance(self, nonreusablelocalcontext): del self.new_ctx
    async def __aenter__(self): return self.__enter__()
    async def __aexit__(self, /, *_): return self.__exit__(*_)
    P.patch_method_signatures((__exit__, s := P.xsig), (__aexit__, s)); del s
class nonreusablelocalcontext(localcontext): __slots__ = ()
def __getattr__(n, /, _=getcontext): return getattr(_(), n)
P.patch_function_signatures((getcontext, ''), (setcontext, 'ctx, /'), (__getattr__, 'name, /'))
del _, P, k, C