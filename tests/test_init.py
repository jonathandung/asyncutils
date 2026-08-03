import asyncutils as au
def test_mod():
    assert au.preloaded_submodules.issuperset(('constants', 'context', 'cli', 'exceptions', 'version'))
    assert au.console_preloaded_submodules.issuperset(au.preloaded_submodules)
    assert au.time_since_boot() > 0
    assert au.VersionInfo(au.__hexversion__) == au.__version__
    for v in au.submodules_map.values(): getattr(v, v.__all__[0])
