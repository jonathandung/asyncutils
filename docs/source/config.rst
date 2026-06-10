Configuration
=============

.. version-added:: 0.8.21

.. currentmodule:: asyncutils.context

Environment Variables
---------------------

The below environment variables directly affect what this library does, mostly in its console, and by extension, the command line:

.. envvar:: AUTILSCFGPATH

  Absolute path to a configuration file
.. envvar:: FORCE_COLOR

  Force coloured output to be used; overrides ``TERM=dumb`` but emits a warning, since this is probably not meant

  .. attention::
    `FORCE_COLOR <force-color.org>`__, `NO_COLOR <no-color.org>`__ and :manpage:`TERM <term(7)>` control both the argument parser and the PyREPL console.

.. envvar:: NO_COLOR

  Force coloured output to be disabled; overrides :envvar:`FORCE_COLOR`

  .. note:: The override is an arbitrary Python convention. It differs in other languages and frameworks.

.. ifconfig:: py313

  .. envvar:: PYTHON_BASIC_REPL

    Use the pre-3.13 REPL if set and not empty, even if the newer REPL may be available

    .. important:: The console will set this variable to "1" when it sees TERM=dumb as long as ``-E`` is not passed to the Python interpreter.

.. envvar:: PYTHONSTARTUP

  Decode the file here with :mod:`tokenize` and execute as a Python source file, making its symbols accessible from the console

.. envvar:: TERM

  Turn off smart terminal features, including ANSI colour sequences, when set to "dumb"

.. note::

  The argument parser does not consider :envvar:`PYTHON_COLORS`, but the coloured edition of the console, which uses ``_colorize`` under the hood,
  may. To avoid this inconsistency, do not use it to customize :mod:`asyncutils`'s coloring.

.. seealso::

  :ref:`Colour control <python:using-on-controlling-color>`
    detailing how Python itself handles the colour-related environment variables above

.. version-changed:: 0.9.10
  Made consideration of environment variables coonsistent with specifications, no longer incorrectly requiring them to be set to "1".

Arguments to Python that are considered
---------------------------------------

.. version-added:: 0.9.4

Some arguments consumed by the Python interpreter are also taken into account by the library:

*
  .. ifconfig:: py313

    ``-E`` - Omit the execution of :envvar:`PYTHONSTARTUP` in the console namespace and the query of :envvar:`PYTHON_BASIC_REPL`

  .. ifconfig:: not py313

    ``-E`` - Omit the execution of :envvar:`PYTHONSTARTUP` in the console namespace

* ``-I`` - Implies ``-E`` (:data:`sys.flags` enforces this relationship out-of-the-box; documented here for completeness)
* ``-i`` - Always make the console interactive even if standard input is not a TTY

  .. warning::
    A piped standard input will cause deadlocks or fail for most shells, and this flag might worsen the situation. It is thus declared experimental
    and unstable; you might see this anomaly vanish after a single patch version, or in a push that does not even bump the patch.

* ``-q`` - To the REPL, ``python -q`` is equivalent to ``asyncutils -q``

.. tip::
  Even if ``python -S`` is used, which indeed does not load :mod:`site` as normal, the ``exit``, ``quit``, ``help``, ``copyright``, ``credits`` and
  ``license`` commands will still work as normal in the console since they are implemented natively, with the help of ``_sitebuiltins``. This is
  attributable to a PyREPL quirk or feature. However, accessing them in any fashion other than a bare statement will cause :exc:`NameError` to be
  thrown. There is also a ``clear`` command to clear the terminal screen that will fail similarly, but that is not related to ``-S``.

.. seealso::

  :ref:`Miscellaneous command-line args <python:using-on-misc-options>`
    authoritative source from the official Python docs

Basic Customization
-------------------

An extensible, two-part configuration system is in place.

The first, frozen part includes aspects such as where to output logging, customizing the underlying executor type used, and setting a seed for random
number generation using :envvar:`AUTILSCFGPATH`.

:envvar:`AUTILSCFGPATH` is read at the first import of this library, and the configuration is loaded and applied immediately. Errors will be thrown
as appropriate if the file is not found or contains values of the incorrect type, after the library tries its best to coerce the types, but you may
see a raw :exc:`ModuleNotFoundError` if the library cannot be located or executed.

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

====== ============== =========== ==================
Format File extension Module name PyPI package name
====== ============== =========== ==================
JSON   .json          json
TOML   .toml          tomllib
YAML   .yaml, .yml    yaml        PyYAML
JSONC  .jsonc         jsonc       json-with-comments
JSON5  .json5         json5       json5
Hjson  .hjson         hjson       hjson
XML    .xml           xmltodict   xmltodict
====== ============== =========== ==================

.. version-added:: 0.9.3
  Support for the XML (Extensible Markup Language) format.
  Be especially careful with using XML, because it is verbose, overkill and not recommeneded for use, especially with many simpler alternatives.

.. version-added:: 0.9.2
  Support for the TOML (Tom's Obvious Minimal Language) and YAML (YAML Ain't Markup Language) formats.

.. danger:: Many implementations used are subject to certain attacks related to crafting of input leading to quadratic complexity or worse.

.. seealso::

  `CVE-2025-9375 <https://nvd.nist.gov/vuln/detail/CVE-2025-9375>`__
    a vulnerability of the :class:`~xml.sax.saxutils.XMLGenerator` class from the standard library used by
    `xmltodict <https://pypi.org/project/xmltodict>`__ without input sanitization

    .. note:: This exploit is disputed by the maintainers of the project.

  `the CVE database <https://www.cve.org/CVERecord>`__
    for any new vulnerabilities

.. important::
  To write the config in each format, adhere to the exact analog of the nested dictionary structure shown in format.json5 in the chosen language.

.. tip::
  :collapsible:

  The :func:`~json.dumps` function from the module corresponding to the format, if any (following the :mod:`json` API), may help you to obtain this
  skeleton approximately.

.. warning::
  The exact parsing method used by this module may allow object nesting deviating from that shown, but you should still strictly adhere to it.

.. tip::
  :collapsible:

  To ensure all supported formats can be parsed, install the ``pconf`` :term:`extra`.

INI is not supported because it is outdated and lacks strong typing, meaning all values are interpreted as strings.

It is currently possible to associate file extensions not shown above with other libraries providing a ``load`` function taking a file object and
returning a dictionary, by modifying the map from file extensions to names of corresponding modules in ``_internal/unparsed.py`` called ``Z``.
However, it is believed that the options offered are versatile enough to fit every individual need.

Contextual "Constants"
----------------------

You can see that the json also includes many submodule names as keys; this is the second, contextual part of the configuration. It is thread-safe,
async-safe and mutable, thanks to :mod:`contextvars`. The sheer magnitude of options makes them infeasible to include as command line arguments.

By convention, they are called contextual constants since no code in this library is expected to change their values, only reading from them to
determine things from dynamic default arguments to frequencies of background tasks and internal thresholds.

One may find it useful to alter the context dynamically without creating a new context. This can be achieved by calling :meth:`Context.update`.

.. seealso::

  :meth:`Context.copy`
    \

  :meth:`Context.replace`
    \

  :meth:`Context.replace_from_dct`
    It is advisable to call these methods, each of which leaves the original context alone and derives a new one from it.

.. ifconfig:: py313

  :meth:`~Context.__copy__` and :meth:`~object.__replace__` are also implemented to help :func:`copy.copy` and :func:`copy.replace` respectively.

.. ifconfig:: not py313

  :meth:`Context.__copy__` is also implemented to help :func:`copy.copy`.

It is even better to use :class:`nonreusablelocalcontext`, which returns a one-time context manager, or the convenience method
:meth:`Context.ascurctx` on context objects that wraps it.

.. version-changed:: 0.8.27
  Started to recommend the use of :class:`nonreusablelocalcontext` rather than its parent class, :class:`localcontext`.

For more detailed documentation on context usage, see the :mod:`~asyncutils.context` page.

.. tip::
  :collapsible:

  You can think of the :class:`Context` class as similar to :class:`decimal.Context`, but with different methods and attributes
  and customizing an entire module insteasd of quirks and traps of the operations of a single class.
