from pytest import mark
from asyncutils.channels import *
from asyncio import gather
@mark.asyncio
async def test_rdv():
    rdv = Rendezvous[int]()
    for i, j in enumerate((await gather(*map(rdv.put, range(10, 20)), rdv.exchange(20), *map(rdv.exchange, range(1, 10)), *(rdv.get() for _ in range(10))))[10:], 1): assert i == j