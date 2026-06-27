import asyncutils as au
def test_mod():
    assert isinstance(au.__getattr__, type)
    assert isinstance(au.submodules_map, dict)
    assert au.preloaded_submodules.issuperset(('constants', 'context', 'cli', 'exceptions', 'version'))
    assert au.console_preloaded_submodules.issuperset(au.preloaded_submodules)
    assert au.time_since_boot() > 0
    assert au.VersionInfo(au.__hexversion__) == au.__version__
