from asyncutils._internal import patch as P
from asyncutils._internal.submodules import context_all as __all__
from asyncutils._internal.unparsed import C
_, k, all_contextual_consts, x = __import__('contextvars').ContextVar(__name__), None, frozenset(C), {'sort_dicts': False, 'underscore_numbers': True, 'width': 88}
if __import__('sys').version_info >= (3, 15): x.update(indent=4, expand=True)
class Context: # noqa: PLW1641
    __slots__ = tuple(C); exec(f'def __new__(cls,/,*,{','.join(f'{k}={v!r}' for k, v in C.items())}):\n\t(_:=object.__new__(cls)).{'\n\t_.'.join(f'{k}={k}' for k in __slots__)}\n\treturn _') # noqa: S102
    def __init_subclass__(cls, /, **_): raise TypeError('cannot subclass asyncutils.context.Context')
    def __getattribute__(self, n, /, _=frozenset(('ascurctx', 'replace_from_dct', 'replace', 'update', 'asdict', 'copy', 'pprint', 'from_dct')), u='__'): return super().__getattribute__(n if n in _ or (n.startswith(u) and n.endswith(u)) else n.upper())
    def __getitem__(self, n, /): return super().__getattribute__(n.upper())
    def __setattr__(self, n, v, /):
        if (n := n.upper()) not in all_contextual_consts: raise AttributeError('asyncutils.context.Context: attribute not found', name=n, obj=self)
        if isinstance(v, list):
            if v and isinstance(v[0], list): v = map(tuple, v) # ty: ignore[invalid-argument-type]
            v = tuple(v)
        super().__setattr__(n, v)
    def __delattr__(self, n, /): raise AttributeError('asyncutils.context.Context: cannot delete attribute', name=n, obj=self)
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
    def ascurctx(self, **k): return NonReusableLocalContext(self, **k)
    def __eq__(self, o, /):
        if type(o) is not __class__: return False
        f, g = map(object.__getattribute__.__get__, (self, o)); return all(f(k) == g(k) for k in self.__slots__)
    @classmethod
    def from_dct(cls, d, /): return cls(**{k.upper(): v for k, v in d.items()})
    def asdict(self): return {k: getattr(self, k) for k in self.__slots__}
    def copy(self): return type(self)(**self.asdict())
    def replace(self, /, **k): return self.replace_from_dct(k)
    def pprint(self, file=__import__('sys').stdout, *, flush=True, pp=__import__('pprint').PrettyPrinter(**x), include_newline=True): file.write('Context.from_dct(\n'); pp._format(self.asdict(), file, 0, 0, {}, 0); print('\n)', end='\n'*include_newline, file=file, flush=flush) # noqa: B008 # ty: ignore[invalid-argument-type]
    def __str__(self, _=__import__('_io').StringIO): self.pprint(s := _(), include_newline=False); return s.getvalue()
    def __repr__(self): return f'Context({', '.join(f'{k}={getattr(self, k)!r}' for k in self.__slots__)})'
    def __reduce__(self): return __class__.from_dct, (self.asdict(),)
    __copy__, __replace__, __setitem__ = copy, replace, __setattr__; P.patch_method_signatures((__str__, ''), (update, 'd=None, /, **k'), (pprint, 'file={0}, *, pp={0}, include_newline=True'), (replace_from_dct, 'd, /'), (__getattribute__, 'name, /'))
def getcontext(_=_, d=Context()): # noqa: B008
    try: return _.get()
    except LookupError: _.set(d); return d
def setcontext(c, /, _=_):
    if not isinstance(c, Context): raise TypeError('asyncutils.context.setcontext: ctx must be an instance of asyncutils.context.Context')
    _.set(c)
class LocalContext:
    __slots__ = 'new_ctx', 'saved_ctx'
    def __init__(self, /, ctx=None, **k):
        if ctx is None: ctx = getcontext()
        if type(ctx) is not Context: raise TypeError('asyncutils.context.LocalContext: ctx must be an instance of asyncutils.context.Context')
        self.new_ctx = ctx.replace_from_dct(k)
    def __enter__(self): self.saved_ctx = getcontext(); setcontext(c := self.new_ctx); return c
    def __exit__(self, /, *_):
        setcontext(self.saved_ctx); del self.saved_ctx
        if isinstance(self, NonReusableLocalContext): del self.new_ctx
    async def __aenter__(self): return self.__enter__()
    async def __aexit__(self, /, *_): return self.__exit__(*_)
    P.patch_method_signatures((__exit__, s := P.exit_sig), (__aexit__, s)); del s
class NonReusableLocalContext(LocalContext): __slots__ = ()
def __getattr__(n, /, _=getcontext): return getattr(_(), n)
P.patch_function_signatures((getcontext, ''), (setcontext, 'ctx, /'), (__getattr__, 'name, /'))
del _, P, k, C
