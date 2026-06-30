Compatibility
=============

Python versions
---------------

We strive to have released versions support all Python versions actively maintained at the time of release, but due to logistical constraints and
major syntactical reworks in 3.12, we will not support Python 3.11 or below. However, the weaker promise to support all actively maintained versions
of Python will be upheld; that is, users need never worry about support for the newest version and the one before it. Also, this codebase is quite
future-proof, integrating modern features such as lazy imports non-intrusively and using the newest compatible syntax.

Our compatibility layer, currently backports the :meth:`~asyncio.Queue.shutdown` method of :class:`asyncio.Queue` and the
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
