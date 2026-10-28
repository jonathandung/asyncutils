Installation
============

.. highlight:: bash

You can prototype async code quickly using the ``uv tool`` interface, if you need only the executable (that is, the CLI) and not the library. This
can be helpful if you wish to decide how much this library suits your needs before committing to installation. Simply execute::

  uvx --from py-asyncutils asyncutils

The REPL starts with the following banner:

.. sub-code-block:: text

  asyncutils REPL (version |version|) running on linux
  Type "help", "copyright", "credits" or "license" for more information, "clear" to clear the terminal, and "exit" or "quit" to exit.
  asyncutils is a multi-purpose and efficient asynchronous utilities library.
  You can use *await* statements directly instead of *asyncio.run* for quick testing.
  All the submodules of asyncutils are also loaded into the namespace.

:mod:`asyncutils` injects itself into the globals. Afterwards, simply type Python code as you normally would, bearing in mind that ``await``
statements are magically supported:

.. code-block:: pycon

  >>> import asyncutils
  >>> from asyncutils import *
  >>> # The above is automatically printed and executed
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

Next, install ``py-asyncutils``:

.. sub-code-block::

  # recommended: uv
  uv pip install py-asyncutils==|version|
  uv pip install git+https://github.com/jonathandung/asyncutils.git # directly from source
  # pip
  pip install py-asyncutils==|version|
  pip install git+https://github.com/jonathandung/asyncutils.git # directly from source
  # conda
  conda install -c conda-forge py-asyncutils=|version|
  # alternatively:
  conda config --add channels conda-forge
  conda config --set channel_priority strict
  conda install py-asyncutils==|version|

other installation pathways:

.. sub-code-block::

  pipx install py-asyncutils==|version| # pipx
  pdm add -g py-asyncutils==|version| # pdm (not exactly a conventional installation)
  pipenv install py-asyncutils==|version| # pipenv
  # no package manager (needs Python and the build and installer packages)
  python3 -m build # generate sdist and wheel in dist/
  python3 -m installer dist/*.whl # install from the wheel

``asyncutils`` will then be made available as an entry point to the asyncutils CLI. The CLI can also be called with a typical and perhaps more
familiar ``python3 -m asyncutils``.

Optional dependencies
---------------------

Below are the :pep:`508` optional dependencies this package provides, also known as "extras".

* executors: All the libraries implementing executors this module supports natively, except `distributed <https://distributed.dask.org/en/stable>`__.
  Recognized executors are listed as follows:

  - `loky.ProcessPoolExecutor <https://loky.readthedocs.io/en/stable/API.html#loky.ProcessPoolExecutor>`__
  - `distributed.Client <https://distributed.dask.org/en/stable/api.html#distributed.Client>`__
  - `ipyparallel.ViewExecutor <https://ipyparallel.readthedocs.io/en/latest/api/ipyparallel.html#ipyparallel.ViewExecutor>`__
  - `executorlib.executor.flux.FluxClusterExecutor <https://executorlib.readthedocs.io/en/latest/_autosummary/executorlib.executor.flux.FluxClusterExecutor.html#executorlib.executor.flux.FluxClusterExecutor>`__
  - `executorlib.executor.flux.FluxJobExecutor <https://executorlib.readthedocs.io/en/latest/_autosummary/executorlib.executor.flux.FluxJobExecutor.html#executorlib.executor.flux.FluxJobExecutor>`__
  - `executorlib.executor.slurm.SlurmClusterExecutor <https://executorlib.readthedocs.io/en/latest/_autosummary/executorlib.executor.slurm.SlurmClusterExecutor.html#executorlib.executor.slurm.SlurmClusterExecutor>`__
  - `executorlib.executor.slurm.SlurmJobExecutor <https://executorlib.readthedocs.io/en/latest/_autosummary/executorlib.executor.slurm.SlurmJobExecutor.html#executorlib-executor-slurm-slurmjobexecutor>`__
  - `executorlib.executor.single.SingleNodeExecutor <https://executorlib.readthedocs.io/en/latest/_autosummary/executorlib.executor.single.SingleNodeExecutor.html#executorlib.executor.single.SingleNodeExecutor>`__
  - `pebble.ProcessPool <https://pebble.readthedocs.io/en/latest/#pebble.ProcessPool>`__
  - `pebble.Thread <https://pebble.readthedocs.io/en/latest/#pebble.ThreadPool>`__
  - `deadpool.Deadpool <https://github.com/cjrh/deadpool#deadpool>`__

* json5: The Cython-backed JSON5 parser.
* pconf: A collection of libraries used to parse config files in various formats.

Dependency groups
-----------------

The :pep:`735` dependency groups of this package are listed below for reference:

* dev: Union of ``sbt`` and ``test``.
* docs: `Sphinx <https://www.sphinx-doc.org/en/master>`__ and plugins.
* furo: The `furo <https://pradyunsg.me/furo>`__ HTML theme for Sphinx and everything in ``docs``.
* sbt: `sphinx-book-theme <https://sphinx-book-theme.readthedocs.io/en/stable>`__ and everything in ``docs``.
* test: `pytest <https://docs.pytest.org/en/stable>`__ and plugins.
