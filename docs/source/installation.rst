Installation
============

.. highlight:: bash

You can prototype async code quickly using the ``uv tool`` interface, if you need only the executable (that is, the CLI) and not the library. This
can be helpful if you wish to decide how much this library suits your needs before committing to installation. Simply execute::

  uvx --from py-asyncutils asyncutils

The REPL starts with the following banner:

.. code-block:: text

  asyncutils REPL (version 1.1.2) running on linux
  Type "help", "copyright", "credits" or "license" for more information, "clear" to clear the terminal, and "exit" or "quit" to exit.
  asyncutils is a multi-purpose and efficient asynchronous utilities library.
  You can use await statements directly instead of asyncio.run for quick testing.
  All the submodules of asyncutils are also loaded into the namespace.

:mod:`asyncutils` injects itself into the globals and the import is automated visually. Afterwards, simply type Python code as you normally would,
bearing in mind that ``await`` statements are magically supported:

.. code-block:: pycon

  >>> import asyncutils
  >>> from asyncutils import *
  >>> # Your code here

For the normal installation pathway, many more package managers are supported.

You are advised to ensure that your package manager is updated to the latest version as follows::

  # uv (preferred for modernity, speed and compatibility with this project)
  uv self update # standalone installation of uv
  pip install -U uv # pip installation of uv
  pip install -U pip # pip
  pip install -U pipx # pipx
  # conda
  conda update conda anaconda
  conda update --all # optional
  poetry self update # poetry
  pip install -U pdm # pdm
  pip install -U pipenv # pipenv

Optionally make and activate a virtual environment::

  uv venv # uv
  pipenv shell # pipenv
  poetry shell # poetry
  hatch shell # hatch
  python -m venv .venv # standard library
  virtualenv venv # virtualenv
  # conda
  conda create --name asyncutils
  conda activate asyncutils
  # pyenv-virtualenv
  pyenv virtualenv 3.14.6 asyncutils
  pyenv activate asyncutils
  # manual activation (venv, virtualenv):
  . .venv/bin/activate # bash/zsh
  . .venv/bin/activate.fish # fish
  . .venv/bin/activate.csh # (t)csh

.. code-block:: bat

  rem activation on Windows (cmd.exe)
  .venv\Scripts\activate

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
  # the last two options need GNU Make on Unix-like systems, but the Windows version points to a batch file.
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
  # no package manager (needs Python and the build and installer packages)
  python -m build # generate sdist and wheel in dist/
  python -m installer dist/*.whl # install from the wheel

.. note:: We will never add setup.py, since only pyproject.toml is the modern way to go.

After this, as long as you have the python Scripts (Windows) or bin (otherwise) directory on
`PATH <https://en.wikipedia.org/wiki/PATH_(variable)>`__, ``asyncutils`` and ``autils`` will be made available as entry points to the asyncutils CLI,
which can also be called with a typical and perhaps more familiar ``python -m asyncutils``.

.. _extras:

Extras
------

The all :term:`extra` includes the dependencies for development, which are not required for normal usage. To install with extras, use the syntax
appropriate for your package manager as shown in the installation instructions above.

The extras are listed below for reference:

* all: All the extras combined
* dev: Packages one would want installed for development; superset of docs, themes, json5, test, tools.
* docs: Documentation dependencies, including Sphinx and some of its plugins, along with sphinx-lint
* executors: All the libraries implementing executors this module supports, except distributed, since that is much too specialized and heavy.
* json5: The Cython-accelerated JSON5 parser, specifically used to read format.json5 in tests.
* pconf: Dependencies to parse configuration files in Hjson, JSONC, JSON5, and YAML formats
* ptw: Monitor test failures on the command line while editing code through pytest-watch
* test: Test dependencies, including pytest and related plugins
* themes: Sphinx themes, including furo and sphinx-book-theme, used in the Read the Docs and GitHub Pages builds respectively; superset of docs.
