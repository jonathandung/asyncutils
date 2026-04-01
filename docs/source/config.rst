Configuration
=============

:mod:`asyncutils` is highly customizable, with an extensible configuration system.

This includes aspects such as where to output logging, customizing the underlying executor type used, and setting a seed for random number generation
using the ``AUTILSCFGPATH`` environment variable (all uppercase due to Windows limitations), which should point to an absolute path to a configuration
.json/.jsonl file. ``AUTILSCFGPATH`` is read at the first import of this library, and the configuration is loaded and applied immediately. Errors will
be thrown as appropriate if the file is not found or contains values of the incorrect type, after the library tries its best to coerce the types.

New options will likely be added in the future, but every current option is considered stable and has a corresponding default value.

The options are shown below, along with their default values and descriptions:

.. literalinclude:: ../../asyncutils/format.json5
  :language: json5
  :caption: config file format
  :force:

The above keys have a near one-to-one correspondence with the command line arguments. Use ``asyncutils -?`` to see detailed usage.
