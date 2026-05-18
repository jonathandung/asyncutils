from asyncutils._internal import helpers as H
from asyncutils._internal.compat import D
from sys import audit as a
K = V = t = None
N, C, D = H.Bag(log_to='STDERR', executor='thread', Q=0, V=0, pdb=False, max_memerrs=3, load_all=False, seed=None, debug=False, **D), {'CIRCUIT_BREAKER_DEFAULT_MAX_FAILS': 3, 'CIRCUIT_BREAKER_DEFAULT_MAX_HALF_OPEN_CALLS': 5, 'CIRCUIT_BREAKER_DEFAULT_RESET': 30.0, 'DYNAMIC_THROTTLE_DEFAULT_JITTER': 0.2, 'DYNAMIC_THROTTLE_DEFAULT_LBOUND': 0.25, 'DYNAMIC_THROTTLE_DEFAULT_LFACTOR': 0.75, 'DYNAMIC_THROTTLE_DEFAULT_MAX_RATE': 100.0, 'DYNAMIC_THROTTLE_DEFAULT_MIN_RATE': 1e-2, 'DYNAMIC_THROTTLE_DEFAULT_UBOUND': 0.75, 'DYNAMIC_THROTTLE_DEFAULT_UFACTOR': 1.25, 'DYNAMIC_THROTTLE_DEFAULT_WINDOW': 100, 'AITER_TO_GEN_DEFAULT_ALLOW_FUTURES': True, 'AITER_TO_GEN_DEFAULT_STRICT': False, 'EVENT_LOOP_BASE_FLAGS': 0, 'ITER_TO_AGEN_DEFAULT_MAY_CREATE_EXECUTOR': False, 'ITER_TO_AGEN_DEFAULT_STRICT': False, 'ITER_TO_AGEN_DEFAULT_USE_EXISTING_EXECUTOR': False, 'LEAKY_BUCKET_ADJMAP': ((256, (0.15, 1.1, 0.85, 0.9)), (128, (0.23, 1.2, 0.77, 0.81)), (0, (0.3, 1.4, 0.7, 0.73))), 'LEAKY_BUCKET_DEFAULT_ACQUIRE_TOKENS': 1.0, 'LEAKY_BUCKET_DEFAULT_EXT_CAN_SET_FACTOR': True, 'LEAKY_BUCKET_DEFAULT_MAX_FACTOR': 10.0, 'LEAKY_BUCKET_DEFAULT_MIN_FACTOR': 0.1, 'LEAKY_BUCKET_DEFAULT_WAIT_FOR_TOKENS_TOKENS': 1.0, 'LEAKY_BUCKET_WAIT_FOR_TOKENS_TICK': 0.1, 'TOKEN_BUCKET_DEFAULT_CONSUME_TOKENS': 1.0, 'ASYNC_LRU_CACHE_DEFAULT_MAX_SIZE': 128, 'BACKGROUND_REFRESH_CACHE_DEFAULT_REFRESH': 15.0, 'BACKGROUND_REFRESH_CACHE_DEFAULT_TTL': 60.0, 'EVENT_BUS_DEFAULT_MAX_CONCURRENT': 64, 'EVENT_BUS_PUBLISH_DEFAULT_SAFE': True, 'EVENT_BUS_STREAM_DEFAULT_BUFFER_SIZE': 100, 'EVENT_BUS_STREAM_DEFAULT_ITEM_TIMEOUT': 3.0, 'EVENT_BUS_STREAM_DEFAULT_TIMEOUT': 5.0, 'OBSERVABLE_DEFAULT_NTIMES_N': 1, 'RENDEZVOUS_MAINTENANCE_INTERVAL': 30.0, 'CONVERT_TO_CORO_ITER_DEFAULT_SKIP_INVALID': True, 'EVENT_WITH_VALUE_DEFAULT_MAX_HIST': 128, 'EVENT_WITH_VALUE_DEFAULT_RECENT': 5.0, 'BENCHMARK_DEFAULT_SEQUENTIAL': False, 'BENCHMARK_DEFAULT_TIMES': 3, 'BENCHMARK_DEFAULT_WARMUP': 0, 'RETRY_DEFAULT_BACKOFF': 2.0, 'RETRY_DEFAULT_DELAY': 0.5, 'RETRY_DEFAULT_JITTER': 0.2, 'RETRY_DEFAULT_MAX_DELAY': 30.0, 'RETRY_DEFAULT_TRIES': 3, 'TIMER_DEFAULT_PRECISION': 7, 'MEMORY_MAPPED_IO_MANAGER_DEFAULT_CHECKSUM_ALG': 'blake2s', 'MEMORY_MAPPED_IO_MANAGER_DEFAULT_MINIMIZE_WRITES': True, 'AFRIEVALDS_DEFAULT_K': 2, 'AONLINESORTER_DEFAULT_SLOW': False, 'AUNZIP_DEFAULT_MAX_QSIZE': 64, 'AUNZIP_DEFAULT_PUT_BATCH': 16, 'MERGE_DEFAULT_MAX_QSIZE': 0, 'TEE_DEFAULT_PUT_EXC': True, 'TEE_DEFAULT_MAX_QSIZE': 32, 'ADVANCED_RATE_LIMIT_DEFAULT_TOKENS': 1.0, 'DYNAMIC_BOUNDED_SEMAPHORE_DEFAULT_VALUE': 1, 'LOCKSMITH_DEFAULT_TIMEOUTS': (1.0, 0.1, None), 'PRIORITY_SEMAPHORE_DEFAULT_VALUE': 1, 'GATHER_WITH_LIMITED_CONCURRENCY_DEFAULT_MAX_CONCURRENT': 8, 'LINE_PROTOCOL_DEFAULT_BUFFER_SIZE': 4096, 'SOCKET_TRANSPORT_LIMITS': (2048, 8192), 'ADVANCED_POOL_DEFAULT_MAX_WORKERS': 5, 'ADVANCED_POOL_DEFAULT_MIN_WORKERS': 1, 'ADVANCED_POOL_FACTOR': 0.3, 'ADVANCED_POOL_THRESHOLD_HI': 1.5, 'ADVANCED_POOL_THRESHOLD_LO': 0.5, 'CONNECTION_POOL_DEFAULT_MAX_LIFE': 3600.0, 'CONNECTION_POOL_DEFAULT_MAX_SIZE': 10, 'CONNECTION_POOL_DEFAULT_MIN_SIZE': 1, 'CONNECTION_POOL_MAINTENANCE_INTERVAL': 30.0, 'BATCH_PROCESSOR_DEFAULT_MAX_SIZE': 128, 'BATCH_PROCESSOR_DEFAULT_MAX_TIME': 1.0, 'BOUNDED_BATCH_PROCESSOR_DEFAULT_BATCH_SIZE': 10, 'BOUNDED_BATCH_PROCESSOR_DEFAULT_MAX_CONCURRENT': 5, 'BULKHEAD_DEFAULT_MAX_QUEUE': 32, 'BULKHEAD_DEFAULT_MAX_REJ': -1, 'PASSWORD_QUEUE_DEFAULT_GET_FROM': 'password', 'PASSWORD_QUEUE_DEFAULT_PUT_FROM': 'password', 'RWLOCK_DEFAULT_PREFER_WRITERS': True, 'WAIT_FOR_SIGNAL_DEFAULT_SIGNALS': (2, 15), 'DUAL_CONTEXT_MANAGER_DEFAULT_MAY_CREATE_EXECUTOR': False, 'DUAL_CONTEXT_MANAGER_DEFAULT_STRICT': False, 'DUAL_CONTEXT_MANAGER_DEFAULT_USE_EXISTING_EXECUTOR': True, 'SEMAPHORE_DEFAULT_VALUE': 1}, {'jsonl': 'json', 'json': 'json', 'jsonc': 'jsonc', 'json5': 'json5', 'hjson': 'hjson', 'toml': 'tomllib', 'yml': 'yaml', 'yaml': 'yaml', 'ini': 'configparser', 'xml': 'xmltodict'} # pragma: allowlist secret
def l(p, e=None, /):
    with open(p) as F:
        match L := D[e or p.rpartition('.')[-1]]: # pragma: no cover
            case 'yaml':
                try: import yaml as Y; f = Y.load(F, Y.CSafeLoader)
                except ImportError as a: raise RuntimeError('asyncutils: PyYAML library is required to load YAML configuration file') from a
            case 'tomllib': f = __import__(L).loads(F.read())
            case 'xmltodict': f = __import__(L).parse(F.read())
            case 'configparser': raise RuntimeError('asyncutils: cannot parse ini-like format due to type ambiguities; you should rewrite the configuration in TOML, which is the most similar to ini')
            case _:
                try: f = __import__(L, fromlist=('',) if '.' in L else ()).load(F)
                except ImportError as a: raise RuntimeError(f'asyncutils: {L} library must be installed for asyncutils to accept configuration from {p!r}') from a
    if F.name.endswith(('/pyproject.toml', '\\pyproject.toml')):
        try: f = f['tool']['asyncutils']
        except KeyError: return {}
    if type(f) is dict: return f
    raise TypeError(f'asyncutils: incorrect configuration format at {p}; top-level structure should be an object/mapping')
def m(m, a, /, _='see format.json5'): (e := TypeError(m%(c, a))).add_note(_); raise e
if c := (E := __import__('os').environ).get(k := 'AUTILSCFGPATH', '').strip('"\' \t\r\n\v\f'): # pragma: no cover
    a('asyncutils/read_config', c)
    if isinstance(v := (d := l(c)).pop('next_config', c), str): a('asyncutils/set_next_config', c, v); E[k] = v
    elif v is None: a('asyncutils/discontinue_config', c); del E[k]
    else: m('asyncutils: key "next_config" in %s should point to a string or null, not %r', v)
else:
    A, f, s, t, i = __import__('pathlib').Path.cwd(), None, 'asyncutils/try_config', 'pyproject.toml', None; a('asyncutils/recurse_configs', A)
    for i, A in enumerate(__import__('itertools').chain((A,), A.parents)):
        if (A := A/t).is_file():
            a(s, i)
            with A.open('rb') as f:
                try: d = __import__('tomllib').load(f)['tool']['asyncutils']
                except KeyError: continue
            a('asyncutils/read_config', c := str(A)); break
    else: d = {}
    del A, f, s, i
if v := d.pop('context', None):
    for v in v.values():
        if (t := type(v)) is not dict: m('asyncutils: key "context" in %s should be an object mapping submodule names to objects, not %r', H.fullname(t))
        for K, V in v.items():
            if type(V) is dict:
                for k, v in V.items(): C[f'{K}_{k}'.upper()] = v # noqa: PLW2901
            elif (K := K.upper()) in C: C[K] = V
N.update(d)
del E, k, H, m, K, V, a, v, d, t