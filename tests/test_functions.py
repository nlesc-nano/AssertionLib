"""Tests for the :mod:`assertionlib.functions>` class."""

import warnings
from collections import OrderedDict

from assertionlib import assertion
from assertionlib.functions import set_docstring, get_sphinx_domain, skip_if


def test_set_docstring() -> None:
    """Tests for :func:`~assertionlib.functions.set_docstring`."""

    @set_docstring('TEST')
    def func1():
        pass

    @set_docstring(None)
    def func2():
        pass

    assertion.eq(func1.__doc__, 'TEST')
    assertion.eq(func2.__doc__, None)


def test_get_sphinx_domain() -> None:
    """Tests for :func:`~assertionlib.functions.get_sphinx_domain`."""
    v1 = get_sphinx_domain(int)
    v2 = get_sphinx_domain(list.count)
    v3 = get_sphinx_domain(OrderedDict)
    v4 = get_sphinx_domain(OrderedDict.keys)
    v5 = get_sphinx_domain(isinstance)

    assertion.eq(v1, ':class:`int<python:int>`')
    assertion.eq(v2, ':meth:`list.count()<python:list.count>`')
    assertion.eq(v3, ':class:`~collections.OrderedDict`')
    assertion.eq(v4, ':meth:`~collections.OrderedDict.keys`')
    assertion.eq(v5, ':func:`isinstance()<python:isinstance>`')

    assertion.assert_(get_sphinx_domain, 1, exception=TypeError)


def test_skip_if() -> None:
    """Tests for :func:`~assertionlib.functions.skip_if`."""
    condition1 = False
    condition2 = True
    condition3 = TypeError('False')

    @skip_if(condition1)
    def func1():
        return True

    @skip_if(condition2)
    def func2():
        return True

    @skip_if(condition3)
    def func3():
        return True

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)

        assertion.is_(func1(), True)
        assertion.is_(func2(), None)
        assertion.is_(func3(), None)

    with warnings.catch_warnings():
        warnings.simplefilter("error", category=UserWarning)

        try:
            func3()
        except UserWarning as ex1:
            assertion.isinstance(ex1.__cause__, TypeError)
        except Exception as ex2:
            raise AssertionError("Failed to raise a TypeError") from ex2
        else:
            raise AssertionError("Failed to raise a TypeError")
