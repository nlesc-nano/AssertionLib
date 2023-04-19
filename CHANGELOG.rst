##########
Change Log
##########

All notable changes to this project will be documented in this file.
This project adheres to `Semantic Versioning <http://semver.org/>`_.


3.2.2
*****
* Add formal Python 3.11 support
* Misc CI updates
* Fix a missing README file in the assertionlib sdist distribution


3.2.1
*****
* Increase the ``NDRepr.maxstring`` default to 800.
* Fixed the signature of ``assertion.str_eq``.


3.2.0
*****
* Added three new ``NDRepr`` methods.
* Added a missing ``AssertionManager.assert_`` overload.


3.1.3
*****
* Updated the typehints.
* Updated the Cancel Workflow Action version.
* Updated the string representation of exceptions.


3.1.2
*****
* Enabled tests for Python 3.9.
* Enable `Cancel Workflow Action <https://github.com/marketplace/actions/cancel-workflow-action>`_ for the unit tests.
* Added tests for building documentation.


3.1.1
*****
* Minor changes.


3.1.0
*****
* Added `assertion.issuperset()` and `assertion.issubset()`.
* Export the source to PyPi.
* Updated MyPy settings.


3.0.0
*****
* Added `Nano-Utils <https://github.com/nlesc-nano/Nano-Utils>`_ as a dependency;
  moved a number of functions there.
* Removed `requirements.txt` in favor of `.readthedocs.yml`.
* Removed travis tests in favor of GitHub Actions.
* Removed `CITATION.cff` in favor of Zenodo.


2.3.2
*****
* Added codecov and zenodo badges.


2.3.1
*****
* Added support for the ``python stup.py test`` command.
* Added support for the ``python stup.py build_sphinx`` command.
* Added a `GitHub Actions <https://github.com/features/actions>`_ workflow for automatic PyPi publishing.
* Enabled `codecov <https://codecov.io/>`_ for the GitHub Action tests.
* Updated the package classifiers and keywords in ``setup.py``.


2.3.0
*****
* Added the ``AssertionManager.xor()``, ``AssertionManager.isdisjoint()`` and ``AssertionManager.length_hint()`` methods.
* Annotate most ``AssertionManager`` methods using Protocols.
* Moved Protocols to their own separate stub module.
* Cleaned up the ``_MetaAM`` metaclass.
* Reworked some of the internals of ``AssertionManager``.
* Added tests using `pydocstyle <https://github.com/henry0312/pytest-pydocstyle>`_.


2.2.3
*****
* Windows bug fix: Check for the presence of the ``AssertionManager._isdir()``
  rather than the type of operating system.


2.2.2
*****
* Replaced `pycodestyle <https://pypi.org/project/pycodestyle/>`_ tests with
  `pytest-flake8 <https://pypi.org/project/pytest-flake8/>`_.
* Added tests using `doctest <https://docs.python.org/3/library/doctest.html>`_.


2.2.1
*****
* Added a mypy test.
* Further refined type annotations.


2.2.0
*****
* Marked AssertionLib as a typed package (`PEP 561 <https://www.python.org/dev/peps/pep-0561/>`_).
* Introduced updates and fixes to the type-annotations across the board.
* Exposed ``NDRepr``, ``aNDRepr`` and ``AbstractDataClass`` in the main ``__init__.py`` file.
* Added the ``__slots__`` attribute to ``AbstractDataClass``.
* Added the ``AssertionManager.any()`` and ``AssertionManager.all()`` methods.
* Added the ``post_process`` and ``message`` keywords to all
  ``AssertionManager`` assertion methods.


2.1.0
*****
* Made the recursion safeguard in ``AbstractDataClass`` thread-safe.
* Added the ``AbstractDataClass._str()`` function for creating string-representations of key/value pairs.
* Added the ``AbstractDataClass._eq()`` function for comparing two attribute values.
* Minor Improvements to ``Exception`` handling.


2.0.0
*****
* Added new ``AssertionManager()`` methods based on the builtin ``math`` module.
* Swapped the ``allclose()`` function with ``math.isclose()``.
  Note that one of its keyword arguments has now changed names from ``rtol`` to ``rel_tol``.
* Added tests for OSX.


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
