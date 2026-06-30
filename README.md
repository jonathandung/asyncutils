# asyncutils

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/py-asyncutils)](https://www.python.org/downloads)
[![PyPI version](https://badge.fury.io/py/py-asyncutils.svg)](https://pypi.org/p/py-asyncutils)
[![Coverage](https://raw.githubusercontent.com/jonathandung/asyncutils/main/badges/coverage.svg)](https://github.com/jonathandung/asyncutils/tree/main/tests)
[![Build](https://github.com/jonathandung/asyncutils/actions/workflows/push.yaml/badge.svg)](https://github.com/jonathandung/asyncutils/actions/workflows/python-package.yaml)
[![CodeQL](https://github.com/jonathandung/asyncutils/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/jonathandung/asyncutils/actions/workflows/github-code-scanning/codeql)
[![Publish](https://github.com/jonathandung/asyncutils/actions/workflows/release.yaml/badge.svg)](https://github.com/jonathandung/asyncutils/actions/workflows/python-publish.yaml)
[![GitHub Pages](https://github.com/jonathandung/asyncutils/actions/workflows/deploy.yaml/badge.svg)](https://jonathandung.github.io/asyncutils)
[![Dependabot](https://github.com/jonathandung/asyncutils/actions/workflows/dependabot/update-graph/badge.svg)](https://github.com/jonathandung/asyncutils/actions/workflows)
[![pre-commit.ci](https://results.pre-commit.ci/badge/github/jonathandung/asyncutils/main.svg)](https://results.pre-commit.ci/latest/github/jonathandung/asyncutils/main)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/13018/badge)](https://www.bestpractices.dev/projects/13018)
[![Read the Docs: stable build](https://img.shields.io/readthedocs/asyncutils/stable?logo=readthedocs&label=docs%20(stable))](https://asyncutils.readthedocs.io/en/stable)
[![Read the Docs: latest build](https://img.shields.io/readthedocs/asyncutils/latest?logo=readthedocs)](https://asyncutils.readthedocs.io/en)
[![Conda version](https://anaconda.org/conda-forge/py-asyncutils/badges/version.svg)](https://anaconda.org/channels/conda-forge/packages/py-asyncutils/overview)
[![conda-forge feedstock](https://img.shields.io/conda/v/conda-forge/py-asyncutils?logo=condaforge)](https://github.com/conda-forge/py-asyncutils-feedstock)
[![Contributor Covenant](https://img.shields.io/badge/Contributor_Covenant-v3.0-ff69b4.svg?logo=contributor-covenant&logoColor=purple)](https://asyncutils.readthedocs.io/en/stable/conduct.html)

A Python library abstracting all the common patterns I can think of that somehow always pop up in async code.

Takes pride in:

- being as fast as can be in terms of import time
- providing detailed type checking via stub files included in the distribution
- having a well-equipped command line interface taking many flags and options

## Setup

Make sure you have CPython 3.12 or above; even a pre-release of 3.15 will do. GraalPy 25.0 or above is also acceptable. You should have at least one
Python package manager you are comfortable with. CPython free-threaded and debug builds are also supported. I have plans to support PyPy, but they are
currently lagging behind the releases of the reference implementation and a 3.11 backport would be required, which is not going to happen.

The support for GraalPy is also experimental and I don't think its particular performance benefits would apply to this library, provided that part of
`asyncio` is written in C, and GraalPy's `asyncio` doesn't support Windows yet.

Discounting the installation, no extra setup is needed. See the [installation guide](https://asyncutils.readthedocs.io/en/stable/installation.html)
for more.

## Usage

This package is very resourceful, containing everything from higher-order error handling functions to network protocols. See the
[usage guide](https://asyncutils.readthedocs.io/en/stable/examples.html) for some basic examples.

## Version

This is asyncutils v1.0.1. For your reference, here are [all version tags up to now](https://github.com/jonathandung/asyncutils/tags).

## Configuration

Besides using command line arguments to change console settings, the behaviour of this module as a library can be customized as well. See the
[configuration guide](https://asyncutils.readthedocs.io/en/stable/config.html).

## Remarks

It is strongly recommended that you read the [asyncio docs](https://docs.python.org/3/library/asyncio.html) thoroughly if using event loop and async
generator related features, since their behaviours are central points of confusion and have troubled me greatly in the development of this library.

## Resources

Here are some resources if you're new to the world of async. They were of great assistance when I was learning async (I still am):

- [asyncio how-to](https://docs.python.org/3/howto/a-conceptual-overview-of-asyncio.html)
- [Basic walkthrough](https://realpython.com/async-io-python)
- [Basic video guide](https://www.youtube.com/watch?v=t5Bo1Je9EmE)
- [asyncio, threading, multiprocessing](https://www.youtube.com/watch?v=0vFgKr5bjWI)
- [Event loop](https://www.youtube.com/watch?v=RIVcqT2OGPA)
- [In-depth tutorial](https://www.youtube.com/watch?v=oAkLSJNr5zY)

## Contributing

If you have suggestions for how asyncutils could be improved, or want to report a bug, do open an issue! All contributions are welcome.
For more, check out the [contributing guide](https://asyncutils.readthedocs.io/en/stable/contributing.html).

## License

[MIT](https://github.com/jonathandung/asyncutils/blob/main/LICENSE) © 2026 Jonathan Dung

## Badges

| GitHub | Repo | Package | Uses | Status | Tests |
| --- | --- | --- | --- | --- | --- |
| ![GitHub release](https://img.shields.io/github/v/release/jonathandung/asyncutils) | ![Project stars](https://img.shields.io/github/stars/jonathandung/asyncutils?style=social) | ![PyPI - Implementation](https://img.shields.io/pypi/implementation/py-asyncutils) | ![Build backend](https://img.shields.io/badge/build_backend-uv-261230?logo=uv) | ![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg) | ![Tests](https://raw.githubusercontent.com/jonathandung/asyncutils/main/badges/tests.svg) |
| ![GitHub release date](https://img.shields.io/github/release-date-pre/jonathandung/asyncutils) | ![GitHub forks](https://img.shields.io/github/forks/jonathandung/asyncutils?style=social) | ![Noarch](https://anaconda.org/conda-forge/py-asyncutils/badges/platforms.svg) | ![ruff](https://img.shields.io/badge/linter-ruff-261230?logo=ruff) | ![Issues Welcome](https://img.shields.io/badge/Issues-Welcome-brightgreen) | ![Warnings](https://raw.githubusercontent.com/jonathandung/asyncutils/main/badges/warnings.svg) |
| ![Commits since last release](https://img.shields.io/github/commits-since/jonathandung/asyncutils/latest) | ![GitHub watchers](https://img.shields.io/github/watchers/jonathandung/asyncutils?style=social) | ![PyPI - Downloads](https://img.shields.io/pypi/dm/py-asyncutils) | ![ty](https://img.shields.io/badge/type_checker-ty-261230?logo=ty) | ![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg) | ![Expected failures](https://raw.githubusercontent.com/jonathandung/asyncutils/main/badges/xfailed.svg) |
| ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/jonathandung/asyncutils) | ![GitHub](https://img.shields.io/github/followers/jonathandung?style=social) | ![PyPI - Format](https://img.shields.io/pypi/format/py-asyncutils) | ![SemVer](https://img.shields.io/badge/semver-2.0.0-green?logo=semver) | ![detect-secrets](https://img.shields.io/badge/detect--secrets-checked-blue?logo=yelp) | ![Duration](https://raw.githubusercontent.com/jonathandung/asyncutils/main/badges/duration.svg) |
| ![GitHub issues](https://img.shields.io/github/issues/jonathandung/asyncutils) | ![GitHub Downloads](https://img.shields.io/github/downloads/jonathandung/asyncutils/total) | ![PyPI - License](https://img.shields.io/pypi/l/py-asyncutils?logo=opensourceinitiative) | ![Sphinx](https://img.shields.io/badge/docs-sphinx-265094?logo=sphinx) | [![Blazingly fast](https://www.blazingly.fast/api/badge.svg?repo=jonathandung%2Fasyncutils)](https://www.blazingly.fast) | ![Skipped](https://raw.githubusercontent.com/jonathandung/asyncutils/main/badges/skipped.svg) |
| ![GitHub pull requests](https://img.shields.io/github/issues-pr/jonathandung/asyncutils) | ![Repo creation](https://img.shields.io/github/created-at/jonathandung/asyncutils) | ![Language count](https://img.shields.io/github/languages/count/jonathandung/asyncutils) | ![Sphinx-lint](https://img.shields.io/badge/sphinx--lint-darkblue?logo=sphinx) | ![Free-threaded support](https://img.shields.io/badge/free_threading-supported-blue) | ![Last test run](https://raw.githubusercontent.com/jonathandung/asyncutils/main/badges/last-run.svg) |
| ![GitHub contributors](https://img.shields.io/github/contributors/jonathandung/asyncutils) | ![GitHub repo size](https://img.shields.io/github/repo-size/jonathandung/asyncutils) | ![Top language](https://img.shields.io/github/languages/top/jonathandung/asyncutils) | ![CSpell](https://img.shields.io/badge/spelling-cspell-green) | | |
| ![GitHub last commit](https://img.shields.io/github/last-commit/jonathandung/asyncutils) | ![Code size](https://img.shields.io/github/languages/code-size/jonathandung/asyncutils) | | ![Pytest](https://img.shields.io/badge/tests-Pytest-yellow?logo=pytest) | | |
