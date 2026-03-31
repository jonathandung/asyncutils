Top level
=========

This section documents the symbols defined at the top level of this package.

.. data:: __version__
  :module: asyncutils
  :annotation: asyncutils.version.VersionInfo

  An instance of :class:`asyncutils.version.VersionInfo` representing the current pip/conda version of this library.
  This library adheres to `Semantic Versioning 2.0.0 <https://semver.org/spec/v2.0.0.html>`_.

.. data:: __hexversion__
  :module: asyncutils
  :annotation: int

  An integer representing the current pip/conda version of this library. Comparison operators working as expected.
  For version 1.3.11, this would be ``0x01030b``.

  Equivalent to ``int(__version__)``

.. data:: preloaded_submodules
  :module: asyncutils
  :annotation: frozenset[str]

  A :class:`frozenset` of submodule names which are preloaded when importing the library for essential initialization.

.. data:: submodules_map
  :module: asyncutils
  :annotation: dict[str, types.ModuleType]

  A :class:`dict` mapping submodule names to the corresponding submodule objects.
  For submodules that are already loaded, these are exact instances of :class:`types.ModuleType`.

  :note:
    For submodules that are not yet loaded, the value is an instance of an internal class with the same behaviour but not inserted into
    :data:`sys.modules`. This class is not a subclass of :class:`types.ModuleType` and provides a :meth:`load` method that fetches the
    submodule and replaces the entry in both :data:`submodules_map` and :data:`sys.modules`, and returns the real submodule object.
    For attribute accesses, it acts as a proxy to the real submodule, loading it when strictly required.

    *The exact deference mechanism is an implementation detail.*

One can access members of submodules as attributes of the main module, which will dispatch to the appropriate submodule.

Each module has an :data:`__all__` attribute that is a tuple of strings, representing its public API. Anything not included in it is unstable.
