Development Chores
==================

This file aims to detail guidelines for some repetitive tasks contributors to this library may need to complete in different recurring scenarios.

.. hint::
  :collapsible:

  The Makefile is sometimes a handy companion in development. Execute ``make help`` to see the available Makefile targets.
  More of them will likely be added on popular demand.

Bumping the version
-------------------

You can use ``uv version --bump patch`` to increment the patch version, and do a per-file find-and-replace in your preferred IDE after inspecting
each instance to avoid unintended changes. :const:`__version__` is already instantiated from a string to streamline this step.

In pyproject.toml, there may be optional dependencies whose version coincides with the project's, so take care not to modify those as well.
Also exclude the changelog file (CHANGELOG.md, at the project root) from the replace operation.

Our release schedule, though stabilizing, does not concern the frequency of patch releases. There is no lower bound on the number of patches per
minor, though due to bit packing shenanigans and concern of code churn or low-quality changes, the upper bound is 256, from 0 to 255. The same
applies for minor releases per major, but we aim to drop majors every year and minors per month, so this should be a non-issue.

Adding a new submodule
----------------------

Search for 'rwlocks' across all files in the repository, excluding asyncutils/rwlocks.py. This should reveal all the locations where submodule names
are referenced without fail. Insert the new submodule name as a string in those occurrences, maintaining alphabetical order where applicable. Bear in
mind that the submodule name should not have more than one word, should not contain underscores or uppercase letters, and a stub should be created
for it that contributors should update in parallel. The stubtest tool from mypy will not work because we use ty ignores that mypy doesn't recognize.

Adding a new configuration option
---------------------------------

This will not usually be done by a contributor, only a collaborator, because there should be evidence that the change is imperative or desirable in a
dedicated GitHub discussions thread. After reviewing the pitch, the collaborator will step in and make necessary changes to the argument parser,
documentation and internal machinery.

Adding a new contextual constant
--------------------------------

The name of the constant should be of the form ``UTILITYNAME_OPTIONALMETHODNAME_DEFAULT_ARGNAMEINCAPS`` if it acts as a dynamic default value, the
most common case by far. Note the uppercase, underscores and rigid format.

After verifying the integrity of the field name according to this metric, navigate to the following locations relative to the project root and
complete the following:

* asyncutils/format.json5

  Find the submodule and add in part of the option name in the object under the appropriate pattern. If this causes there to be more than one option
  for a utility with no dedicated mapping having it as key, create one and move the other in. If these guidelines sound vague, surrounding keys will
  help you.
* asyncutils/context.pyi

  Be sure to update the contextual constant count:
  - in the :data:`~context.all_contextual_constants` docstring,
  - within the :data:`~context.Context` fake dataclass body, and
  - at the top level.

  Keep alphabetical order within the submodule concerned, with submodules ordered alphabetically as well.
* asyncutils/_internal/unparsed.py

  There should be a massive dictionary affixed with ``# pragma: allowlist secret`` that contains the option names mapped to their factory defaults.
  Edit that dictionary accordingly.

Adding a documentation page
---------------------------

1. Choose a format: .md or .rst.
   Though .md is easier to write, one may want .rst for its rich directive support that integrates seamlessly with Sphinx and allows for smoother
   redirection, though the MyST parser is improving to accommodate these.
2. Choose a location: docs/source or the project root.
3. If the page is of paramount importance even to end users or people doing a read-through of the project, expand the README with a new section
   containing a summary and linking to the page on the bottom.
4. Update the relevant table of contents tree (toctree) in docs/source/index.rst. Do not move documents across the four different trees.
5. If copying from the root to the Read the Docs page is required during build, so that users can see it in both places, update .readthedocs.yaml
   by adding a cp (copy) statement in the post_create_environment job, following the syntax of its sibling commands.
