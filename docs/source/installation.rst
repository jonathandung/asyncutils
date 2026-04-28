Installation
============

No setup is required. Of course, ensure that your package manager is updated to the latest version as follows:

pip:

.. code-block:: bash

  pip install -U pip

pipx:

.. code-block:: bash

  pip install -U pipx

conda:

.. code-block:: bash

  conda update conda anaconda
  conda update --all # optional

uv:

.. code-block:: bash

  uv self update # may not work if uv was installed with pip; in which case:
  pip install -U uv

poetry:

.. code-block:: bash

  poetry self update

pdm:

.. code-block:: bash

  pip install -U pdm

pipenv:

.. code-block:: bash

  pip install -U pipenv

Next, install py-asyncutils from pip:

.. code-block:: bash

  pip install py-asyncutils==0.9.0

or directly from the github repository (still requires pip):

.. code-block:: bash

  pip install git+https://github.com/jonathandung/asyncutils.git#egg=py-asyncutils

or if you are installing for development, and wish to obtain the corresponding :ref:`extras`:

.. code-block:: bash

  pip install py-asyncutils[dev]
  uv tool install ruff

alternatively, after:

.. code-block:: bash

  git clone https://github.com/jonathandung/asyncutils.git
  cd asyncutils

do:

.. code-block:: bash

  pip install .

or if you don't have pip for some reason (you should really install it; build and installer are still required):

.. code-block:: bash

  python -m build
  python -m installer dist/*.whl

or with pipx:

.. code-block:: bash

  pipx install py-asyncutils==0.9.0

or with conda:

.. code-block:: bash

  conda install -c conda-forge py-asyncutils=0.9.0

alternatively:

.. code-block:: bash

  conda config --add channels conda-forge
  conda config --set channel_priority strict
  conda install py-asyncutils==0.9.0

or with uv:

.. code-block:: bash

  uv pip install 'py-asyncutils==0.9.0'

or with poetry:

.. code-block:: bash

  poetry add py-asyncutils@0.9.0

or with pdm:

.. code-block:: bash

  pdm add py-asyncutils==0.9.0

or with pipenv:

.. code-block:: bash

  pipenv install py-asyncutils==0.9.0

After this, as long as you have the python scripts directory on PATH, ``asyncutils`` and ``autils`` will be made available as entry points
to the asyncutils CLI.

Refer to `SUPPORT.md <https://github.com/jonathandung/asyncutils/blob/main/SUPPORT.md>`_ for steps to checking the installation.

.. _extras:

Extras
------

The all :term:`extra` includes the dependencies for development, which are not required for normal usage. To install with extras, use the syntax
appropriate for your package manager as shown in the installation instructions above.

The extras are listed below for reference:

* all: All the extras combined
* dev: Packages one would want installed for development; superset of docs, dlint, json5, pub, test, tools
* dlint: Dependencies for linting documentation source files
* docs: Documentation dependencies, including sphinx and some of its plugins, along with dlint
* pconf: Dependencies to parse configuration files in Hjson, JSONC, JSON5, and YAML formats
* ptw: pytest-watch
* json5: The JSON5 parser, specifically used to read format.json5 in tests.
* pub: Dependencies for building and publishing packages to PyPI
* test: Test dependencies, including pytest and related plugins
* tools: Development tools dependencies, including mypy and uv
