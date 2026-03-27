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
    __slots__ = 'func', 'args', 'keywords', '_phcount', '_merger'
    @__import__('reprlib').recursive_repr()
    def __repr__(self): (f := (A := [repr(self.func)]).extend)(map(repr, self.args)); f(f'{k}={v!r}' for k, v in self.keywords.items()); return f'asyncutils._internal.compat.partial({', '.join(A)})'
    def __new__(cls, f, /, *a, **k):
        if a and a[-1] is Placeholder: raise TypeError('trailing Placeholders are not allowed')
        if any(v is Placeholder for v in k.values()): raise TypeError('Placeholder cannot be passed as a keyword argument')
        if isinstance(f, partial):
            P, e = f._phcount, (A := list(f.args)).extend
            if a:
                e(a)
                if P:
                    N = len(a)
                    if N < P: e(Placeholder for _ in range(P-N))
                    A = list(f._merger(A)) # type: ignore
                    if N > P: A.extend(a[P:])
                C, M = _partial_prepare_merger(A)
            else: C, M = P, f._merger
            k, f = f.keywords|k, f.func
        else: A = a; C, M = _partial_prepare_merger(a)
        (_ := object.__new__(cls)).func, _.args, _.keywords, _._phcount, _._merger = f, tuple(A), k, C, M; return _
    def __call__(self, /, *a, **k):
        if (c := self._phcount):
            try: A, a = self._merger(self.args+a), a[c:] # type: ignore
            except IndexError: raise TypeError(f"missing positional arguments in 'partial' call; expected at least {c}, got {len(a)}") from None
        else: A = self.args
        return self.func(*A, *a, **self.keywords, **k)
    def __get__(self, o, _=None, m=__import__('_types').MethodType, /): return self if o is None else m(self, o)
    def __reduce__(self): return type(self), (self.func,), (self.func, self.args, self.keywords or None)
    def __setstate__(self, state):
        f, a, k = state
        if (not callable(f) or not isinstance(a, tuple) or (k is not None and not isinstance(k, dict))): raise TypeError('invalid partial state')
        if a and a[-1] is Placeholder: raise TypeError('trailing Placeholders are not allowed')
        if k is None: k = {}
        self.func, self.args, self.keywords = f, a, k; self._phcount, self._merger = _partial_prepare_merger(a)