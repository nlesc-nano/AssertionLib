##########
Change Log
##########

All notable changes to this project will be documented in this file.
This project adheres to `Semantic Versioning <http://semver.org/>`_.

0.1.4
*****
* Reduced the `AssertionManager()` traceback verbosity.
* Added the `AssertionManager.__call__()` method which simply asserts the supplied value.
* A couple of docstring, codestyle and consistency improvements.
* Added tests for Python 3.8.


0.1.3
*****
* Added precautions against recursive calls of `AbstractDataClass.__repr__()`, `__eq__()` and `__hash__()`.
* Fixed a bug where `AbstractDataClass.__repr__()` would crash when passing empty instances.
* Deleted `AbstractDataClass.__str__()`; rely on `AbstractDataClass.__repr__()` for printing.
* Setting `AbstractDataClass._HASHABLE` to `False` now truly removes the `__hash__` method.
* The frozenset stored in `AbstractDataClass._PRIVATE_ATTR` is now always added to class instances
  as a normal (unfrozen) set.


0.1.2
*****
* `bind_callable()` can now handle all types of keyword arguments.
* `bind_callable()` can now handle methods.


0.1.1
*****
* Added tests.


0.1.0
*****
* Release.


[Unreleased]
************
* Empty Python project directory structure.
