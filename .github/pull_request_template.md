<!--markdownlint-disable-next-line MD041-->
## Checklist

<!--Please delete all comments and inapplicable sections, but leave checkbox descriptions unedited.-->

### All PRs

- [] I have skimmed through the [contributing guidelines](https://asyncutils.readthedocs.io/en/latest/contributing.html) and followed relevant links.
- [] All existing tests pass locally, according to ``make test``.
- [] No lints or type checker complaints have emerged as a direct consequence of my change.
- [] I did not add a broken link. This has been checked on the GitHub view and the generated documentation pages.

#### Title

- [] The pull request title is descriptive.
- [] The title is prefixed with one of "bugfix", "docs", "deps", "feat", "pattern", "tests", followed by a colon.
- [] The full expanse of the title fits in the box without scrolling to the right.

### For documentation PRs

- [] Local Sphinx build passes.
- [] I have refrained from touching `docs/source/conf.py` unless absolutely necessary.

### For small PRs

- [] This is a one-off change, or I have gathered as many homogeneous changes as I can find across the codebase to be patched at once by this PR.

### For big PRs

- [] If this PR concerns a big architectural change or loosely related modifications, I have split them into smaller PRs tracked in an umbrella issue
     linked to in the Issue reference section without marking it as a resolution.
- [] I have added passing tests such that the coverage did not decrease by over 0.5%.
- [] Documentation has been updated suitably.
- [] The section corresponding to the next release in the changelog has been updated.
- [] I have read through [the chores page](https://asyncutils.readthedocs.io/en/latest/chores.html) and followed through with the relevant processes.

## Summary

<!--Briefly describe the feature being introduced, the bug being rectified or the tool being implemented, whichever applies.-->

## Changes

<!--List where all changes were applied. Preferably, explain the rationale of each change in sub-sections.-->

## Issue reference

Closes #<!--Replace this comment with the issue number or delete this section if there is no corresponding issue.-->.

## Additional context

<!--Enter helpful context here. Include shell commands in a tripe-backtick-fenced code block with language "bash", or "console" if their output is
included, Python code with language "python", and Python REPL content with language "pycon".-->

### Screenshots

### Relevant Links
