"""Tests for the :mod:`assertionlib.functions` module."""

from collections import OrderedDict

from assertionlib import assertion
from assertionlib.functions import get_sphinx_domain


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
