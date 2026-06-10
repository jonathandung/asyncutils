from asyncutils.properties import *
from asyncutils.rwlocks import CoercedMethod, FairRWLock
from pytest import raises
from tests.conftest import mk
class TestProp:
    __slots__ = '_cprop', '_lprop', '_rprop'
    meth = CoercedMethod(id)
    @LazyAsyncProperty
    async def lprop(self):
        '''docstring'''
        return self._lprop
    @lprop.setter
    async def lprop(self, value): self._lprop = value
    @lprop.deleter
    async def lprop(self): del self._lprop
    @ConcurrentAsyncProperty(strict=False)
    async def cprop(self):
        '''docstring 2'''
        return self._cprop
    @cprop.setter
    async def cprop(self, value): self._cprop = value
    @cprop.deleter
    async def cprop(self): del self._cprop
    @RWLockedAsyncProperty(policy=FairRWLock, hide=True)
    async def rprop(self): return self._rprop
    @rprop.setter
    async def rprop(self, value): self._rprop = value
    @rprop.deleter
    async def rprop(self): del self._rprop
    @mk
    async def test_lprop(self):
        self.lprop = 42
        assert await self.lprop == 42
        del self.lprop
        with raises(AttributeError): await self.lprop
        assert not hasattr(self, '_lprop')
    @mk
    async def test_cprop(self):
        self.cprop = 41
        assert await self.cprop == 41
        del self.cprop
        with raises(AttributeError): await self.cprop
        assert not hasattr(self, '_cprop')
    @mk
    async def test_rprop(self):
        self.rprop = 40
        assert await self.rprop == 40
        del self.rprop
        with raises(AttributeError): await self.rprop
        assert not hasattr(self, '_rprop')
def test_outer():
    with raises(AttributeError): TestProp.rprop
    assert type(TestProp.lprop) is LazyAsyncProperty
    assert isinstance(TestProp.cprop, AsyncPropertyBase)
    assert TestProp.lprop.__doc__ == 'docstring'
    assert TestProp.cprop.__doc__ == 'docstring 2'
