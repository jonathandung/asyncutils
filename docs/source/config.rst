Configuration
=============

Basic Customization
-------------------

:mod:`asyncutils` is highly customizable, with an extensible configuration system.

This includes aspects such as where to output logging, customizing the underlying executor type used, and setting a seed for random number generation
using the ``AUTILSCFGPATH`` environment variable (all uppercase for Windows support), which should point to an absolute path to a configuration .json
or .jsonl file. ``AUTILSCFGPATH`` is read at the first import of this library, and the configuration is loaded and applied immediately. Errors will
be thrown as appropriate if the file is not found or contains values of the incorrect type, after the library tries its best to coerce the types.

Automatic discovery of config files, as in other libraries or command-line tools, is not supported, because there is no standard location for it and
determining a precedence for the different allowed file extensions would be arbitrary, non-trivial and difficult to maintain.

New options will likely be added in the future, but every current option is considered stable and has a corresponding default value.

The options are shown below, along with their default values and descriptions:

.. literalinclude:: ../../asyncutils/format.json5
  :language: json5
  :caption: config file format
  :force:

The above keys have a near one-to-one correspondence with the command line arguments, as the comments below each key explain; besides the contextual
constants, due to the sheer magnitude of options making them infeasible to include. Use ``asyncutils -?`` to see detailed CLI usage.

JSON and TOML are the native formats of the configuration file. Notably, INI is not supported because it is not strongly typed and outdated.
YAML, JSON5, JSONC and Hjson formats are also supported for the configuration file, though the corresponding pip libraries must be installed.
To write the config in these formats, adhere to the analog of the same nested dictionary structure in the chosen language.

The exact parsing method used by this module may allow object nesting deviating from that shown, but you should strictly adhere to it.

To ensure all formats can be parsed, the ``pconf`` extra should be installed.

Modifying the context at runtime
--------------------------------

On the other hand, one may find it useful to alter the context dynamically. This can be achieved as follows:

.. code-block:: python

  asyncutils.getcontext().update( # call the update method of the current context to modify in-place
    {'SOCKET_TRANSPORT_LIMITS': (1024, 16384)}, # can optionally pass in a dictionary as the first and only positional argument
    ITER_TO_AGEN_DEFAULT_USE_EXISTING_EXECUTOR=True, # fields go here; keyword arguments are accepted
    observable_default_ntimes_n=3, # lowercase or mixed-case is allowed but not recommended
    lEAky_BUckeT_WaiT_for_toKEnS_tick=0.1 # fields do not have to be in order
  ) # check if a string is a valid field name using `name.upper() in asyncutils.all_contextual_constants`

For more detailed documentation on context usage, see the :mod:`context` page. You can think of it as similar to :mod:`decimal`, but with different
methods and attributes.
