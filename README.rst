.. image:: https://readthedocs.org/projects/assertionlib/badge/?version=latest
    :target: https://assertionlib.readthedocs.io/en/latest/
.. image:: https://badge.fury.io/py/AssertionLib.svg
    :target: https://badge.fury.io/py/AssertionLib
.. image:: https://github.com/nlesc-nano/AssertionLib/workflows/Python%20package/badge.svg
    :target: https://github.com/nlesc-nano/AssertionLib/actions
.. image:: https://codecov.io/gh/nlesc-nano/AssertionLib/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/nlesc-nano/AssertionLib
.. image:: https://zenodo.org/badge/214183943.svg
    :target: https://zenodo.org/badge/latestdoi/214183943

|

.. image:: https://img.shields.io/badge/python-3.6-blue.svg
    :target: https://docs.python.org/3.6/
.. image:: https://img.shields.io/badge/python-3.7-blue.svg
    :target: https://docs.python.org/3.7/
.. image:: https://img.shields.io/badge/python-3.8-blue.svg
    :target: https://docs.python.org/3.8/
.. image:: https://img.shields.io/badge/python-3.9-blue.svg
    :target: https://docs.python.org/3.9/


##################
AssertionLib 3.2.1
##################
A package for performing assertions and providing informative exception messages.


Installation
************
* PyPi: ``pip install AssertionLib``
* GitHub: ``pip install git+https://github.com/nlesc-nano/AssertionLib``


Usage
*****
A comprehensive overview of all available assertion methods is
provided in the documentation_.
A few examples of some basic assertion:

.. code:: python

    >>> import numpy as np
    >>> from assertionlib import assertion

    # Assert the output of specific callables
    >>> assertion.eq(5, 5)  # 5 == 5
    >>> assertion.lt(5, 6)  # 5 < 6
    >>> assertion.gt(6, 5)  # 5 > 6
    >>> assertion.isinstance(5, int)
    >>> assertion.hasattr(5, '__init__')
    >>> assertion.any([False, False, True])
    >>> assertion.isfinite(1.0)

    # Simply assert a value
    >>> assertion(5 == 5)
    >>> assertion(isinstance(5, int))

    # Apply post-processing before conducting the assertion
    >>> ar_large = np.ones(10)
    >>> ar_small = np.zeros(10)
    >>> assertion.gt(ar_large, ar_small, post_process=np.all)  # all(ar_large > ar_small)

    # Perform an assertion which will raise an AssertionError
    >>> assertion.eq(5, 6, message='Fancy custom error message')  # 5 == 6
    Traceback (most recent call last):
      ...
    AssertionError: output = eq(a, b); assert output

    exception: AssertionError = AssertionError('Fancy custom error message')

    output: bool = False
    a: int = 5
    b: int = 6

A few examples of AssertionErrors raised due to incorrect method signatures:

.. code:: python

    >>> from assertionlib import assertion

    >>> assertion.len(5)
    Traceback (most recent call last):
      ...
    AssertionError: output = len(obj); assert output

    exception: TypeError = TypeError("object of type 'int' has no len()")

    output: NoneType = None
    obj: int = 5


.. code:: python

    >>> from assertionlib import assertion

    >>> assertion.eq(5, 5, 5, 5)
    Traceback (most recent call last):
      ...
    AssertionError: output = eq(a, b, _a, _b); assert output

    exception: TypeError = TypeError('eq expected 2 arguments, got 4')

    output: NoneType = None
    a: int = 5
    b: int = 5
    _a: int = 5
    _b: int = 5

A demonstration of the ``exception`` parameter.
Providing an exception type will assert that the provided exception is raised
during/before the assertion process:

.. code:: python

    >>> from assertionlib import assertion

    >>> len(5)
    Traceback (most recent call last):
      ...
    TypeError: object of type 'int' has no len()


.. code:: python

    >>> from assertionlib import assertion

    >>> assertion.len(5, exception=TypeError)  # i.e. len(5) should raise a TypeError
    >>> assertion.len([5], exception=TypeError)
    Traceback (most recent call last):
      ...
    AssertionError: output = len(obj); assert output

    exception: AssertionError = AssertionError("Failed to raise 'TypeError'")

    output: int = 1
    obj: list = [5]

Lastly, the output of custom callables can be asserted in one of the following two ways,
supplying the callable to ``AssertionManager.assert()`` or creating a custom assertion
method and adding it to an instance with ``AssertionManager.add_to_instance()``:

.. code:: python

    >>> from assertionlib import assertion

    >>> def my_fancy_func(a: object) -> bool:
    ...     return False

    # Approach #1, supply to-be asserted callable to assertion.assert_()
    >>> assertion.assert_(my_fancy_func, 5)
    Traceback (most recent call last):
      ...
    AssertionError: output = my_fancy_func(a); assert output

    exception: AssertionError = AssertionError(None)

    output: bool = False
    a: int = 5


.. code:: python

    >>> from assertionlib import assertion

    # Approach #2, permanantly add a new bound method using assertion.add_to_instance()
    >>> assertion.add_to_instance(my_fancy_func)
    >>> assertion.my_fancy_func(5)
    Traceback (most recent call last):
      ...
    AssertionError: output = my_fancy_func(a); assert output

    exception: AssertionError = AssertionError(None)

    output: bool = False
    a: int = 5

.. _documentation: https://assertionlib.readthedocs.io/en/latest/3_assertionmanager.html
