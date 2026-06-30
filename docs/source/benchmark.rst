Benchmarks
==========

  "Statistics are like bikinis. What they reveal is suggestive, but what they conceal is vital."

  .. cspell:disable-next-line

  -- Aaron Levenstein, 1951

.. note::
  :collapsible: closed

  The above quote is not to downplay the importance of this document, but the performance of async code depends heavily on the event loop
  implementation, which is not well captured by this data because only import time is counted.

When used as a REPL (Read-Eval-Print Loop), this module starts slow since it builds on the standard library :mod:`asyncio`, which loads all its
submodules on import, and the event loop is quite difficult to implement. This is understandable but suboptimal. On the contrary, we focus on
simplifying boilerplate-heavy code and integrating and combining existing patterns seamlessly with a set of core utilities, so :mod:`asyncutils` is
not at all heavy in terms of import time. In addition, you only pay for what you use; the parts of the code you don't call are not executed until
you request them to be, thanks to cleanly separated submodules with somewhat simplistic dependency graphs. This module is overall fast and light
because of its design goals and philosophy.

The figures below are obtained by running each of the following sequentially with no warmup elevenfold in a fresh console session, then discarding
the first run because it is treated as a warmup:

Environment
-----------

* ``python -VV`` gives: ``Python 3.14.6 (tags/v3.14.6:c63aec6, Jun 10 2026, 10:26:10) [MSC v.1944 64 bit (AMD64)]``
* ``python -m platform`` gives: ``Windows-11-10.0.26200-SP0``
* With ``__pycache__`` directories persisted across runs

It would be very nice if somebody could do the benchmarks on Ubuntu or other platforms and add a new section with the same structure detailing the
results, since asyncio works drastically different on Windows than other systems.

.. note:: The user and sys measurements below have a granularity of 15 ms.

Baseline: asyncio
-----------------

::

  python -SIqX importtime -c "import asyncio"

Cumulative import time of asyncio: 122.60 ± 10.14 ms; max 138.83 ms, min 103.49 ms; n = 10

::

  time printf "raise SystemExit\n" | python -SIqm asyncio 2>/dev/null

Time taken to start and immediately exit the asyncio console:

* real: 500.7 ± 14.5 ms; max 520 ms, min 474 ms
* user: 42.0 ± 28.1 ms; max 105 ms, min 15 ms
* sys: 67.5 ± 19.1 ms; max 90 ms, min 30 ms

n = 10

.. note:: This includes Python startup time and immense I/O and process overhead with piping.
.. note::
  The time command is not really a benchmarking tool, so these are rounded to 0.1 ms. It is also run in Git Bash on a slow computer. This must be
  improved on in the future.

asyncutils
----------

::

  python -SIqX importtime -c "import asyncutils"

Cumulative import time of asyncutils: 147.34 ± 7.53 ms; max 156.40 ms, min 131.94 ms; n = 10

.. note::
  :collapsible:

  The figures below are relative to the time when ``asyncutils/__init__.py`` is executed, and may not reflect the actual time taken, because Python
  is not free to boot up itself, having to perform various initialization tasks.

::

  python -SIqm asyncutils -dl

Time taken to start the console, which includes importing :mod:`asyncio`: 99.89 ± 6.19 ms; max 110.25 ms, min 91.97 ms, n = 10

::

  python -SIqm asyncutils -dpl

Time taken to import :mod:`asyncio` along with all 31 ordinary submodules: 196.96 ± 18.30 ms; max 225.08 ms, min 172.51 ms, n = 10

.. note:: Up to 10 required internal submodules are also fetched.

::

  time printf "raise SystemExit\n" | asyncutils 2>/dev/null

Time taken to start and immediately exit the asyncutils console, timed like the asyncio console:

* real: 380.8 ± 22.7 ms; max 412 ms, min 350 ms
* user: 25.5 ± 17.4 ms; max 45 ms, min 0 ms
* sys: 37.5 ± 17.7 ms; max 60 ms, min 0 ms

n = 10

::

  time printf "load_all()\nraise SystemExit\n" | asyncutils 2>/dev/null

The above including all submodules:

* real: 485.3 ± 12.2 ms; max 506 ms, min 459 ms
* user: 19.5 ± 10.1 ms; max 30 ms, min 0 ms
* sys: 55.5 ± 17.4 ms; max 90 ms, min 30 ms

n = 10

.. note::
  :collapsible:

  :mod:`asyncio` is still loaded early such that attribute accesses later on would not randomly take more than 100 ms, and you logically wouldn't use
  this module without an async entry point, such that asyncio and its event loop are crucial and unavoidable.
