from asyncutils.func import *
from asyncutils.config import _randinst
async def test_areduce():
    assert await areduce(int.__add__, range(10), await_=False) == 45
    assert await areduce(max, l := _randinst.choices(range(100), k=30), await_=False) == max(l)
    assert await areduce(lambda *_: True, (), None) is None # type: ignore