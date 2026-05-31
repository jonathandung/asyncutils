Development Chores
==================

.. version-added:: 0.9.6

This file aims to detail guidelines for some monotonous tasks contributors to this library may need to complete in different recurring scenarios.

Bumping the version
-------------------

Using something like ``uv version --bump patch`` to increment the patch version may not work because the version as a string is hardcoded into
certain locations. Instead, follow these steps:

1. Do a per-file find-and-replace in your preferred IDE after inspecting each instance to avoid unintended changes. :data:`__version__` is already
   instantiated from a string to streamline this step.
2. In pyproject.toml, there may be optional dependencies whose version coincides with the project's, so take care not to modify those as well.
3. Also exclude the changelog file (CHANGELOG.md, at the project root) from the replace operation.
4. A core developer of this project will help you create a GitHub release with the default release notes.
5. This will automatically trigger a stable Read the Docs build, a push to PyPI and cause a conda-forge bot automerge.
6. If you include your desired remarks in the PR under a "Release Notes" section, those will be used as the release notes instead after the developer
   tries their best to correct grammatical or spelling mistakes.

.. note:: Our release schedule, though stabilizing, does not concern the frequency of patch releases, while that is usually every 2-3 days as of now.

.. note::
  :collapsible:

  There is no lower bound on the number of patches per minor, though because support for packing versions into integers in a specific format must
  be supported, and there is concern of code churn or low-quality changes, the upper bound is 256, i.e. the numbers from 0 to 255.
  The same applies for minor releases per major, but we aim to drop majors every year and minors per month, so this should be a non-issue.

Adding a new submodule
----------------------

1. Search for 'rwlocks' (without the quotes) across all files in the repository, excluding asyncutils/rwlocks.py, asyncutils/_internal/types.pyi and
   this file. This should reveal all the locations where submodule names are referenced. Still check each one to see if it is a correct place.
2. Insert the new submodule name as a string in those occurrences, maintaining alphabetical order where applicable.
3. Bear in mind that the submodule name should not have more than one word, should not contain underscores or uppercase letters, and a stub should be
   created for it that contributors should update in parallel. The stubtest tool from mypy will not work because we use ty ignores that mypy doesn't
   recognize, causing stubtest to report something along the lines of "Not checking due to mypy build errors".
4. Add a test file for the new submodule importing all names from the submodule.

Adding a new configuration option
---------------------------------

This will not usually be done by a contributor, only a collaborator, because there should be evidence that the change is imperative or desirable in a
dedicated GitHub discussions thread. Stack Overflow is only for general questions; you should really not be tagging :mod:`asyncutils` there.
After reviewing the pitch, the collaborator will step in and make necessary changes to the argument parser, documentation and internal machinery.

For collaborators and those interested, this is the general procedure:

1. Edit the setup of the argument parser and the dictionary of defaults :data:`N` in ``_internal/unparsed.py``. It is not a :class:`frozendict`
   because the class was introduced in Python 3.15. (It will be in asyncutils 7.0, however.)
2. Edit ``format.json5`` by adding the key in the same order as the new help from the parser appears and a comment describing what it does, and take
   note of the line numbers where the pairs corresponding to logging configuration are shifted to.
3. If the value of the configuration option is to be accessible by users at runtime, it should be in the form of a symbol in :mod:`config`.
4. Update config.pyi, noting the line numbers at which the logging-related declarations appear.
5. Edit the definition of :func:`tools.json_to_argv` and update the test suite to account for that, preserving round-trip conversion as promised.
6. Update the literalincludes in logging.rst with the line numbers marked down from steps 2 and 4.
7. Execute the platform-suitable genhelp batch file as a sanity check, but do not commit the outputs.

Adding a new contextual constant
--------------------------------

The name of the constant should be of the form ``UTILITYNAME_OPTIONALMETHODNAME_DEFAULT_ARGNAMEINCAPS`` if it acts as a dynamic default value, the
most common case by far. Note the uppercase, underscores and rigid format.

After verifying the integrity of the field name according to this metric, navigate to the following locations relative to the project root and
complete the following:

* asyncutils/format.json5

  Find the submodule and add in part of the option name in the object under the appropriate pattern. If this causes there to be more than one option
  for a utility with no dedicated mapping having it as key, create one and merge the other in. If these guidelines sound vague, surrounding keys will
  help you. Bear in mind that because of organizational, readability, maintainability and consistency standards, the options should be in the same
  order as those in ``context.pyi``, as elaborated on below.

  .. caution:: The option name should be lowercase, as opposed to being fully capitalized like how you are recommended to access it.
  .. attention:: Also remember to update the line numbers in the literalinclude directive referring to format.json5 in logging.rst.
* asyncutils/context.pyi

  Be sure to update the contextual constant count:

  - in the :data:`~context.all_contextual_constants` docstring,
  - within the :data:`~context.Context` fake dataclass body, and
  - at the top level.

  Keep alphabetical order within the submodule concerned, with submodules ordered alphabetically as well.
* asyncutils/_internal/unparsed.py

  There should be a massive dictionary called :data:`~asyncutils._internal.unparsed.C` that contains the option names mapped to their factory
  defaults on line 5. Edit it accordingly.

Updating config.pyi
-------------------

Special care must be taken, since the :doc:`logging` page depends on the exact line numbers at which specific symbols are declared here in the form
of a literalinclude. The same applies for format.json5. Take a look at the current state of the site, and hopefully you can determine what the new
line numbers should be accordingly.

Adding a documentation page
---------------------------

1. Choose a format: .md or .rst.
   Though .md is easier to write, one may want .rst for its rich directive support that integrates seamlessly with Sphinx and allows for smoother
   redirection, though the MyST parser is improving to accommodate these.
2. Choose a location depending on how visible you wish the page to be: ``docs/source`` or the project root.
3. If the page is of paramount importance even to end users or people doing a read-through of the project, expand the README with a new section
   containing a summary and linking to the page on the bottom.
4. Update the relevant table of contents tree (toctree) in docs/source/index.rst. Do not move documents across the four different trees.
5. If copying from the root to the Read the Docs page is required during build, so that users can see it in both places, add an entry to the mapping
   representing sources and respective targets for copy statements in scripts/rtd.sh, maintaining alphabetical order.

.. note:: ``autoapi_keep_files`` is set to ``True`` in conf.py only to allow local incremental builds. Do not commit the docs/source/api directory!

Changing help messages for command-line arguments
-------------------------------------------------

Remember not to indent the help strings when using multiline strings; keep them at the left margin such that they display correctly.

If you want to preview the changes to the argument parser help in the form of an HTML page, run ``scripts/genhelp.sh`` on Unix or
``.\scripts\win\genhelp.ps1`` on Windows before running the sphinx-build command. Do not, however, commit the resultant file.

Modifying the Makefile
----------------------

Remember to sync up the Makefile with ``make.bat`` in the same directory, and vice versa. If you wish to remove a target, it must have exceeded a
previously declared deprecation period, and been moved into a special section with a "Deprecated targets" header in the ``make help`` output.

If you want to preview the changes to the help message in the form of the eventually created page, run ``scripts/genmakefileusage.sh`` on Unix or
``.\scripts\win\genmakefileusage.ps1`` on Windows before running ``sphinx-build``. Do not, however, commit the resultant file.

Adding tests
------------

Make sure the name of the test function is prefixed with "test\_" such that pytest correctly discovers it. Run pytest, selecting only that test, to
verify the test is written correctly and your implementation is resilient against edge cases.

.. tip::
  :collapsible:

  If you are puzzled as to how to write tests for your feature, you may simply try it out in the console and check its behaviour against your
  expectations. As long as you include the statements you entered in the console in your issue or PR description, the maintainer making the merge
  commit can write the tests for you.

.. seealso::

  `This basic pytest how-to <https://docs.pytest.org/en/stable/how-to/assert.html>`__
    includes assert statement usage and other fundamental guidelines, for those more used to other frameworks like :mod:`unittest`.

Before committing, run the whole test suite by entering the following command at the project root to check for regressions and update the relevant
static badges in the README:

::

  make test-with-badges

If the tests are failing, do not commit the badges! Reviewers would assume your PR is ready for merging when you commit the badge, and may close the
PR if they don't appear with a passing status.

.. version-changed:: 0.9.9
  A bare ``pytest`` can no longer cover all the necessary options. Use the above command only.

.. version-changed:: 0.9.9
  Use pytest-asyncio-cooperative instead of the less idiomatic pytest-asyncio wherever possible. However, a complication arises because the former
  does not mix well with coverage, and a separate run must be employed in the test-with-badges target to account for this.

.. version-added:: 0.9.9
  The test-with-badges target.

.. version-changed:: 0.9.9
  In light of massive pytest-local-badge updates with the 1.1.1 release making four more badges available to choose from, the command has been
  changed. Update your workflow and the plugin accordingly.

.. note:: The above snippet requires the pytest-local-badge plugin, which should come packaged with the tests dependency group.

The test ought to go in the test source file corresponding to the submodule from which the feature can be publicly imported, even if its
implementation is spread across files, with the exceptions of the base and iterclasses submodules, whose tests I find inseparable with the logic for
tests for :mod:`iters`, compelling me to put them into ``tests/test_iters.py`` together.
