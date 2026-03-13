'''A versioning scheme for asyncutils. Inspired by torch/torch_version.py, but with quite some differences.'''
from _collections_abc import Callable, Iterator, Iterable
from typing import Any, Self, Literal, NoReturn, final, overload
from ._internal.protocols import IntCompatible
__all__ = 'VersionInfo', 'VersionDelta', 'normalize', 'register_normalizer', 'unregister_normalizer', 'dispatch_normalizer', 'autogenerate_normalizers'
@final
class VersionInfo(str):
    def __new__(cls, /, *a: IntCompatible) -> Self: ...
    def __hash__(self) -> int: '''A perfect hash function for versions! May produce larger integers than __int__ in some cases, and may also produce negative integers.'''
    @classmethod
    def from_hash(cls, hashed: int, /) -> Self: '''Reconstruct the version from its hash.'''
    def __iter__(self) -> Iterator[int]: '''An iterator yielding (major, minor, patch) sequentially.'''
    def __len__(self) -> Literal[3]: '''len((major, minor, patch)) == 3.'''
    def __getitem__(self, idx: int, /) -> int:
        '''idx = 0 -> major
        idx = 1 -> minor
        idx = 2 -> patch'''
    def __lt__(self, other: Any, /) -> bool: ...
    def __le__(self, other: Any, /) -> bool: ...
    def __gt__(self, other: Any, /) -> bool: ...
    def __ge__(self, other: Any, /) -> bool: ...
    def __eq__(self, other: Any, /) -> bool: ...
    def __ne__(self, other: Any, /) -> bool: ...
    def __reduce__(self) -> tuple[type[Self], tuple[int, int, int]]: '''Pickling support.'''
    def __repr__(self) -> str: '''`version == eval(repr(version))` holds.'''
    @overload
    def __add__(self, n: int, /) -> Self: ...
    @overload
    def __add__(self, delta: VersionDelta, /) -> Self: '''Return this version incremented by `n` patches or `delta`.'''
    @overload
    def __sub__(self, n: int, /) -> Self: ...
    @overload
    def __sub__(self, delta: VersionDelta, /) -> Self: ...
    @overload
    def __sub__(self, other: Self, /) -> VersionDelta: ''''Return this version decremented by `n` patches or `delta`, or the delta between `self` and `other`.'''
    def __setattr__(self, name: str, /) -> NoReturn: ...
    def __format__(self, format_spec: Literal['', 'x', 'b', 'o', 'd', '0', '1', '2', 'major', 'minor', 'patch', 'short', 'long', 'chars', 'dec', 'hex', 'bin', 'oct', 'tuple'], /) -> str:
        """Format specification and corresponding return value: (using 123.4.0 as example)
        x, hex: `'0x7b0400'`
        o, oct: `'0o36602000'`
        b, bin: `'0b11110110000010000000000'`
        d, dec: `'8061952'`
        0, major: `'123'`
        1, minor: `'4'`
        2, patch: `'0'`
        short: `'123.4'`
        long: `'asyncutils version 123.4.0'`
        chars: `'{\x04\x00'`
        tuple: `'(123, 4, 0)'`
        <anything else>: `'123.4.0'`"""
    def __int__(self) -> int: '''Assumes minor and patch are less than 256.'''
    def __floor__(self) -> int: '''Returns the major version.'''
    def __ceil__(self) -> int: '''Returns the major version, adding one if there is a minor or patch version.'''
    def __bytes__(self) -> bytes: '''Assumes major, minor, and patch are all less than 256.'''
    def __float__(self) -> float: '''Assumes minor and patch are less than 100.'''
    def __complex__(self) -> complex: '''Loses the patch version.'''
    def replace_parts(self, *, major: int=..., minor: int=..., patch: int=...) -> Self: '''Another instance of this class with the specified parts.'''
    def change_sep(self, sep: str) -> str: '''This version as a string with the specified separator instead of a dot between parts.'''
    def compatible(self, other: Self, /, majtol: int|None=..., mintol: int|None=...) -> bool: '''Whether this version is compatible with the other, given the major and minor tolerances.'''
    def next_patch(self) -> Self: '''The patch version following this version.'''
    def next_minor(self) -> Self: '''The minor version following this version, with a patch of 0.'''
    def next_major(self) -> Self: '''The major version following this version, with a minor and patch of 0.'''
    @classmethod
    def get_current_version(cls) -> Self: '''Return the current version number of asyncutils; equivalent to asyncutils.__version__.'''
    @classmethod
    def to_version(cls, o: Any, /) -> Self: '''Builds an instance from any normalizable object; throws an exception if not possible.'''
    @property
    def is_valid(self) -> Literal[True]: '''If this returns False, the user must have messed something up intentionally.'''
    @property
    def representation(self) -> str:
        """>>> print(VersionInfo(4, 2).representation)
        asyncutils v4.2.0"""
    @property
    def is_unstable(self) -> Literal[False]: '''True only in development, so should be considered always False.'''
    @property
    def parts(self) -> tuple[int, int, int]: '''The tuple (major, minor, patch).'''
    @property
    def major(self) -> int: '''The major part of the version.'''
    @property
    def minor(self) -> int: '''The minor part of the version.'''
    @property
    def patch(self) -> int: '''The patch part of the version.'''
    __index__, __trunc__ = __int__, __floor__
class VersionDelta(tuple[int, int, int]):
    '''A named tuple representing the difference between versions. Can be taken by the + or - operators.'''
    def __new__(cls, major: int=..., minor: int=..., patch: int=...) -> Self: ...
    @property
    def major(self) -> int: ...
    @property
    def minor(self) -> int: ...
    @property
    def patch(self) -> int: ...
    def __neg__(self) -> Self: ...
def normalize(o: Any, /) -> tuple[int, int, int]|None:
    '''Returns a tuple of three integers: major, minor, patch, from the information provided by the object, to be extracted by registered normalizers.
    Normalization is hardcoded for str, complex, int, float. For iterables, the default is to take the first three items and pad zeros behind if necessary.
    Register normalizers using register_normalizer, which returns False if there is already a normalizer registered.
    Unregister normalizers using unregister_normalizer, which returns the previous normalizer (if any) and None otherwise.
    Get the normalizer to be used to normalize an object using dispatch_normalizer.
    A normalizer can return None for unnormalizable objects, in which case the comparison operators against instances of VersionInfo will delegate to that object.
    If there is fault in the normalizer (it raises an exception or returns a non-iterable), the normalizer is removed and the error propagated.
    Returns None if a normalizer is not found.
    >>> normalize('1.2.3')
    (1, 2, 3)
    >>> normalize(19.0203)
    (19, 2, 3)
    >>> normalize(0x10F0203)
    (271, 2, 3)
    >>> normalize((1, 3, 5, 7))
    (1, 3, 5)
    >>> normalize(1.2+2.3j)
    (1, 2, 0)
    >>> autogenerate_normalizers()
    True
    >>> normalize(Decimal('1.2345'))
    (1, 23, 45)
    >>> normalize(Fraction(1, 3))
    (1, 3, 0)'''
@overload
def register_normalizer[T](o: T, f: Callable[[T], Iterable[int]], /) -> bool: ...
@overload
def register_normalizer[T](o: type[T], f: Callable[[T], Iterable[int]], /) -> bool: '''Registers a custom normalizer for the object or type; returns success, with failure resulting from a normalizer having already been registered.'''
@overload
def unregister_normalizer[T](o: T, /) -> Callable[[T], Iterable[int]]|None: ...
@overload
def unregister_normalizer[T](o: type[T], /) -> Callable[[T], Iterable[int]]|None: '''Unregister the normalizer for the object or type and return it if any.'''
@overload
def dispatch_normalizer[T](o: T, /) -> Callable[[T], Iterable[int]]|None: ...
@overload
def dispatch_normalizer[T](o: type[T], /) -> Callable[[T], Iterable[int]]|None: '''Return the normalizer to be used for the object or type.'''
def autogenerate_normalizers() -> bool: '''Registers normalizers for decimal.Decimal and fractions.Fraction. Returns if both normalizers were successfully registered (including re-registration of the same normalizer).'''