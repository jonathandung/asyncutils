__all__ = 'Placeholder', 'apargs', 'partial'
apargs, Placeholder = {}, 'Placeholder'
def _get_merger(A, _=__import__('_operator').itemgetter):
    if not A: return 0, None
    j = n = len(A)
    f = (O := []).append
    for i, a in enumerate(A):
        if a is Placeholder: f(j); j += 1
        else: f(i)
    return (C := j-n), _(*O) if C else None
class partial: # noqa: N801
    __slots__ = '_mg', '_phs', 'args', 'func', 'keywords'
    @__import__('reprlib').recursive_repr()
    def __repr__(self): (f := (A := [repr(self.func)]).extend)(map(repr, self.args)); f(f'{k}={v!r}' for k, v in self.keywords.items()); return f'asyncutils._internal.compat.partial({', '.join(A)})'
    def __new__(cls, f, /, *a, **k):
        if a and a[-1] is Placeholder: raise TypeError('trailing Placeholders are not allowed')
        if any(v is Placeholder for v in k.values()): raise TypeError('Placeholder cannot be passed as a keyword argument')
        if isinstance(f, partial):
            P, e = f._phs, (A := list(f.args)).extend
            if a:
                e(a)
                if P:
                    if (N := len(a)) < P: e(Placeholder for _ in range(P-N))
                    A = list(f._mg(A)) # type: ignore
                    if N > P: A.extend(a[P:])
                C, M = _get_merger(A)
            else: C, M = P, f._mg
            k, f = f.keywords|k, f.func
        else: C, M = _get_merger(A := a)
        (_ := object.__new__(cls)).func, _.args, _.keywords, _._phs, _._mg = f, tuple(A), k, C, M; return _
    def __call__(self, /, *a, **k):
        if (c := self._phs):
            try: A, a = self._mg(self.args+a), a[c:] # type: ignore
            except IndexError: raise TypeError(f"missing positional arguments in 'partial' call; expected at least {c}, got {len(a)}") from None
        else: A = self.args
        return self.func(*A, *a, **self.keywords, **k)
    def __get__(self, o, _=None): return self if o is None else type(self.__get__)(self, o) # type: ignore
    def __reduce__(self): return type(self), (self.func,), (self.func, self.args, self.keywords or None)
    def __setstate__(self, s, /):
        f, a, k = s
        if not (callable(f) and isinstance(a, tuple) and (k is None or isinstance(k, dict))): raise TypeError('invalid partial state')
        if a and a[-1] is Placeholder: raise TypeError('trailing Placeholders are not allowed')
        if k is None: k = {}
        self.func, self.args, self.keywords = f, a, k; self._phs, self._mg = _get_merger(a)