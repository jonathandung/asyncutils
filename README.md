# asyncutils (unfortunately py-asyncutils on pip)

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/py-asyncutils)](https://www.python.org/downloads)
[![PyPI version](https://badge.fury.io/py/py-asyncutils.svg)](https://pypi.org/p/py-asyncutils)
[![Coverage](https://codecov.io/gh/jonathandung/asyncutils/branch/main/graph/badge.svg?token=PTRNW1RGXA)](https://app.codecov.io/gh/jonathandung/asyncutils)
[![Tests](https://github.com/jonathandung/asyncutils/blob/main/assets/tests.svg)](https://github.com/jonathandung/asyncutils/tree/main/tests)
[![Build](https://github.com/jonathandung/asyncutils/actions/workflows/python-package.yaml/badge.svg)](https://github.com/jonathandung/asyncutils/actions/workflows/python-publish.yaml)
[![Publish](https://github.com/jonathandung/asyncutils/actions/workflows/python-publish.yaml/badge.svg)](https://github.com/jonathandung/asyncutils/actions/workflows/python-publish.yaml)
[![pre-commit.ci](https://results.pre-commit.ci/badge/github/jonathandung/asyncutils/main.svg)](https://results.pre-commit.ci/latest/github/jonathandung/asyncutils/main)
[![Docs](https://app.readthedocs.org/projects/asyncutils/badge)](https://asyncutils.readthedocs.io/en/stable)
[![Blazingly fast](https://www.blazingly.fast/api/badge.svg?repo=jonathandung%2Fasyncutils)](https://www.blazingly.fast)

A python library abstracting all the common patterns I can think of that somehow always pop up in async code.

Includes a wide range of submodules tailored for specific usages, though concrete low-level implementations are lacking.

Takes pride in:

- being as fast as can be in terms of import time
- providing detailed type checking via stub files included in the distribution
- having a well-equipped command line interface taking many flags and options

## Setup

I am not sure how this package would work on alternate python implementations. However, it is set to be extensively tested on CPython.

Since the name 'asyncutils' was somehow unavailable on PyPI, 'py-asyncutils' was chosen instead.

This package is also [available on anaconda](https://anaconda.org/channels/conda-forge/packages/py-asyncutils/overview) via the conda-forge channel.

You can install using either conda or pip, or directly from roughly fortnightly GitHub releases; no extra setup is needed.

See the [installation guide](https://asyncutils.readthedocs.io/en/stable/installation.html) for more.

## Usage

This package is very resourceful, containing everything from higher-order error handling functions to network protocols.

See the [usage guide](https://asyncutils.readthedocs.io/en/stable/usage.html) for some basic examples.

## Version

This is asyncutils v0.9.1.

This library is currently in the beta stage, meaning the public API is subject to change even between patch versions, and changes made may be
backward-incompatible. See [the compatibility page](https://asyncutils.readthedocs.io/en/stable/compat.html).

See [this page](https://github.com/jonathandung/asyncutils/tags) for the version tags up to now. Many older tags are obsolete and were deleted.

## Configuration

Besides using command line arguments to change console settings, the behaviour of this module as a library can be customized as well.

See the [configuration guide](https://asyncutils.readthedocs.io/en/stable/config.html).

## Remarks

It is strongly recommended that you read the [asyncio docs](https://docs.python.org/3/library/asyncio.html) thoroughly if using event loop related
features.

Other resources if you're new to the world of async:

- [asyncio HOWTO](https://docs.python.org/3/howto/a-conceptual-overview-of-asyncio.html)
- [Basic tutorial](https://realpython.com/async-io-python)
- [Basic video guide](https://www.youtube.com/watch?v=t5Bo1Je9EmE)
- [asyncio, threading, multiprocessing](https://www.youtube.com/watch?v=0vFgKr5bjWI)
- [Event loop](https://www.youtube.com/watch?v=RIVcqT2OGPA)
- [In-depth tutorial](https://www.youtube.com/watch?v=oAkLSJNr5zY)

## Contributing

If you have suggestions for how asyncutils could be improved, or want to report a bug, do open an issue! All contributions are welcome.

For more, check out the [contributing guide](https://github.com/jonathandung/asyncutils/blob/main/CONTRIBUTING.md).

## License

[MIT](https://github.com/jonathandung/asyncutils/blob/main/LICENSE) © 2026 Jonathan Dung

Have fun!

| GitHub | Repo | Package | Uses | | Status |
| --- | --- | --- | --- | --- | --- |
| ![GitHub release](https://img.shields.io/github/v/release/jonathandung/asyncutils) | ![Project stars](https://img.shields.io/github/stars/jonathandung/asyncutils?style=social) | ![Conda version](https://anaconda.org/conda-forge/py-asyncutils/badges/version.svg) | ![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json) | ![Pytest](https://img.shields.io/badge/tests-Pytest-yellow?logo=pytest) | ![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg) |
| ![GitHub release date](https://img.shields.io/github/release-date/jonathandung/asyncutils) | ![GitHub forks](https://img.shields.io/github/forks/jonathandung/asyncutils?style=social) | ![Noarch](https://anaconda.org/conda-forge/py-asyncutils/badges/platforms.svg) | ![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit) | ![Sphinx-lint](https://img.shields.io/badge/sphinx-sphinx--lint-darkblue?logo=sphinx) | ![Contributions Welcome](https://img.shields.io/static/v1.svg?label=Contributions&message=Welcome&color=brightgreen) |
| ![GitHub last commit](https://img.shields.io/github/last-commit/jonathandung/asyncutils) | ![GitHub watchers](https://img.shields.io/github/watchers/jonathandung/asyncutils?style=social) | ![PyPI - Wheel](https://img.shields.io/pypi/wheel/py-asyncutils) | ![Mypy](https://img.shields.io/badge/mypy-checked-blue?logo=python&&logoColor=blue) | ![Read the Docs](https://img.shields.io/badge/docs-Read_the_Docs-green?logo=readthedocs) | ![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg) |
| ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/jonathandung/asyncutils) | ![GitHub](https://img.shields.io/github/followers/jonathandung?style=social) | ![PyPI - Format](https://img.shields.io/pypi/format/py-asyncutils) | ![SemVer](https://img.shields.io/badge/semver-2.0.0-green?logo=semver) | ![Actionlint](https://img.shields.io/badge/actions-actionlint-yellow) | ![Beta](https://img.shields.io/badge/stage-beta-yellow.svg) |
| ![GitHub issues](https://img.shields.io/github/issues/jonathandung/asyncutils) | ![User stars](https://img.shields.io/github/stars/jonathandung) | ![PyPI - License](https://img.shields.io/pypi/l/py-asyncutils) | ![Sphinx](https://img.shields.io/badge/docs-sphinx-265094?logo=sphinx) | ![setuptools](https://img.shields.io/badge/packaged_with-setuptools-brightgreen?logo=setuptools) | |
| ![GitHub pull requests](https://img.shields.io/github/issues-pr/jonathandung/asyncutils) | ![Repo creation](https://img.shields.io/github/created-at/jonathandung/asyncutils) | ![PyPI - Downloads](https://img.shields.io/pypi/dm/py-asyncutils) | ![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json) | ![PyPI](https://img.shields.io/badge/on-pypi-blue?logo=pypi) | |
| ![GitHub contributors](https://img.shields.io/github/contributors/jonathandung/asyncutils) | ![GitHub repo size](https://img.shields.io/github/repo-size/jonathandung/asyncutils) | ![Conda-forge](https://img.shields.io/conda/v/conda-forge/py-asyncutils?logo=condaforge) | ![Stubtest](https://img.shields.io/badge/stubtest-checked-blue) | ![Conda](https://img.shields.io/badge/on-conda-green?logo=anaconda) | |
| ![Commits since last release](https://img.shields.io/github/commits-since/jonathandung/asyncutils/latest.svg) | | | ![detect-secrets](https://img.shields.io/badge/detect--secrets-checked-blue?logo=yelp) | ![conda-forge](https://img.shields.io/badge/via-conda--forge-blue?logo=conda-forge) | |
