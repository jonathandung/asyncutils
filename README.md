# asyncutils

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/py-asyncutils)](https://www.python.org/downloads)
[![PyPI version](https://badge.fury.io/py/py-asyncutils.svg)](https://pypi.org/p/py-asyncutils)
[![Coverage](https://github.com/jonathandung/asyncutils/blob/main/assets/coverage.svg)](https://github.com/jonathandung/asyncutils/blob/main/tests)
[![Build](https://github.com/jonathandung/asyncutils/actions/workflows/python-package.yaml/badge.svg)](https://github.com/jonathandung/asyncutils/actions/workflows/python-package.yaml)
[![CodeQL](https://github.com/jonathandung/asyncutils/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/jonathandung/asyncutils/actions/workflows/github-code-scanning/codeql)
[![Publish](https://github.com/jonathandung/asyncutils/actions/workflows/python-publish.yaml/badge.svg)](https://github.com/jonathandung/asyncutils/actions/workflows/python-publish.yaml)
[![GitHub Pages](https://github.com/jonathandung/asyncutils/actions/workflows/deploy.yaml/badge.svg)](https://jonathandung.github.io/asyncutils)
[![pre-commit.ci](https://results.pre-commit.ci/badge/github/jonathandung/asyncutils/main.svg)](https://results.pre-commit.ci/latest/github/jonathandung/asyncutils/main)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/13018/badge)](https://www.bestpractices.dev/projects/13018)
[![Docs](https://app.readthedocs.org/projects/asyncutils/badge)](https://asyncutils.readthedocs.io/en/stable)
[![Conda version](https://anaconda.org/conda-forge/py-asyncutils/badges/version.svg)](https://anaconda.org/channels/conda-forge/packages/py-asyncutils/overview)
[![conda-forge feedstock](https://img.shields.io/conda/v/conda-forge/py-asyncutils?logo=condaforge)](https://github.com/conda-forge/py-asyncutils-feedstock)
[![Contributor Covenant](https://img.shields.io/badge/Contributor_Covenant-v3.0-ff69b4.svg?logo=contributor-covenant&logoColor=purple)](https://asyncutils.readthedocs.io/en/stable/conduct.html)

A Python library abstracting all the common patterns I can think of that somehow always pop up in async code.

Includes a wide range of submodules tailored for specific usages, though concrete low-level implementations are lacking.

Takes pride in:

- being as fast as can be in terms of import time
- providing detailed type checking via stub files included in the distribution
- having a well-equipped command line interface taking many flags and options

## Setup

This package probably wouldn't work on alternate Python implementations. Make sure you have CPython 3.12 or above (even a pre-release of 3.15 will
do), and at least one Python package manager you're comfortable with.

Discounting the installation, no extra setup is needed. See the [installation guide](https://asyncutils.readthedocs.io/en/stable/installation.html)
for more.

## Usage

This package is very resourceful, containing everything from higher-order error handling functions to network protocols.
See the [usage guide](https://asyncutils.readthedocs.io/en/stable/usage.html) for some basic examples.

## Version

This is asyncutils v0.9.10.

This library is currently in the beta stage, meaning the public API is subject to change even between patch versions, and changes made may be
backward-incompatible. See [the compatibility page](https://asyncutils.readthedocs.io/en/stable/compat.html).

See [all version tags up to now](https://github.com/jonathandung/asyncutils/tags).

## Configuration

Besides using command line arguments to change console settings, the behaviour of this module as a library can be customized as well.

See the [configuration guide](https://asyncutils.readthedocs.io/en/stable/config.html).

## Remarks

Regarding .markdownlint.json, even though there is no longer a pre-commit or workflow step requiring it, it contains the most basic ignores suitable
for this project's files and should be respected. It will be auto-detected by relevant IDE extensions and allows running the linter locally.

It is strongly recommended that you read the [asyncio docs](https://docs.python.org/3/library/asyncio.html) thoroughly if using event loop and async
generator related features, since their behaviours are central points of confusion and have troubled me greatly in the development of this library.

## Resources

Here are some resources if you're new to the world of async. They were of great assistance on my async journey:

- [asyncio HOWTO](https://docs.python.org/3/howto/a-conceptual-overview-of-asyncio.html)
- [Basic tutorial](https://realpython.com/async-io-python)
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

| GitHub | Repo | Package | Uses | | Status | Tests |
| --- | --- | --- | --- | --- | --- | --- |
| ![GitHub release](https://img.shields.io/github/v/release/jonathandung/asyncutils?include_prereleases) | ![Project stars](https://img.shields.io/github/stars/jonathandung/asyncutils?style=social) | ![PyPI - Implementation](https://img.shields.io/pypi/implementation/py-asyncutils) | ![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json) | ![Pytest](https://img.shields.io/badge/tests-Pytest-yellow?logo=pytest) | ![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg) | ![Tests](https://github.com/jonathandung/asyncutils/blob/main/assets/tests.svg) |
| ![GitHub release date](https://img.shields.io/github/release-date-pre/jonathandung/asyncutils) | ![GitHub forks](https://img.shields.io/github/forks/jonathandung/asyncutils?style=social) | ![Noarch](https://anaconda.org/conda-forge/py-asyncutils/badges/platforms.svg) | ![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json) | ![Sphinx-lint](https://img.shields.io/badge/sphinx-sphinx--lint-darkblue?logo=sphinx) | ![Contributions Welcome](https://img.shields.io/static/v1.svg?label=Contributions&message=Welcome&color=brightgreen) | ![Warnings](https://github.com/jonathandung/asyncutils/blob/main/assets/warnings.svg) |
| ![Commits since last release](https://img.shields.io/github/commits-since/jonathandung/asyncutils/latest.svg?include_prereleases) | ![GitHub watchers](https://img.shields.io/github/watchers/jonathandung/asyncutils?style=social) | ![PyPI - Wheel](https://img.shields.io/pypi/wheel/py-asyncutils) | ![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json) | ![Read the Docs](https://img.shields.io/badge/docs-Read_the_Docs-green?logo=readthedocs) | ![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg) | ![Expected failures](https://github.com/jonathandung/asyncutils/blob/main/assets/xfailed.svg) |
| ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/jonathandung/asyncutils) | ![GitHub](https://img.shields.io/github/followers/jonathandung?style=social) | ![PyPI - Format](https://img.shields.io/pypi/format/py-asyncutils) | ![SemVer](https://img.shields.io/badge/semver-2.0.0-green?logo=semver) | ![Dependabot](https://github.com/jonathandung/asyncutils/actions/workflows/dependabot/update-graph/badge.svg) | ![Beta](https://img.shields.io/badge/stage-beta-yellow.svg) | ![Duration](https://github.com/jonathandung/asyncutils/blob/main/assets/duration.svg) |
| ![GitHub issues](https://img.shields.io/github/issues/jonathandung/asyncutils) | ![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/jonathandung/asyncutils/total) | ![PyPI - License](https://img.shields.io/pypi/l/py-asyncutils?logo=opensourceinitiative) | ![Sphinx](https://img.shields.io/badge/docs-sphinx-265094?logo=sphinx) | ![setuptools](https://img.shields.io/badge/packaged_with-setuptools-brightgreen?logo=setuptools) | [![Blazingly fast](https://www.blazingly.fast/api/badge.svg?repo=jonathandung%2Fasyncutils)](https://www.blazingly.fast) | ![Skipped](https://github.com/jonathandung/asyncutils/blob/main/assets/skipped.svg) |
| ![GitHub pull requests](https://img.shields.io/github/issues-pr/jonathandung/asyncutils) | ![Repo creation](https://img.shields.io/github/created-at/jonathandung/asyncutils) | ![PyPI - Downloads](https://img.shields.io/pypi/dm/py-asyncutils) | ![GitHub Pages](https://img.shields.io/badge/github_pages-jonathandung.github.io-blue) | | | |
| ![GitHub contributors](https://img.shields.io/github/contributors/jonathandung/asyncutils) | ![GitHub repo size](https://img.shields.io/github/repo-size/jonathandung/asyncutils) | | ![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit) | | | |
| ![GitHub last commit](https://img.shields.io/github/last-commit/jonathandung/asyncutils) | ![Top language](https://img.shields.io/github/languages/top/jonathandung/asyncutils) | | ![detect-secrets](https://img.shields.io/badge/detect--secrets-checked-blue?logo=yelp) | | | |
