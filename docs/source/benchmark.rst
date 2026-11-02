Benchmarks
==========

  "Statistics are like bikinis. What they reveal is suggestive, but what they conceal
  is vital."

  -- Aaron Levenstein, 1951

When used as a REPL (Read-Eval-Print Loop), this module starts slow since it builds on
the standard library :mod:`asyncio`, which loads all its submodules on import, and the
event loop is quite difficult to implement.

The figures below are obtained by running each of the following sequentially with no
warmup elevenfold in a fresh console session and discarding the first run, which is
considered a warmup run:

Environment
-----------

Benchmarked on an old HP laptop.

* ``python -VV`` gives
  ``Python 3.15.2 (main, Oct 26 2026, 14:23:21) [MSC v.1951 64 bit (AMD64)]``
* ``python -m platform`` gives ``Windows-11-10.0.26300-SP0``
* ``__pycache__`` directories are persisted across runs

Baseline: asyncio
-----------------

::

  python -SIqX importtime -c "import asyncio"

Cumulative import time of asyncio: 122.60 ± 10.14 ms; max 138.83 ms, min 103.49 ms; n = 10

.. note:: Above, 122.60 ms is the mean and 10.14 ms is the standard deviation.

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

.. note::
  :collapsible:

  :mod:`asyncio` is still loaded early such that attribute accesses later on would not randomly take more than 100 ms, and you logically wouldn't use
  this module without an async entry point, such that asyncio and its event loop are crucial and unavoidable.
