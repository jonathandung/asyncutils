Audit events table
==================

This page details all events raised by this library through sys.audit and the corresponding arguments. This module takes care not to expose sensitive
information in the events, so that the audit hooks often only see the fully qualified name of the type of some handled object rather than the object
itself. For consistency and namespace integrity, the name of all audit events begin with 'asyncutils', and are often exactly the fully qualified name
of the function being called.

See the official documentation for :func:`sys.audit` and :func:`sys.addaudithook` on how to listen to these events, as well as
:class:`asyncutils.channels.EventBus`, which is capable of triggering mass publications to async subscribers for audit events with little overhead.

Also see `the standard library audit event table <https://docs.python.org/3/library/audit_events.html>`_, from which the inclustion and format of
this table take inspiration.

.. list-table:: Audit events
  :header-rows: 1
  :widths: 35 30 35

  * - Audit event
    - Arguments
    - Description
  * - asyncutils/create_executor
    - ``fname``: :class:`str`
    - Raised when asyncutils creates an executor, type dictated by configuration. ``fname`` is of the form 'submodule.function'.
  * - asyncutils/read_config
    - ``cfg_path``: :class:`str`
    - Raised when asyncutils reads its configuration file expected to be in json format at ``cfg_path``, which is not guaranteed to be absolute.
