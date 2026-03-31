Glossary
========

.. glossary::

  extra
    A name corresponding to a set of optional dependencies, supported by most package managers (pip, pipx, conda and uv). This module has no
    runtime dependencies outside of the standard library (unless you count json-with-comments, json5 and hjson used by :func:`tools.json_to_argv` and
    :func:`tools.json_to_argstr`, which come with the ``json`` extra), and the other extras are for development only.

  submodule
    A module that is part of a library or package that is not the main module/entry point. For this project, :mod:`asyncutils` is the main module and
    its submodules include :mod:`asyncutils.context`, :mod:`asyncutils.locks`, :mod:`asyncutils.queues` and more. A lazy loading system is in place
    to avoid the overhead of gathering all submodules on import and make them accessible using attribute access syntax.
