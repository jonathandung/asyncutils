Glossary
========

.. glossary::

  extra
    A name corresponding to a set of optional dependencies, supported by most package managers (pip, pipx, conda and uv). This module has no
    runtime dependencies outside of the standard library save for the config file parsers, and all the extras are for development only.

  submodule
    A module that is part of a library or package that is not the main module/entry point. See :doc:`submodules`.

  subpackage
    A directory within a package containing submodules, along with an ``__init__.py`` file.

  entry point
    A function serving as the main interface for a module or package, allowing it to be run as a command-line tool or imported as a library.
