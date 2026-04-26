Configuration
=============

Basic Customization
-------------------

:mod:`asyncutils` is highly customizable, with an extensible configuration system.

This includes aspects such as where to output logging, customizing the underlying executor type used, and setting a seed for random number generation
using the ``AUTILSCFGPATH`` environment variable (all uppercase for Windows support), which should point to an absolute path to a configuration .json
or .jsonl file. ``AUTILSCFGPATH`` is read at the first import of this library, and the configuration is loaded and applied immediately. Errors will
be thrown as appropriate if the file is not found or contains values of the incorrect type, after the library tries its best to coerce the types.

New options will likely be added in the future, but every current option is considered stable and has a corresponding default value.

The options are shown below, along with their default values and descriptions:

.. literalinclude:: ../../asyncutils/format.json5
  :language: json5
  :caption: config file format
  :force:

The above keys have a near one-to-one correspondence with the command line arguments. Use ``asyncutils -?`` to see detailed CLI usage.

Note that though the format above is in json5 for readability, you should write the configuration file in standard JSON.

Modifying the context
---------------------

On the other hand, one may find it useful to configure the contextual constants in :mod:`~asyncutils.context`. However, due to the sheer magnitude of
options, it would be infeasible to include them in the command line. Therefore, it is advised to toggle that in your app-/project-/library-wide
config submodule, or when :mod:`asyncutils` is first imported or used, as follows:

.. code-block:: python

  import asyncutils
  asyncutils.setcontext(asyncutils.Context(
    ITER_TO_AITER_DEFAULT_USE_EXISTING_EXECUTOR=True, # fields go here
    observable_default_ntimes_n=3, # lowercase is allowed but not recommended
    lEAky_BUckeT_WaiT_for_toKEnS_tick=0.1 # fields do not have to be in order
  )) # check if a string is a vaild field name using `name.upper() in asyncutils.all_contextual_constants`

Please read the documentation there as well to get an idea of what each field does.
