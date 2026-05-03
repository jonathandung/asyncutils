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

The options are shown below, along with their default values and descriptions:

.. literalinclude:: ../../asyncutils/format.json5
  :language: json5
  :caption: config file format
  :force:

New options will likely be added in the future, but every current option is considered stable and has a corresponding default value.

The above keys have a near one-to-one correspondence with the command line arguments, as the comments below each key explain; besides the contextual
constants, due to the sheer magnitude of options making them infeasible to include. Use ``asyncutils -?`` to see detailed CLI usage.

JSON and TOML are the native formats of the configuration file.
YAML, JSON5, JSONC and Hjson formats are also supported for the configuration file, though the corresponding pip libraries must be installed.

.. attention::
  :collapsible:

  To write the config in each format, adhere to the analog of the nested dictionary structure shown in format.json5 in the chosen language.

.. danger::

  Many implementations used are subject to certain attacks related to crafting of input leading to quadratic complexity or worse.
  Write your configs yourself to avoid malicious inputs exhausting computing resources.

.. important::

  INI is not supported because it is outdated and lacks strong typing; that is, all values are interpreted as strings.

.. warning::

  Though the exact parsing method used by this module may allow object nesting deviating from that shown, you should still strictly adhere to it.

.. admonition::
  :collapsible:

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

For more detailed documentation on context usage, see the :mod:`context` page.
.. tip::
  :collapsible:

  You can think of the :class:`~asyncutils.context.Context` class as similar to :mod:`decimal`, but with different methods and attributes.
