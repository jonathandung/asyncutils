from ._internal.types import Timer, ValidExcType
from .mixins import AsyncContextMixin, EventualLoopMixin
from types import TracebackType
from typing import overload
__all__ = 'LeakyBucket', 'TokenBucket'
class TokenBucket:
    '''A token bucket rate limiter that controls the rate of operations.
    The bucket fills up with tokens at a fixed rate, with each operation consuming a certain amount of tokens.
    If there are not enough tokens, the operation must wait until there are.'''
    def __init__(self, rate: float, capacity: float, timer: Timer=...):
        '''`rate`: The number of tokens the bucket gains per time interval, as defined by the timer
        `capacity`: The maximum number of tokens the bucket can hold
        `timer` (optional): A function such as `time.time` that returns the current time; default `time.monotonic`'''
    async def consume(self, tokens: float=...) -> None: '''Consume tokens from the bucket as described. The default amount to consume if `tokens` is not passed can be set through context.TOKEN_BUCKET_DEFAULT_CONSUME_TOKENS.'''
    @property
    def capacity(self) -> float: '''The capacity of the bucket.'''
class LeakyBucket(AsyncContextMixin[LeakyBucket], EventualLoopMixin):
    '''A leaky bucket rate limiter with adaptive flow control. Use as a context manager.
    In the context, tokens leak from the bucket at a constant rate. Operations can add tokens to the bucket.
    The bucket includes an adaptive factor that adjusts based on current fill level to provide smoother rate limiting under varying loads.'''
    def __init__(self, capacity: float, leak: float, min_factor: float=..., max_factor: float=..., external_factor_settable: bool=..., timer: Timer=...):
        '''`capacity`: The maximum number of tokens the bucket can hold
        `leak`: The rate at which tokens leak from the bucket
        `min_factor` (optional): Minimum adaptive factor; default `context.LEAKY_BUCKET_DEFAULT_MIN_FACTOR`.
        `max_factor` (optional): Maximum adaptive factor; default `context.LEAKY_BUCKET_DEFAULT_MAX_FACTOR`.
        `external_factor_settable` (optional): Whether the factor attribute can be modified; default `context.LEAKY_BUCKET_DEFAULT_EXT_CAN_SET_FACTOR`.'''
    @overload
    def __exit__(self, exc_typ: ValidExcType, exc_val: BaseException, exc_tb: TracebackType, /) -> None: '''Stop draining the tokens in the bucket.'''
    @overload
    def __exit__(self, exc_typ: None, exc_val: None, exc_tb: None, /) -> None: ...
    async def acquire(self, amount: float=...) -> bool: '''Attempt to add `amount` tokens to the bucket immediately; return success.'''
    async def wait_for_tokens(self, amount: float=...) -> float: '''Wait until `amount` tokens can be added to the bucket **at once**. Return the total wait time.'''
    @property
    def factor(self) -> float: '''The current adaptive factor.'''
    @factor.setter
    def factor(self, value: float, /) -> None: '''Manually set the adaptive factor to `value`, clamped to `min_factor` and `max_factor`.'''