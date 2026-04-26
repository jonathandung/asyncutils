Audit events table
==================

This page details all events raised by this library through :func:`sys.audit` and the corresponding arguments.

This module takes care not to expose sensitive information in the events, so that the audit hooks often only see the fully qualified name of the type
of some handled object rather than the object itself.

For consistency and namespace integrity, all audit event names begin with 'asyncutils', and are often exactly the fully qualified name
of the function being called.

See the official documentation for :func:`sys.audit` and :func:`sys.addaudithook` on how to listen to these events, as well as
:class:`asyncutils.channels.EventBus`, which is capable of triggering mass publications to async subscribers for audit events efficiently.

Also see `the standard library audit event table <https://docs.python.org/3/library/audit_events.html>`_, from which the inclustion and format of
this table take inspiration.

.. rst-class:: widepage

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
    - ``loop``: :class:`~asyncio.base_events.BaseEventLoop`
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
    - Raised when :class:`~asyncutils.altlocks.UniqueResourceGuard` is instantiated, with ``rtyp`` being the fully qualified name of the type of the resource being guarded, including its module.
  * - asyncutils.altlocks.CircuitBreaker
    - ``name``: :class:`str`, ``max_fails``: :class:`int`
    - Raised when :class:`~asyncutils.altlocks.CircuitBreaker` is instantiated, with ``name`` being its name and ``max_fails`` the number of consecutive failures that will cause the circuit to open.
  * - asyncutils.altlocks.CircuitBreaker.__call__
    - ``name``: :class:`str`, ``fname``: :class:`str`
    - Raised when a :class:`~asyncutils.altlocks.CircuitBreaker` of name ``name`` is applied on a function with name ``fname``.
  * - asyncutils.base.safe_cancel_batch
    - ``ityp``: :class:`str`
    - Raised when :func:`~asyncutils.base.safe_cancel_batch` is called on the (possibly async) iterable with exact type of name ``ityp``.
  * - asyncutils.base.iter_to_agen
    - ``tname``: :class:`str`
    - Raised when :func:`~asyncutils.base.iter_to_agen` is called on an iterable of type with name ``tname``.
  * - asyncutils.base.aiter_to_gen
    - ``tname``: :class:`str`
    -  Raised when :func:`~asyncutils.base.aiter_to_gen` is called on an async iterable of type with name ``tname``.
  * - asyncutils.buckets.TokenBucket
    - ``rate``: :class:`float`, ``capacity``: :class:`float`
    - Raised when :class:`~asyncutils.buckets.TokenBucket` is instantiated, with ``rate`` being the token refill rate and ``capacity`` the maximum number of tokens.
  * - asyncutils.buckets.LeakyBucket
    - ``capacity``: :class:`float`, ``leak``: :class:`float`
    - Raised when :class:`~asyncutils.buckets.LeakyBucket` is instantiated, with ``capacity`` being the maximum number of tokens and ``leak`` the leak rate.
  * - asyncutils.caches.CacheWithBackgroundRefresh
    - ``ttl``: :class:`float`, ``refresh``: :class:`float`
    - Raised when :class:`~asyncutils.caches.CacheWithBackgroundRefresh` is instantiated, with ``ttl`` being the time to live of cache entries and ``refresh`` the time before expiry at which background refreshes are triggered.
  * - asyncutils.caches.AsyncLRUCache
    - ``maxsize``: :class:`int`, ``ttl``: :class:`float|None`
    - Raised when :class:`~asyncutils.caches.AsyncLRUCache` is instantiated, with ``maxsize`` being the maximum number of entries and ``ttl`` their time to live.
  * - asyncutils.channels.Observable
    - ``maxsize``: :class:`int|None`
    - Raised when :class:`~asyncutils.channels.Observable` is instantiated, with ``maxsize`` being the maximum number of subscribers or ``None`` if there is no such limit.
  * - asyncutils.channels.EventBus
    - ``name``: :class:`str`
    - Raised when :class:`~asyncutils.channels.EventBus` is instantiated, with ``name`` being its name or ``None`` if not passed.
  * - asyncutils.channels.EventBus.start_audit
    - ``addr``: :class:`int`
    - Raised when the :meth:`start_audit` method of :class:`~asyncutils.channels.EventBus` is called, with the memory address of the instance as argument.
  * - asyncutils.channels.EventBus.stop_audit
    - ``addr``: :class:`int`
    - Raised when the :meth:`stop_audit` method of :class:`~asyncutils.channels.EventBus` is called, with the memory address of the instance as argument.
  * - asyncutils.channels.EventBus.event_stream
    - ``addr``: :class:`int`, ``event_type``: :class:`str|None`
    - Raised when the :meth:`event_stream` method of :class:`~asyncutils.channels.EventBus` is called. ``addr`` is the memory address of the instance, and ``event_type`` is the event type the stream was opened for or ``None`` for catch-all streams.
  * - asyncutils.cli.run
    - \
    - Raised with no arguments when the command-line interface of this library is first invoked through the entry point ``asyncutils``, even if just asking for the version or help.
  * - asyncutils.compete.first_completed/start
    - ``ntasks``: :class:`int`
    - Raised when :func:`~asyncutils.compete.first_completed` is called, with ``ntasks`` coroutines.
  * - asyncutils.compete.first_completed/end
    - ``ntasks``: :class:`int`
    - Raised when :func:`~asyncutils.compete.first_completed` finishes, with ``ntasks`` coroutines.
  * - asyncutils.compete.race_with_callback/start
    - ``ntasks``: :class:`int`
    - Raised when :func:`~asyncutils.compete.race_with_callback` is called, with ``ntasks`` coroutines.
  * - asyncutils.compete.race_with_callback/end
    - ``ntasks``: :class:`int`
    - Raised when :func:`~asyncutils.compete.race_with_callback` finishes, with ``ntasks`` coroutines.
  * - asyncutils.compete.multi_winner_race_with_callback/start
    - ``ntasks``: :class:`int`
    - Raised when :func:`~asyncutils.compete.multi_winner_race_with_callback` is called, with ``ntasks`` coroutines.
  * - asyncutils.compete.multi_winner_race_with_callback/end
    - ``ntasks``: :class:`int`
    - Raised when :func:`~asyncutils.compete.multi_winner_race_with_callback` finishes, with ``ntasks`` coroutines.
  * - asyncutils.console.AsyncUtilsConsole.run
    - ``addr``: :class:`int`
    - Raised when the :meth:`run` method of an instance of :class:`asyncutils.console.AsyncUtilsConsole` at ``addr`` is called.
  * - asyncutils.exceptions.unnest
    - ``n``: :type:`int`
    - Raised when :func:`~asyncutils.exceptions.unnest` is called, with ``n`` being a sloppy lower bound on the number of exception( group)s.
  * - asyncutils.exceptions.unnest_reverse
    - ``n``: :type:`int`
    - Raised when :func:`~asyncutils.exceptions.unnest_reverse` is called, with ``n`` being a sloppy lower bound on the number of exception( group)s.
  * - asyncutils.exceptions.raise_exc
    - ``exc``: :class:`BaseException`
    - Raised when :func:`~asyncutils.exceptions.raise_exc` is about to raise ``exc``, such that hooks may process the instance or perform validation outside the scope of :func:`~asyncutils.exceptions.prepare_exception`.
  * - asyncutils.func.benchmark
    - ``fname``: :class:`str`, ``total_rounds``: :class:`int`
    - Raised when :func:`~asyncutils.func.benchmark` is called, with ``fname`` being the name of the function being benchmarked, and ``total_rounds`` the total number of rounds to be executed, including warmup rounds.
  * - asyncutils.func.RateLimited
    - ``fname``: :class:`str`, ``calls``: :class:`int`, ``period``: :class:`float`
    - Raised when a :class:`~asyncutils.func.RateLimited` is instantiated, with ``fname`` being the name of the function being rate limited, ``calls`` the number of calls allowed every ``period`` seconds.
  * - asyncutils.futures.AsyncCallbacksFuture/schedule_callbacks
    - ``addr``: :class:`int`
    - Raised when the exact instance of :class:`~asyncutils.futures.AsyncCallbacksFuture` at address ``addr`` schedules its sync and async callbacks.
  * - asyncutils.futures.AsyncCallbacksTask/schedule_callbacks
    - ``addr``: :class:`int`
    - The above, but for exact instances of :class:`~asyncutils.futures.AsyncCallbacksTask`.
  * - asyncutils.futures.EagerAsyncCallbacksFuture/schedule_callbacks
    - ``addr``: :class:`int`
    - The above, but for exact instances of :class:`~asyncutils.futures.EagerAsyncCallbacksFuture`.
  * - asyncutils.futures.EagerAsyncCallbacksTask/schedule_callbacks
    - ``addr``: :class:`int`
    - The above, but for exact instances of :class:`~asyncutils.futures.EagerAsyncCallbacksTask`.
  * - asyncutils.io.double_ended_pipe
    - ``reader1``: :class:`int`, ``writer1``: :class:`int`, ``reader2``: :class:`int`, ``writer2``: :class:`int`
    - Raised when :func:`~asyncutils.io.double_ended_text_pipe` or :func:`~asyncutils.io.double_ended_binary_pipe` is called, with the file descriptors of the reader and writer ends of both pipes as arguments.
  * - asyncutils.iterclasses.online_sorter
    - \
    - Raised when :class:`~asyncutils.iterclasses.online_sorter` is instantiated.
  * - asyncutils.iters.agetitems_from_indices
    - ``tname``: :class:`str`
    - Raised when :func:`~asyncutils.iters.agetitems_from_indices` is called on an iterable, the type of which has full name ``tname``.
  * - asyncutils.iters.aintersend
    - ``tname1``: :class:`str`, ``tname2``: :class:`str`
    - Raised when :func:`~asyncutils.iters.aintersend` is called on two async generators, the types of which have full names ``tname1`` and ``tname2`` respectively.
  * - asyncutils.iters.asendstream
    - ``tname1``: :class:`str`, ``tname2``: :class:`str`
    - Raised when :func:`~asyncutils.iters.asendstream` is called, the full name of the type of the async generator being ``tname1`` and that of the (async) iterable being ``tname2``.
  * - asyncutils.iters.acat
    - ``first``: :class:`~typing.Any`
    - Raised when :func:`~asyncutils.iters.acat` is called, ``first`` being the item yielded to start the async generator.
  * - asyncutils.iters.aforever
    - \
    - Raised when :func:`~asyncutils.iters.aforever` is called.
  * - asyncutils.networking.LineProtocol
    - \
    - Raised when :class:`~asyncutils.networking.LineProtocol` is instantiated.
  * - asyncutils.networking.CRLFProtocol
    - \
    - Raised when :class:`~asyncutils.networking.CRLFProtocol` is instantiated.
  * - asyncutils.networking.CRProtocol
    - \
    - Raised when :class:`~asyncutils.networking.CRProtocol` is instantiated.
  * - asyncutils.networking.LFProtocol
    - \
    - Raised when :class:`~asyncutils.networking.LFProtocol` is instantiated.
  * - asyncutils.networking.SocketTransport
    - \
    - Raised when :class:`~asyncutils.networking.SocketTransport` is instantiated.
  * - asyncutils.queues.password_queue
    - ``get_from``: :class:`str|None`, ``put_from``: :class:`str|None`
    - Raised when :func:`~asyncutils.queues.password_queue` is called, with the names of the variables from which passwords for get and put operations will be retrieved in the caller scope if they are protected, or ``None`` if they are not protected. Of course, the audit hooks do not see the passwords themselves.
  * - asyncutils.queues.SmartQueue.push
    - ``addr``: :class:`int`, ``pushed``: :class:`T`, ``popped``: :class:`T`
    - Raised when the :meth:`push` method of an exact instance of :class:`~asyncutils.queues.SmartQueue[T]` is called and the queue is full, such that an item must be popped, to avoid data loss. ``addr`` is the memory address of the instance, ``pushed`` the item being pushed, and ``popped`` the item being popped.
  * - asyncutils.queues.SmartQueue.transaction/start
    - ``addr``: :class:`int`
    - Raised when the :meth:`~asyncutils.queues.SmartQueue.transaction` method of an exact instance of :class:`~asyncutils.queues.SmartQueue` is called, with ``addr`` being the memory address of the instance.
  * - asyncutils.queues.SmartQueue.transaction/end
    - ``addr``: :class:`int`
    - Raised when the context manager returned by the :meth:`~asyncutils.queues.SmartQueue.transaction` method of an exact instance of :class:`~asyncutils.queues.SmartQueue` exits (the transaction succeeds or fails), with ``addr`` being the memory address of the instance.
  * - asyncutils.queues.SmartQueue.map
    - ``addr``: :class:`int`, ``fname``: :class:`str`
    - Raised when the :meth:`~asyncutils.queues.SmartQueue.map` method of an exact instance of :class:`~asyncutils.queues.SmartQueue` is called, with ``addr`` being the memory address of the instance and ``fname`` the fully qualified name of the transformation function.
  * - asyncutils.queues.SmartQueue.starmap
    - ``addr``: :class:`int`, ``fname``: :class:`str`
    - Raised when the :meth:`~asyncutils.queues.SmartQueue.starmap` method of an exact instance of :class:`~asyncutils.queues.SmartQueue` is called, with ``addr`` being the memory address of the instance and ``fname`` the fully qualified name of the transformation function.
  * - asyncutils.queues.SmartQueue.filter
    - ``addr``: :class:`int`, ``fname``: :class:`str`
    - Raised when the :meth:`~asyncutils.queues.SmartQueue.filter` method of an exact instance of :class:`~asyncutils.queues.SmartQueue` is called, with ``addr`` being the memory address of the instance and ``fname`` the fully qualified name of the predicate.
  * - asyncutils.queues.SmartQueue.enumerate
    - ``addr``: :class:`int`
    - Raised when the :meth:`~asyncutils.queues.SmartQueue.enumerate` method of an exact instance of :class:`~asyncutils.queues.SmartQueue` is called, with ``addr`` being the memory address of the instance.
  * - asyncutils.queues.SmartLifoQueue.push
    - ``addr``: :class:`int`, ``pushed``: :class:`T`, ``popped``: :class:`T`
    - Raised when the :meth:`~asyncutils.queues.SmartLifoQueue.push` method of an exact instance of :class:`~asyncutils.queues.SmartLifoQueue[T]` is called and the queue is full, such that an item must be popped, to avoid data loss. ``addr`` is the memory address of the instance, ``pushed`` the item being pushed, and ``popped`` the item being popped.
  * - asyncutils.queues.SmartLifoQueue.transaction/start
    - ``addr``: :class:`int`
    - Raised when the :meth:`~asyncutils.queues.SmartLifoQueue.transaction` method of an exact instance of :class:`~asyncutils.queues.SmartLifoQueue` is called, with ``addr`` being the memory address of the instance.
  * - asyncutils.queues.SmartLifoQueue.transaction/end
    - ``addr``: :class:`int`
    - Raised when the context manager returned by the :meth:`~asyncutils.queues.SmartLifoQueue.transaction` method of an exact instance of :class:`~asyncutils.queues.SmartLifoQueue` exits (the transaction succeeds or fails), with ``addr`` being the memory address of the instance.
  * - asyncutils.queues.SmartLifoQueue.map
    - ``addr``: :class:`int`, ``fname``: :class:`str`
    - Raised when the :meth:`~asyncutils.queues.SmartLifoQueue.map` method of an exact instance of :class:`~asyncutils.queues.SmartLifoQueue` is called, with ``addr`` being the memory address of the instance and ``fname`` the fully qualified name of the transformation function.
  * - asyncutils.queues.SmartLifoQueue.starmap
    - ``addr``: :class:`int`, ``fname``: :class:`str`
    - Raised when the :meth:`~asyncutils.queues.SmartLifoQueue.starmap` method of an exact instance of :class:`~asyncutils.queues.SmartLifoQueue` is called, with ``addr`` being the memory address of the instance and ``fname`` the fully qualified name of the transformation function.
  * - asyncutils.queues.SmartLifoQueue.filter
    - ``addr``: :class:`int`, ``fname``: :class:`str`
    - Raised when the :meth:`~asyncutils.queues.SmartLifoQueue.filter` method of an exact instance of :class:`~asyncutils.queues.SmartLifoQueue` is called, with ``addr`` being the memory address of the instance and ``fname`` the fully qualified name of the predicate.
  * - asyncutils.queues.SmartLifoQueue.enumerate
    - ``addr``: :class:`int`
    - Raised when the :meth:`~asyncutils.queues.SmartLifoQueue.enumerate` method of an exact instance of :class:`~asyncutils.queues.SmartLifoQueue` is called, with ``addr`` being the memory address of the instance.
  * - asyncutils.queues.SmartPriorityQueue.push
    - ``addr``: :class:`int`, ``pushed``: :class:`T`, ``popped``: :class:`T`
    - Raised when the :meth:`~asyncutils.queues.SmartPriorityQueue.push` method of an exact instance of :class:`~asyncutils.queues.SmartPriorityQueue[T]` is called and the queue is full, such that an item must be popped, to avoid data loss. ``addr`` is the memory address of the instance, ``pushed`` the item being pushed, and ``popped`` the item being popped.
  * - asyncutils.queues.SmartPriorityQueue.transaction/start
    - ``addr``: :class:`int`
    - Raised when the :meth:`~asyncutils.queues.SmartPriorityQueue.transaction` method of an exact instance of :class:`~asyncutils.queues.SmartPriorityQueue` is called, with ``addr`` being the memory address of the instance.
  * - asyncutils.queues.SmartPriorityQueue.transaction/end
    - ``addr``: :class:`int`
    - Raised when the context manager returned by the :meth:`~asyncutils.queues.SmartPriorityQueue.transaction` method of an exact instance of :class:`~asyncutils.queues.SmartPriorityQueue` exits (the transaction succeeds or fails), with ``addr`` being the memory address of the instance.
  * - asyncutils.queues.SmartPriorityQueue.map
    - ``addr``: :class:`int`, ``fname``: :class:`str`
    - Raised when the :meth:`~asyncutils.queues.SmartPriorityQueue.map` method of an exact instance of :class:`~asyncutils.queues.SmartPriorityQueue` is called, with ``addr`` being the memory address of the instance and ``fname`` the fully qualified name of the transformation function.
  * - asyncutils.queues.SmartPriorityQueue.starmap
    - ``addr``: :class:`int`, ``fname``: :class:`str`
    - Raised when the :meth:`~asyncutils.queues.SmartPriorityQueue.starmap` method of an exact instance of :class:`~asyncutils.queues.SmartPriorityQueue` is called, with ``addr`` being the memory address of the instance and ``fname`` the fully qualified name of the transformation function.
  * - asyncutils.queues.SmartPriorityQueue.filter
    - ``addr``: :class:`int`, ``fname``: :class:`str`
    - Raised when the :meth:`~asyncutils.queues.SmartPriorityQueue.filter` method of an exact instance of :class:`~asyncutils.queues.SmartPriorityQueue` is called, with ``addr`` being the memory address of the instance and ``fname`` the fully qualified name of the predicate.
  * - asyncutils.queues.SmartPriorityQueue.enumerate
    - ``addr``: :class:`int`
    - Raised when the :meth:`~asyncutils.queues.SmartPriorityQueue.enumerate` method of an exact instance of :class:`~asyncutils.queues.SmartPriorityQueue` is called, with ``addr`` being the memory address of the instance.
  * - asyncutils.queues.UserPriorityQueue.push
    - ``addr``: :class:`int`, ``pushed``: :class:`T`, ``popped``: :class:`T`
    - Raised when the :meth:`~asyncutils.queues.UserPriorityQueue.push` method of an exact instance of :class:`~asyncutils.queues.UserPriorityQueue[T]` is called and the queue is full, such that an item must be popped, to avoid data loss.
  * - asyncutils.queues.UserPriorityQueue.transaction/start
    - ``addr``: :class:`int`
    - Raised when the :meth:`~asyncutils.queues.UserPriorityQueue.transaction` method of an exact instance of :class:`~asyncutils.queues.UserPriorityQueue` is called, with ``addr`` being the memory address of the instance.
  * - asyncutils.queues.UserPriorityQueue.transaction/end
    - ``addr``: :class:`int`
    - Raised when the context manager returned by the :meth:`~asyncutils.queues.UserPriorityQueue.transaction` method of an exact instance of :class:`~asyncutils.queues.UserPriorityQueue` exits (the transaction succeeds or fails), with ``addr`` being the memory address of the instance.
  * - asyncutils.queues.UserPriorityQueue.map
    - ``addr``: :class:`int`, ``fname``: :class:`str`
    - Raised when the :meth:`~asyncutils.queues.UserPriorityQueue.map` method of an exact instance of :class:`~asyncutils.queues.UserPriorityQueue` is called, with ``addr`` being the memory address of the instance and ``fname`` the fully qualified name of the transformation function.
  * - asyncutils.queues.UserPriorityQueue.starmap
    - ``addr``: :class:`int`, ``fname``: :class:`str`
    - Raised when the :meth:`~asyncutils.queues.UserPriorityQueue.starmap` method of an exact instance of :class:`~asyncutils.queues.UserPriorityQueue` is called, with ``addr`` being the memory address of the instance and ``fname`` the fully qualified name of the transformation function.
  * - asyncutils.queues.UserPriorityQueue.filter
    - ``addr``: :class:`int`, ``fname``: :class:`str`
    - Raised when the :meth:`~asyncutils.queues.UserPriorityQueue.filter` method of an exact instance of :class:`~asyncutils.queues.UserPriorityQueue` is called, with ``addr`` being the memory address of the instance and ``fname`` the fully qualified name of the predicate.
  * - asyncutils.queues.UserPriorityQueue.enumerate
    - ``addr``: :class:`int`
    - Raised when the :meth:`~asyncutils.queues.UserPriorityQueue.enumerate` method of an exact instance of :class:`~asyncutils.queues.UserPriorityQueue` is called, with ``addr`` being the memory address of the instance.
  * - asyncutils.signals.wait_for_signal
    - ``sigs``: :type:`tuple[int, ...]`
    - Raised when :func:`~asyncutils.signals.wait_for_signal` is called on signal numbers ``sigs``.
  * - asyncutils.util.sync_await
    - ``atname``: :class:`str`
    - Raised when :func:`~asyncutils.util.sync_await` is called on an awaitable whose type is of name ``atname``.
  * - asyncutils.util.to_async
    - ``fname``: :class:`str`
    - Raised when :func:`~asyncutils.util.to_async` is called on a function with name ``fname``.
  * - asyncutils.util.to_sync
    - ``fname``: :class:`str`
    - Raised when :func:`~asyncutils.util.to_sync` is called on a function with name ``fname``.
