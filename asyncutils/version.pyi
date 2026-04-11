'''A versioning scheme for `asyncutils`. Inspired by `torch/torch_version.py`, but with quite some differences.
`asyncutils` [uses a subset of SemVer](https://github.com/jonathandung/asyncutils/blob/main/CONTRIBUTING.md), with two additional restrictions:
- **MINOR VERSIONS CANNOT SPAN MORE THAN 256 PATCHES.**
- **MAJOR VERSIONS CANNOT SPAN MORE THAN 256 MINORS.**'''
from ._internal.protocols import IntCompatible, Openable, ValidSlice
from _collections_abc import Callable, Iterable, Iterator
from typing import Any, Literal, NamedTuple, NoReturn, Self, final, overload
__all__ = 'VersionDelta', 'VersionInfo', 'autogenerate_normalizers', 'dispatch_normalizer', 'normalize', 'normalize_allow_unimplemented', 'register_normalizer', 'unregister_normalizer'
@final
class VersionInfo(str): # noqa: FURB189
    @overload
    def __new__(cls, from_: object, /) -> Self: ...
    @overload
    def __new__(cls, /, *parts: IntCompatible) -> Self: '''Constructor. With one argument, attempts to normalize it and return the corresponding instance. Otherwise, treats the arguments as (major, minor, patch), zero-padding if required. Throws an appropriate exception if not possible.'''
    def __hash__(self) -> int:
        '''A perfect hash function for versions! May produce larger integers than __int__ in some cases, and may also produce negative integers.
        Of course, since `builtins.hash` stupidly returns the output of `__hash__` modulo 2^61-1 (largest Mersenne prime within 64 bits), the
        reasonable limit for versions that can be hashed and unhashed losslessly lies around version `46340.41707.2147483645`.'''
    @classmethod
    def from_hash(cls, hashed: int, /) -> Self: '''Reconstruct the version from its hash.'''
    def __iter__(self) -> Iterator[int]: '''An iterator yielding `major`, `minor`, `patch` sequentially.''' # type: ignore[override]
    def __len__(self) -> Literal[3]: '''`len((major, minor, patch)) == 3`.'''
    @overload # type: ignore[override]
    def __getitem__(self, idx: Literal[0, 1, 2], /) -> int: # type: ignore[overload-overlap]
        '''Depending on the value of `idx`, corresponds to the following attributes:
        0 -> `major`
        1 -> `minor`
        2 -> `patch`'''
    @overload
    def __getitem__(self, idx: ValidSlice, /) -> tuple[int, ...]: ...
    @overload
    def __getitem__(self, idx: int, /) -> NoReturn: ...
    def __lt__(self, other: Any, /) -> bool: '''Whether self precedes the other as a version.'''
    def __le__(self, other: Any, /) -> bool: '''Whether self precedes or is equal to the other as a version.'''
    def __gt__(self, other: Any, /) -> bool: '''Whether self succeeds the other as a version.'''
    def __ge__(self, other: Any, /) -> bool: '''Whether self succeeds or is equal to the other as a version.'''
    def __eq__(self, other: Any, /) -> bool: '''Whether self is the same version as the other.'''
    def __ne__(self, other: Any, /) -> bool: '''Whether self is a different version than the other.'''
    def __reduce__(self) -> tuple[type[Self], tuple[int, int, int]]: '''Support for pickling.'''
    @overload
    def __round__(self, ndigits: int, /) -> NoReturn: ...
    @overload
    def __round__(self, ndigits: Literal[1, 2, 3]|None, /) -> Self: '''Support for rounding.'''
    @overload # type: ignore[override]
    def __add__(self, n: int, /) -> Self: ...
    @overload
    def __add__(self, delta: VersionDelta, /) -> Self: '''Return this version incremented by `n` patches or `delta`.'''
    @overload
    def __sub__(self, n: int, /) -> Self: ...
    @overload
    def __sub__(self, delta: VersionDelta, /) -> Self: ...
    @overload
    def __sub__(self, other: Self, /) -> VersionDelta: ''''Return this version decremented by `n` patches or `delta`, or the delta between `self` and `other`.'''
    def __setattr__(self, name: str, /) -> NoReturn: '''Disallow modifying attributes of the object.''' # type: ignore[misc,override]
    def __format__(self, format_spec: str, /) -> str:
        """Format specification and corresponding return value: (using 123.4.0 as example)
        x, hex: `'0x7b0400'`
        o, oct: `'0o36602000'`
        b, bin: `'0b11110110000010000000000'`
        d, dec: `'8061952'`
        0, major, maj: `'123'`
        1, minor, min: `'4'`
        2, patch: `'0'`
        s, short: `'123.4'`
        l, long: `'asyncutils version 123.4.0'`
        c, chars: `'{\\x04\\x00'`
        t, tuple: `'(123, 4, 0)'`
        h, hash: `'116380397'`
        n, majmin: `'123.4'`
        <anything else>: `'123.4.0'`"""
    def __int__(self) -> int: '''Assumes minor and patch are less than 256.'''
    def __floor__(self) -> int: '''Returns the major version.'''
    def __ceil__(self) -> int: '''Returns the major version, adding one if there is a minor or patch version.'''
    def __float__(self) -> float: '''Assumes minor and patch are less than 100.'''
    def to_complex(self) -> complex: '''Loses the patch version. Since this class is a `str` subclass, an implementation of `__complex__` will not be recognized.'''
    def replace_parts(self, *, major: int=..., minor: int=..., patch: int=...) -> Self: '''Another instance of this class with the specified parts.'''
    def change_sep(self, sep: str) -> str: '''This version as a string with the specified separator instead of a dot between parts.'''
    def compatible(self, other: Self, /, majtol: int|None=..., mintol: int|None=...) -> bool: '''Whether this version is compatible with the other, given the major and minor tolerances.'''
    def next_patch(self) -> Self: '''The patch version following this version.'''
    def next_minor(self) -> Self: '''The minor version following this version, with a patch of 0.'''
    def next_major(self) -> Self: '''The major version following this version, with a minor and patch of 0.'''
    def shelve(self, path: Openable, little: bool=...) -> None: '''Store this version into the specified `path`.'''
    @classmethod
    def unshelve(cls, path: Openable, little: bool=...) -> Self: '''Recover a stored version.'''
    @classmethod
    def get_current_version(cls) -> Self: '''Return the current version number of asyncutils; equivalent to asyncutils.__version__.'''
    def assert_valid(self) -> None: '''Signify an error if the user messed something up in this object, likely intentionally.'''
    @property
    def representation(self) -> str:
        '''```python
        >>> print(VersionInfo(4, 2).representation)
        asyncutils v4.2.0
        ```'''
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
    __index__, __trunc__, __radd__ = __int__, __floor__, __add__ # noqa: PYI017
class VersionDelta(NamedTuple):
    '''A named tuple representing the difference between versions. Can be taken by the + or - operators.'''
    major: int = ...
    '''The major part of the version.'''
    minor: int = ...
    '''The minor part of the version.'''
    patch: int = ...
    '''The patch part of the version.'''
    def __neg__(self) -> Self: '''Return the negative of the delta. Additions and subtractions taking the return value correspond to subtractions and additions taking the original delta respectively.'''
def normalize(o: object, /) -> tuple[int, int, int]:
    '''Returns a tuple of three integers: major, minor, patch, from the information provided by the object, to be extracted by registered normalizers.
    Normalization is hardcoded for str, complex, int, float. For iterables, the default is to take the first three items and pad zeros behind if necessary.
    Register normalizers using register_normalizer, which returns False if there is already a normalizer registered.
    Unregister normalizers using unregister_normalizer, which returns the previous normalizer (if any) and None otherwise.
    Get the normalizer to be used to normalize an object using dispatch_normalizer.
    A normalizer can return None for unnormalizable objects, in which case the comparison operators against instances of VersionInfo will delegate to that object.
    If there is fault in the normalizer (it raises an exception or returns a non-iterable), the normalizer is removed and the error propagated.
    >>> normalize('1.2.3')
    (1, 2, 3)
    >>> normalize(19.0203)
    (19, 2, 3)
    >>> normalize(0x10F0203)
    (271, 2, 3)
    >>> normalize((1, 3, 5, 7))
    (1, 3, 5)
    >>> normalize(1.2+3.4j)
    (1, 3, 0)
    >>> autogenerate_normalizers()
    True
    >>> normalize(Decimal('1.2345'))
    (1, 23, 45)
    >>> normalize(Fraction(1, 3))
    (1, 3, 0)'''
def normalize_allow_unimplemented(o: object, /) -> tuple[int, int, int]|None: '''Same as `normalize`, but return None if a normalizer is not found.'''
@overload
def register_normalizer[T](o: type[T], f: Callable[[T], Iterable[int]], /) -> bool: '''Registers a custom normalizer for the object or type; returns success, with failure resulting from a normalizer having already been registered.'''
@overload
def register_normalizer[T](o: T, f: Callable[[T], Iterable[int]], /) -> bool: ...
@overload
def unregister_normalizer[T](o: type[T], /) -> Callable[[T], Iterable[int]]|None: '''Unregister the normalizer for the object or type and return it if any.'''
@overload
def unregister_normalizer[T](o: T, /) -> Callable[[T], Iterable[int]]|None: ...
@overload
def dispatch_normalizer[T](o: type[T], /) -> Callable[[T], Iterable[int]]|None: '''Return the normalizer to be used for the object or type.'''
@overload
def dispatch_normalizer[T](o: T, /) -> Callable[[T], Iterable[int]]|None: ...
def autogenerate_normalizers() -> bool: '''Registers normalizers for decimal.Decimal and fractions.Fraction. Returns if both normalizers were successfully registered (including re-registration of the same normalizer).'''