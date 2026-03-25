# Changelog

All notable changes to this project are and will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

This project uses [Semantic Versioning](https://semver.org/).

## [0.8.17] - 2026-03-24: newest; [unstable](https://semver.org/#spec-item-4)

This branch was created on 2026-03-25 to integrate PEP 810 lazy imports into the library, greatly improving its efficiency.

### Tests

45% coverage, 22 tests

### Docs

41% complete

### Added

Top level:

- \_\_version__
- \_\_hexversion__
- submodules_map
- preloaded_submodules

Submodules:

- altlocks

  Classes:
  - DynamicBoundedSemaphore
  - ResourceGuard
  - UniqueResourceGuard
  - CircuitBreaker
  - StatefulBarrier
  - DynamicThrottle

- base

  Classes:
  - event_loop (context manager)

  Functions:
  - adisembowelleft
  - adisembowel
  - safe_cancel_batch
  - iter_to_aiter
  - aiter_to_iter
  - collect
  - take
  - drop
  - aenumerate

  Awaitables:
  - dummy_task
  - yield_to_event_loop

- buckets

  Classes:
  - TokenBucket
  - LeakyBucket

- caches

  Classes:
  - AsyncLRUCache
  - CacheWithBackgroundRefresh

- channels
  Classes:
  - Observable
  - EventBus
  - Rendezvous

- cli

  Functions:
  - run

- compete

  Functions:
  - first_completed
  - race_with_callback
  - convert_to_coro_iter
  - enhanced_staggered_race

- config

  Classes:
  - debugging
  - Executor

  Functions:
  - set_logger_level
  - get_past_logs

  Constants:
  - debug
  - silent
  - basic_repl
  - max_memerrs
  - loaded_all
  - logging_to

- console

  Classes:
  - ConsoleBase
  - AsyncUtilsConsole

- constants

  Classes:
  - sentinel_base

  Constants:
  - RECIP_E

  Sentinels:
  - RAISE
  - SYNC_AWAIT

- context

  Classes:
  - Context
  - localcontext (context manager)

  Functions:
  - getcontext
  - setcontext

  Configuration variables: Refer to the IDE autocomplete

- events

  Classes:
  - SingleWaiterEventWithValue
  - EventWithValue

- exceptions:

  Classes:
  - ref
  - IgnoreErrors
  - WarningToError

  Constants:
  - CRITICAL

  Context managers (ignore_*):
  - ignore_all

  Exception types:
  - Critical
  - StateCorrupted
  - VersionError
  - VersionConversionError
  - VersionNormalizerMissing
  - VersionCorrupted
  - VersionValueError
  - VersionNormalizerTypeError
  - VersionNormalizerFault
  - BulkheadError
  - BulkheadFull
  - BulkheadShutDown
  - PoolError
  - PoolFull
  - PoolShutDown
  - BusError
  - BusTimeout
  - BusShutDown
  - BusStatsErrors
  - BusPublishingError
  - CircuitBreakerError
  - CircuitHalfOpen
  - CircuitOpen
  - EventValueError
  - FutureCorrupted
  - MaxIterationsError
  - ItemsExhausted
  - LockForceRequest
  - PasswordQueueError
  - PasswordRetrievalError
  - GetPasswordRetrievalError
  - PutPasswordRetrievalError
  - ForbiddenOperation
  - PasswordError
  - WrongPassword
  - WrongPasswordType
  - PasswordMissing
  - GetPasswordMissing
  - PutPasswordMissing

  Functions:
  - unnest
  - unnest_reverse
  - potent_derive
  - prepare_exception
  - raise_
  - exception_occurred
  - wrap_exc
  - unwrap_exc

- func

  Classes:
  - RateLimited

  Functions:
  - areduce
  - every
  - everymethod
  - timer
  - retry
  - throttle
  - debounce
  - measure
  - benchmark

- futures

  Classes:
  - AsyncCallbacksFuture
  - AsyncCallbacksTask

- io

  Classes:
  - AsyncReadWriteCouple
  - MemoryMappedIOManager

  Functions:
  - double_ended_text_pipe
  - double_ended_binary_pipe

- iterclasses

  Classes:
  - anullcontext (context manager)
  - achain
  - apeekable
  - abucket
  - OnlineSorter

- iters

  Refer to the IDE autocomplete

- locks

  Classes:
  - AdvancedRateLimit
  - PrioritySemaphore
  - KeyedCondition
  - RLock
  - PriorityLock
  - PriorityRLock
  - LocksmithBase

- misc

  Classes:
  - StateMachine

  Functions:
  - gather_with_limited_concurrency

- mixins

  Interfaces/Mixins:
  - EventualLoopMixin
  - LoopContextMixin
  - AwaitableMixin
  - AsyncContextMixin
  - LockMixin
  - LockWithOwnerMixin
  - EventMixin

- networking

  Classes:
  - LineProtocol
  - SocketTransport

- pools

  Classes:
  - Pool
  - AdvancedPool
  - ConnectionPool
  - CallbackAccumulator

- processors

  Classes:
  - SemBatchProcessor
  - BatchProcessor
  - Bulkhead

- properties

  Classes:
  - AsyncProperty
  - AsyncLockProperty

- queues

  Interfaces:
  - PotentQueueBase

  Classes:
  - SmartQueue
  - SmartLifoQueue
  - SmartPriorityQueue
  - UserPriorityQueue

  Functions:
  - password_queue

  Context managers (ignore_*):
  - ignore_qshutdown
  - ignore_qempty
  - ignore_qfull
  - ignore_qerrs
  - ignore_valerrs

- signals

  Functions:
  - wait_for_signal

- tools

  Functions:
  - json_to_argv
  - json_to_argstr
  - argv_to_json
  - argstr_to_json
  - get_cfg_json_format
  - print_cfg_json_format
  - get_cmd_help
  - print_cmd_help

- util

  Functions:
  - get_future
  - new_tasks
  - to_sync
  - to_async
  - to_sync_from_loop
  - sync_await
  - sync_lock
  - sync_lock_from_binder
  - lockf
  - semaphore
  - get_aiter_fromf
  - safe_cancel

- version

  Classes:
  - VersionInfo
  - VersionDelta

  Functions:
  - normalize
  - normalize_allow_unimplemented
  - register_normalizer
  - unregister_normalizer
  - dispatch_normalizer
  - autogenerate_normalizers

## [0.8.0] - 2026-03-06

Created [GitHub repository](https://github.com/jonathandung/asyncutils.git).

## [0.0.0] - 2025-08-xx

Development begins. This can be classified as a passion project.
