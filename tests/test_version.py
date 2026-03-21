from pytest import raises, fixture
from asyncutils.exceptions import VersionValueError
from asyncutils.version import *
@fixture(scope='session')
def ver(): from asyncutils.config import _randinst as _; return VersionInfo(*map(_.randrange, (10, 20)), _.randint(256, 300))
def test_hash(ver):
    assert (h := hash(ver)) != -1 and VersionInfo.from_hash(h) == ver
    with raises(VersionValueError): VersionInfo.from_hash(-1)
    assert hash(VersionInfo(42, 0xdead, 0xbeef)) == -0x4945ce289172b3b6
def test_ver(ver):
    ver.assert_valid()
    assert type(ver) is VersionInfo
    assert ver.__floor__() == ver.__trunc__() == ver.major == ver[0] == ver.__ceil__()-1
    with raises(AttributeError, match=r"attribute 'parts' cannot be set to \(0, 0, 0\) on VersionInfo object"): ver.parts = 0, 0, 0
    with raises(OverflowError, match=r'cannot pack version \d+\.\d+\.\d+ into an integer'): int(ver)
    assert ((ver := VersionInfo(float(round(ver, 2))))+3).patch == len(ver) == 3
    import pickle
    assert eval(repr(ver)) == VersionInfo(ver) == round(ver, None) == round(ver, 3) == pickle.loads(pickle.dumps(ver)) == VersionInfo(ver.change_sep('-').split('-', 2)) == VersionInfo(ver.to_complex()) == ver.replace_parts() == ver
def test_fmt(ver):
    assert (_ := str(ver)) == f'{ver:0}.{ver:1}.{ver:2}' == f'{ver:maj}.{ver:min}.{ver:patch}' == ver.representation.removeprefix('asyncutils v')
    assert ver == VersionInfo(_)
    assert not (ver := ver.next_major()).is_unstable
    assert ver[0] == (ver := ver.next_minor())[0]
    assert (ver[0], ver[1]) == (ver := ver.next_patch())[:2]
    assert hex(int(_ := f'{ver:x}', 0)) == _ == f'{ver:hex}'
    assert oct(int(_ := f'{ver:o}', 0)) == _ == f'{ver:oct}'
    assert bin(int(_ := f'{ver:b}', 0)) == _ == f'{ver:bin}'
    assert repr(int(_ := f'{ver:d}')) == _ == f'{ver:dec}'
    assert eval(f'{ver:t}') == ver.parts
def test_cls():
    assert issubclass(VersionInfo, str)
    with raises(TypeError): type('', (VersionInfo,), {})
    from asyncutils import __version__
    assert __version__ is VersionInfo.get_current_version()