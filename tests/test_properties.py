from asyncutils.properties import *
from asyncutils.rwlocks import RWLock
from pytest import raises
class TestProp:
    __slots__ = '__weakref__', '_lprop', '_prop'
    @AsyncProperty
    @RWLock.lock
    async def prop(self):
        '''docstring'''
        return self._prop
    @prop.setter
    @prop.writer
    async def prop(self, value): self._prop = value
    @prop.deleter
    @prop.writer
    async def prop(self): del self._prop
    @AsyncLockProperty(strict=False)
    async def lprop(self):
        '''docstring 2'''
        return self._lprop
    @lprop.setter
    async def lprop(self, value): self._lprop = value
    @lprop.deleter
    async def lprop(self): del self._lprop
    def test_prop(self, prop=prop):
        assert prop.__wrapped__.__doc__ == 'docstring'
        self.prop = 42
        assert self.prop == 42
        del self.prop
        assert not hasattr(self, '_prop')
    def test_lprop(self, lprop=lprop):
        assert lprop.__doc__ == 'docstring 2'
        self.lprop = 42
        assert self.lprop == 42
        del self.lprop
        assert not hasattr(self, '_lprop')
    def test_cls(self, prop=prop, lprop=lprop):
        t = type(self)
        assert t.prop is prop and t.lprop is lprop