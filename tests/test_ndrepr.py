"""Tests for the :mod:`NDRepr<assertionlib.ndrepr.NDRepr>` class."""

import inspect

import numpy as np

from assertionlib import assertion
from assertionlib.ndrepr import aNDRepr, NDRepr


def test_float() -> None:
    """Tests for :meth:`NDRepr.repr_float`."""
    assertion.eq('5.0000', aNDRepr.repr(5.0))
    assertion.eq('5.0000', aNDRepr.repr(5.00000000000))
    assertion.eq('5.0000', aNDRepr.repr(5.0000))
    assertion.eq('5.0000e+10', aNDRepr.repr(5.0*10**10))
    assertion.eq('5.0000e-10', aNDRepr.repr(5.0*10**-10))


def test_exception() -> None:
    """Tests for :meth:`NDRepr.repr_exception`."""
    repr_instance = NDRepr()
    repr_instance.maxException = 80

    exc1 = repr_instance.repr(TypeError('bob'))
    exc2 = repr_instance.repr(TypeError('bob' * 100))
    ref1 = 'TypeError(bob)'
    ref2 = 'TypeError(bobbobbobbobbobbobbobbobbobbobbobbobbobbobbobbobbobbobbobbobbobbobbobbobbobbobbo...)'  # noqa
    assertion.eq(exc1, ref1)
    assertion.eq(exc2, ref2)


def _test_func(a, b, *args, c=1): pass


def test_callables() -> None:
    """Tests for :meth:`NDRepr.repr_method`."""
    builtin_bound_meth = aNDRepr.repr(list().count)
    builtin_meth = aNDRepr.repr(list.count)
    builtin_func = aNDRepr.repr(hasattr)
    class_ = aNDRepr.repr(list)
    func = aNDRepr.repr(_test_func)
    mod = aNDRepr.repr(inspect)

    ref1 = "<built-in bound method 'list.count(value, /)'>"
    ref2 = "<method 'list.count(self, value, /)'>"
    ref3 = "<built-in function 'hasattr(obj, name, /)'>"
    ref4 = "<class 'list(iterable=(), /)'>"
    ref5 = "<function '_test_func(a, b, *args, c=1)'>"
    ref6 = "<module 'inspect'>"

    assertion.eq(builtin_bound_meth, ref1)
    assertion.eq(builtin_meth, ref2)
    assertion.eq(builtin_func, ref3)
    assertion.eq(class_, ref4)
    assertion.eq(func, ref5)
    assertion.eq(mod, ref6)


def test_Signature() -> None:
    """Tests for :meth:`NDRepr.repr_Signature`."""
    sgn1 = inspect.signature(len)
    sgn2 = inspect.signature(np.testing.assert_allclose)

    ref1 = '(obj, /)'
    ref2 = "(actual, desired, rtol=1e-07, atol=0, equal_nan=True, err_msg='', ...)"
    str1 = aNDRepr.repr(sgn1)
    str2 = aNDRepr.repr(sgn2)

    assertion.eq(str1, ref1)
    assertion.eq(str2, ref2)


def test_ndarray() -> None:
    """Tests for :meth:`NDRepr.repr_ndarray`."""
    ar1 = np.ones((10, 10), dtype=float)
    ar2 = np.ones((10, 10), dtype=int)

    ref1 = 'array([[1.0000, 1.0000, 1.0000, ..., 1.0000, 1.0000, 1.0000],\n       [1.0000, 1.0000, 1.0000, ..., 1.0000, 1.0000, 1.0000],\n       [1.0000, 1.0000, 1.0000, ..., 1.0000, 1.0000, 1.0000],\n       ...,\n       [1.0000, 1.0000, 1.0000, ..., 1.0000, 1.0000, 1.0000],\n       [1.0000, 1.0000, 1.0000, ..., 1.0000, 1.0000, 1.0000],\n       [1.0000, 1.0000, 1.0000, ..., 1.0000, 1.0000, 1.0000]])'  # noqa
    ref2 = 'array([[1, 1, 1, ..., 1, 1, 1],\n       [1, 1, 1, ..., 1, 1, 1],\n       [1, 1, 1, ..., 1, 1, 1],\n       ...,\n       [1, 1, 1, ..., 1, 1, 1],\n       [1, 1, 1, ..., 1, 1, 1],\n       [1, 1, 1, ..., 1, 1, 1]])'  # noqa
    str1 = aNDRepr.repr(ar1)
    str2 = aNDRepr.repr(ar2)

    assertion.eq(str1, ref1)
    assertion.eq(str2, ref2)
