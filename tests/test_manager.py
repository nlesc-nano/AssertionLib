"""Tests for the :class:`AssertionManager<assertionlib.manager.AssertionManager>` class."""

from typing import Optional

try:
    import numpy as np
    NUMPY_EX: Optional[ImportError] = None
except ImportError as ex:
    NUMPY_EX = ex

from assertionlib import assertion
from assertionlib.functions import skip_if


def test_abs() -> None:
    """Test :meth:`AssertionManager.abs`."""
    assertion.abs(5)
    assertion.abs(5)
    assertion.abs(0, invert=True)
    assertion.abs(5, 6, 7, 8, exception=TypeError)
    assertion.abs([], exception=TypeError)


def test_add() -> None:
    """Test :meth:`AssertionManager.add`."""
    assertion.add(5, 5)
    assertion.add(0, 0, invert=True)
    assertion.add(5, 6, 7, 8, exception=TypeError)
    assertion.add([], 5, exception=TypeError)


def test_and() -> None:
    """Test :meth:`AssertionManager.and_`."""
    assertion.and_(5, 5)
    assertion.and_(0, 5, invert=True)
    assertion.and_(0, 0, invert=True)
    assertion.and_(5, 6, 7, 8, exception=TypeError)


def test_concat() -> None:
    """Test :meth:`AssertionManager.concat`."""
    assertion.concat([1], [2])
    assertion.concat([], [], invert=True)
    assertion.concat([], {}, exception=TypeError)
    assertion.concat(5, 6, exception=TypeError)
    assertion.concat([], [], [], exception=TypeError)


def test_contains() -> None:
    """Test :meth:`AssertionManager.contains`."""
    assertion.contains([1], 1)
    assertion.contains({1}, 1)
    assertion.contains({1: None}, 1)
    assertion.contains([1], 2, invert=True)
    assertion.contains([1], 5, 6, 7, exception=TypeError)
    assertion.contains(5, 5, exception=TypeError)


def test_countof() -> None:
    """Test :meth:`AssertionManager.countOf`."""
    assertion.countOf([1, 1, 1], 1)
    assertion.countOf([1, 1, 1], 2, invert=True)
    assertion.countOf([1], 5, 6, 7, exception=TypeError)
    assertion.countOf(5, 5, exception=TypeError)


def test_eq() -> None:
    """Test :meth:`AssertionManager.eq`."""
    assertion.eq(5, 5)
    assertion.eq(5, 6, invert=True)
    assertion.eq(5, 6, 7, 8, exception=TypeError)


def test_floordiv() -> None:
    """Test :meth:`AssertionManager.floordiv`."""
    assertion.floordiv(5, 1)
    assertion.floordiv(5, 5)
    assertion.floordiv(0.5, 5, invert=True)
    assertion.floordiv(0, 5, invert=True)
    assertion.floordiv(5, 0, exception=ZeroDivisionError)
    assertion.floordiv(5, 6, 7, 8, exception=TypeError)
    assertion.floordiv([1], 5, exception=TypeError)


def test_ge() -> None:
    """Test :meth:`AssertionManager.ge`."""
    assertion.ge(6, 5)
    assertion.ge(5, 5)
    assertion.ge(5, 6, invert=True)
    assertion.ge(5, 6, 7, 8, exception=TypeError)
    assertion.ge([], 6, exception=TypeError)


def test_getitem() -> None:
    """Test :meth:`AssertionManager.getitem`."""
    assertion.getitem([1], 0)
    assertion.getitem([0], 0, invert=True)
    assertion.getitem(5, 6, 7, 8, exception=TypeError)
    assertion.getitem(5, 6, exception=TypeError)
    assertion.getitem([1], 5, exception=IndexError)
    assertion.getitem({1: None}, 5, exception=KeyError)


def test_gt() -> None:
    """Test :meth:`AssertionManager.gt`."""
    assertion.gt(6, 5)
    assertion.gt(5, 6, invert=True)
    assertion.gt(6, 6, invert=True)
    assertion.gt(5, 6, 7, 8, exception=TypeError)
    assertion.gt([], 6, exception=TypeError)


def test_index() -> None:
    """Test :meth:`AssertionManager.index`."""
    assertion.index(6)
    assertion.index(0, invert=True)
    assertion.index(5, 6, 7, 8, exception=TypeError)
    assertion.index(5.0, exception=TypeError)


def test_inv() -> None:
    """Test :meth:`AssertionManager.inv`."""
    assertion.inv(6)
    assertion.inv(-1, invert=True)
    assertion.inv(5, 6, 7, 8, exception=TypeError)
    assertion.inv(5.0, exception=TypeError)


def test_invert() -> None:
    """Test :meth:`AssertionManager.invert`."""
    assertion.invert(6)
    assertion.invert(-1, invert=True)
    assertion.invert(5, 6, 7, 8, exception=TypeError)
    assertion.invert(5.0, exception=TypeError)


def test_is() -> None:
    """Test :meth:`AssertionManager.is_`."""
    a = 5
    b = 6

    assertion.is_(a, a)
    assertion.is_(a, b, invert=True)
    assertion.is_(a, a, a, a, a, exception=TypeError)


def test_is_not() -> None:
    """Test :meth:`AssertionManager.is_not`."""
    a = 5
    b = 6

    assertion.is_not(a, b)
    assertion.is_not(a, a, invert=True)
    assertion.is_not(a, a, a, a, a, exception=TypeError)


def test_le() -> None:
    """Test :meth:`AssertionManager.le`."""
    assertion.le(5, 6)
    assertion.le(5, 5)
    assertion.le(6, 5, invert=True)
    assertion.le(5, 6, 7, 8, exception=TypeError)
    assertion.le([], 6, exception=TypeError)


def test_lshift() -> None:
    """Test :meth:`AssertionManager.lshift`."""
    assertion.lshift(5, 6)
    assertion.lshift(0, 5, invert=True)
    assertion.lshift(0, 0, invert=True)
    assertion.lshift(-5, 6)
    assertion.lshift(-5, -6, exception=ValueError)
    assertion.lshift(5, -6, exception=ValueError)
    assertion.lshift(5, 6, 7, 8, exception=TypeError)
    assertion.lshift([], 6, exception=TypeError)


def test_lt() -> None:
    """Test :meth:`AssertionManager.lt`."""
    assertion.lt(5, 6)
    assertion.lt(6, 5, invert=True)
    assertion.lt(6, 6, invert=True)
    assertion.lt(5, 6, 7, 8, exception=TypeError)
    assertion.lt([], 6, exception=TypeError)


@skip_if(NUMPY_EX)
def test_matmul() -> None:
    """Test :meth:`AssertionManager.matmul`."""
    assertion.matmul(np.ones(2), np.ones(2))
    assertion.matmul(np.zeros(2), np.zeros(2), invert=True)
    assertion.matmul(np.ones(2), np.ones(4), exception=ValueError)
    assertion.matmul(5, 6, 7, 8, exception=TypeError)
    assertion.matmul(2, 2, exception=TypeError)


def test_mod() -> None:
    """Test :meth:`AssertionManager.mod`."""
    assertion.mod(5, 6)
    assertion.mod(0, 6, invert=True)
    assertion.mod(5, 0, exception=ZeroDivisionError)
    assertion.mod(5, 6, 7, 8, exception=TypeError)
    assertion.mod([5], 6, exception=TypeError)


def test_mul() -> None:
    """Test :meth:`AssertionManager.mul`."""
    assertion.mul(5, 6)
    assertion.mul(0, 6, invert=True)
    assertion.mul(6, 0, invert=True)
    assertion.mul(5, 6, 7, 8, exception=TypeError)
    assertion.mul({1}, 6, exception=TypeError)


def test_ne() -> None:
    """Test :meth:`AssertionManager.ne`."""
    assertion.ne(5, 6)
    assertion.ne(5, 5, invert=True)
    assertion.ne(5, 6, 7, 8, exception=TypeError)


def test_neg() -> None:
    """Test :meth:`AssertionManager.neg`."""
    assertion.neg(5)
    assertion.neg(5.0)
    assertion.neg(0, invert=True)
    assertion.neg(5, 6, 7, 8, exception=TypeError)
    assertion.neg([1], exception=TypeError)


def test_not() -> None:
    """Test :meth:`AssertionManager.not_`."""
    assertion.not_(0)
    assertion.not_(5, invert=True)
    assertion.not_(5, 6, 7, 8, exception=TypeError)


@skip_if(NUMPY_EX)
def test_not_np() -> None:
    """Test :meth:`AssertionManager.not_` with a NumPy array."""
    assertion.not_(np.random.rand(10), exception=ValueError)


def test_or() -> None:
    """Test :meth:`AssertionManager.or_`."""
    assertion.or_(5, 6)
    assertion.or_(0, 6)
    assertion.or_(5, 0)
    assertion.or_(0, 0, invert=True)
    assertion.or_(5, 6, 7, 8, exception=TypeError)


def test_xor() -> None:
    """Test :meth:`AssertionManager.xor`."""
    assertion.xor(5, 6)
    assertion.xor(0, 6)
    assertion.xor(5, 0)
    assertion.xor(0, 0, invert=True)
    assertion.xor(5, 6, 7, 8, exception=TypeError)


@skip_if(NUMPY_EX)
def test_or_np() -> None:
    """Test :meth:`AssertionManager.not_` with a NumPy array."""
    assertion.or_(np.random.rand(10), 6, exception=TypeError)


def test_pos() -> None:
    """Test :meth:`AssertionManager.pos`."""
    assertion.pos(-5)
    assertion.pos(5)
    assertion.pos(0, invert=True)
    assertion.pos(5, 6, 7, 8, exception=TypeError)
    assertion.pos([1], exception=TypeError)


def test_pow() -> None:
    """Test :meth:`AssertionManager.pow`."""
    assertion.pow(5, 5)
    assertion.pow(5, 0)
    assertion.pow(0, 5, invert=True)
    assertion.pow(0, -5, exception=ZeroDivisionError)
    assertion.pow(5, 6, 7, 8, exception=TypeError)
    assertion.pow([1], 5, exception=TypeError)


def test_rshift() -> None:
    """Test :meth:`AssertionManager.rshift`."""
    assertion.rshift(5, 1)
    assertion.rshift(5, 0)
    assertion.rshift(0, 0, invert=True)
    assertion.rshift(0, 6, invert=True)
    assertion.rshift(-5, -6, exception=ValueError)
    assertion.rshift(5, -6, exception=ValueError)
    assertion.rshift(5, 6, 7, 8, exception=TypeError)
    assertion.rshift([], 6, exception=TypeError)


def test_sub() -> None:
    """Test :meth:`AssertionManager.sub`."""
    assertion.sub(5, 6)
    assertion.sub(5, 0)
    assertion.sub(5, 5, invert=True)
    assertion.sub(5, 6, 7, 8, exception=TypeError)
    assertion.sub([], 6, exception=TypeError)


def test_truediv() -> None:
    """Test :meth:`AssertionManager.truediv`."""
    assertion.truediv(5, 1)
    assertion.truediv(5, 5)
    assertion.truediv(0.5, 5)
    assertion.truediv(0, 5, invert=True)
    assertion.truediv(5, 0, exception=ZeroDivisionError)
    assertion.truediv(5, 6, 7, 8, exception=TypeError)
    assertion.truediv([5], 5, exception=TypeError)


def test_truth() -> None:
    """Test :meth:`AssertionManager.truth`."""
    assertion.truth(5)
    assertion.truth(0, invert=True)
    assertion.truth(5, 6, 7, 8, exception=TypeError)


@skip_if(NUMPY_EX)
def test_truth_np() -> None:
    """Test :meth:`AssertionManager.truth` with a NumPy array."""
    assertion.truth(np.random.rand(10), exception=ValueError)
