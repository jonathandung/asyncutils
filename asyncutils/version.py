from ._internal import patch as P
from ._internal.submodules import version_all as __all__
from . import exceptions as E
def p(I, /, f=0 .__gt__, e=E.VersionValueError):
    a, i = (r := []).append, 0
    for i, j in enumerate(I):
        a(int(j, 0) if isinstance(j, str) else int(j))
        if i == 2: break
    else: r.extend(0 for _ in range(2-i))
    if any(map(f, r)): raise e('major, minor and patch should all be positive')
    return tuple(r)
@P.patch_properties
class VersionInfo(str):
    __slots__ = 'parts'
    def __new__(cls, /, *a, p=p): object.__setattr__(s := super().__new__(cls, '.'.join(map(str, a := normalize(a[0]) if len(a) == 1 else p(a)))), 'parts', a); return s
    def __init_subclass__(cls, /, **_): raise TypeError('cannot subclass VersionInfo')
    def __hash__(self, f=lambda x, y, /: y*y+x if x < y else x*x+x+y):
        if (x := f(f(*self[:2]), self[2]))&1: x = ~x
        x >>= 1; return x+(x > -2)
    @classmethod
    def from_hash(cls, c, /, f=lambda z, f=__import__('math').isqrt: (x, y) if (x := z-(y := f(z))*y) < y else (y, x-y), e=E.VersionValueError('hash cannot be -1')):
        if c == -1: raise e
        b, c = f(~c if (c := (c-1 if c > -1 else c)<<1) < 0 else c)
        return cls(*f(b), c)
    def __round__(self, n=None, /): return __class__(self[:n])
    def __repr__(self): return f'VersionInfo{self:t}'
    def __ceil__(self): return self[0]+any(self[1:])
    def __len__(self): return 3
    def __complex__(self): return complex(*self[:2])
    def __float__(self, r=.01): return sum((j*r**i for i, j in enumerate(self)), start=.0)
    def __reduce__(self): return __class__, self.parts
    def __iter__(self): return self.parts.__iter__()
    def __getitem__(self, i, /): return tuple.__getitem__(self.parts, i)
    def assert_valid(self, _=E.VersionCorrupted):
        try:
            if isinstance(p := self.parts, tuple) and len(p) == 3 and all(isinstance(i, int) and i == j >= 0 for i, j in zip(map(int, self.split('.')), p, strict=True)): return
        except ValueError, TypeError, AttributeError: ...
        raise _(self)
    def replace_parts(self, *, _=('major', 'minor', 'patch'), **k): return __class__(*(getattr(self, _) if (v := k.pop(_, None)) is None else v for _ in _))
    @classmethod
    def get_current_version(cls, _=E.StateCorrupted):
        from . import __version__ as V
        if isinstance(V, cls): V.assert_valid(); return V
        raise _('module-internal', 'asyncutils.__version__ is inconsistent with expectations')
    def __format__(self, s, /, a=dict(x='hex', b='bin', o='oct', dec='d', major='0', minor='1', patch='2', short='s', long='l', chars='c', tuple='t', hash='h', majmin='n').get):
        match s := a(s := s.lower(), s):
            case '0'|'1'|'2': return str(self[int(s)])
            case 's': return 'asyncutils v'+'.'.join(map(str, self[:None if self[2] else 2 if self[1] else 1]))
            case 'l': return f'asyncutils version {self}'
            case 'c': return bytes(self).decode('latin-1')
            case 't': return str(self.parts)
            case 'd': return repr(int(self))
            case 'h': return repr(hash(self))
            case 'n': return self.rpartition('.')[0]
            case 'hex'|'bin'|'oct': return __builtins__[s](int(self))
        return str(self)
    def __add__(self, o, /): return __class__(self[:2], self[2]+o) if isinstance(o, int) else __class__(*map(int.__add__, self, o)) if isinstance(o, VersionDelta) else NotImplemented
    def __sub__(self, o, /, f=lambda x, y: max(0, x-y)): return __class__(self[:2], f(self[2], o)) if isinstance(o, int) else T[1-T.index(t)](*map(f, self, o)) if (t := type(o)) in (T := (VersionDelta, __class__)) else NotImplemented
    def next_patch(self): return self.replace_parts(patch=self[2]+1)
    def next_minor(self): return __class__(self[0], self[1]+1)
    def next_major(self): return __class__(self[0]+1)
    def change_sep(self, sep): return self.replace('.', sep)
    def __setattr__(self, name, value, /): raise AttributeError(f'attribute {name!r} cannot be set to {value!r} on {__class__.__name__} object')
    @property
    def is_unstable(self): return self[0] == 0
    def compatible(self, o, /, majtol=0, mintol=None): return majtol is None or (abs(self[0]-o[0]) <= majtol and (mintol is None or abs(self[1]-o[1]) <= mintol))
    representation = property('asyncutils v'.__add__); __int__ = __index__ = lambda self: self[2]|self[1]<<8|self[0]<<16; P.patch_classmethod_signatures((__new__, '/, *args'), (get_current_version, ''), (from_hash, 'hashed, /')); P.patch_method_signatures((__format__, 'format_spec, /'), (__hash__, ''), (__sub__, 'other, /'), (replace_parts, '*, major=None, minor=None, patch=None'))
VersionInfo.__trunc__ = VersionInfo.__floor__ = VersionInfo.major.fget
N, t = {}, lambda o, /: o if isinstance(o, type) else type(o)
@P.patch_properties
class VersionDelta(tuple):
    def __new__(cls, major=0, minor=0, patch=0): return super().__new__(cls, (major, minor, patch))
    def __init_subclass__(cls, /, **_): raise TypeError('cannot subclass VersionDelta')
    def __neg__(self): return __class__(*map(int.__neg__, self))
def normalize_allow_unimplemented(o, /, E=E, p=p, c=lambda o, /, t=(type(p.__get__(True)), type(True.__init__), type(''.lower)), a='__iter__': isinstance(getattr(o, a, None), t), s=frozenset(('inf', '-inf', 'nan')), m=0xFF):
    if isinstance(o, VersionInfo): return o.parts
    if isinstance(o, str): o = o.split('.')
    elif isinstance(o, complex): o = o.real, o.imag, 0
    if isinstance(o, int): o = o>>16, (o>>8)&m, o&m
    elif isinstance(o, float):
        if (o := format(o, '.4f')) in s: return
        o, _ = o.split('.', 1); o = map(int, (o, _[:2], _[2:]))
    elif f := dispatch_normalizer(o, t=type):
        try:
            if (o := f(o)) is None: return
            if not c(o): raise E.VersionNormalizerTypeError(f, o)
        except E.CRITICAL: raise E.Critical
        except BaseException as e: unregister_normalizer(o, t=type); raise E.VersionNormalizerFault(f, o, e)
    elif not c(o): return
    try: return p(o)
    except TypeError, ValueError: return
def normalize(o, /, e=E.VersionNormalizerMissing):
    if (r := normalize_allow_unimplemented(o)) is None: raise e(o)
    return r
def register_normalizer(o, n, /, f=N.setdefault, t=t): return f(t(o), n) is n
def unregister_normalizer(o, /, f=N.pop, t=t): return f(t(o), None)
def dispatch_normalizer(o, /, f=N.get, t=t): return f(t(o))
def autogenerate_normalizers(): return register_normalizer(__import__('decimal').Decimal, lambda d, /: map(int, ((d := format(d, '.4f'))[:-4], d[-4:-2], d[-2:])))&register_normalizer(F := __import__('fractions').Fraction, F.as_integer_ratio)
P.patch_function_signatures((normalize, t := 'o, /'), (normalize_allow_unimplemented, t), (unregister_normalizer, t), (dispatch_normalizer, t), (register_normalizer, 'o, f, /'))
for _ in ('__lt__', '__le__', '__gt__', '__ge__', '__eq__', '__ne__'): setattr(VersionInfo, _, lambda self, other, /, m=getattr(tuple, _): NotImplemented if (other := normalize_allow_unimplemented(other)) is None else m(self.parts, other))
del _, N, t, P, p, E