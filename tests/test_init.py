import asyncutils
def test_mod():
    assert isinstance(asyncutils.__getattr__, type)
    assert asyncutils.__all__ is asyncutils.__dir__()
    assert isinstance(asyncutils.submodules_map, dict)
    assert asyncutils.preloaded_submodules.issuperset(('config', 'exceptions', 'version'))
    assert asyncutils.VersionInfo(asyncutils.__hexversion__) == asyncutils.__version__