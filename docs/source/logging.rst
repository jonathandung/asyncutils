Logging
=======

Since code is bound to contain bugs, and this library is no exception, logging is an important aspect of :mod:`asyncutils`. Users can also see what
is being done under the hood and view the timestamps of significant events, without exercising advanced reflection or metaprogramming or attaching a
tracer, profiler or debugger.

This module employs logging as provided by the standard library, which may contribute to a significant chunk of the boot time of this module but is
much too widely used for us to find alternatives such as `loguru <https://loguru.readthedocs.io/en/stable>`__, especially due to concerns in adding
a dependency and compatibility issues.

While we also use auditing for applications where it is deemed useful to have custom behaviour programmatically triggered, we follow the DRY (don't
repeat yourself) philosophy, meaning most audit events and logs are mutually exclusive, and anything displayed in the console banner is not logged.

.. tip::
  :collapsible:

  If logging is still desired then, an audit hook that calls the logger if and only if the name of the event begins with 'asyncutils' should be added
  using :func:`sys.addaudithook`, but performance may take a hit.

As to how the loquacity and output whereabouts of the logger can be altered, refer to the following snippets:

.. literalinclude:: ../../asyncutils/config.pyi
  :language: python
  :caption: relevant portion of the stub of the :mod:`~asyncutils.config` submodule
  :lines: 13-33,42-
  :force:

.. literalinclude:: ../../asyncutils/format.json5
  :language: json5
  :caption: json-based or command-line configuration
  :lines: 4-13,18-20,27-30,213
  :force:

The format of each log message as printed is "<asctime> - asyncutils - <levelname> - <message>", where ``levelname`` is one of ``DEBUG``, ``INFO``,
``WARNING``, ``ERROR``, and ``CRITICAL``.

.. note::
  :collapsible: closed

  Though the above is stable and allows deterministic parsing of a log file, it is recommended to instead attach custom handlers to the logger, as
  returned by ``logging.getLogger('asyncutils')``, using the :mod:`logging` API to achieve the same effect more efficiently and less hackily.
