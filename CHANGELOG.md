---
hide-toc: true
---

# Changelog

All notable changes to this project are and will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com).

This project uses [Semantic Versioning](https://semver.org).

## Summary

### Tests

59% coverage, 76 tests

### Docs

95% complete

## Versions

## Below versions are [unstable](https://semver.org/#spec-item-4)

### [0.9.12] - 2026-06-12; unreleased

### [0.9.11] - 2026-06-04; newest

Upgraded to Python 3.15.0b2; added experimental GraalPy and free-threaded support.

### [0.9.10] - 2026-05-29

Removed actionlint step; integrated CodeQL fully.

### [0.9.9] - 2026-05-26

Added more tests and more badges to the readme; removed codecov upload step superseded by GitHub Code Quality.

### [0.9.8] - 2026-05-23

Added the genmakefileusage scripts, among some rewrites, most notably eliminating instances of a bare `Any` annotating an argument.

### [0.9.7] - 2026-05-21

Removed unnecessary .nojekyll file from docs directory; regenerated secrets baseline; added `locksmiths` submodule.

### [0.9.6] - 2026-05-19

Re-committed .markdownlint.json to version control; documentation nears completion; used GitHub Actions for page deployment.

### [0.9.5] - 2026-05-17

Some bugfixes; began deployment to [GitHub Pages](https://jonathandung.github.io/asyncutils).

#### BREAKING

Changed the default key used when shelving and unshelving versions.

### [0.9.4] - 2026-05-15

Fixed workflows once more and integrated uv more fully; migrated from mypy to ty, removing stubtest step.

### [0.9.3] - 2026-05-11

Added some tests; changed symbolic links to a copy step in the Read the Docs build, which is more reliable; fixed codecov trigger; added
sphinx-copybutton as an optional dependency.

### [0.9.2] - 2026-05-07

Created symbolic links in docs directory linking to root .md files; fixed some bugs; respected some more environment variables and documented this
behaviour; completed benchmarks; added myst_parser as an optional dependency; bumped some dependencies; added some examples.

### [0.9.1] - 2026-05-01

Declared full support for python[ -m] asyncutils an entry point; patched function, method and class method signatures where appropriate; added
-P/--pdb option; switched to furo theme.

### [0.9.0] - 2026-04-27

Added `__lazy_modules__` attribute to submodules where appropriate; added some iteration, functional programming and context management utilities.

#### BREAKING

- Declared end of life for all alpha versions.
- Changed version shelving and unshelving schema.
- Finalized the following top level objects:

  Constants:
  - \_\_version__
  - \_\_hexversion__
  - submodules_map
  - preloaded_submodules
  - console_preloaded_submodules

  Functions:
  - time_since_boot

- Declared the following submodules and symbols as part of the public API:

  - altlocks

    Classes:
    - ResourceGuard
    - UniqueResourceGuard
    - CircuitBreaker
    - StatefulBarrier
    - DynamicThrottle
    - Releasing

  - base

    Classes:
    - event_loop (context manager)

    Functions:
    - adisembowelleft
    - adisembowel
    - safe_cancel_batch
    - iter_to_agen
    - aiter_to_gen
    - collect
    - take
    - drop
    - aenumerate
    - sleep_forever

    Awaitables:
    - dummy_task
    - yield_to_event_loop

  - buckets

    Classes:
    - TokenBucket
    - LeakyBucket

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
    - multi_winner_race_with_callback
    - convert_to_coro_iter
    - enhanced_gather
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
    - EXECUTORS_FROZENSET
    - POSSIBLE_EXECUTORS

    Sentinels:
    - RAISE

  - context

    Classes:
    - Context
    - localcontext (context manager)
    - nonreusablelocalcontext (context manager)

    Constants:
    - all_contextual_consts
    - ... (every constant in the `all_contextual_consts` frozenset)

    Functions:
    - getcontext
    - setcontext

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
    - ignore_noncritical
    - ignore_typical
    - ignore_stopiteration
    - ignore_stopaiteration
    - ignore_valerrs
    - ignore_typeerrs

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
    - RateLimitExceeded
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
    - raise_exc
    - exception_occurred
    - wrap_exc
    - unwrap_exc

  - func

    Classes:
    - RateLimited

    Functions:
    - areduce
    - iterf
    - acompose
    - every
    - everymethod
    - timer
    - retry
    - throttle
    - debounce
    - measure
    - measure2
    - benchmark
    - star
    - unstar

  - futures

    Classes:
    - AsyncCallbacksFuture
    - AsyncCallbacksTask
    - EagerAsyncCallbacksFuture
    - EagerAsyncCallbacksTask
    - TimeAwareAsyncCallbacksFuture
    - TimeAwareAsyncCallbacksTask
    - TimeAwareFuture
    - TimeAwareTask

  - io

    Classes:
    - AsyncReadWriteCouple
    - MemoryMappedIOManager

    Functions:
    - double_ended_text_pipe
    - double_ended_binary_pipe

  - iterclasses

    Classes:
    - achain
    - apeekable
    - abucket

  - iters

    Functions:
    - ... (There are too many of these, so just refer to the IDE autocomplete or read the stub)

  - locks

    Classes:
    - AdvancedRateLimit
    - DynamicBoundedSemaphore
    - PrioritySemaphore
    - KeyedCondition
    - RLock
    - PriorityLock
    - PriorityRLock
    - MultiCountDownLatch

  - locksmiths

    Classes:
    - LocksmithBase

    Enumerations:
    - ForceResult
    - RecognitionResult

    Functions:
    - succeeded

  - misc

    Classes:
    - CallbackAccumulator
    - StateMachine
    - CacheWithBackgroundRefresh

    Functions:
    - gather_with_limited_concurrency

  - mixins

    Interfaces/Mixins:
    - LoopContextMixin
    - AwaitableMixin
    - AsyncContextMixin
    - ExecutorRequiredAsyncContextMixin
    - LockMixin
    - LockWithOwnerMixin
    - EventMixin

  - networking

    Classes:
    - LineProtocol
    - LFProtocol
    - CRLFProtocol
    - CRProtocol
    - SocketTransport

  - pools

    Classes:
    - AdvancedPool
    - ConnectionPool

  - processors

    Classes:
    - BoundedBatchProcessor
    - BatchProcessor
    - Bulkhead

  - properties

    Classes:
    - AsyncPropertyBase
    - LazyAsyncProperty
    - ConcurrentAsyncProperty
    - RWLockedAsyncProperty

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

  - rwlocks

    Classes:
    - RWLock
    - FairRWLock
    - ReadPreferredRWLock
    - WritePreferredRWLock
    - PriorityRWLock
    - FairPriorityRWLock
    - WritePreferredPriorityRWLock
    - AgingRWLock
    - CoercedMethod

  - signals

    Functions:
    - wait_for_signal

  - tools

    Functions:

    - loadf
    - json_to_argv
    - json_to_argstr
    - argv_to_json
    - argstr_to_json
    - get_cfg_json_format
    - print_cfg_json_format
    - get_cmd_help
    - print_cmd_help

  - util

    Context managers (ignore_*):
    - ignore_cancellation

    Context manager classes:
    - anullcontext

    Functions:
    - aawcmf2dcmf
    - aawcmf2dcmff
    - afcopy
    - dcm
    - get_future
    - new_eager_tasks
    - to_sync
    - to_async
    - to_sync_from_loop
    - sync_await
    - lockf
    - done_evt
    - done_fut
    - locked_lock
    - dualcontextmanager
    - semaphore
    - aiter_from_f
    - safe_cancel
    - transient_block
    - transient_block_from_loop
    - wrap_in_coro
    - atruthify
    - afalsify
    - anullify
    - avalify

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

## Below versions have reached [EOL](https://en.wikipedia.org/wiki/Software_release_life_cycle#End-of-life)

### [0.8.28] - 2026-04-24

Rewrote submodules loading mechanism; removed fragile relative imports; compressed asyncio and sibling module imports to avoid overhead.

### [0.8.27] - 2026-04-21

Added more tests and fixed stubtest errors; abolished slow markdownlint step in pre-commit; various API additions.

### [0.8.26] - 2026-04-18

Squashed many bugs and stub inaccuracies; integrated stubtest; simplified workflows; added more contextual constants.

### [0.8.25] - 2026-04-14

Created issue templates.

### [0.8.24] - 2026-04-10

Created AI_USAGE_POLICY.md.

### [0.8.23] - 2026-04-09

Integrated pre-commit CI.

### [0.8.22] - 2026-04-05

Created the audit events table.

### [0.8.21] - 2026-04-01

Organized badges into table; started using mypy.

### [0.8.20] - 2026-03-29

Started hosting documentation on Read the Docs.

### [0.8.19] - 2026-03-27

Set up docs directory.

### [0.8.17] - 2026-03-24

Started using detect-secrets.

### [0.8.16] - 2026-03-22

Started using ruff; created py.typed.

### [0.8.14] - 2026-03-21

Set up tests directory; started using pytest.

### [0.8.9] - 2026-03-14

Created Dockerfile.

### [0.8.8] - 2026-03-12

Created .editorconfig and .pre-commit-config.yaml.

### [0.8.6] - 2026-03-10

Created ROADMAP.md.

### [0.8.4] - 2026-03-09

Created SUPPORT.md and CHANGELOG.md.

### [0.8.2] - 2026-03-07

Created .dockerignore, .github/workflows/python-package.yaml, CODE_OF_CONDUCT.md, CONTRIBUTING.md, and LICENSE.

### [0.8.1] - 2026-03-06

Created pyproject.toml and SECURITY.md.

### [0.8.0] - 2026-03-06

Created [GitHub repository](https://github.com/jonathandung/asyncutils.git); added version submodule.

## Below entries are abridged

### [0.7.0] - 2026-02-09

Began migration of implementation details into `_internal` subpackage; fixed initialization logic and command line.

### [0.6.0] - 2026-01-1x

Completed migration from inline annotations to separated stubs; perfected `base.event_loop` and lazy loading; added `console` and `cli` submodules.

### [0.5.0] - 2025-12-0x

Added classes such as `altlocks.CircuitBreaker` and `channels.EventBus`; implemented preliminary lazy loading system; created `exceptions` submodule;
began separation of type annotations from .py into .pyi.

### [0.4.0] - 2025-10-0x

Added more complicated patterns and procedures such as `channels.Observable` and `signals.wait_for_signal`.

### [0.3.0] - 2025-08-2x

Basically completed refactoring; added more object-oriented patterns such as `altlocks.DynamicThrottle` and `misc.CacheWithBackgroundRefresh`.

### [0.2.0] - 2025-07-0x

Began reorganizing single file containing all functions into submodules.

### [0.1.0] - 2025-06-xx

Added basic but untested features such as `iters.tee`, `iters.merge`, `base.to_async`, `base.iter_to_agen` and `util.sync_await`.

### [0.0.0] - 2025-05-xx

Development began. This can be classified as a passion project.
