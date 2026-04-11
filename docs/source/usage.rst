Usage
=====

A simple program that uses this module would look like this:

.. code-block:: python

    import asyncutils as autils, asyncio as aio
    with autils.event_loop(check_running=True) as loop:
        # this wraps the asyncio event loop implementation with proper cleanup
        rdv = autils.Rendezvous[int](loop=loop) # some types support subscripting
        print(*(loop.run_until_complete(aio.gather(*map(rdv.put, range(10, 20)), rdv.exchange(20), *map(rdv.exchange, range(1, 10)), *(rdv.get() for
        _ in range(10)))))[10:])
        # simulate some work with values passed between tasks
        # Here Rendezvous is a class implementing get and put methods that complete only after there is a corresponding putter or getter respectively

This prints ``1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20`` in 170 ms including the import time of asyncio, which needs around 160 ms to load!
That is, the only reason this module starts slow is due to asyncio loading all its submodules on import, which is frankly suboptimal. However, we
still load asyncio early such that attribute accesses later on would not randomly take more than 150 ms.

Command used:

.. code-block:: bash

    python -S -E -I -m timeit -n 1 -r 1 "
    import asyncutils as autils, asyncio as aio
    with autils.event_loop(check_running=True) as loop:
        rdv = autils.Rendezvous[int](loop=loop)
        print(*(loop.run_until_complete(aio.gather(*map(rdv.put, range(10, 20)), rdv.exchange(20), *map(
            rdv.exchange, range(1, 10)), *(rdv.get() for _ in range(10)))))[10:])
    "

The above demo may be considered bad practice in that the shortened names (``autils.event_loop``, ``autils.Rendezvous``) are used instead of the
fully-qualified names (``autils.base.event_loop``, ``autils.channels.Rendezvous``), though considering how many submodules we provide (32 and
ever-increasing!), it is acceptable. In fact, the submodules are only loaded on demand by a sophisticated name exposure system, unless the
``--load-all`` switch is passed.
