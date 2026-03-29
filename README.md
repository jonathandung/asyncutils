# asyncutils (unfortunately py-asyncutils on pip)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/py-asyncutils)
![PyPI version](https://badge.fury.io/py/py-asyncutils.svg)
![Coverage](https://codecov.io/gh/jonathandung/asyncutils/branch/main/graph/badge.svg?token=PTRNW1RGXA)
![Build](https://github.com/jonathandung/asyncutils/actions/workflows/python-package.yaml/badge.svg)
![Publish](https://github.com/jonathandung/asyncutils/actions/workflows/python-publish.yaml/badge.svg)
![Conda](https://github.com/jonathandung/asyncutils/actions/workflows/test-conda.yaml/badge.svg)
![Docs](https://app.readthedocs.org/projects/asyncutils/badge)

A python library abstracting all the common patterns the creator can think of that somehow always pop up in async code.

Includes a wide range of submodules tailored for specific usages, though concrete implementations are lacking.

Prides in being as fast as can be in terms of import time, with detailed type checking provided via stub files included in the distribution.

Also has a well-equipped command line interface taking many flags and options.

## Setup

Since the name `asyncutils` was somehow unavailable on PyPI, `py-asyncutils` was chosen instead.
Packaging for conda has also been done via conda-forge.
You can install using either conda or pip, or directly from roughly forthnightly GitHub releases; no extra setup is needed.
See [installation.rst](https://github.com/jonathandung/asyncutils/blob/main/docs/source/installation.rst) for more.

## Usage

A simple program that uses this module would look like this:

`# demo.py`

```python
import asyncutils as autils, asyncio as aio
with autils.event_loop(check_running=True) as loop:
    # this wraps the asyncio event loop implementation with proper cleanup
    rdv = autils.Rendezvous[int](loop=loop) # some types support subscripting
    print(*(loop.run_until_complete(aio.gather(*map(rdv.put, range(10, 20)), rdv.exchange(20), *map(
        rdv.exchange, range(1, 10)), *(rdv.get() for _ in range(10)))))[10:])
    # simulate some work with values passed between tasks
    # Here `Rendezvous` is a class implementing get and put methods that complete only after there is
    # a corresponding putter or getter respectively
```

This prints `1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20` in 190 ms including the import time of asyncio, which needs around
160-165 ms to load! That is, the only reason this module starts slow is due to asyncio loading all its submodules on import, which is
frankly suboptimal. However, we still load asyncio early such that attribute accesses later on would not randomly take more than 150 ms.

Command used:

```bash
python -m timeit -n 1 -r 1 "import demo"
```

The above demo may be considered bad practice in that the shortened names (`autils.event_loop`, `autils.Rendezvous`) are used instead of the
fully qualified names (`asyncutils.base.event_loop`, `asyncutils.channels.Rendezvous`), though considering how many submodules we provide (32
and ever-increasing!), it is acceptable. In fact, the submodules are only loaded on demand by a sophisticated name exposure system, unless the
`--load-all` switch is passed.

## Version

This is asyncutils v0.8.20.

This library is currently in the alpha stage, meaning the public API is subject to change even between patch versions, and changes made may be
backward-incompatible. (Of course, this isn't a significant issue, seeing as though nobody currently uses it.)

## Environment variables and configuration

Besides using command line arguments to change console settings, the behaviour of this module as a library can be customized as well.
This includes aspects such as where to output logging, customizing the underlying executor type used, and setting a seed for random number generation using the `AUTILSCFGPATH` environment variable (all uppercase due to Windows limitations),
which should point to an absolute path to a configuration .json[l].

See [format.jsonc](https://github.com/jonathandung/asyncutils/blob/main/format.jsonc) for details.

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
![GitHub stars](https://img.shields.io/github/stars/jonathandung/asyncutils?style=social)
![GitHub forks](https://img.shields.io/github/forks/jonathandung/asyncutils?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/jonathandung/asyncutils?style=social)
![GitHub contributors](https://img.shields.io/github/contributors/jonathandung/asyncutils)
![GitHub](https://img.shields.io/github/followers/jonathandung?style=social)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/py-asyncutils)
![PyPI - License](https://img.shields.io/pypi/l/py-asyncutils)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/py-asyncutils)
![PyPI - Format](https://img.shields.io/pypi/format/py-asyncutils)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)
![Tests](https://github.com/jonathandung/asyncutils/blob/main/tests.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)
