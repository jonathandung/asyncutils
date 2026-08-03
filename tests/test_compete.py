# ty: ignore[no-matching-overload]
from asyncio import sleep, timeout
from asyncutils.compete import *
from asyncutils import arange, agives, done_evt, done_fut
from tests.conftest import mk
import pytest
@mk
async def test_coro_it_conv():
    for i, j in zip(convert_to_coro_iter([arange(2), sleep(0, 2), {3}, done_fut(4)], skip_invalid=False), ([0, 1], 2, [3], 4), strict=True): assert await i == j
@mk
async def test_enhanced_gather(): assert await enhanced_gather((range(3), 42, agives(3), None, done_evt().wait())) == [[0, 1, 2], [3], True]
@mk
async def test_first_completed():
    with pytest.raises(TypeError, match=r'asyncutils\.compete\.first_completed: pass in at least one coroutine'): await first_completed()
    async with timeout(0.1): assert await first_completed(sleep(0.1, 1), sleep(0.01, 2), sleep(0.2, 3), sleep(0.3, 4)) == 2
@mk
async def test_race():
    with pytest.raises(TypeError, match=r'asyncutils\.compete\.race_with_callback: pass in at least one coroutine'): await race_with_callback()
    assert await race_with_callback(sleep(0.01, 1), sleep(0.2, 2), sleep(0.01, 3))&1
@mk
async def test_multi_winner_race():
    with pytest.raises(TypeError, match=r'asyncutils\.compete\.multi_winner_race_with_callback: pass in at least one coroutine'): await multi_winner_race_with_callback(timeout=5) # ty: ignore[missing-argument]
    assert set(await multi_winner_race_with_callback(sleep(0.01, 1), sleep(0.2, 2), sleep(0.01, 3), timeout=0.1)) == {1, 3}
