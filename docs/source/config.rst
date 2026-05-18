Configuration
=============

Environment Variables
---------------------

The below environment variables directly affect what this library does, mostly in its console, and by extension, the command line:

* ``AUTILSCFGPATH`` - See below
* ``FORCE_COLOR`` - Force coloured output to be used; overrides ``TERM=dumb`` but emits a warning, since this is probably not meant

  .. attention:: ``FORCE_COLOR``, ``NO_COLOR`` and ``TERM=dumb`` control both the argument parser and the PyREPL console.

* ``NO_COLOR`` - Force coloured output to be disabled; overrides ``FORCE_COLOR``

  .. note:: The override is an arbitrary Python convention. It may be different in other languages.

.. ifconfig:: py313

  * ``PYTHON_BASIC_REPL`` - Use the pre-3.13 REPL if equal to "1", even if the newer REPL may be available

    .. important:: The console will set this variable to "1" when it sees TERM=dumb as long as ``-E`` is not passed to the Python interpreter.

* ``PYTHONSTARTUP`` - Decode the file here with :mod:`tokenize` and execute as a Python source file, making its symbols accessible from the console
* ``TERM`` - Turn off smart terminal features, including ANSI colour sequences, when set to "dumb"

.. note::

  The argument parser does not consider the ``PYTHON_COLORS`` environment variable, but the coloured edition of the console, which uses
  :mod:`_colorize` under the hood, may. To avoid this inconsistency, do not use ``PYTHON_COLORS`` to customize :mod:`asyncutils`'s coloring.

Arguments to Python that are considered
---------------------------------------

Some arguments consumed by the Python interpreter are also taken into account by the library:

* ``-E`` - Omit the query of ``PYTHON_BASIC_REPL`` and the execution of ``PYTHONSTARTUP`` in the console namespace
* ``-I`` - Implies ``-E`` (:data:`sys.flags` enforces this implication already)
* ``-i`` - Always make the console interactive even if standard input is not a TTY

  .. warning:: A piped standard input will cause deadlocks or fail for most shells, and this flag may make it worse.

* ``-q`` - To the REPL, ``python -q`` is equivalent to ``asyncutils -q``

.. tip::

  Even if ``python -S`` is used, the ``exit``, ``quit``, ``help``, ``copyright``, ``credits`` and ``license`` commands will still work as normal in
  the console since they are implemented natively, albeit with the help of :mod:`_sitebuiltins`. However, accessing them in any fashion other than a
  bare statement will cause :exc:`NameError` to be thrown. There is also a ``clear`` command to clear the terminal screen that will fail similarly.

Basic Customization
-------------------

An extensible, two-part configuration system is in place. The first part is static/frozen, detailed below.

It includes aspects such as where to output logging, customizing the underlying executor type used, and setting a seed for random number generation
using the ``AUTILSCFGPATH`` environment variable, which should point to an absolute path to a configuration file.

``AUTILSCFGPATH`` is read at the first import of this library, and the configuration is loaded and applied immediately. Errors will be thrown as
appropriate if the file is not found or contains values of the incorrect type, after the library tries its best to coerce the types, but you may see
raw :exc:`ModuleNotFoundError`'s if the library cannot be located or executed.

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

The config file can be written in the below formats, listed with the third-party libraries they require if any:

====== ============== ================== ===========
Format File extension PyPI package name  Module name
====== ============== ================== ===========
JSON   .json                             json
TOML   .toml                             tomllib
YAML   .yaml, .yml    PyYAML             yaml
JSON5  .json5         json5              json5
JSONC  .jsonc         json-with-comments jsonc
Hjson  .hjson         hjson              hjson
XML    .xml           xmltodict          xmltodict
====== ============== ================== ===========

.. danger::

  Many implementations used are subject to certain attacks related to crafting of input leading to quadratic complexity or worse.
  Be especially careful with XML. It is verbose, overkill and not recommeneded for use, especially with many simpler alternatives.
  Thus, write your configs yourself to avoid malicious inputs exhausting computing resources.

.. seealso::

  `CVE-2025-9375 <https://nvd.nist.gov/vuln/detail/CVE-2025-9375>`__
    a vulnerability of the :class:`xml.sax.saxutils.XMLGenerator` class of the standard library used by :mod:`xmltodict` without input sanitization

  `the CVE database <https://www.cve.org/CVERecord>`__
    for any new vulnerabilities


.. important::

  To write the config in each format, adhere to the analog of the nested dictionary structure shown in format.json5 in the chosen language.

.. warning::

  Though the exact parsing method used by this module may allow object nesting deviating from that shown, you should still strictly adhere to it.

.. note::

  INI is not supported because it is outdated and lacks strong typing, meaning all values are interpreted as strings.

.. tip::
  :collapsible:

  To ensure all supported formats can be parsed, install the ``pconf`` :term:`extra`.

.. note::

  It is currently possible to associate file extensions not shown above with other libraries providing a :func:`load` function taking a file object
  and returning a dictionary, by modifying the :data:`asyncutils._internal.unparsed.D` map from file extensions to names of corresponding modules.
  However, it is believed that the offered options are versatile enough to fit every individual need, so this functionality is just a quirk of the
  implementation that just so happens to have been declared stable.

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
    lEAky_BUckeT_WaiT_for_toKEnS_tick=0.1, # fields do not have to be in order
    WAIT_FOR_SIGNAL_DEFAULT_SIGNALS=[2] # list will be automatically converted into tuple
  ) # check if a string is a valid field name using `name.upper() in asyncutils.all_contextual_constants`

However, due care must be exercised to avoid messing up other parts of your program relying on this context. It is advisable to call the following
methods that leave the original context alone by deriving a new one from it:

* :meth:`~asyncutils.context.Context.copy`
* :meth:`~asyncutils.context.Context.replace`
* :meth:`~asyncutils.context.Context.replace_from_dct`

:meth:`~asyncutils.context.Context.__copy__` and :meth:`~asyncutils.context.Context.__replace__` are also implemented to help :func:`copy.copy` and
:func:`copy.replace` (python 3.13+) respectively.

It is even better to use :class:`asyncutils.context.nonreusablelocalcontext`, which returns a one-time context manager, or the convenience method
:meth:`~asyncutils.context.Context.ascurctx` on context objects that wraps it.

For more detailed documentation on context usage, see the :mod:`context` page.

.. tip::
  :collapsible:

  You can think of the :class:`~asyncutils.context.Context` class as similar to :class:`decimal.Context`, but with different methods and attributes
  and customizing an entire module insteasd of quirks of the operations of a single class.
