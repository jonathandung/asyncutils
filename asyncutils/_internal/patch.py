def patch_asyncio_warnings(): __import__('logging').getLogger('asyncio').disabled = True
def patch_unawaited_coroutine_warnings(): __import__('warnings').filterwarnings('ignore', "coroutine '.*' was never awaited", RuntimeWarning)
def _(t, d, a='__text_signature__', u='<unrepresentable>', c=('__wrapped__', '__func__')):
    def patch(*I):
        m, f = {}, True
        for k, v in I:
            while (i := id(k)) not in m: m[i], k, f = k, getattr(k, c[f], k), not f # noqa: PLW2901
            setattr(k, a, t%v.format(u) if v else d)
    return patch
patch_function_signatures, patch_method_signatures, patch_classmethod_signatures = map(_, ('(%s)', '($self, %s)', '($cls, %s)'), ('()', '($self)', '($cls)'))
xsig = 'exc_typ, exc_val, exc_tb, /'
del _