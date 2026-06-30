Submodules
==========

:mod:`asyncutils` includes a wide range of submodules tailored for specific, mostly high-level, use cases. These include :mod:`asyncutils.context`,
:mod:`asyncutils.locks`, :mod:`asyncutils.queues` and more. A lazy loading system, complete with logging, is in place to avoid the overhead of
gathering all submodules on import and make them accessible using attribute access syntax.

.. note::
  For submodules that are not yet loaded, the value in :data:`~asyncutils.submodules_map` is an instance of an internal class with the same
  behaviour, except it is not inserted into :data:`sys.modules`. This class is not a subclass of :class:`types.ModuleType` and provides a
  :meth:`!load` method that fetches the submodule and replaces the entry in both :data:`~asyncutils.submodules_map` and :data:`sys.modules`, and
  returns the real submodule object. For attribute accesses, it acts as a proxy to the real submodule, loading it when strictly required; however,
  when modifying or deleting attributes, the submodule is gotten unconditionally and replaces the proxy.

.. admonition:: Implementation detail

  The exact deferment mechanism is not part of the public API.

The remarks below are inapplicable to the contextually configured constants in :mod:`~asyncutils.context`:

* One can directly access members of submodules as attributes of the main module, which will dispatch to the appropriate submodule.
* The submodule objects are also accessible as attributes of the library without triggering the loading immediately if not loaded.
* Each module has an :attr:`~module.__all__` attribute, a tuple of strings representing its public API.
