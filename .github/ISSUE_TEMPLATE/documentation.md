---
name: Documentation issue
about: Point out an issue with documentation, including inconsistency with runtime behaviour that is likely not a bug
title: ''
labels: docs
assignees: jonathandung
---

## Type

If the issue is a minor typo or tiny grammar fault, open a PR directly.
Otherwise, do not open a PR until your issue has been triaged.

Only report issues with the latest version of the docs, not the stable build.
If the referenced build is outdated by five builds or more, the issue will be closed.

## Links

Link to the generated html page or the source file (.rst; .pyi if issue lies in API reference from stub docstrings) in this section.

For the reviewer's convenience, you are encouraged to include both.

## Description

Describe the problem concisely and include a possible solution if you see fit.

## Examples

Situations where, for instance, the current documentation phrasing would apply but the actual behaviour differs. Delete if irrelevant.

## Screenshots

If applicable, add screenshots to help explain your problem.

## Complete the following

- Python version tag (`python -VV`)
- Read the docs build number; see [this page](https://app.readthedocs.org/projects/asyncutils/builds/?utm_source=asyncutils&utm_content=flyout)
- Package version (`pip show py-asyncutils | grep Version:` or `conda list py-asyncutils --fields version`)

## Additional context

Add any other context about the problem here.
