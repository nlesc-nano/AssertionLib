"""Tests for the :class:`AssertionManager<assertionlib.manager.AssertionManager>` class."""

import operator
from sys import version_info
from typing import Optional, cast

from assertionlib import assertion, AssertionManager
from assertionlib.functions import skip_if

try:
    import numpy as np  # type: ignore
    NUMPY_EX: Optional[ImportError] = None
except ImportError as ex:
    NUMPY_EX = ex


def test_callable() -> None:
    """Test :meth:`AssertionManager.callable`."""
    assertion.callable(int)
    assertion.callable(len)
    assertion.callable(callable)
    assertion.callable(5, invert=True)
    assertion.callable(5, 6, 7, 8, exception=TypeError)


def test_hasattr() -> None:
    """Test :meth:`AssertionManager.hasattr`."""
    assertion.hasattr(int, '__str__')
    assertion.hasattr(len, '__name__')
    assertion.hasattr(5, 'count', invert=True)
    assertion.hasattr(5, 6, 7, 8, exception=TypeError)


def test_isinstance() -> None:
    """Test :meth:`AssertionManager.isinstance`."""
    assertion.isinstance(int, type)
    assertion.isinstance(5, int)
    assertion.isinstance(5, (float, list, int))
    assertion.isinstance(5, str, invert=True)
    assertion.isinstance(5, 6, 7, 8, exception=TypeError)
    assertion.isinstance(5, 5, exception=TypeError)


def test_issubclass() -> None:
    """Test :meth:`AssertionManager.issubclass`."""
    class Test(int):
        pass

    assertion.issubclass(Test, int)
    assertion.issubclass(Test, float, invert=True)
    assertion.issubclass(int, Test, invert=True)
    assertion.issubclass(int, 5, exception=TypeError)
    assertion.issubclass(5, int, exception=TypeError)
    assertion.issubclass(5, 6, 7, 8, exception=TypeError)


def test_len() -> None:
    """Test :meth:`AssertionManager.len`."""
    assertion.len([1])
    assertion.len({1, 2})
    assertion.len([], invert=True)
    assertion.len(5, 6, 7, 8, exception=TypeError)
    assertion.len(5, exception=TypeError)


def test_len_eq() -> None:
    """Test :meth:`AssertionManager.len_eq`."""
    assertion.len_eq([1], 1)
    assertion.len_eq({1, 2, 3, 1}, 3)
    assertion.len_eq({1: None}, 5, invert=True)
    assertion.len_eq(5, 6, 7, 8, exception=TypeError)
    assertion.len_eq(5, 5, exception=TypeError)


def test_copy() -> None:
    """Test :meth:`AssertionManager.copy`."""
    cp = assertion.copy()
    assertion.eq(assertion, cp)
    assertion.is_not(assertion, cp)


def test_as_dict() -> None:
    """Test :meth:`AssertionManager.as_dict` and :meth:`AssertionManager.from_dict`."""
    cls = type(assertion)
    dct = assertion.as_dict()
    new = cast(AssertionManager, cls.from_dict(dct))
    assertion.eq(vars(assertion.repr_instance), vars(new.repr_instance))


class _TestClass:
    def instance_meth(self) -> bool: return True

    @classmethod
    def class_meth(cls) -> bool: return True

    @staticmethod
    def static_meth() -> bool: return True


def test_add_to_instance() -> None:
    """Test :meth:`AssertionManager.add_to_instance`."""
    def func(a, b): return True

    assertion_ = AssertionManager()
    assertion_.add_to_instance(func)
    assertion_.hasattr(assertion_, 'func')
    assertion_.func(1, 2)  # type: ignore

    try:
        assertion_.add_to_instance(func)
    except AttributeError:
        pass
    else:
        raise AssertionError

    assertion_.add_to_instance(func, name='bob')
    assertion_.hasattr(assertion_, 'bob')
    assertion_.bob(1, 2)  # type: ignore

    try:
        assertion_.add_to_instance(func)
    except AttributeError:
        pass
    else:
        raise AssertionError

    assertion_.add_to_instance(_TestClass.instance_meth)
    assertion_.add_to_instance(_TestClass.class_meth)
    assertion_.add_to_instance(_TestClass.static_meth)
    assertion_.hasattr(assertion_, 'instance_meth')
    assertion_.hasattr(assertion_, 'class_meth')
    assertion_.hasattr(assertion_, 'static_meth')


def test_assert_() -> None:
    """Test :meth:`AssertionManager.assert_`."""
    assertion.assert_(len, [1])
    assertion.assert_(len, [], invert=True)
    assertion.assert_(len, 1, exception=TypeError)
    assertion.assert_(len, [1], [1], exception=TypeError)
    assertion.assert_(len, [1], bob=1, exception=TypeError)

    try:
        assertion.assert_(len, [1], exception=bool)  # type: ignore
    except TypeError:
        pass
    else:
        raise AssertionError('Failed to raise a TypeError')

    try:
        assertion.assert_(len, [1], exception=AssertionError)
    except ValueError:
        pass
    else:
        raise AssertionError('Failed to raise a ValueError')

    func = operator.__invert__
    assertion(False, post_process=func)
    assertion(True, invert=True, post_process=func)

    try:
        assertion.truth(False, message='Funcy custom message')
    except AssertionError as ex:
        assertion.contains(str(ex), 'Funcy custom message')
    else:
        raise AssertionError('Failed to raise am AssertionError')


def test_repr() -> None:
    """Test :meth:`AssertionManager.__repr__`."""
    ref = 'AssertionManager(\n    repr_instance = <assertionlib.ndrepr.NDRepr object '
    output = repr(assertion).split('at')[0]
    assertion.eq(ref, output)


def test_call() -> None:
    """Test :meth:`AssertionManager.__call__`."""
    assertion(5 == 5)
    assertion(len([1]))
    assertion(len([]), invert=True)

    assertion.__call__(5 == 5)
    assertion.__call__(len([1]))
    assertion.__call__(len([]), invert=True)


@skip_if(NUMPY_EX)
def test_shape_eq() -> None:
    """Test :meth:`AssertionManager.shape_eq`."""
    ar1: np.ndarray = np.random.rand(10, 10)
    ar2: np.ndarray = np.random.rand(10, 10)
    shape = ar1.shape

    assertion.shape_eq(ar1, ar2)
    assertion.shape_eq(ar1, shape)
    assertion.shape_eq(ar1, (5,), invert=True)

    assertion.shape_eq(ar1, ar1, ar1, ar1, exception=TypeError)
    assertion.shape_eq(shape, ar1, exception=AttributeError)


def test_function_eq() -> None:
    """Test :meth:`AssertionManager.function_eq`."""
    func1 = lambda x: x + 5  # noqa: E731
    func2 = lambda x: x + 5  # noqa: E731
    func3 = lambda x: 5 + x  # noqa: E731
    func4 = lambda x: x / 5 + 9.0**2  # noqa: E731

    assertion.function_eq(func1, func2)
    assertion.function_eq(func1, func3, invert=True)
    assertion.function_eq(func1, func4, invert=True)
    assertion.function_eq(func1, None, exception=TypeError)


def test_any() -> None:
    """Test :meth:`AssertionManager.any`."""
    assertion.any([True, True, False])
    assertion.any({True, True, False})
    assertion.any({True: None, False: None})

    assertion.any({False: None, False: None}, invert=True)
    assertion.any((False, False), invert=True)

    assertion.any(True, exception=TypeError)
    assertion.any(5, exception=TypeError)


def test_all() -> None:
    """Test :meth:`AssertionManager.all`."""
    assertion.all([True, True, True])
    assertion.all({True, True, True})
    assertion.all({True: None, True: None})

    assertion.all({True: None, False: None}, invert=True)
    assertion.all((False, False), invert=True)

    assertion.all(True, exception=TypeError)
    assertion.all(5, exception=TypeError)


def test_get_exc_message() -> None:
    """Test :meth:`AssertionManager._get_exc_message`."""
    ex = TypeError("object of type 'int' has no len()")
    func = len
    args = (1,)

    str1 = assertion._get_exc_message(ex, func, *args, invert=False, output=None)  # type: ignore
    str2 = assertion._get_exc_message(ex, func, *args, invert=True, output=None)  # type: ignore
    comma = ',' if version_info.minor < 7 else ''   # For Python 3.6 and later
    ref1 = f"""output = len(obj); assert output

exception: TypeError = TypeError("object of type 'int' has no len()"{comma})

output: NoneType = None
obj: int = 1"""
    ref2 = f"""output = not len(obj); assert output

exception: TypeError = TypeError("object of type 'int' has no len()"{comma})

output: NoneType = None
obj: int = 1"""

    assertion.eq(str1, ref1)
    assertion.eq(str2, ref2)
