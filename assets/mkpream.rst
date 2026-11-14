Using the `Makefile <https://github.com/jonathandung/asyncutils/blob/main/Makefile>`__
======================================================================================

.. highlight:: text

``make.bat`` on Windows, or ``Makefile`` on \*nix, is often a handy companion in
development. It makes development less dry, repetitive and error-prone, and the process
as a whole more smooth-sailing. It can also pull in non-Python dependencies when needed
and leaves behind automatically ignored marker files removable by a simple cleanup
command. Tasks are effectively automated using the ``make <target>`` syntax.

The Makefile is intended to be used by developers, not end users, and it obviously
requires
`GNU Make <https://ftp.gnu.org/old-gnu/Manuals/make-3.80/html_node/make.html>`__.

You are strongly advised to develop in ``cmd.exe`` on Windows. There shouldn't be a
need to run ``scripts\generate.ps1`` manually.

Certain executables, some of which are entry points to Python dependencies, will be on
``PATH`` once ``make setup`` has been run and the environment activated. In this step,
`prek`_, `uv`_, `ruff`_, and `ty`_ will be automatically installed on your system if
not present. For this to work, internet access is required, as well as `cURL`_ or
`GNU wget <https://man7.org/linux/man-pages/man1/wget.1.html>`__ on \*nix.

Target-specific dependencies
----------------------------

Requires `docker <https://docs.docker.com/engine>`__:

* build
* run

Requires `uv`_:

* lint
* lock

Requires `ruff`_:

* lint

Requires `ty`_:

* lint

Requires `prek`_:

* pc

Requires `gh`_:

* rel

Requires `cURL`_ 7.66.0+ on \*nix (for parallel downloads):

* docs
* links

Optional target-specific dependencies
-------------------------------------

Some targets invoke executables only if they are found on the system.

* audit: `zizmor <https://zizmor.sh>`__ and  `betterleaks <https://betterleaks.com>`__
* lint: `CSpell <https://cspell.org>`__,
  `markdownlint-cli2 <https://github.com/DavidAnson/markdownlint-cli2>`__, and
  `sphinx-lint <https://github.com/sphinx-contrib/sphinx-lint>`__ if found

All targets
-----------
