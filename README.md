# asyncutils (unfortunately py-asyncutils on pip)

A python library abstracting common patterns that somehow always pop up in async code.

Includes a wide range of submodules tailored for specific usages, though concrete implementations are lacking.

Prides in being as fast as can be in terms of import time, with detailed type checking provided via stub files included in the distribution.

Also has a well-equipped command line interface taking many flags and options.

A typical program that uses this module would look like this:

\# demo.py

    import asyncutils as autils
    with autils.event_loop() as loop: # this wraps the asyncio event loop implementation with proper cleanup
        rdv = autils.Rendezvous[int](loop=loop) # some types support subscripting
        print(*(loop.run_until_complete(asyncio.gather(*map(rdv.put, range(10, 20)), rdv.exchange(20),\
        *map(rdv.exchange, range(1, 10)), *(rdv.get() for _ in range(10)))))[20:]) # simulate some work with values passed between tasks
        # Here Rendezvous is a class implementing get and put methods that complete only after there is a corresponding putter or getter

which prints `1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20` in 175 ms including the import time of both modules! For reference, asyncio loads in around 160-165 ms. TL;DR, the only reason this module starts slow is due to asyncio loading all its submodules on import, which is frankly suboptimal. Command used:

    python3 -m timeit -n 1 -r 1 "import demo"

The above demo may be considered bad practice in that the shortened names (`autils.event_loop`, `autils.Rendezvous`) are used instead of the fully qualified names (`asyncutils.base.event_loop`, `asyncutils.channels.Rendezvous`), though considering how many submodules we provide (30 and ever-increasing!), it is acceptable. In fact, the submodules are only loaded on demand by a sophisticated name exposure system, unless the -p/--load-all switch is passed.

It is strongly recommended that you read the [asyncio docs](https://docs.python.org/3/library/asyncio.html) thoroughly if using event loop related features.

Other resources if you're new to the world of async: [asyncio HOWTO](https://docs.python.org/3/howto/a-conceptual-overview-of-asyncio.html#a-conceptual-overview-of-asyncio), [Real Python's Async IO Tutorial](https://realpython.com/async-io-python/), [Python Async Basics Video Guide](https://www.youtube.com/watch?v=t5Bo1Je9EmE)

Have fun!

![GitHub release](https://img.shields.io/github/v/release/jonathandung/asyncutils)
![GitHub Release Date](https://img.shields.io/github/release-date/jonathandung/asyncutils)
![GitHub last commit](https://img.shields.io/github/last-commit/jonathandung/asyncutils)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/jonathandung/asyncutils)
![GitHub issues](https://img.shields.io/github/issues/jonathandung/asyncutils)
![GitHub pull requests](https://img.shields.io/github/issues-pr/jonathandung/asyncutils)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![GitHub stars](https://img.shields.io/github/stars/jonathandung/asyncutils?style=social)
![GitHub forks](https://img.shields.io/github/forks/jonathandung/asyncutils?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/jonathandung/asyncutils?style=social)
![GitHub contributors](https://img.shields.io/github/contributors/jonathandung/asyncutils)
![GitHub](https://img.shields.io/github/followers/jonathandung?style=social)