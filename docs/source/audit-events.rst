Audit events table
==================

This page details all events raised by this library through sys.audit and the corresponding arguments. This module takes care not to expose sensitive
information in the events, so that the audit hooks often only see the fully qualified name of the type of some handled object rather than the object
itself. For consistency and namespace integrity, the name of all audit events begin with 'asyncutils', and are often exactly the fully qualified name
of the function being called.

See the official documentation for :func:`sys.audit` and :func:`sys.addaudithook` on how to listen to these events, as well as
:class:`asyncutils.channels.EventBus`, which is capable of triggering mass publications to async subscribers for audit events with little overhead.

Also see `the standard library audit event table <https://docs.python.org/3/library/audit_events.html>`_, from which the inclustion and format of
this table take inspiration.

.. list-table:: Audit events
  :header-rows: 1
  :widths: 35 30 35

  * - Audit event
    - Arguments
    - Description
  * - asyncutils/create_executor
    - ``fname``: :class:`str`
    - Raised when :mod:`asyncutils` creates an executor, type dictated by configuration. ``fname`` is of the form 'submodule.function'.
  * - asyncutils/get_loop_and_set
    - ``loop``: :class:`asyncio.BaseEventLoop`
    - Raised when :mod:`asyncutils` retrieves an event loop ``loop``, creating one if necessary, and sets it as the event loop for the current thread if not already set.
  * - asyncutils/read_config
    - ``cfg_path``: :class:`str`
    - Raised when :mod:`asyncutils` reads its configuration file expected to be in json format at ``cfg_path`` (not guaranteed to be absolute).
  * - asyncutils/discontinue_config
    - ``cfg_path``: :class:`str`
    - Raised when :mod:`asyncutils` no longer uses the configuration file at ``cfg_path``, since its ``next_config`` key corresponds to ``null``.
  * - asyncutils/set_next_config
    - ``old_path``: :class:`str`, ``new_path``: :class:`str`
    - Raised when :mod:`asyncutils` changes its configuration file from that at ``old_path`` to that at ``new_path``, as dictated by the ``next_config`` field.
  * - asyncutils.altlocks.UniqueResourceGuard
    - ``rtyp``: :class:`str`
    - Raised when :class:`asyncutils.altlocks.UniqueResourceGuard` is instantiated, with ``rtyp`` being the fully qualified name of the type of the resource being guarded, including its module.
  * - asyncutils.altlocks.CircuitBreaker
    - ``name``: :class:`str`, ``max_fails``: :class:`int`
    - Raised when :class:`asyncutils.altlocks.CircuitBreaker` is instantiated, with ``name`` being its name and ``max_fails`` the number of consecutive failures that will cause the circuit to open.
  * - asyncutils.altlocks.CircuitBreaker.__call__
    - ``name``: :class:`str`, ``fname``: :class:`str`
    - Raised when a :class:`asyncutils.altlocks.CircuitBreaker` of name ``name`` is applied on a function with name ``fname``.
  * - asyncutils.base.safe_cancel_batch
    - ``it``: :class:`asyncutils._internal.protocols.SupportsIteration[asyncio.futures.Future]`
    - Raised when :func:`asyncutils.base.safe_cancel_batch` is called on the (possibly async) iterable ``it``.
  * - asyncutils.base.iter_to_aiter
    - ``tname``: :class:`str`
    - Raised when :func:`asyncutils.base.iter_to_aiter` is called on an iterable of type with name ``tname``.
  * - asyncutils.base.aiter_to_iter
    - ``tname``: :class:`str`
    -  Raised when :func:`asyncutils.base.aiter_to_iter` is called on an async iterable of type with name ``tname``.
  * - asyncutils.buckets.TokenBucket
    - ``rate``: :class:`float`, ``capacity``: :class:`float`
    - Raised when :class:`asyncutils.buckets.TokenBucket` is instantiated, with ``rate`` being the token refill rate and ``capacity`` the maximum number of tokens.
  * - asyncutils.buckets.LeakyBucket
    - ``capacity``: :class:`float`, ``leak``: :class:`float`
    - Raised when :class:`asyncutils.buckets.LeakyBucket` is instantiated, with ``capacity`` being the maximum number of tokens and ``leak`` the leak rate.
  * - asyncutils.caches.CacheWithBackgroundRefresh
    - ``ttl``: :class:`float`, ``refresh``: :class:`float`
    - Raised when :class:`asyncutils.caches.CacheWithBackgroundRefresh` is instantiated, with ``ttl`` being the time to live of cache entries and ``refresh`` the time before expiry at which background refreshes are triggered.
  * - asyncutils.caches.AsyncLRUCache
    - ``maxsize``: :class:`int`, ``ttl``: :class:`float|None`
    - Raised when :class:`asyncutils.caches.AsyncLRUCache` is instantiated, with ``maxsize`` being the maximum number of entries and ``ttl`` their time to live.
  * - asyncutils.channels.Observable
    - ``maxsize``: :class:`int|None`
    - Raised when :class:`asyncutils.channels.Observable` is instantiated, with ``maxsize`` being the maximum number of subscribers or ``None`` if there is no such limit.
  * - asyncutils.channels.EventBus
    - ``max_concurrent``: :class:`int`
    - Raised when :class:`asyncutils.channels.EventBus` is instantiated, with ``max_concurrent`` being the maximum number of event handlers allowed to run concurrently.
  * - asyncutils.cli.run
    - \
    - Raised with no arguments when the command-line interface of this library is first invoked through the entry point ``[python [-m ]]asyncutils``, even if just asking for the version or help.
  * - asyncutils.compete.first_completed/start
    - ``ntasks``: :class:`int`
    - Raised when :func:`asyncutils.compete.first_completed` is called, with ``ntasks`` coroutines.
  * - asyncutils.compete.first_completed/end
    - ``ntasks``: :class:`int`
    - Raised when :func:`asyncutils.compete.first_completed` finishes, with ``ntasks`` coroutines.
  * - asyncutils.compete.race_with_callback/start
    - ``ntasks``: :class:`int`
    - Raised when :func:`asyncutils.compete.race_with_callback` is called, with ``ntasks`` coroutines.
  * - asyncutils.compete.race_with_callback/end
    - ``ntasks``: :class:`int`
    - Raised when :func:`asyncutils.compete.race_with_callback` finishes, with ``ntasks`` coroutines.
  * - asyncutils.compete.multi_winner_race_with_callback/start
    - ``ntasks``: :class:`int`
    - Raised when :func:`asyncutils.compete.multi_winner_race_with_callback` is called, with ``ntasks`` coroutines.
  * - asyncutils.compete.multi_winner_race_with_callback/end
    - ``ntasks``: :class:`int`
    - Raised when :func:`asyncutils.compete.multi_winner_race_with_callback` finishes, with ``ntasks`` coroutines.
  * - asyncutils.exceptions.unnest
    - ``excdq``: :class:`collections.deque[BaseException]`
    - Raised when :func:`asyncutils.exceptions.unnest` is called, with ``excdq`` being the queue that is to store the exceptions and flatten them, the items in which are initially not all the groups that will be processed.
  * - asyncutils.exceptions.unnest_reverse
    - ``exclst``: :class:`list[BaseException]`
    - Raised when :func:`asyncutils.exceptions.unnest_reverse` is called, with ``exclst`` being the stack that is to store the exceptions and flatten them, with only a subset of the groups to be eventually collapsed in it at the beginning.
  * - asyncutils.exceptions.raise\_
    - ``exc``: :class:`BaseException`
    - Raised when :func:`asyncutils.exceptions.raise_` is about to raise ``exc``, such that hooks may process the instance or perform validation outside the scope of :func:`asyncutils.exceptions.prepare_exception`.
  * - asyncutils.func.benchmark
    - ``fname``: :class:`str`, ``total_rounds``: :class:`int`
    - Raised when :func:`asyncutils.func.benchmark` is called, with ``fname`` being the name of the function being benchmarked, and ``total_rounds`` the total number of rounds to be executed, including warmup rounds.
  * - asyncutils.func.RateLimited
    - ``fname``: :class:`str`, ``calls``: :class:`int`, ``period``: :class:`float`
    - Raised when a :class:`asyncutils.func.RateLimited` is instantiated, with ``fname`` being the name of the function being rate limited, ``calls`` the number of calls allowed every ``period`` seconds.
  * - asyncutils.futures.AsyncCallbacksFuture/schedule_callbacks
    - ``addr``: :class:`int`
    - Raised when the exact instance of :class:`asyncutils.futures.AsyncCallbacksFuture` at address ``addr`` schedules its sync and async callbacks.
  * - asyncutils.futures.AsyncCallbacksTask/schedule_callbacks
    - ``addr``: :class:`int`
    - The above, but for exact instances of :class:`asyncutils.futures.AsyncCallbacksTask`.
  * - asyncutils.io.double_ended_pipe
    - ``reader1``: :class:`int`, ``writer1``: :class:`int`, ``reader2``: :class:`int`, ``writer2``: :class:`int`
    - Raised when :func:`asyncutils.io.double_ended_text_pipe` or :func:`asyncutils.io.double_ended_binary_pipe` is called, with the file descriptors of the reader and writer ends of both pipes as arguments.
