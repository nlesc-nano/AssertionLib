"""Tests for the :class:`AssertionManager<assertionlib.manager.AssertionManager>` class."""

import math

from assertionlib import assertion

inf = math.inf
nan = math.nan


def test_allclose() -> None:
    """Test :meth:`AssertionManager.allclose`."""
    assertion.allclose(1, 1)
    assertion.allclose(1, 1, rel_tol=10**-5)
    assertion.allclose(1.0, (1.0 - 10**-10))
    assertion.allclose(1, 0, invert=True)
    assertion.allclose(5, 6, 7, 8, exception=TypeError)
    assertion.allclose([], [], exception=TypeError)
    assertion.allclose(1, 1, rel_tol='bob', exception=TypeError)


def test_isclose() -> None:
    """Test :meth:`AssertionManager.isclose`."""
    cls = type(assertion)
    assertion.is_(cls.isclose, cls.allclose)


def test_isfinite() -> None:
    """Test :meth:`AssertionManager.isfinite`."""
    assertion.isfinite(0)
    assertion.isfinite(0.0)
    assertion.isfinite(98)
    assertion.isfinite(nan, invert=True)
    assertion.isfinite(inf, invert=True)
    assertion.isfinite(-inf, invert=True)
    assertion.isfinite(1, 1, 1, exception=TypeError)
    assertion.isfinite('bob', exception=TypeError)


def test_isinf() -> None:
    """Test :meth:`AssertionManager.isinf`."""
    assertion.isinf(inf)
    assertion.isinf(-inf)
    assertion.isinf(0.0, invert=True)
    assertion.isinf(98, invert=True)
    assertion.isinf(nan, invert=True)
    assertion.isinf(1, 1, 1, exception=TypeError)
    assertion.isinf('bob', exception=TypeError)


def test_isnan() -> None:
    """Test :meth:`AssertionManager.isnan`."""
    assertion.isnan(nan)
    assertion.isnan(0.0, invert=True)
    assertion.isnan(98, invert=True)
    assertion.isnan(inf, invert=True)
    assertion.isnan(-inf, invert=True)
    assertion.isnan(1, 1, 1, exception=TypeError)
    assertion.isnan('bob', exception=TypeError)
