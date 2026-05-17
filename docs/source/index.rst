asyncutils 0.9.5: makes async straightforward and enjoyable
===========================================================

**PyPI package name**: `asyncutils <https://pypi.org/p/py-asyncutils>`__

:mod:`asyncutils` is a Python library which, as the name suggests, contains helpful routines and types for asynchronous programming applications,
organized under various submodules. It offers a simple and intuitive API and a colorful command line interface, and bundles a Makefile such that
development is less dry and more smooth-sailing.

This is partly also to compensate for the lack of a setup.py after adaptation of the standardized pyproject.toml; see :pep:`621` and `the guide
<https://packaging.python.org/en/latest/guides/writing-pyproject-toml>`__ for more.

.. toctree::
  :maxdepth: 2
  :caption: Contents:

  installation
  config
  audit-events
  logging
  top-level
  api/index
  examples
  benchmark
  glossary

.. toctree::
  :caption: About the project
  :hidden:

  compat
  contributing
  conduct
  ai-use
  support
  security
  changelog
  roadmap

.. toctree::
  :caption: Links
  :hidden:

  asyncutils @ PyPI <https://pypi.org/p/py-asyncutils/>
  asyncutils @ GitHub <https://github.com/jonathandung/asyncutils/>
  Issue tracker <https://github.com/jonathandung/asyncutils/issues>
  PDF documentation <https://media.readthedocs.org/pdf/asyncutils/latest/asyncutils.pdf>
  .zip archive of pages <https://asyncutils.readthedocs.io/_/downloads/en/latest/htmlzip>

.. note:: This project is being actively developed and maintained. It currently only supports CPython 3.12 or above.

.. version-changed:: 0.9.3

  Added the documentation downloads to the links section in the sidebar.

.. version-changed:: 0.9.3

  Copied more pages from the root to the sidebar for easier navigation.

.. version-changed:: 0.9.2

  Started releasing documentation in pdf and htmlzip formats.

.. version-removed:: 0.9.0

  0.8.x versions reached end-of-life.

.. version-changed:: 0.8.18

  Completed the backport of the project to Python 3.12 and Python 3.14.

.. hint::
  :collapsible:

  Execute ``make help`` to see the available Makefile targets, more of which will be added on popular demand.

.. note::
  :collapsible: closed

  The format of this page was inspired by `pytest <https://docs.pytest.org/en/stable>`__.
