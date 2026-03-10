from ._internal import patch as P
from ._internal.submodules import version_all as __all__
from . import exceptions as E
def p(I, /, f=0 .__gt__, e=E.VersionValueError):
    r = []
    for i, j in enumerate(I):
        r.append(int(j, 0) if isinstance(j, str) else int(j))
        if i == 2: break
    else: r.extend(0 for _ in range(2-i))
    if any(map(f, r)): raise e('major, minor and patch should all be positive')
    return tuple(r)
s = 'major', 'minor', 'patch'
class VersionInfo(str):
    __slots__ = 'parts'
    def __new__(cls, /, *a, p=p): object.__setattr__(s := super().__new__(cls, '.'.join(map(str, a))), 'parts', p(a)); return s
    def __init_subclass__(cls, /, **_): raise TypeError('cannot subclass VersionInfo')
    def __hash__(self): return hash(self.parts)
    def __repr__(self): return f'VersionInfo{self.parts}'
    def __ceil__(self): return self[0]+any(self[1:])
    def __len__(self): return 3
    def __bytes__(self): return bytes(self.parts)
    def __complex__(self): return complex(*self[:2])
    def __float__(self, r=.01): return sum((j*r**i for i, j in enumerate(self)), start=.0)
    def __reduce__(self): return __class__, self.parts
    def __iter__(self): return self.parts.__iter__()
    def __getitem__(self, i, /): return tuple.__getitem__(self.parts, i)
    @property
    def is_valid(self):
        try: return isinstance(p := self.parts, tuple) and len(p) == 3 and all(isinstance(i, int) and i == j > 0 for i, j in zip(map(int, self.split('.')), p, strict=True))
        except ValueError, TypeError, AttributeError: return False
    def replace_parts(self, *, _=s, **k): return __class__(*(getattr(self, _) if (v := k.pop(_, None)) is None else v for _ in _))
    @classmethod
    def get_current_version(cls, E=E):
        from . import __version__ as V
        if isinstance(V, cls):
            if V.is_valid: return V
            raise E.VersionCorrupted(V)
        raise E.StateCorrupted('module-internal', '__version__ is inconsistent with expectations')
    @classmethod
    def to_version(cls, o, /): return cls(*normalize(o))
    def __format__(self, s, /, a={'x': 'hex', 'b': 'bin', 'o': 'oct', 'd': 'dec', '0': 'major', '1': 'minor', '2': 'patch'}.get):
        match a(s := s.lower(), s):
            case 'major'|'minor'|'patch': return str(getattr(self, s))
            case 'short': return '.'.join(map(str, self[:2+bool(self[2])]))
            case 'long': return f'asyncutils version {self}'
            case 'chars': return bytes(self).decode('ascii')
            case 'dec': return repr(int(self))
            case 'hex'|'bin'|'oct': return __builtins__[s](int(self))
            case 'tuple': return str(self.parts)
        return str(self)
    def __add__(self, o, /): return __class__(self[:2], self[2]+o) if isinstance(o, int) else __class__(*map(int.__add__, self, o)) if isinstance(o, VersionDelta) else NotImplemented
    def __sub__(self, o, /, f=lambda x, y: max(0, x-y)): return __class__(self[:2], f(self[2], o)) if isinstance(o, int) else T[1-T.index(t)](*map(f, self, o)) if (t := type(o)) in (T := (VersionDelta, __class__)) else NotImplemented
    def next_patch(self): return self.replace_parts(patch=self[2]+1)
    def next_minor(self): return __class__(self[0], self[1]+1)
    def next_major(self): return __class__(self[0]+1)
    def change_sep(self, sep): return self.replace('.', sep)
    @property
    def is_unstable(self): return self[0] == 0
    def compatible(self, o, /, majtol=0, mintol=None): return majtol is None or (abs(self[0]-o[0]) <= majtol and (mintol is None or abs(self[1]-o[1]) <= mintol))
    representation = property('asyncutils v'.__add__); major, minor, patch = map(property, map(__import__('_operator').itemgetter, range(3))); __int__ = __index__ = lambda self: self[2]|self[1]<<8|self[0]<<16; __trunc__ = __floor__ = major.fget; P.patch_classmethod_signatures((__new__, '/, *a'))
VersionDelta, N, t = __import__('collections').namedtuple('VersionDelta', s, module='asyncutils.version', defaults=(0,)*3), {}, lambda o, /: o if isinstance(o, type) else type(o)
def normalize(o, /, E=E, p=p, c=lambda o, /, t=(type(p.__get__(True)), type(True.__init__), type(''.lower)), a='__iter__': isinstance(getattr(o, a, None), t), s=frozenset(('inf', '-inf', 'nan')), m=-0x10000, n=0xFF00, l=0xFF):
    if isinstance(o, VersionInfo): return o.parts
    if isinstance(o, str): o = o.split('.')
    elif isinstance(o, complex): o = o.real, o.imag, 0
    if isinstance(o, int): o = o&m, o&n, o&l
    elif isinstance(o, float):
        if (o := format(o, '.4f')) in s: return
        o = map(int, (o[:-4], o[-4:-2], o[-2:]))
    elif f := dispatch_normalizer(o, t=type):
        try:
            if (o := f(o)) is None: return
            if not c(o): raise E.VersionNormalizerTypeError(f, o)
        except E.CRITICAL: raise E.Critical
        except BaseException as e: unregister_normalizer(o, t=type); raise E.VersionNormalizerFault(f, o, e)
    elif not c(o): return
    try: return p(o)
    except TypeError, ValueError: return
def register_normalizer(o, n, /, f=N.setdefault, t=t): return f(t(o), n) is n
def unregister_normalizer(o, /, f=N.pop, t=t): return f(t(o), None)
def dispatch_normalizer(o, /, f=N.get, t=t): return f(t(o))
def autogenerate_normalizers(): return register_normalizer(__import__('decimal').Decimal, lambda d, /: map(int, ((d := format(d, '.4f'))[:-4], d[-4:-2], d[-2:])))&register_normalizer(F := __import__('fractions').Fraction, F.as_integer_ratio)
P.patch_function_signatures((normalize, t := 'o, /'), (unregister_normalizer, t), (dispatch_normalizer, t), (register_normalizer, 'o, f, /'))
for _ in ('__lt__', '__le__', '__gt__', '__ge__', '__eq__', '__ne__'): setattr(VersionInfo, _, lambda self, other, /, m=getattr(tuple, _): m(self.parts, other) if (other := normalize(other)) else NotImplemented)
del _, N, t, P, p, s, E