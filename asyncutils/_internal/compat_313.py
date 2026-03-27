__all__ = 'apargs', 'partial', 'Placeholder'
from _operator import itemgetter
apargs, Placeholder = {}, 'Placeholder'
def _partial_prepare_merger(A):
    if not A: return 0, None
    j = n = len(A)
    f = (O := []).append
    for i, a in enumerate(A):
        if a is Placeholder: f(j); j += 1
        else: f(i)
    return (C := j-n), itemgetter(*O) if C else None
class partial:
    __slots__ = "func", "args", "keywords", "_phcount", "_merger"
    @__import__('reprlib').recursive_repr()
    def __repr__(self): (f := (A := [repr(self.func)]).extend)(map(repr, self.args)); f(f'{k}={v!r}' for k, v in self.keywords.items()); return f'asyncutils._internal.compat.partial({', '.join(A)})'
    def __new__(cls, func, /, *args, **keywords):
        if args and args[-1] is Placeholder: raise TypeError('trailing Placeholders are not allowed')
        if any(v is Placeholder for v in keywords.values()): raise TypeError('Placeholder cannot be passed as a keyword argument')
        if isinstance(func, partial):
            pto_phcount, e = func._phcount, (tot_args := list(func.args)).extend
            if args:
                e(args)
                if pto_phcount:
                    nargs = len(args)
                    if nargs < pto_phcount: e(Placeholder for _ in range(pto_phcount-nargs))
                    tot_args = func._merger(tot_args) # type: ignore
                    if nargs > pto_phcount: tot_args += args[pto_phcount:]
                phcount, merger = _partial_prepare_merger(tot_args)
            else: phcount, merger = pto_phcount, func._merger
            keywords, func = func.keywords|keywords, func.func
        else: tot_args, phcount, merger = args, *_partial_prepare_merger(args)
        (_ := object.__new__(cls)).func, _.args, _.keywords, _._phcount, _._merger = func, tot_args, keywords, phcount, merger; return _
    def __call__(self, /, *args, **keywords):
        if (phcount := self._phcount):
            try: pto_args, args = self._merger(self.args+args), args[phcount:] # type: ignore
            except IndexError: raise TypeError(f"missing positional arguments in 'partial' call; expected at least {phcount}, got {len(args)}") from None
        else:
            pto_args = self.args
        keywords = {**self.keywords, **keywords}
        return self.func(*pto_args, *args, **keywords)
    def __get__(self, o, _=None, m=__import__('_types').MethodType, /): return self if o is None else m(self, o)
    def __reduce__(self): return type(self), (self.func,), (self.func, self.args, self.keywords or None)
    def __setstate__(self, state):
        func, args, kwds = state
        if (not callable(func) or not isinstance(args, tuple) or
           (kwds is not None and not isinstance(kwds, dict))):
            raise TypeError("invalid partial state")
        if args and args[-1] is Placeholder:
            raise TypeError("trailing Placeholders are not allowed")
        phcount, merger = _partial_prepare_merger(args)
        if kwds is None: kwds = {}
        self.func, self.args, self.keywords, self._phcount, self._merger = func, args, kwds, phcount, merger