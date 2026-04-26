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

  uv self update

Next, install py-asyncutils from pip:

.. code-block:: bash

  pip install py-asyncutils==0.8.28

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

  pipx install py-asyncutils==0.8.28

or with conda:

.. code-block:: bash

  conda install -c conda-forge py-asyncutils=0.8.28

alternatively:

.. code-block:: bash

  conda config --add channels conda-forge
  conda config --set channel_priority strict
  conda install py-asyncutils==0.8.28

or with uv:

.. code-block:: bash

  uv pip install 'py-asyncutils==0.8.28'

After this, as long as you have the python scripts directory on PATH, ``asyncutils`` and ``autils`` will be made available as entry points
to the asyncutils CLI.

Refer to `SUPPORT.md <https://github.com/jonathandung/asyncutils/blob/main/SUPPORT.md>`_ for steps to checking the installation.

.. _extras:

Extras
------

The all :term:`extra` includes the dev, docs, pub and json extras, mainly for development.

The dev extra installs uv (for ruff), pytest and some required plugins thereof. Please use uv to install ruff yourself.

The docs extra includes sphinx and some plugins for readthedocs builds.

The pub extra includes build, twine and keyring for publishing.

The json extra bundles libraries on pip used to parse json variants (`jsonc <https://pypi.org/project/json-with-comments/>`_, `json5
<https://pypi.org/project/json5/>`_ and `hjson <https://pypi.org/project/hjson/>`_), to be used by :func:`tools.json_to_argv` and
:func:`tools.json_to_argstr`.
