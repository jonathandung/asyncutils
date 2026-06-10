Top level
=========

.. version-added:: 0.8.21

.. currentmodule:: asyncutils

This section documents the symbols defined at the top level of this package, mostly related to project metadata.

.. data:: __version__
  :type: version.VersionInfo

  An instance of :class:`version.VersionInfo` representing the current pip/conda version of this library.

  :note: This library adheres to `Semantic Versioning 2.0.0 <https://semver.org/spec/v2.0.0.html>`__.

.. data:: __hexversion__
  :type: int

  An integer representing the current pip/conda version of this library. Comparison operators behave as expected.
  For version 1.3.11, for instance, this would be ``0x01030b``.

  :note: Equivalent to ``int(__version__)``

.. data:: console_preloaded_submodules
  :type: frozenset[str]

  A :class:`frozenset` of submodule names which are loaded when starting the interactive console of this module.

  :note: It is a strict superset of :data:`preloaded_submodules`.

  .. version-changed:: 0.9.3
    Removed :mod:`~asyncutils.config` from this set.

  .. version-changed:: 0.9.0
    Added :mod:`~asyncutils.cli` to this set.

  .. version-changed:: 0.8.28
    Added :mod:`~asyncutils.context` to this set.

.. data:: preloaded_submodules
  :type: frozenset[str]

  A :class:`frozenset` of names of submodules which are preloaded when importing the library for essential initialization.

  .. version-changed:: 0.9.3
    Removed :mod:`~asyncutils.config` from this set.

  .. version-changed:: 0.9.0
    Added :mod:`~asyncutils.cli` to this set.

  .. version-changed:: 0.8.28
    Added :mod:`~asyncutils.context` to this set.

.. data:: submodules_map
  :type: dict[str, types.ModuleType]

  A :class:`dict` mapping submodule names to the corresponding submodule objects.

  :tip: For submodules that are already loaded, these are exact instances of :class:`types.ModuleType`.

  :note:
    For submodules that are not yet loaded, the value is an instance of an internal class with the same behaviour but not inserted into
    :data:`sys.modules`. This class is not a subclass of :class:`types.ModuleType` and provides a ``load`` method that fetches the submodule and
    replaces the entry in both :data:`submodules_map` and :data:`sys.modules`, and returns the real submodule object. For attribute accesses, it acts
    as a proxy to the real submodule, loading it when strictly required; however, when modifying or deleting attributes, the submodule is gotten
    unconditionally and replaces the proxy.

  :admonition: Implementation detail

    The exact deferment mechanism is not part of the public API.

.. function:: time_since_boot() -> float

  Time since the module was imported or invoked in the command line in milliseconds, as returned by :func:`time.monotonic`, as a :class:`float`.
  Useful for benchmarking the module's performance.

The remarks below are inapplicable to the contextually configured constants in :mod:`~asyncutils.context`:

* One can directly access members of submodules as attributes of the main module, which will dispatch to the appropriate submodule.
* The submodule objects are also accessible as attributes of the library without triggering the loading immediately if not loaded.
* Each module has an :attr:`~module.__all__` attribute, a tuple of strings representing its public API.
* Except :data:`__version__` and :data:`__hexversion__`, anything not included in the above is considered unstable or private.
