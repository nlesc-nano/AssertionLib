"""Tests for :mod:`assertionlib.signature`."""

from assertionlib import assertion
from assertionlib.signature import (
    _get_backup_signature, BACK_SIGNATURE, generate_signature, _signature_to_str
)


def test_get_backup_signature() -> None:
    """Test :func:`assertionlib.signature._get_backup_signature`."""
    sgn_str = '<Signature (self, *args, invert: bool = False, exception: Union[Type[Exception], NoneType] = None, **kwargs) -> None>'  # noqa
    assertion.eq(sgn_str, repr(BACK_SIGNATURE))
    assertion.eq(sgn_str, repr(_get_backup_signature()))


def test_generate_signature() -> None:
    """Test :func:`assertionlib.signature.generate_signature`."""
    def test(a, *args, b=1, **kwargs):
        pass

    ref1 = '<Signature (self, a, *args, b=1, invert: bool = False, exception: Union[Type[Exception], NoneType] = None, **kwargs) -> None>'  # noqa
    sgn1 = generate_signature(test)
    assertion.eq(ref1, repr(sgn1))

    ref2 = '<Signature (self, *args, invert: bool = False, exception: Union[Type[Exception], NoneType] = None, **kwargs) -> None>'  # noqa
    sgn2 = generate_signature(bool)
    assertion.eq(ref2, repr(sgn2))


def test_signature_to_str() -> None:
    """Test :func:`assertionlib.signature._signature_to_str`."""
    def test(a, *args, b=1, **kwargs):
        pass

    ref1 = '(self, a, *args, b=b, invert=invert, exception=exception, **kwargs)'
    ref2 = '(self, *args, invert=invert, exception=exception, **kwargs)'
    sgn1 = generate_signature(test)
    sgn2 = generate_signature(bool)
    sgn1_str = _signature_to_str(sgn1)
    sgn2_str = _signature_to_str(sgn2)

    assertion.eq(sgn1_str, ref1)
    assertion.eq(sgn2_str, ref2)
