"""Tests for the :class:`~assertionlib.ndrepr.NDRepr` class."""

import inspect
from sys import version_info
from typing import Optional

import pytest
from assertionlib import assertion
from assertionlib.ndrepr import aNDRepr, NDRepr

try:
    import numpy as np
    NUMPY_EX: Optional[Exception] = None
except Exception as ex:
    NUMPY_EX = ex

try:
    import pandas as pd
    PANDAS_EX: Optional[Exception] = None
except Exception as ex:
    PANDAS_EX = ex


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
    ref2 = 'TypeError(bobbobbobbobbobbobbobbobbobbobbobbobbobbobbobbobbobbobbobbobbobbobbobbobbobbobbo...)'  # noqa: E501
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
    ref1_backup = "<built-in bound method 'list.count(...)'>"
    ref2 = "<method descriptor 'list.count(self, value, /)'>"
    ref2_backup = "<method descriptor 'list.count(...)'>"
    ref3 = "<built-in function 'hasattr(obj, name, /)'>"
    ref4 = "<class 'list(iterable=(), /)'>"
    ref4_backup = "<class 'list(...)'>"
    ref5 = "<function '_test_func(a, b, *args, c=1)'>"
    ref6 = "<module 'inspect'>"

    if version_info >= (3, 7):  # Python 3.7 and later
        assertion.eq(builtin_bound_meth, ref1)
        assertion.eq(builtin_meth, ref2)
        assertion.eq(class_, ref4)
    else:  # Python versions predating 3.7
        assertion.eq(builtin_bound_meth, ref1_backup)
        assertion.eq(builtin_meth, ref2_backup)
        assertion.eq(class_, ref4_backup)

    assertion.eq(builtin_func, ref3)
    assertion.eq(func, ref5)
    assertion.eq(mod, ref6)


@pytest.mark.skipif(bool(NUMPY_EX), reason=str(NUMPY_EX))
def test_signature() -> None:
    """Tests for :meth:`NDRepr.repr_Signature`."""
    sgn1 = inspect.signature(len)
    sgn2 = inspect.signature(np.testing.assert_allclose)

    ref1 = '(obj, /)'
    ref2 = "(actual, desired, rtol=1e-07, atol=0, equal_nan=True, ...)"
    str1 = aNDRepr.repr(sgn1)
    str2 = aNDRepr.repr(sgn2)

    assertion.eq(str1, ref1)
    assertion.eq(str2, ref2)


@pytest.mark.skipif(bool(NUMPY_EX), reason=str(NUMPY_EX))
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


@pytest.mark.skipif(bool(PANDAS_EX), reason=str(PANDAS_EX))
def test_dataframe() -> None:
    """Tests for :meth:`NDRepr.repr_DataFrame`."""
    df1 = pd.DataFrame(np.ones((10, 10), dtype=float))
    df2 = pd.DataFrame(np.ones((10, 10), dtype=int))

    ref1 = '     0    1    2  ...    7    8    9\n0  1.0  1.0  1.0  ...  1.0  1.0  1.0\n1  1.0  1.0  1.0  ...  1.0  1.0  1.0\n2  1.0  1.0  1.0  ...  1.0  1.0  1.0\n3  1.0  1.0  1.0  ...  1.0  1.0  1.0\n4  1.0  1.0  1.0  ...  1.0  1.0  1.0\n5  1.0  1.0  1.0  ...  1.0  1.0  1.0\n6  1.0  1.0  1.0  ...  1.0  1.0  1.0\n7  1.0  1.0  1.0  ...  1.0  1.0  1.0\n8  1.0  1.0  1.0  ...  1.0  1.0  1.0\n9  1.0  1.0  1.0  ...  1.0  1.0  1.0\n\n[10 rows x 10 columns]'  # noqa: E501
    ref2 = '   0  1  2  ...  7  8  9\n0  1  1  1  ...  1  1  1\n1  1  1  1  ...  1  1  1\n2  1  1  1  ...  1  1  1\n3  1  1  1  ...  1  1  1\n4  1  1  1  ...  1  1  1\n5  1  1  1  ...  1  1  1\n6  1  1  1  ...  1  1  1\n7  1  1  1  ...  1  1  1\n8  1  1  1  ...  1  1  1\n9  1  1  1  ...  1  1  1\n\n[10 rows x 10 columns]'  # noqa: E501
    str1 = aNDRepr.repr(df1)
    str2 = aNDRepr.repr(df2)

    assertion.eq(str1, ref1)
    assertion.eq(str2, ref2)


@pytest.mark.skipif(bool(PANDAS_EX), reason=str(PANDAS_EX))
def test_series() -> None:
    """Tests for :meth:`NDRepr.repr_Series`."""
    s1 = pd.Series(np.ones(10, dtype='float64'))
    s2 = pd.Series(np.ones(10, dtype='int64'))

    ref1 = '0    1.0\n1    1.0\n2    1.0\n3    1.0\n4    1.0\n5    1.0\n6    1.0\n7    1.0\n8    1.0\n9    1.0\ndtype: float64'  # noqa: E501
    ref2 = '0    1\n1    1\n2    1\n3    1\n4    1\n5    1\n6    1\n7    1\n8    1\n9    1\ndtype: int64'  # noqa: E501
    str1 = aNDRepr.repr(s1)
    str2 = aNDRepr.repr(s2)

    assertion.eq(str1, ref1)
    assertion.eq(str2, ref2)
