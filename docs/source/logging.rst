Logging
=======

Since code is bound to contain bugs, and this library is no exception, logging is an important aspect of :mod:`asyncutils`. Users can also see what
is being done under the hood and view the timestamps of significant events, without exercising advanced reflection or metaprogramming or attaching a
tracer or debugger.

This module employs logging as provided by the standard library, which may contribute to a significant chunk of the boot time of this module but is
much too widely used for us to find alternatives such as :mod:`loguru`, especially due to concerns in adding a dependency and compatibility issues.
The logger is named 'asyncutils' and retrievable by a :func:`logging.getLogger` call as expected. No submodule-specific logger is used for fear that
output would be spread too thin. To keep things simple, the logging level defaults to warning, and only the standard levels are used; that is, there
is no 'trace' or 'subwarning' level.

While we also use auditing for applications where it is deemed useful to have custom behaviour programatically triggered, we adhere to the don't
repeat yourself philosophy, such that most audit events and logs are mutually exclusive, and anything displayed in the console banner is not logged.
If logging is still desired then, an audit hook that calls the logger if and only if the name of the event begins with 'asyncutils' should be added.

As to how the loquacity and output whereabouts of the logger can be altered, refer to the following snippets:

.. literalinclude:: ../../asyncutils/config.pyi
  :language: python
  :caption: relevant portion of the stub of the :mod:`config` submodule
  :lines: 9-28,39-
  :force:

.. literalinclude:: ../../asyncutils/format.json5
  :language: json5
  :caption: json-based or command-line configuration
  :lines: 4-13,18-20,27-30,183
  :force:

The format of each log message is "<asctime> - asyncutils - <levelname> - <message>". Though this is definitely not meant, it allows deterministic
parsing of a log file. Instead, custom handlers should be attached to the logger using the :mod:`logging` API.
