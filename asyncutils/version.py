from asyncutils import exceptions as E
from asyncutils._internal import patch as P
from asyncutils._internal.submodules import version_all as __all__
def p(I, /, f=0 .__gt__, e=E.VersionValueError):
    a, i = (r := []).append, 0
    for i, j in enumerate(I):
        a(int(j, 0) if isinstance(j, str) else int(j))
        if i == 2: break
    else: r.extend(0 for _ in range(2-i))
    if any(map(f, r)): raise e('major, minor and patch should all be positive')
    return tuple(r)
def r(c, /, _='cannot subclass asyncutils.version.%s'):
    def f(_=TypeError(_%c.__name__)): raise _
    return f
def a(c, /, t=tuple(property(lambda o, _=i: o[_]) for i in range(3)), _=r, f=('major', 'minor', 'patch')): c._fields, c._asdict = f, lambda self, _=f: dict(zip(_, self)); c.major, c.minor, c.patch = t; c.__floor__ = c.__trunc__ = t[0].fget; c._replace = c.__replace__ = lambda self, **k: c(**self._asdict(), **k); c.__init_subclass__ = _(c); return c
N, t, _ = {}, lambda o, /: o if isinstance(o, type) else type(o), 0xFF
def b(z): z <<= 1; return ~z if z < 0 else z
def c(key, _=_, f=b): return (key := f(key))&_, key>>18, (key>>10)&_, key>>9&1
@a
class VersionDelta(tuple):
    __slots__ = (); _make = classmethod(tuple.__new__)
    def __new__(cls, major=0, minor=0, patch=0): return cls._make((major, minor, patch))
    def __neg__(self): return __class__(*map(int.__neg__, self))
@a
class VersionInfo(str): # noqa: FURB189
    __slots__ = 'parts',
    def __new__(cls, /, *a, p=p): object.__setattr__(s := super().__new__(cls, '.'.join(map(str, a := normalize(a[0]) if len(a) == 1 else p(a)))), 'parts', a); return s
    def _hash(self, _=lambda x, y, /: y*y+x if x < y else x*x+x+y, f=lambda n: (~n if n&1 else n)>>1): return f(_(_(*self[:2]), self[2]))
    def __hash__(self): return (x := self._hash())+(x > -2)
    def shelve(self, path, /, key=5, _=_, g=c):
        x, h, y, l = g(key); y ^= self._hash()
        with open(path, 'wb') as f: (w := f.write)(bytes((h,))); w(bytes((i-x)&_ for i in y.to_bytes((y.bit_length()>>3)+1, 'little' if l else 'big', signed=True)))
    @classmethod
    def unshelve(cls, path, /, key=5, _=_, g=c):
        x, h, y, l = g(key)
        with open(path, 'rb') as f:
            if (r := f.read)(1)[0] != h: raise ValueError('bad key')
            return cls._unhash(int.from_bytes(((i+x)&_ for i in r()), 'little' if l else 'big', signed=True)^y)
    @classmethod
    def from_hash(cls, hashed, _=E.VersionValueError('hash cannot be -1')):
        if hashed == -1: raise _
        return cls._unhash(hashed-(hashed > -1))
    @classmethod
    def _unhash(cls, c, /, _=b, f=lambda z, f=__import__('math').isqrt: (x, y) if (x := z-(y := f(z))*y) < y else (y, x-y)): b, c = f(_(c)); return cls(*f(b), c)
    @classmethod
    def from_rep(cls, rep): return cls(rep.removeprefix('asyncutils v'))
    @classmethod
    def get_current_version(cls, _=E.StateCorrupted('module-internal', 'asyncutils.__version__ is inconsistent with expectations')):
        from asyncutils import __version__ as V
        if isinstance(V, cls): V.assert_valid(); return V
        raise _
    def is_current_version(self): return __class__.get_current_version() == self
    def __round__(self, n=None, /): return __class__(self[:n])
    def __repr__(self): return f'VersionInfo{self:t}'
    def __ceil__(self): return self[0]+any(self[1:])
    def __len__(self): return 3
    def to_complex(self): return complex(*self[:2])
    def __float__(self, _=.01): return sum((j*_**i for i, j in enumerate(self)), start=.0)
    def __reduce__(self): return __class__, self.parts
    def __iter__(self): return self.parts.__iter__()
    def __getitem__(self, i, /): return tuple.__getitem__(self.parts, i)
    def assert_valid(self, _=E.VersionCorrupted):
        try:
            if isinstance(p := self.parts, tuple) and len(p) == 3 and all(isinstance(i, int) and i == j >= 0 for i, j in zip(map(int, self.split('.')), p, strict=True)): return
        except (ValueError, TypeError, AttributeError): ...
        raise _(self) # type: ignore
    def replace_parts(self, *, _=('major', 'minor', 'patch'), **k): return __class__(*(getattr(self, _) if (v := k.pop(_, None)) is None else v for _ in _))
    def __format__(self, s, /, a=dict(x='hex', b='bin', o='oct', dec='d', major='0', minor='1', patch='2', maj='0', min='1', short='s', long='l', chars='c', tuple='t', hash='h', majmin='n').get): # noqa: C408
        match s := a(s := s.lower(), s):
            case '0'|'1'|'2': return str(self[int(s)])
            case 's': return 'v'+'.'.join(map(str, self if self[2] else self[:2 if self[1] else 1]))
            case 'l': return f'asyncutils version {self}'
            case 'c': return bytes(self).decode('latin-1')
            case 't': return str(self.parts)
            case 'd': return repr(int(self))
            case 'h': return repr(hash(self))
            case 'n': return self.rpartition('.')[0]
            case 'bin'|'hex'|'oct': return __builtins__[s](int(self))
        return str(self)
    def __add__(self, o, /): return __class__(*self[:2], self[2]+o) if isinstance(o, int) else __class__(*map(int.__add__, self, o)) if isinstance(o, VersionDelta) else NotImplemented # type: ignore
    def __sub__(self, o, /, f=lambda x, y: max(0, x-y)): return __class__(*self[:2], f(self[2], o)) if isinstance(o, int) else T[1-T.index(t)](*map(f, self, o, strict=True)) if (t := type(o)) in (T := (VersionDelta, __class__)) else NotImplemented
    def next_patch(self): return self.replace_parts(patch=self[2]+1)
    def next_minor(self): return __class__(self[0], self[1]+1)
    def next_major(self): return __class__(self[0]+1, 0)
    def change_sep(self, sep): return self.replace('.', sep)
    def __setattr__(self, name, value, /): raise AttributeError(f'attribute {name!r} cannot be set to {value!r} on {__class__.__name__} object')
    def __int__(self, _=0x100):
        M, m, p = self
        if not 0 <= p < _ > m >= 0: raise OverflowError(f'cannot pack version {self} into an integer')
        return p|m<<8|M<<16
    @property
    def is_api_unstable(self): return self[0] == 0
    def compatible(self, o, /, majtol=0, mintol=None): return majtol is None or (abs(self[0]-o[0]) <= majtol and (mintol is None or abs(self[1]-o[1]) <= mintol))
    representation, __index__, __radd__ = property('asyncutils v'.__add__), __int__, __add__; P.patch_classmethod_signatures((__new__, '/, *args'), (get_current_version, ''), (from_hash, 'hashed'), (unshelve, _ := 'path, /, key=5')); P.patch_method_signatures((shelve, _), (__format__, 'format_spec, /'), (__hash__, ''), (__sub__, 'other, /'), (replace_parts, '*, major=None, minor=None, patch=None')); del _
def normalize_allow_unimplemented(o, /, E=E, p=p, c=lambda o, /, t=tuple(map(type, (p.__get__(True), True.__init__, ''.lower))), a='__iter__': isinstance(getattr(o, a, None), t), s=frozenset(('inf', '-inf', 'nan')), m=0xFF):
    if (T := type(o)) is VersionInfo: return o.parts
    if T is str: o = o.split('.')
    elif T is complex: o = o.real, o.imag, 0
    if T is int: o = o>>16, (o>>8)&m, o&m
    elif T is float:
        if (o := format(o, '.4f')) in s: return
        o, _ = o.split('.', 1); o = map(int, (o, _[:2], _[2:]))
    elif f := dispatch_normalizer(o, type):
        try:
            if (o := f(o)) is None: return
        except E.CRITICAL: raise E.Critical
        except BaseException as e: unregister_normalizer(o, type); raise E.VersionNormalizerFault(f, o, e) from None # noqa: BLE001
        else:
            if not c(o): raise E.VersionNormalizerTypeError(f, o)
    elif not c(o): return
    with E.IgnoreErrors(TypeError, ValueError): return p(o)
def normalize(o, /, e=E.VersionNormalizerMissing):
    if (r := normalize_allow_unimplemented(o)) is None: raise e(o)
    return r
def register_normalizer(o, n, /, _=t, f=N.setdefault): return f(_(o), n) is n
def unregister_normalizer(o, /, _=t, f=N.pop): return f(_(o), None)
def dispatch_normalizer(o, /, _=t, f=N.get): return f(_(o))
def autogenerate_normalizers(): return register_normalizer(__import__('_decimal').Decimal, lambda d, /: map(int, ((d := format(d, '.4f'))[:-4], d[-4:-2], d[-2:])))&register_normalizer(F := __import__('fractions').Fraction, F.as_integer_ratio)
P.patch_function_signatures((normalize, t := 'o, /'), (normalize_allow_unimplemented, t), (unregister_normalizer, t), (dispatch_normalizer, t), (register_normalizer, 'o, f, /'))
for _ in ('__lt__', '__le__', '__gt__', '__ge__', '__eq__', '__ne__'): setattr(VersionInfo, _, lambda self, other, /, _=getattr(tuple, _): NotImplemented if (other := normalize_allow_unimplemented(other)) is None else _(self.parts, other))
del _, N, t, P, p, E, a, b, c, r