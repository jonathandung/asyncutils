Benchmarks
==========

When used as a REPL (Read-Eval-Print Loop), this module starts slow since it builds on the standard library :mod:`asyncio`, which loads all its
submodules on import, and the event loop is quite difficult to implement. This is understandable but suboptimal. On the contrary, we focus on
simplifying boilerplate-heavy code and integrating and combining existing patterns seamlessly with a set of core utilities, so :mod:`asyncutils` is
not at all heavy in terms of import time. In addition, you only pay for what you use; the parts of the code you don't call are not executed until
you request them to be, thanks to cleanly separated submodules with somewhat simplistic dependency graphs. This module is overall fast, light and
tightly coupled to the ever-evolving asyncio ecosystem, because of its design goals and philosophy, so have some concrete figures:

Below are obtained by running each of the following commands sequentially with no warmup:

.. code-block:: bash

  python -SEqX importtime -c "import asyncutils"

Cumulative import time of asyncutils: 7774 ± 653 μs; max 8786 μs, min 6708 μs, n = 12

.. code-block:: bash

  python -SEqX importtime -m asyncutils

Time taken to initialize all submodules (and import asyncio): 122.0 ± 9.5 ms; max 136.4 ms, min 109.1 ms, n = 10

.. note::
  :collapsible:

  We still load asyncio early such that attribute accesses later on would not randomly take more than 150 ms. However, this is not guaranteed when
  the library is imported, because a different initialization and bootstrapping path is taken. As the above results show, asyncio must not have been
  loaded in such a short interval.
