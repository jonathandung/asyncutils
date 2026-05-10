Benchmarks
==========

When used as a REPL (Read-Eval-Print Loop), this module starts slow since it builds on the standard library :mod:`asyncio`, which loads all its
submodules on import, and the event loop is quite difficult to implement. This is understandable but suboptimal. On the contrary, we focus on
simplifying boilerplate-heavy code and integrating and combining existing patterns seamlessly with a set of core utilities, so :mod:`asyncutils` is
not at all heavy in terms of import time. In addition, you only pay for what you use; the parts of the code you don't call are not executed until
you request them to be, thanks to cleanly separated submodules with somewhat simplistic dependency graphs. This module is overall fast, light and
tightly coupled to the ever-evolving asyncio ecosystem, because of its design goals and philosophy.

The figures below are obtained by running each of the following sequentially with no warmup tenfold in a fresh console session:

Baseline:

.. code-block:: bash

  python -SEqX importtime -c "import asyncio"

Cumulative import time of asyncio: 115.1 ± 12.4 ms; max 134.4 ms, min 103.3 ms; n = 10

.. code-block:: bash

  python -SEqX importtime -c "import asyncutils"

Cumulative import time of asyncutils: 123.8 ± 12.6 ms; max 138.3 ms, min 107.9 ms; n = 10

.. code-block:: bash

  python -SEqm asyncutils -d

Time taken to start the console with asyncio imported: 122.1 ± 9.5 ms; max 136.5 ms, min 109.2 ms, n = 10

.. code-block:: bash

  python -SEqm asyncutils -dp

Time taken to actually import asyncio and all 32 submodules: 266.2 ± 13.2 ms; max 282.4 ms, min 237.0 ms, n = 10

.. note::
  :collapsible:

  :mod:`asyncio` is still loaded early such that attribute accesses later on would not randomly take more than 150 ms.
