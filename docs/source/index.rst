asyncutils 0.9.1: makes async straightforward and enjoyable
===========================================================

**PyPI package name**: `asyncutils <https://pypi.org/p/py-asyncutils>`_

:mod:`asyncutils` is a Python library which, as the name suggests, contains helpful routines and types for asynchronous programming applications,
organized under various submodules. It offers a simple and intuitive API and a colorful command line interface, and bundles a Makefile such that
development is less dry and more smooth-sailing.

This is partly also to compensate for the lack of a setup.py after adaptation of the standardized pyproject.toml; see :pep:`621` and `the guide
<https://packaging.python.org/en/latest/guides/writing-pyproject-toml>`_ for more.

.. toctree::
  :maxdepth: 2
  :caption: Contents:

  installation
  config
  audit-events
  logging
  top-level
  api/index
  benchmark
  glossary

.. toctree::
  :caption: About the project
  :hidden:

  examples
  compat
  contributing
  support
  changelog
  roadmap

.. toctree::
  :caption: Links
  :hidden:

  asyncutils @ PyPI <https://pypi.org/p/py-asyncutils/>
  asyncutils @ GitHub <https://github.com/jonathandung/asyncutils/>
  Issue Tracker <https://github.com/jonathandung/asyncutils/issues>
  PDF Documentation <https://media.readthedocs.org/pdf/asyncutils/latest/asyncutils.pdf>

.. note::

  This project is being actively developed and maintained. It currently only supports CPython 3.12 or above.

.. hint::
  :collapsible:

  Execute ``make help`` to see the available Makefile targets. More of them will be added on popular demand.

.. note::
  :collapsible: closed

  The format of this page was inspired by `pytest <https://docs.pytest.org/en/stable>`_.
