Configuration
=============

Environment Variables
---------------------

The below environment variables directly affect what this library does, mostly in its console, and by extension, the command line:

* ``AUTILSCFGPATH`` - See below
* ``PYTHON_BASIC_REPL`` - Not read under ``python -E``
* ``PYTHONSTARTUP`` - Not executed with ``python -E``
* ``NO_COLOR`` - Overrides ``FORCE_COLOR`` (python convention)
* ``FORCE_COLOR`` - Overrides ``TERM``
* ``TERM`` - Turn off smart terminal features when set to "dumb"

Basic Customization
-------------------

An extensible, two-part configuration system is in place. The first part is static/frozen, detailed below.

It includes aspects such as where to output logging, customizing the underlying executor type used, and setting a seed for random number generation
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

The above keys have a near one-to-one correspondence with the command line arguments, as the comments below each key explain. Use ``asyncutils -?``
to see detailed CLI usage.

JSON and TOML are the native formats of the configuration file, the parsers for which come with the standard library.
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

.. tip::
  :collapsible:

  To ensure all formats can be parsed, the ``pconf`` extra should be installed.

Contextual "Constants"
----------------------

You can see that the json also includes many submodule names as keys; this is the second, contextual part of the configuration. It is thread-safe,
async-safe and mutable, thanks to :mod:`contextvars`. The sheer magnitude of options makes them infeasible to include as command line arguments.

By convention, they are called contextual constants since no code in this library is expected to change their values, only reading from them to
determine things from dynamic default arguments to frequencies of background tasks and internal thresholds.

One may find it useful to alter the context dynamically without creating a new context. This can be achieved as follows:

.. code-block:: python

  asyncutils.getcontext().update( # call the update method of the current context to modify in-place
    {'SOCKET_TRANSPORT_LIMITS': (1024, 16384)}, # can optionally pass in a dictionary as the first and only positional argument
    ITER_TO_AGEN_DEFAULT_USE_EXISTING_EXECUTOR=True, # fields go here; keyword arguments are accepted
    observable_default_ntimes_n=3, # lowercase or mixed-case is allowed but not recommended
    lEAky_BUckeT_WaiT_for_toKEnS_tick=0.1 # fields do not have to be in order
  ) # check if a string is a valid field name using `name.upper() in asyncutils.all_contextual_constants`

However, due care must be exercised to avoid messing up other parts of your program relying on this context. It is advisable to call the following
methods that leave the original context alone by deriving a new one from it:

* :meth:`~asyncutils.context.Context.copy`
* :meth:`~asyncutils.context.Context.replace`
* :meth:`~asyncutils.context.Context.replace_from_dct`

:meth:`~asyncutils.context.Context.__copy__` and :meth:`~asyncutils.context.Context.__replace__` are also implemented to help :func:`copy.copy` and
:func:`copy.replace` (python 3.13+) respectively.

For more detailed documentation on context usage, see the :mod:`context` page.

.. tip::
  :collapsible:

  You can think of the :class:`~asyncutils.context.Context` class as similar to :class:`decimal.Context`, but with different methods and attributes.
