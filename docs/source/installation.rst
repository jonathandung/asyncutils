Installation
============

.. version-added:: 0.8.20

No setup is required, besides ensuring that your package manager is updated to the latest version as follows:

.. code-block:: bash

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

.. version-added:: 0.8.13
  Achieved distribution on conda-forge and by extension, conda installation support.

Next, install py-asyncutils:

.. code-block:: bash

  # recommended: pip
  pip install py-asyncutils==0.9.10
  # directly from source
  pip install git+https://github.com/jonathandung/asyncutils.git
  # alternatively, after:
  git clone https://github.com/jonathandung/asyncutils.git
  cd asyncutils
  # you have options (a):
  pip install .
  # (b):
  make install # verbose; or
  make install-silent # no clutter
  # uses Make, though pip is still used under the hood
  # or if you are not on a unix-like system and don't have pip for some reason:
  python -m build
  python -m installer dist/*.whl
  # you should really install pip in this case, since build and installer are still required

or if you wish to obtain the :ref:`extras`:

.. code-block:: bash

  # tools likely enough for developers
  pip install "py-asyncutils[dev]"
  # or the equivalent syntax for extras installation in other package managers

other installation pathways:

.. code-block:: bash

  # pipx
  pipx install py-asyncutils==0.9.10
  # conda
  conda install -c conda-forge py-asyncutils=0.9.10
  # alternatively:
  conda config --add channels conda-forge
  conda config --set channel_priority strict
  conda install py-asyncutils==0.9.10
  # uv essentially supports the same interface as pip with uv pip
  # poetry
  poetry add py-asyncutils@0.9.10
  # pdm
  pdm add py-asyncutils==0.9.10
  # pipenv
  pipenv install py-asyncutils==0.9.10

.. note:: We will never add setup.py, since only pyproject.toml is the modern way to go.

After this, as long as you have the python Scripts (Windows) or bin (otherwise) directory on :envvar:`PATH`, ``asyncutils`` and ``autils`` will be made
available as entry points to the asyncutils CLI, which can also be called with a typical and perhaps more familiar ``python -m``.

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

.. version-changed:: 0.9.9
  Added pytest-asyncio-cooperative to the test extra.

.. version-added:: 0.9.7
  The themes extra, to make CI/CD steps involving documentation deployment more convenient.

.. version-removed:: 0.9.5
  The pub extra, because uv already provides that functionality.

.. version-removed:: 0.9.5
  mypy is no longer in any extra, since ty provides type checking.

.. version-changed:: 0.9.3
  Removed the pytest-local-badge dependency from pytest's required plugins. However, it is still present in the tests group for convenience of
  development.

.. version-removed:: 0.9.2
  The tools extra. Install uv yourself if you wish.

.. version-added:: 0.9.2
  The executors extra.

.. version-added:: 0.9.1
  The ptw extra.

.. version-removed:: 0.9.1
  The dlint extra, since doc8 no longer appears to be maintained.

.. version-changed:: 0.9.0
  Completely reorganized optional dependencies, moving them around among groups.
