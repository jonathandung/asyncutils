Compatibility
=============

.. version-added:: 0.9.1

Python versions
---------------

We strive to have released versions support all Python versions actively maintained at the time of release, but due to logistical constraints and
major syntactical reworks in 3.12, it would be very difficult to support Python 3.11 or below. This codebase is, however, future-proof, integrating
modern features such as lazy imports non-intrusively and using the newest compatible syntax. Like most libraries with multiple submodules, we have a
compatibility layer, which currently backports the :meth:`shutdown` method of :class:`asyncio.Queue` and the :const:`~functools.Placeholder` support
in :class:`functools.partial`, albeit slower than the C version. We also can't port this package to PyPy because it is stuck on 3.11 and some
internals crucial to how some utilities are written differ. However, the weaker promise to support all actively maintained versions of Python will
be upheld; that is, users need not worry about support for the newest version and the one before it, along with the version the main branch
corresponds to, which is the one in the development (alpha, beta, rc) phase. See :pep:`602` for a detailed explanation, and the `status of Python
versions <https://devguide.python.org/versions>`_ here.

asyncutils versions
-------------------

Due to this library being in an early stage of development, it is not suitable to make a 1.0 release, which is really when the backward compatibility
concerns start flooding in. Currently, no guarantees regarding breaking changes or API stability are made, even in the same patch version, but
hopefully that soon changes.

Support matrix
--------------

================== ===============
asyncutils version CPython version
================== ===============
0.8.18+            3.12+
0.8.0 - 0.8.17     3.14+
================== ===============
