__all__ = 'patch_asyncio_warnings', 'patch_unawaited_coroutine_warnings', 'patch_function_signatures', 'patch_method_signatures', 'patch_classmethod_signatures'
def patch_asyncio_warnings(): __import__('logging').getLogger('asyncio').disabled = True
def patch_unawaited_coroutine_warnings(): __import__('warnings').filterwarnings('ignore', "coroutine '.*' was never awaited", RuntimeWarning)
def patch_properties(c, /, t=tuple(map(property, map(__import__('_operator').itemgetter, range(3))))): c.major, c.minor, c.patch = t; return c
def _(t, d, a='__text_signature__', u='<unrepresentable>', w='__wrapped__', f='__func__'):
    def patch(*I):
        for k, v in I: setattr(getattr(k := getattr(k, f, k), w, k), a, t%v.format(u) if v else d)
    return patch
patch_function_signatures, patch_method_signatures, patch_classmethod_signatures = map(_, ('(%s)', '($self, %s)', '($cls, %s)'), ('()', '($self)', '($cls)'))
del _