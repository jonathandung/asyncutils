from asyncutils.properties import *
class TestProp:
    __slots__ = '_prop',
    @AsyncProperty
    async def prop(self):
        '''docstring'''
        return self._prop
    @prop.setter
    async def prop(self, value): self._prop = value
    @prop.deleter
    async def prop(self): del self._prop
    def test_prop(self, prop=prop):
        assert prop.__doc__ == 'docstring'
        assert prop._name == 'prop'
        assert prop._cls is __class__
        self.prop = 42
        assert self.prop == 42
        del self.prop
        assert not hasattr(self, '_prop')