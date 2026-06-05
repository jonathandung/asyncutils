import asyncutils
def test_mod():
    assert isinstance(asyncutils.__getattr__, type)
    assert isinstance(asyncutils.submodules_map, dict)
    assert asyncutils.preloaded_submodules.issuperset(('constants', 'context', 'cli', 'exceptions', 'version'))
    assert asyncutils.console_preloaded_submodules.issuperset(asyncutils.preloaded_submodules)
    assert asyncutils.time_since_boot() > 0
    assert asyncutils.VersionInfo(asyncutils.__hexversion__) == asyncutils.__version__
