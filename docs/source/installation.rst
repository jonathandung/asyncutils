Installation
============

.. highlight:: bash

You are advised to ensure that your package manager is updated to the latest version as follows::

  # pip:
  pip install -U pip
  # pipx:
  pip install -U pipx
  # conda:
  conda update conda anaconda
  conda update --all # optional
  # uv (preferred for modernity, speed and compatibility with this project):
  uv self update # may not work if uv was installed with pip
  pip install -U uv # in that case
  # poetry:
  poetry self update
  # pdm:
  pip install -U pdm
  # pipenv:
  pip install -U pipenv

Next, install py-asyncutils:

.. sub-code-block::

  # recommended: uv
  uv pip install py-asyncutils==|version|
  uv pip install git+https://github.com/jonathandung/asyncutils.git # directly from source
  # for development, after:
  git clone https://github.com/jonathandung/asyncutils.git
  cd asyncutils
  # you have the three options below:
  uv pip install -e .
  make install
  make install-silent # no clutter
  # the last two options need GNU Make on *nix, but the Windows version points to a batch file.
  # uv is invoked under the hood and installed if absent; pip is not needed!

other installation pathways:

.. sub-code-block::

  pip install py-asyncutils==|version| # pip
  pip install git+https://github.com/jonathandung/asyncutils.git # directly from source
  conda install -c conda-forge py-asyncutils=|version| # conda
  # alternatively:
  conda config --add channels conda-forge
  conda config --set channel_priority strict
  conda install py-asyncutils==|version|
  pipx install py-asyncutils==|version| # pipx
  poetry add py-asyncutils@|version| # poetry
  pdm add py-asyncutils==|version| # pdm
  pipenv install py-asyncutils==|version| # pipenv
  # no package manager (needs the build and installer packges)
  python -m build # generate sdist and wheel in dist/
  python -m installer dist/*.whl # install from the wheel

.. note:: We will never add setup.py, since only pyproject.toml is the modern way to go.

After this, as long as you have the python Scripts (Windows) or bin (otherwise) directory on
`PATH <https://en.wikipedia.org/wiki/PATH_(variable)>`__, ``asyncutils`` and ``autils`` will be made available as entry points to the asyncutils CLI,
which can also be called with a typical and perhaps more familiar ``python -m asyncutils``.

Refer to :doc:`support` for steps to check the installation.

.. _extras:

Extras
------

The all :term:`extra` includes the dependencies for development, which are not required for normal usage. To install with extras, use the syntax
appropriate for your package manager as shown in the installation instructions above.

The extras are listed below for reference:

* all: All the extras combined
* dev: Packages one would want installed for development; superset of docs, themes, json5, test, tools, and includes pre-commit as well.
  Notably, ruff and ty are absent because it is recommended to install them with uv, which renders them unspecifiable as dependencies.
* docs: Documentation dependencies, including Sphinx and some of its plugins, along with sphinx-lint
* executors: All the libraries implementing executors this module supports, except distributed, since that is much too specialized and heavy.
* json5: The JSON5 parser, specifically used to read format.json5 in tests.
* pconf: Dependencies to parse configuration files in Hjson, JSONC, JSON5, and YAML formats
* ptw: Monitor test failures on the command line while editing code through pytest-watch
* test: Test dependencies, including pytest and related plugins
* themes: Sphinx themes, including furo and sphinx-book-theme, used in the Read the Docs and GitHub Pages builds respectively; superset of docs.
