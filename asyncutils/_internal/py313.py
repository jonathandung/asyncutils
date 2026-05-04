from asyncutils._internal.helpers import verify_compat
if verify_compat('3.13'): from _heapq import heapify_max as heapify, heappop_max as heappop, heapreplace_max as heapreplace, heappush_max as heappush, heappushpop_max as heappushpop # type: ignore[import-not-found]
else:
    from _heapq import _heapify_max as heapify, _heappop_max as heappop, _heapreplace_max as heapreplace; from heapq import _siftdown_max, _siftup_max # type: ignore[import-not-found]
    def heappush(heap, item, /, _=_siftdown_max): heap.append(item); _(heap, 0, len(heap)-1)
    def heappushpop(heap, item, /, _=_siftup_max):
        if heap and item > (m := heap[0]): item, heap[0] = m, item; _(heap, 0)
    del _siftdown_max, _siftup_max
__all__ = 'Placeholder', 'heapify', 'heappop', 'heappush', 'heappushpop', 'heapreplace', 'pargs', 'partial'
pargs, Placeholder = {}, 'Placeholder'
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
    def __repr__(self): (f := (A := [repr(self.func)]).extend)(map(repr, self.args)); f(f'{k}={v!r}' for k, v in self.keywords.items()); return f'asyncutils._internal.py313.partial({', '.join(A)})'
    def __new__(cls, f, /, *a, **k): return cls._new(f, a, k)
    @classmethod
    def _new(cls, f, a, k, /, _=_get_merger):
        if a and a[-1] is Placeholder: raise TypeError('trailing Placeholders are not allowed')
        if k is None: k = {}
        if any(v is Placeholder for v in k.values()): raise TypeError('Placeholder cannot be passed as a keyword argument')
        if isinstance(f, partial):
            P, e = f._phs, (A := list(f.args)).extend
            if a:
                e(a)
                if P:
                    if (N := len(a)) < P: e(Placeholder for _ in range(P-N))
                    A = list(f._mg(A))
                    if N > P: A.extend(a[P:])
                C, M = _(A)
            else: C, M = P, f._mg
            k, f = f.keywords|k, f.func
        else: C, M = _(A := a)
        (_ := object.__new__(cls)).func, _.args, _.keywords, _._phs, _._mg = f, tuple(A), k, C, M; return _
    def __call__(self, /, *a, **k):
        if (c := self._phs):
            try: A, a = self._mg(self.args+a), a[c:]
            except IndexError: raise TypeError(f"missing positional arguments in 'partial' call; expected at least {c}, got {len(a)}") from None
        else: A = self.args
        return self.func(*A, *a, **self.keywords, **k)
    def __get__(self, o, _=None): return self if o is None else type(self.__get__)(self, o)
    def __reduce__(self): return type(self)._new, (self.func, self.args, self.keywords or None)
del verify_compat, _get_merger