from ._internal.patch import patch_function_signatures as f
from ._internal.submodules import context_all as __all__
import dataclasses as D
@D.dataclass(kw_only=True, match_args=False, slots=True)
class Context:
    CIRCUIT_BREAKER_DEFAULT_RESET: float = 30.0
    CIRCUIT_BREAKER_DEFAULT_MAX_HALF_OPEN_CALLS: int = 5
    CIRCUIT_BREAKER_DEFAULT_MAX_FAILS: int = 3
    DYNAMIC_BOUNDED_SEMAPHORE_DEFAULT_VALUE: int = 1
    DYNAMIC_THROTTLE_DEFAULT_MIN_RATE: float = 1e2
    DYNAMIC_THROTTLE_DEFAULT_MAX_RATE: float = 100.0
    DYNAMIC_THROTTLE_DEFAULT_WINDOW: int = 100
    DYNAMIC_THROTTLE_DEFAULT_UBOUND: float = 0.75
    DYNAMIC_THROTTLE_DEFAULT_LBOUND: float = 0.25
    DYNAMIC_THROTTLE_DEFAULT_UFACTOR: float = 1.1
    DYNAMIC_THROTTLE_DEFAULT_LFACTOR: float = 0.9
    DYNAMIC_THROTTLE_DEFAULT_JITTER: float = 0.2
    ITER_TO_AITER_DEFAULT_USE_EXISTING_EXECUTOR: bool = False
    ITER_TO_AITER_DEFAULT_MAY_CREATE_EXECUTOR: bool = False
    TOKEN_BUCKET_DEFAULT_CONSUME_TOKENS: float = 1.0
    LEAKY_BUCKET_DEFAULT_MINFACTOR: float = 0.1
    LEAKY_BUCKET_DEFAULT_MAXFACTOR: float = 10.0
    LEAKY_BUCKET_WAIT_FOR_TOKENS_TICK: float = 0.1
    LEAKY_BUCKET_DEFAULT_EXT_CAN_SET_FACTOR: bool = True
    LEAKY_BUCKET_ADJMAP: object = (0x100, (0.15, 1.1, 0.85, 0.9)), (0x80, (0.23, 1.2, 0.77, 0.81)), (0, (0.3, 1.4, 0.7, 0.73))
    BACKGROUND_REFRESH_CACHE_DEFAULT_TTL: float = 60.0
    BACKGROUND_REFRESH_CACHE_DEFAULT_REFRESH: float = 15.0
    ASYNC_LRU_CACHE_DEFAULT_MAX_SIZE: int = 128
    EVENT_BUS_STREAM_DEFAULT_BUFFER_SIZE: int = 100
    EVENT_BUS_STREAM_DEFAULT_ITEM_TIMEOUT: float|None = 3.0
    EVENT_BUS_STREAM_DEFAULT_TIMEOUT: float|None = 5.0
    EVENT_WITH_VALUE_DEFAULT_MAX_HIST: int = 128
    EVENT_WITH_VALUE_DEFAULT_RECENT: float = 5.0
    RETRY_DEFAULT_TRIES: int = 3
    RETRY_DEFAULT_DELAY: float = 0.5
    RETRY_DEFAULT_MAX_DELAY: float = 30.0
    RETRY_DEFAULT_BACKOFF: float = 2.0
    RETRY_DEFAULT_JITTER: float = 0.2
    ADVANCED_RATE_LIMIT_DEFAULT_TOKENS: float = 1.0
    PRIORITY_SEMAPHORE_DEFAULT_VALUE: int = 1
    RWLOCK_DEFAULT_PREFER_WRITERS: bool = True
    LOCKSMITH_DEFAULT_TIMEOUTS: object = 1.0, 0.1, None
    GATHER_WITH_LIMITED_CONCURRENCY_DEFAULT_MAX_CONCURRENT: int = 8
    LINE_PROTOCOL_DEFAULT_BUFFER_SIZE: int = 0x1000
    SOCKET_TRANSPORT_LIMITS: object = 0x800, 0x2000
    ADVANCED_POOL_DEFAULT_MAX_WORKERS: int = 5
    ADVANCED_POOL_DEFAULT_MIN_WORKERS: int = 1
    ADVANCED_POOL_THRESHOLD_HI: float = 1.5
    ADVANCED_POOL_THRESHOLD_LO: float = 0.5
    ADVANCED_POOL_FACTOR: float = 0.3
    CONNECTION_POOL_DEFAULT_MAX_SIZE: int = 10
    CONNECTION_POOL_DEFAULT_MIN_SIZE: int = 1
    CONNECTION_POOL_DEFAULT_MAX_LIFE: float = 3600.0
    CONNECTION_POOL_MAINTENANCE_INTERVAL: float = 30.0
    BOUNDED_BATCH_PROCESSOR_DEFAULT_BATCH_SIZE: int = 10
    BOUNDED_BATCH_PROCESSOR_DEFAULT_MAX_CONCURRENT: int = 5
    BATCH_PROCESSOR_DEFAULT_MAX_SIZE: int = 128
    BATCH_PROCESSOR_DEFAULT_MAX_TIME: float = 1.0
    BULKHEAD_DEFAULT_MAX_QUEUE: int = 0
    BULKHEAD_DEFAULT_MAX_REJ: int = -1
    WAIT_FOR_SIGNAL_DEFAULT_SIGNALS: object = 2, 15
    def __post_init__(self):
        if not (self.CIRCUIT_BREAKER_DEFAULT_RESET > 0 < self.CIRCUIT_BREAKER_DEFAULT_MAX_HALF_OPEN_CALLS and self.DYNAMIC_BOUNDED_SEMAPHORE_DEFAULT_VALUE > 0 < self.DYNAMIC_THROTTLE_DEFAULT_LBOUND < self.DYNAMIC_THROTTLE_DEFAULT_UBOUND < 1 < self.DYNAMIC_THROTTLE_DEFAULT_UFACTOR > self.DYNAMIC_THROTTLE_DEFAULT_LFACTOR < 1 < self.LEAKY_BUCKET_DEFAULT_MAXFACTOR > self.LEAKY_BUCKET_DEFAULT_MINFACTOR > 0.0 < self.LEAKY_BUCKET_WAIT_FOR_TOKENS_TICK and self.BACKGROUND_REFRESH_CACHE_DEFAULT_REFRESH > 0.0 < self.BACKGROUND_REFRESH_CACHE_DEFAULT_TTL and self.ASYNC_LRU_CACHE_DEFAULT_MAX_SIZE > 0 < self.EVENT_BUS_STREAM_DEFAULT_BUFFER_SIZE and all(i is None or i > 0.0 for i in (self.EVENT_BUS_STREAM_DEFAULT_TIMEOUT, self.EVENT_BUS_STREAM_DEFAULT_TIMEOUT)) and self.EVENT_WITH_VALUE_DEFAULT_MAX_HIST > 0 < self.EVENT_WITH_VALUE_DEFAULT_RECENT and self.RETRY_DEFAULT_TRIES > 0 < self.DYNAMIC_THROTTLE_DEFAULT_JITTER < 1.0 and self.RETRY_DEFAULT_BACKOFF > 1.0 > self.RETRY_DEFAULT_JITTER > 0.0 < self.RETRY_DEFAULT_DELAY <= self.RETRY_DEFAULT_MAX_DELAY): raise ValueError
    def __init_subclass__(cls): raise TypeError('cannot subclass asyncutils.context.Context')
    copy = D.replace # noqa: RUF045
_ = __import__('_contextvars').ContextVar('asyncutils_contextvar')
def getcontext(_=_, d=Context()): # noqa: B008
    try: return _.get()
    except LookupError: _.set(d); return d
def setcontext(c, /, _=_):
    if not isinstance(c, Context): raise TypeError('setcontext: ctx must be an instance of asyncutils.context.Context')
    _.set(c)
f((getcontext, ''), (setcontext, 'ctx, /'))
class localcontext:
    __slots__ = 'new_ctx', 'saved_ctx'
    def __init__(self, new_ctx): self.new_ctx = new_ctx.copy()
    def __enter__(self): self.saved_ctx = getcontext(); setcontext(self.new_ctx)
    def __exit__(self, /, *_): setcontext(self.saved_ctx)
def __getattr__(name, /): return getattr(getcontext(), name)
del _, D, f