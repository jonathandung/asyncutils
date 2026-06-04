from asyncutils.properties import *
from asyncutils.rwlocks import RWLock
from pytest import raises
from tests.conftest import mk
class TestProp:
    __slots__ = '__weakref__', '_lprop', '_prop'
    @LazyAsyncProperty
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
    @ConcurrentAsyncProperty(strict=False)
    async def lprop(self):
        '''docstring 2'''
        return self._lprop
    @lprop.setter
    async def lprop(self, value): self._lprop = value
    @lprop.deleter
    async def lprop(self): del self._lprop
    @mk
    async def test_prop(self):
        assert __class__.prop.__wrapped__.__doc__ == 'docstring'
        self.prop = 42
        assert await self.prop == 42
        del self.prop
        with raises(AttributeError): await self.prop
        assert not hasattr(self, '_prop')
    @mk
    async def test_lprop(self):
        assert __class__.lprop.__doc__ == 'docstring 2'
        self.lprop = 42
        assert await self.lprop == 42
        del self.lprop
        with raises(AttributeError): await self.lprop
        assert not hasattr(self, '_lprop')
