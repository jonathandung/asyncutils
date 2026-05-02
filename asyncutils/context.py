from asyncutils._internal import patch as P
from asyncutils._internal.submodules import context_all as __all__
from asyncutils._internal.unparsed import C
_, k, all_contextual_consts = __import__('_contextvars').ContextVar('asyncutils_contextvar'), None, frozenset(C)
class Context:
    __slots__ = tuple(C); exec(f'''def __new__(cls, /, *, {", ".join(f"{k}={v!r}" for k, v in C.items())}):\n\t(_ := object.__new__(cls)).{"\n\t_.".join(f"{k} = {k}" for k in __slots__)}\n\treturn _''') # noqa: S102
    def __init_subclass__(cls, /, **_): raise TypeError('cannot subclass asyncutils.context.Context')
    def __getattribute__(self, n, /):
        if n[0] == '_': return object.__getattribute__(self, n)
        if isinstance(r := object.__getattribute__(self, n := n.upper()), list):
            if isinstance(r[0], list): r = map(tuple, r)
            r = tuple(r)
        return r
    def __setattr__(self, n, v, /):
        if (n := n.upper()) in all_contextual_consts: object.__setattr__(self, n, v)
        else: raise AttributeError(f'{type(self).__name__!r} object has no attribute {n!r}')
    def replace_from_dct(self, d, /, _=all_contextual_consts):
        D = self.asdict()
        for n, v in d.items():
            if (n := n.upper()) in _: D[n] = v
        return type(self)(**D)
    def update(self, d=None, /, **k):
        for _ in (d or {}, k):
            for n, v in _.items():
                if (n := n.upper()) in all_contextual_consts: setattr(self, n, v)
    @classmethod
    def from_dct(cls, d, /): return cls(**{k.upper(): v for k, v in d.items()})
    def asdict(self): return {k: getattr(self, k) for k in self.__slots__}
    def copy(self): return type(self)(**self.asdict())
    def replace(self, /, **k): return self.replace_from_dct(k)
    def pprint(self, *, file=__import__('sys').stdout, pp=__import__('pprint').PrettyPrinter(sort_dicts=False, underscore_numbers=True)): print(f'Context(\n {pp.pformat(self.asdict())[1:-1]}\n)', file=file) # noqa: B008
    def __repr__(self): return f'Context({", ".join(f"{k}={getattr(self, k)!r}" for k in self.__slots__)})'
    __copy__, __replace__ = copy, replace; P.patch_method_signatures((pprint, '*, file={0}, pp={0}'))
def getcontext(_=_, d=Context()): # noqa: B008
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
        self.new_ctx = ctx.replace(**{n.upper(): v for n, v in k.items()})
    def __enter__(self): self.saved_ctx = getcontext(); setcontext(c := self.new_ctx); return c
    def __exit__(self, /, *_): setcontext(self.saved_ctx); del self.saved_ctx
class nonreusablelocalcontext(localcontext):
    __slots__ = ()
    def __exit__(self, /, *_): super().__exit__(*_); del self.new_ctx
def __getattr__(n, /, _=getcontext): return getattr(_(), n)
P.patch_function_signatures((getcontext, ''), (setcontext, 'ctx, /'), (__getattr__, 'name, /'))
del _, P, k, C