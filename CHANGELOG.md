---
hide-toc: true
---

# Changelog

All notable changes to this project are and will be documented in this file.

This project uses [Semantic Versioning](https://semver.org) since v1.3.1.

## [1.3]

### [1.3.0] - 2026-09-22; newest

Changed all extras to dependency groups; removed XML config parsing since XML is not typed.

## [1.2]

### [1.2.4] - 2026-09-06

Upgraded to Python 3.15.0rc2.

### [1.2.3] - 2026-08-31

Refactors.

### [1.2.2] - 2026-08-29

Again, some workflow changes.

### [1.2.1] - 2026-08-25

Various workflows.

### [1.2.0] - 2026-08-19

Started using Zizmor.

## [1.1]

### [1.1.4] - 2026-08-18

Pinned GitHub workflow action usages by hashes; some workflow enhancements.

### [1.1.3] - 2026-08-13

Switched from detect-secrets to betterleaks; added `asyncutils bug` subcommand.

### [1.1.2] - 2026-08-03

Some bugfixes and moves around submodules.

## [1.0]

Breaking changes:

- Declared end of life for all beta versions.
- Included all the symbols listed in the previous section in the public API.

### [1.0.1] - 2026-06-30
<!--cspell:disable-next-line-->
Implemented `util.evaluate_and_return`, `iters.awrapf`, and `exceptions.ignore_warnings`; added `reject_cb` and `await_cb` parameters to
`iters.aguessmax` and `iters.aguessmin`; added `yield_sentinel` keyword argument to `util.aiter_from_f`.

### [1.0.0] - 2026-06-26; first stable version

Added some tests; enabled some pydocstyle lint rules; refactored internal modules to avoid importing asyncio to show the help message and library
version; moved warnings badge generation to slower test run; switched back to codecov due to pricing; integrated spelling checker.

## [0.9]

Breaking changes:

- Declared end of life for all alpha versions.
- Changed version shelving and unshelving schema.

### [0.9.16] - 2026-06-22

Greatly improved futures and properties functionality.

### [0.9.15] - 2026-06-17

Committed uv.lock to version control; replaced `AsyncGenerator` with `AsyncGeneratorType` and `Generator` with `GeneratorType` where appropriate.

### [0.9.14] - 2026-06-13

Refactored `base.EventLoop`; improved submodule logging and `__dir__` method handling.

### [0.9.13] - 2026-06-12

Reorganized the project structure; added a test; clarified documentation.

### [0.9.12] - 2026-06-10

Fixed all warnings in Sphinx nitpicky builds; declared free-threaded support as standard; unpinned the exact beta of Python 3.15.

### [0.9.11] - 2026-06-04

Upgraded to Python 3.15.0b2; added experimental GraalPy and free-threaded support.

### [0.9.10] - 2026-05-29

Integrated CodeQL fully.

### [0.9.9] - 2026-05-26

Added more tests and more badges to the readme; removed codecov upload step superseded by GitHub Code Quality.

### [0.9.8] - 2026-05-23

Eliminated instances of bare `Any` used to annotate arguments.

### [0.9.7] - 2026-05-21

Added `locksmiths` submodule.

### [0.9.6] - 2026-05-19

Re-committed .markdownlint.json to version control; documentation nears completion; used GitHub Actions for page deployment.

### [0.9.5] - 2026-05-17

Some bugfixes; began deployment to [GitHub Pages](https://jonathandung.github.io/asyncutils).

### [0.9.4] - 2026-05-15

Fixed workflows once more and integrated uv more fully; migrated from mypy to ty, removing stubtest step.

### [0.9.3] - 2026-05-11

Added some tests; changed symbolic links to a copy step in the Read the Docs build, which is more reliable; fixed codecov trigger; added
sphinx-copybutton as an optional dependency.

### [0.9.2] - 2026-05-07

Created symbolic links in docs directory linking to root .md files; fixed some bugs; respected some more environment variables and documented this
behaviour; completed benchmarks; added myst_parser as an optional dependency; bumped some dependencies; added some examples.

### [0.9.1] - 2026-05-01

Declared full support for python[ -m] asyncutils an entry point; patched function, method and class method signatures where appropriate; added
`-P` / `--pdb` option; switched to `furo` theme.

### [0.9.0] - 2026-04-27

Added some iteration, functional programming and context management utilities.

## [0.8]

### [0.8.28] - 2026-04-24

Rewrote submodules loading mechanism; removed fragile relative imports; compressed asyncio and sibling module imports to avoid overhead.

### [0.8.27] - 2026-04-21

Added more tests and fixed stubtest errors; abolished slow markdownlint step in pre-commit; various API additions.

### [0.8.26] - 2026-04-18

Squashed many bugs and stub inaccuracies; integrated stubtest; simplified workflows; added more contextual constants.

### [0.8.25] - 2026-04-14

Created issue templates.

### [0.8.24] - 2026-04-10

Created AI_USAGE_POLICY.md.

### [0.8.23] - 2026-04-09

Integrated pre-commit CI.

### [0.8.22] - 2026-04-05

Created the audit events table.

### [0.8.21] - 2026-04-01

Organized badges into table; started using mypy.

### [0.8.20] - 2026-03-29

Started hosting documentation on Read the Docs.

### [0.8.19] - 2026-03-27

Set up docs directory.

### [0.8.17] - 2026-03-24

Started using detect-secrets.

### [0.8.16] - 2026-03-22

Started using ruff; created py.typed.

### [0.8.14] - 2026-03-21

Set up tests directory; started using pytest.

### [0.8.9] - 2026-03-14

Created Dockerfile.

### [0.8.8] - 2026-03-12

Created .editorconfig and .pre-commit-config.yaml.

### [0.8.6] - 2026-03-10

Created ROADMAP.md.

### [0.8.4] - 2026-03-09

Created SUPPORT.md and CHANGELOG.md.

### [0.8.2] - 2026-03-07

Created CODE_OF_CONDUCT.md and CONTRIBUTING.md.

### [0.8.1] - 2026-03-06

Created pyproject.toml and SECURITY.md.

### [0.8.0] - 2026-03-06

Set up version control; added version submodule.

## [0.7] - 2026-02-09

Began migration of implementation details into `_internal` subpackage; fixed initialization logic and command line.

## [0.6] - 2026-01

Completed migration from inline annotations to separated stubs; perfected `base.EventLoop` and lazy loading; added `console` and `cli` submodules.

## [0.5] - 2025-12

Added classes such as `altlocks.CircuitBreaker` and `channels.EventBus`; implemented preliminary lazy loading system; created `exceptions` submodule;
began separation of type annotations from .py into .pyi.

## [0.4] - 2025-10

Added more complicated patterns and procedures such as `channels.Observable` and `signals.wait_for_signal`.

## [0.3] - 2025-08

Basically completed refactoring; added more object-oriented patterns such as `altlocks.DynamicThrottle` and `misc.CacheWithBackgroundRefresh`.

## [0.2] - 2025-07

Began reorganizing single file containing all functions into submodules.

## [0.1] - 2025-06

Added basic but untested features such as `iters.tee`, `iters.merge`, `base.to_async`, `base.iter_to_agen` and `util.sync_await`.
