**Installation**

No setup is required. Of course, ensure that your package manager is updated to the latest version as follows:

pip:

.. code-block:: bash
    pip install -U pip

pipx:

.. code-block:: bash
    pip install -U pipx

conda:

.. code-block:: bash
    conda update conda
    conda update anaconda
    conda update --all # optional

uv:

.. code-block:: bash
    uv self update

Next, install py-asyncutils from pip:

.. code-block:: bash
    pip install py-asyncutils==0.8.19

or if installing for development [Ref1]_:

.. code-block:: bash
    pip install py-asyncutils[dev,docs,pub]

or directly from the github repository:

.. code-block:: bash
    pip install git+https://github.com/jonathandung/asyncutils.git#egg=py-asyncutils

or with pipx:

.. code-block:: bash
    pipx install py-asyncutils==0.8.19

or with conda:

.. code-block:: bash
    conda install -c conda-forge py-asyncutils=0.8.19

or with uv:

.. code-block:: bash
    uv pip install 'py-asyncutils==0.8.19'

After this, as long as you have the python scripts directory on PATH, `asyncutils` and `autils` will be made available as entry points
to the asyncutils CLI.

Refer to [SUPPORT.md](https://github.com/jonathandung/asyncutils/blob/main/SUPPORT.md) for steps to checking the installation.

.. [Ref1]
The dev extra differs from the dev branch, which is currently not installable. It installs ruff, pytest and some required plugins thereof.
The docs extra includes sphinx and some plugins for readthedocs builds.
The pub extra includes build and twine for publishing.