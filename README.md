# asyncutils (unfortunately py-asyncutils on pip)

A python library abstracting all the common patterns the creator can think of that somehow always pop up in async code.

Includes a wide range of submodules tailored for specific usages, though concrete implementations are lacking.

Prides in being as fast as can be in terms of import time, with detailed type checking provided via stub files included in the distribution.

Also has a well-equipped command line interface taking many flags and options.

## Setup

Essentially no setup required! Just install py-asyncutils from pip:

```bash
python -m pip install py-asyncutils==0.8.18 # This version
```

or

```bash
python -m pip install py-asyncutils[dev] # If installing for development
# currently installs ruff, pytest and some plugins thereof
```

or with conda:

```bash
conda install -c conda-forge py-asyncutils=0.8.18
```

Refer to [SUPPORT.md](https://github.com/jonathandung/asyncutils/blob/main/SUPPORT.md) for steps to checking the installation.

## Usage

A typical program that uses this module would look like this:

`# demo.py`

```python
import asyncutils as autils
with autils.event_loop() as loop: # this wraps the asyncio event loop implementation with proper cleanup
    rdv = autils.Rendezvous[int](loop=loop) # some types support subscripting
    print(*(loop.run_until_complete(asyncio.gather(*map(rdv.put, range(10, 20)), rdv.exchange(20),
    *map(rdv.exchange, range(1, 10)), *(rdv.get() for _ in range(10)))))[10:])
    # simulate some work with values passed between tasks
    # Here `Rendezvous` is a class implementing get and put methods that complete only after there is
    # a corresponding putter or getter respectively
```

which prints `1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20` in 175 ms including the import time of both modules! For reference, asyncio loads in around 160-165 ms.
That is, the only reason this module starts slow is due to asyncio loading all its submodules on import, which is frankly suboptimal.
However, we load asyncio early such that attribute accesses later on would not randomly take more than 150 ms.

Command used:

```bash
python -m timeit -n 1 -r 1 "import demo"
```

The above demo may be considered bad practice in that the shortened names (`autils.event_loop`, `autils.Rendezvous`) are used instead of the fully qualified names (`asyncutils.base.event_loop`, `asyncutils.channels.Rendezvous`),
though considering how many submodules we provide (30 and ever-increasing!), it is acceptable.
In fact, the submodules are only loaded on demand by a sophisticated name exposure system, unless the `--load-all` switch is passed.

## Version

This is asyncutils v0.8.18.

This library is currently in alpha stage, meaning the public API is subject to change even between patch versions, and changes made may be backward-incompatible.
Of course, this isn't a significant issue, seeing as though nobody currently uses it.

## Environment variables and configuration

Besides using command line arguments to change console settings, the behaviour of this module as a library can be customized as well.
This includes aspects such as where to output logging, customizing the underlying executor type used, and setting a seed for random number generation using the `AUTILSCFGPATH` environment variable (all uppercase due to Windows limitations),
which should point to an absolute path to a configuration .json[l].

See [format.jsonc](asyncutils/format.jsonc) for details.

## Remarks

It is strongly recommended that you read the [asyncio docs](https://docs.python.org/3/library/asyncio.html) thoroughly if using event loop related features.

Other resources if you're new to the world of async: [asyncio HOWTO](https://docs.python.org/3/howto/a-conceptual-overview-of-asyncio.html#a-conceptual-overview-of-asyncio), [Real Python's Async IO Tutorial](https://realpython.com/async-io-python/), [Python Async Basics Video Guide](https://www.youtube.com/watch?v=t5Bo1Je9EmE)

## Contributing

If you have suggestions for how asyncutils could be improved, or want to report a bug, do open an issue! All contributions are welcome.

For more, check out the [Contributing Guide](https://github.com/jonathandung/asyncutils/blob/main/CONTRIBUTING.md).

## License

[MIT](https://github.com/jonathandung/asyncutils/blob/main/LICENSE) © 2026 Jonathan Dung

Have fun!

![GitHub release](https://img.shields.io/github/v/release/jonathandung/asyncutils)
![GitHub release date](https://img.shields.io/github/release-date/jonathandung/asyncutils)
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
![PyPI version](https://badge.fury.io/py/py-asyncutils.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/py-asyncutils)
![PyPI - Downloads](https://img.shields.io/pypi/dm/py-asyncutils)
![PyPI - License](https://img.shields.io/pypi/l/py-asyncutils)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/py-asyncutils)
![PyPI - Format](https://img.shields.io/pypi/format/py-asyncutils)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)
![Build](https://github.com/jonathandung/asyncutils/actions/workflows/python-package.yaml/badge.svg)
![Publish](https://github.com/jonathandung/asyncutils/actions/workflows/python-publish.yaml/badge.svg)
![Tests](https://github.com/jonathandung/asyncutils/blob/main/badges/tests.svg)
![Coverage](https://app.codecov.io/gh/jonathandung/asyncutils/branch/main/graph/badge.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)
