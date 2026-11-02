Development Chores
==================

.. highlight:: bash

This file aims to detail guidelines for some monotonous tasks contributors to this
library may need to complete in different recurring scenarios.

Preliminaries
-------------

To start development, run the following::

  git clone https://github.com/jonathandung/asyncutils.git
  cd asyncutils
  make setup
  # installs prek v0.5.10, the latest version of uv, ruff and ty (as tools), then
  # creates a virtual environment at .venv using uv and installs asyncutils in editable
  # mode along with its development dependencies into the environment
  . .venv/bin/activate # or how you would normally activate the uv environment in your
  # preferred shell

If you are using an IDE outside of the VS Code family, you may want to use an
`.editorconfig <https://editorconfig.org>`__ extension.

Adding words to the incorrect spelling whitelist
------------------------------------------------

Edit ``assets/words.txt`` and check for regressions by running ``cspell .``.

Bumping the version
-------------------

1. Do a per-file find-and-replace in your preferred IDE after inspecting each instance
   to avoid unintended changes. :data:`~asyncutils.__version__` is already instantiated
   from a string to streamline this step.
2. In pyproject.toml, there may be optional dependencies whose version coincides with
   the project's, so take care not to modify those as well.
3. Also exclude the ``CHANGELOG.md`` at the project root from the replace operation.
4. A core developer will help you create a GitHub release with default release notes
   using ``make release``. This will automatically trigger, among others, a stable Read
   the Docs build, a push to PyPI and cause a conda-forge bot automerge.
5. If you include your desired remarks in the PR under a "Release Notes" section, those
   will be used as the release notes instead after said core developer tries their best
   to correct grammatical or spelling mistakes.

Cleaning artifacts and caches
-----------------------------

Safer: ``make clean``; more aggressive: ``make clean-all``.

Implementing a new utility
--------------------------

Add proper stubs for it in the .pyi file and include it in the appropriate
``<submodule>_all`` declaration in ``asyncutils/_internal/submodules.py``. Also add
tests such that at least the required coverage is still met.

Adding a new submodule
----------------------

1. Search for 'rwlocks' (without the quotes) across all files in the repository,
   excluding asyncutils/rwlocks.py, asyncutils/_internal/types.pyi and
   docs/source/chores.rst. This should reveal all the locations where submodule names
   are referenced. Still check each one to see if it is a correct place.
2. Insert the new submodule name as a string in those occurrences, maintaining
   alphabetical order where applicable.
3. Bear in mind that the submodule name should not have more than one word, should not
   contain underscores or uppercase letters, and a stub should be created for it that
   contributors should update in parallel.
4. Add a test file for the new submodule importing all names from the submodule.

Adding a new configuration option
---------------------------------

This will not usually be done by a contributor, only a collaborator, because there
should be evidence that the change is imperative or desirable in a dedicated GitHub
discussions thread.

After reviewing the pitch, the collaborator will step in and make necessary changes to
the argument parser, documentation and internal machinery.

For collaborators and those interested, this is the general procedure:

1. Edit the setup of the argument parser and the dictionary of defaults ``N`` in
   ``_internal/unparsed.py``.
2. Edit ``format.json5`` by adding the key in the same order as the new help from the
   parser appears and a comment describing what it does, and take note of the line
   numbers where the pairs corresponding to logging configuration are shifted to.
3. If the value of the configuration option is to be accessible by users at runtime, it
   should be in the form of a symbol in :mod:`~asyncutils.config`.
4. Update ``config.pyi``, noting the line numbers at which the logging-related
   declarations appear.
5. Edit the definition of :func:`~asyncutils.tools.cfg_to_argv` and update the test
   suite to account for that, preserving round-trip conversion as promised.
6. Update the literalinclude's in logging.rst with the line numbers jotted down from
   steps 2 and 4.
7. Run ``make docs`` and look at the help pages in the generated documentation as a
   sanity check.

Adding a new contextual constant
--------------------------------
..
  cspell:disable

The name of the constant should be of the form
``UTILITYNAME_OPTIONALMETHODNAME_DEFAULT_ARGNAMEINCAPS`` if it acts as a dynamic
default value, the most common case by far. Note the uppercase, underscores and rigid
format.

..
  cspell:enable

After verifying the integrity of the field name according to this metric, navigate to
the following locations relative to the project root and complete the following:

* asyncutils/format.json5

  Find the submodule and add in part of the option name in the object under the
  appropriate pattern. If this causes there to be more than one option for a utility
  with no dedicated mapping having it as key, create one and merge the other in. If
  these guidelines sound vague, surrounding keys will help you. Bear in mind that
  because of organizational, readability, maintainability and consistency standards,
  the options should be in the same order as those in ``context.pyi``, as elaborated on below.

  .. caution::
    The option name should be lowercase, as opposed to being fully capitalized, much
    like how you are recommended to access it.
  .. attention::
    Also remember to update the line numbers in the literalinclude directive referring
    to format.json5 in logging.rst.
* asyncutils/format.hjson, asyncutils/format.toml, asyncutils/format.yaml

  Update them accordingly.
* asyncutils/context.pyi

  Be sure to update the contextual constant count:

  - in the :const:`~asyncutils.context.all_contextual_consts` docstring,
  - within the :class:`~asyncutils.context.Context` fake dataclass body, and
  - at the top level.

  Keep alphabetical order within the submodule concerned, with submodules ordered
  alphabetically as well.
* asyncutils/_internal/unparsed.py

  There should be a massive dictionary assigned to the name ``C`` that contains the
  option names mapped to their factory defaults on line 5. Edit it accordingly.

Regenerating the lockfile after dependency updates
--------------------------------------------------

Run ``make lock``.

Updating config.pyi
-------------------

Special care must be taken, since the :doc:`logging` page depends on the exact line
numbers at which specific symbols are declared here in the form of a literalinclude.
The same applies for format.json5 and friends. Take a look at the current state of the
site, and hopefully you can determine what the new line numbers should be accordingly.

Adding a documentation page
---------------------------

1. Choose a format: .md or .rst.
   Though .md is easier to write, you may want .rst for its rich directive support that
   integrates seamlessly with Sphinx and allows for smoother redirection.
2. Choose a location depending on how visible you wish the page to be: ``docs/source``
   or the project root.
3. If the page is of paramount importance even to end users or people doing a
   read-through of the project, expand the README with a new section containing a
   summary and linking to the page on the bottom.
4. Update the relevant table of contents tree (toctree) in docs/source/index.rst. Do
   not move documents across the four different trees.
5. If copying from the root to the Read the Docs page is required during build, so that
   users can see it in both places, add an entry to the mapping representing sources
   and respective targets for copy statements inlined in .readthedocs.yaml, maintaining
   alphabetical order.

Changing help messages for command-line arguments
-------------------------------------------------

Remember not to indent the help strings when using multiline strings; keep them at the
left margin such that they display correctly. Then run ``make docs``.

Modifying the Makefile
----------------------

Remember to sync up the Makefile with ``make.bat`` in the same directory, and vice
versa. If you wish to remove a target, it must have exceeded a previously declared
deprecation period, and been moved into a special section with a "Deprecated targets"
header in the ``make help`` output. Finally, run ``make docs``.

Adding tests
------------

Make sure the name of the test function is prefixed with "test\_" such that
:mod:`!pytest` correctly discovers it. Run :mod:`!pytest` on each test individually
with the ``pytest-asyncio`` plugin instead of ``pytest-asyncio-cooperative`` (since its
benefits do not apply for singular tests), to verify the test is written correctly and
your implementation is resilient against edge cases. Do not drop edge cases from tests
because they do not pass; try your best to fix the code instead. If you are unable to
do so, please ask for help in the issue or PR discussion.

.. tip::
  :collapsible:

  If you are puzzled as to how to write tests for your feature, you may simply try it
  out in the console and check its behaviour against your expectations, and include the
  statements you entered in the console in your issue or PR description. The maintainer
  who is to merge your PR can write the tests for you.

.. seealso::

  `This basic pytest how-to <https://docs.pytest.org/en/stable/how-to/assert.html>`__
    assert statement usage and other fundamental guidelines, for those more used to
    other frameworks like :mod:`unittest`.

Before committing, run the whole test suite by entering the following command at the
project root to check for regressions and update the relevant static badges in the
readme::

  make badges

If the tests are failing, do not commit the badges, since reviewers would assume your
PR is ready for merging when you do so, and may close the PR just because they don't
appear with a passing status.
