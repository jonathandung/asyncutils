Installation
============

No setup is required, besides ensuring that your package manager is updated to the latest version as follows:

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

  uv self update # may not work if uv was installed with pip
  pip install -U uv # in that case

poetry:

.. code-block:: bash

  poetry self update

pdm:

.. code-block:: bash

  pip install -U pdm

pipenv:

.. code-block:: bash

  pip install -U pipenv

.. version-added:: 0.8.13
  Achieved distribution on conda-forge and by extension, conda installation support.

Next, install py-asyncutils from pip:

.. code-block:: bash

  pip install py-asyncutils==0.9.1

or directly from the github repository (still requires pip):

.. code-block:: bash

  pip install git+https://github.com/jonathandung/asyncutils.git#egg=py-asyncutils

or if you are installing for development, and wish to obtain the corresponding :ref:`extras`:

.. code-block:: bash

  pip install py-asyncutils[dev]
  uv tool install ruff # make ruff available with the uvx interface

alternatively, after:

.. code-block:: bash

  git clone https://github.com/jonathandung/asyncutils.git
  cd asyncutils

do:

.. code-block:: bash

  pip install .

or using Make, though pip is still used under the hood:

.. code-block:: bash

  make install # verbose
  make install-silent # no clutter

.. version-added:: 0.9.0
  Created a Makefile to simplify development chores.

or if you are not on a unix-like system and don't have pip for some reason:

.. code-block:: bash

  python -m build
  python -m installer dist/*.whl

you should really install pip in this case, since build and installer are still required

or with pipx:

.. code-block:: bash

  pipx install py-asyncutils==0.9.1

or with conda:

.. code-block:: bash

  conda install -c conda-forge py-asyncutils=0.9.1

alternatively:

.. code-block:: bash

  conda config --add channels conda-forge
  conda config --set channel_priority strict
  conda install py-asyncutils==0.9.1

or with uv:

.. code-block:: bash

  uv pip install 'py-asyncutils==0.9.1'

or with poetry:

.. code-block:: bash

  poetry add py-asyncutils@0.9.1

or with pdm:

.. code-block:: bash

  pdm add py-asyncutils==0.9.1

or with pipenv:

.. code-block:: bash

  pipenv install py-asyncutils==0.9.1

After this, as long as you have the python scripts directory on PATH, ``asyncutils`` and ``autils`` will be made available as entry points
to the asyncutils CLI, which can also be called with a typical and perhaps more familiar ``python -m``.

Refer to `SUPPORT.md <https://github.com/jonathandung/asyncutils/blob/main/SUPPORT.md>`_ for steps to check the installation.

.. _extras:

Extras
------

The all :term:`extra` includes the dependencies for development, which are not required for normal usage. To install with extras, use the syntax
appropriate for your package manager as shown in the installation instructions above.

The extras are listed below for reference:

* all: All the extras combined
* dev: Packages one would want installed for development; superset of docs, json5, pub, test, tools
* docs: Documentation dependencies, including sphinx and some of its plugins, along with sphinx-lint
* pconf: Dependencies to parse configuration files in Hjson, JSONC, JSON5, and YAML formats
* ptw: Monitor test failures on the command line while editing code through pytest-watch
* json5: The JSON5 parser, specifically used to read format.json5 in tests.
* pub: Dependencies for building and publishing packages to PyPI
* test: Test dependencies, including pytest and related plugins
* tools: Development tools dependencies, including mypy and uv

.. version-added:: 0.9.1
  Added the ptw group.

.. version-removed:: 0.9.1
  Removed the dlint group, since doc8 no longer appears to be maintained.

.. version-changed:: 0.9.0
  Completely reorganized optional dependencies, moving them around among groups. Still no strictly required dependencies!
