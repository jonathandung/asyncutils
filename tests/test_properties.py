from asyncutils.properties import *
from asyncutils.rwlocks import CoercedMethod, FairRWLock
from pytest import raises
from tests.conftest import mk
class TestProp:
    __slots__ = '_cp', '_lp', '_rp'
    meth = CoercedMethod(id)
    @LazyAsyncProperty
    async def lp(self):
        '''Docstring.'''
        return self._lp
    @lp.setter
    async def lp(self, value): self._lp = value
    @lp.deleter
    async def lp(self): del self._lp
    @ConcurrentAsyncProperty
    async def cp(self):
        '''Docstring 2.'''
        return self._cp
    @cp.setter
    async def cp(self, value): self._cp = value
    @cp.deleter
    async def cp(self): del self._cp
    @RWLockedAsyncProperty(policy=FairRWLock, hide=True)
    async def rp(self): return self._rp
    @rp.setter
    async def rp(self, value): self._rp = value
    @rp.deleter
    async def rp(self): del self._rp
    @mk
    async def test_lp(self):
        self.lp = 42
        assert await self.lp == 42
        del self.lp
        with raises(AttributeError): await self.lp
        assert not hasattr(self, '_lp')
    @mk
    async def test_cp(self):
        self.cp = 41
        assert await self.cp == 41
        del self.cp
        with raises(AttributeError): await self.cp
        assert not hasattr(self, '_cp')
    @mk
    async def test_rp(self):
        self.rp = 40
        assert await self.rp == 40
        del self.rp
        with raises(AttributeError): await self.rp
        assert not hasattr(self, '_rp')
    def test_meth(self): assert self.meth() == id(self)
@mk
async def test_outer():
    with raises(AttributeError): await TestProp.rp
    with raises(AttributeError): TestProp.meth
    assert type(await TestProp.lp) is LazyAsyncProperty
    assert isinstance(await TestProp.cp, AsyncPropertyBase)
    assert (await TestProp.lp).__doc__ == 'Docstring.'
    assert (await TestProp.cp).__doc__ == 'Docstring 2.'
