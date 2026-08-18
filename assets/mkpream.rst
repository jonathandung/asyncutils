Using the Makefile
==================

.. highlight:: text

``make.bat`` on Windows, or ``Makefile`` on \*nix, is often a handy companion in development. It makes development less dry, repetitive and
error-prone, and the process as a whole more smooth-sailing. It can also pull in non-Python dependencies when needed and leaves behind automatically
ignored marker files removable by a simple cleanup command. Tasks are effectively automated using the ``make <target>`` syntax.

The Makefile is intended to be used by developers, not end users, and it obviously requires
`GNU Make <https://ftp.gnu.org/old-gnu/Manuals/make-3.80/html_node/make.html>`__.

If you are in PowerShell, ``make`` will not work directly and you must input ``.\make`` instead. You are strongly advised to develop in ``cmd.exe``.

Target-specific dependencies
----------------------------

Besides some Python dependencies that will be on ``PATH`` once ``make install`` has been run and the environment is activated, the following
executables will be automatically installed on your system if not present. This implicit installation process requires internet access, as well as
`cURL <https://curl.se>`__ or `GNU wget <https://man7.org/linux/man-pages/man1/wget.1.html>`__ on \*nix (dependency-free on Windows):

Requires `uv`_:

* audit
* install (Also pulls in `ruff`_ and `ty`_ if not present)
* lint (Requires `ruff`_ and `ty`_)
* lock
* venv

Requires `prek`_:

* install
* pc

Requires cURL 7.66.0+ on Unix (for parallel downloads):

* docs

All targets
-----------
