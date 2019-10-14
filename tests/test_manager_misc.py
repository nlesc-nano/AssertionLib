"""Tests for the :class:`AssertionManager<assertionlib.manager.AssertionManager>` class."""

from assertionlib import assertion, AssertionManager


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


def test_allclose() -> None:
    """Test :meth:`AssertionManager.allclose`."""
    assertion.allclose(1, 1)
    assertion.allclose(1, 1, rtol=10**-5)
    assertion.allclose(1.0, (1.0 - 10**-10))
    assertion.allclose(1, 0, invert=True)
    assertion.allclose(5, 6, 7, 8, exception=TypeError)
    assertion.allclose([], [], exception=TypeError)
    assertion.allclose(1, 1, rtol='bob', exception=TypeError)


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
    new = cls.from_dict(dct)
    assertion.eq(vars(assertion.repr_instance), vars(new.repr_instance))


def test_add_to_instance() -> None:
    """Test :meth:`AssertionManager.add_to_instance`."""
    def func(a, b): return True

    assertion_ = AssertionManager()
    assertion_.add_to_instance(func)
    assertion_.hasattr(assertion_, 'func')
    assertion_.func(1, 2)

    try:
        assertion_.add_to_instance(func)
    except AttributeError:
        pass
    else:
        raise AssertionError

    assertion_.add_to_instance(func, name='bob')
    assertion_.hasattr(assertion_, 'bob')
    assertion_.bob(1, 2)


def test_assert_() -> None:
    """Test :meth:`AssertionManager.assert_`."""
    assertion.assert_(len, [1])
    assertion.assert_(len, [], invert=True)
    assertion.assert_(len, 1, exception=TypeError)
    assertion.assert_(len, [1], [1], exception=TypeError)
    assertion.assert_(len, [1], bob=1, exception=TypeError)

    try:
        assertion.assert_(len, [1], exception=bool)
    except TypeError:
        pass
    else:
        raise AssertionError

    try:
        assertion.assert_(len, [1], exception=AssertionError)
    except ValueError:
        pass
    else:
        raise AssertionError


def test_repr() -> None:
    """Test :meth:`AssertionManager.__repr__`."""
    assertion.is_(AssertionManager.__repr__, AssertionManager.__str__)

    ref = 'AssertionManager(\n    repr_instance = <assertionlib.ndrepr.NDRepr object '
    output = repr(assertion).split('at')[0]

    assertion.eq(ref, output)
