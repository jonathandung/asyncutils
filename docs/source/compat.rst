Compatibility
=============

Python versions
---------------

We support all actively maintained versions of Python; that is, users need never worry about support for the newest Python and the one before it.
This will be fortified in version 4.4, by which time Python 3.17 will have been released, and we will begin supporting all non-EOL Python versions
(5 minor versions in total). Also, this codebase is quite future-proof, integrating modern features non-intrusively and using the newest compatible
syntax.

Our compatibility layer currently backports the :meth:`~asyncio.Queue.shutdown` method of :class:`asyncio.Queue` and the
:data:`~functools.Placeholder` support in :func:`functools.partial`. The latter performs slower than its C-accelerated counterpart.

See :pep:`602` for a detailed explanation of the Python release cycle, and the `status of Python versions <https://devguide.python.org/versions>`__.

Support matrix
--------------

===================== ===============
asyncutils version    CPython version
===================== ===============
6.0 - 6.11            3.14+
5.0 - 5.7             3.13+
1.0 - 4.7             3.12+
0.8.18 - 0.9.16 (EOL) 3.12+
0.8.0 - 0.8.17 (EOL)  3.14+
===================== ===============
