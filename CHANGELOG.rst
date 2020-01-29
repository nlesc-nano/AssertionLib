##########
Change Log
##########

All notable changes to this project will be documented in this file.
This project adheres to `Semantic Versioning <http://semver.org/>`_.


2.0.0
*****
* Added new ``AssertionManager()`` methods based on the builtin ``math`` module.
* Swapped the ``allclose()`` function with ``math.isclose()``.
  Note that one of its keyword arguments has now changed names from ``rtol`` to ``rel_tol``.
* Added tests for iOS and Windows.


1.1.1
*****
* Fixed an issue where ``AssertionManager.function_eq()`` would raise an ``AttributeError`` if
  the two functions ``__code__`` attributes were not equal in length.


1.1.0
*****
* Added the new ``AssertionManager.function_eq()`` method for testing the equivalency of functions.


1.0.0
*****
* Changed the license from lgpl-3.0 to apache-2.0.
* Added tests for ``AbstractDataClass``.
* Release of version 1.0.0.


0.1.5
*****
* Added the ``AssertionManager.shape_eq()`` method for comparing array shapes.
* Re-enabled all NumPy-related tests.
* Fixed indentation and attribute ordering in ``AbstractDataClass.__repr__()``: https://github.com/nlesc-nano/AssertionLib/commit/4d6c16d0d2bc85c92c52507605f026ee1ef1d06f.
* ``NDRepr._get_ndformatter()` no longer raises a ``TypeError`` when handling zero-sized arrays: https://github.com/nlesc-nano/AssertionLib/commit/e1601b5b41b53884436c51fd2ee98ff615447dac.


0.1.4
*****
* Reduced the ``AssertionManager()`` traceback verbosity.
* Added the ``AssertionManager.__call__()`` method which simply asserts the supplied value.
* A couple of docstring, codestyle and consistency improvements.
* Added tests for Python 3.8.


0.1.3
*****
* Added precautions against recursive calls of ``AbstractDataClass.__repr__()``, ``__eq__()`` and ``__hash__()``.
* Fixed a bug where ``AbstractDataClass.__repr__()`` would crash when passing empty instances.
* Deleted ``AbstractDataClass.__str__()``; rely on ``AbstractDataClass.__repr__()`` for printing.
* Setting ``AbstractDataClass._HASHABLE`` to ``False`` now truly removes the ``__hash__`` method.
* The frozenset stored in ``AbstractDataClass._PRIVATE_ATTR`` is now always added to class instances
  as a normal (unfrozen) set.


0.1.2
*****
* ``bind_callable()`` can now handle all types of keyword arguments.
* ``bind_callable()`` can now handle methods.


0.1.1
*****
* Added tests.


0.1.0
*****
* Release.


[Unreleased]
************
* Empty Python project directory structure.
