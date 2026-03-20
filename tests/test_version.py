from pytest import raises, fixture
from asyncutils.exceptions import VersionValueError
from asyncutils.version import *
from re import escape
@fixture(scope='session')
def version(): from asyncutils.config import _randinst as _; return VersionInfo(*map(_.randrange, (10, 20)), _.randint(1, 100))
def test_hash(version):
    assert (h := hash(version)) != -1 and VersionInfo.from_hash(h) == version
    with raises(VersionValueError): VersionInfo.from_hash(-1)
    assert hash(VersionInfo(42, 0xdead, 0xbeef)) == -0x4945ce289172b3b6
def test_version(version):
    version.assert_valid()
    assert version.__floor__() == version.__trunc__() == version.major == version[0] == version.__ceil__()-1
    assert eval(repr(version)) == VersionInfo(version) == round(version, None) == round(version, 3) == version
    with raises(AttributeError, match=escape("attribute 'parts' cannot be set to (0, 0, 0) on VersionInfo object")): version.parts = (0, 0, 0)
def test_format(version):
    assert (_ := str(version)) == f'{version:0}.{version:1}.{version:2}' == f'{version:major}.{version:minor}.{version:patch}' == version.representation.removeprefix('asyncutils v')
    assert version == VersionInfo(_)
    assert hex(int(_ := f'{version:x}', 0)) == _ == f'{version:hex}'
    assert oct(int(_ := f'{version:o}', 0)) == _ == f'{version:oct}'
    assert bin(int(_ := f'{version:b}', 0)) == _ == f'{version:bin}'
    assert repr(int(_ := f'{version:d}')) == _ == f'{version:dec}'
    assert eval(f'{version:t}') == version.parts
def test_class():
    assert issubclass(VersionInfo, str)
    with raises(TypeError): type('', (VersionInfo,), {})