"""Tests for :mod:`assertionlib.signature`."""

from sys import version_info

from assertionlib import assertion
from assertionlib.signature import (
    _get_backup_signature, BACK_SIGNATURE, generate_signature, _signature_to_str
)


def test_get_backup_signature() -> None:
    """Test :func:`assertionlib.signature._get_backup_signature`."""
    if version_info >= (3, 7):  # Python >= 3.7
        sgn_str = '<Signature (self, *args, invert: bool = False, exception: Union[Type[Exception], NoneType] = None, post_process: Union[Callable[[Any], Any], NoneType] = None, message: Union[str, NoneType] = None, **kwargs) -> None>'  # noqa: E501
    else:  # Python < 3.7
        sgn_str = '<Signature (self, *args, invert:bool=False, exception:Union[Type[Exception], NoneType]=None, post_process:Union[Callable[[Any], Any], NoneType]=None, message:Union[str, NoneType]=None, **kwargs) -> None>'  # noqa: E501

    assertion.str_eq(BACK_SIGNATURE, sgn_str)
    assertion.str_eq(_get_backup_signature(), sgn_str)


def _test_func(a, *args, b=1, **kwargs): pass


def test_generate_signature() -> None:
    """Test :func:`assertionlib.signature.generate_signature`."""
    if version_info.minor >= 7:  # Python >= 3.7
        ref1 = '<Signature (self, a, *args, b=1, invert: bool = False, exception: Union[Type[Exception], NoneType] = None, post_process: Union[Callable[[Any], Any], NoneType] = None, message: Union[str, NoneType] = None, **kwargs) -> None>'  # noqa: E501
        ref2 = '<Signature (self, *args, invert: bool = False, exception: Union[Type[Exception], NoneType] = None, post_process: Union[Callable[[Any], Any], NoneType] = None, message: Union[str, NoneType] = None, **kwargs) -> None>'  # noqa: E501
    else:  # Python < 3.6
        ref1 = '<Signature (self, a, *args, b=1, invert:bool=False, exception:Union[Type[Exception], NoneType]=None, post_process:Union[Callable[[Any], Any], NoneType]=None, message:Union[str, NoneType]=None, **kwargs) -> None>'  # noqa: E501
        ref2 = '<Signature (self, *args, invert:bool=False, exception:Union[Type[Exception], NoneType]=None, post_process:Union[Callable[[Any], Any], NoneType]=None, message:Union[str, NoneType]=None, **kwargs) -> None>'  # noqa: E501

    sgn1 = generate_signature(_test_func)
    sgn2 = generate_signature(bool)
    assertion.str_eq(sgn1, ref1)
    assertion.str_eq(sgn2, ref2)


def test_signature_to_str() -> None:
    """Test :func:`assertionlib.signature._signature_to_str`."""
    def test(a, *args, b=1, **kwargs):
        pass

    ref1 = '(self, a, *args, b=b, invert=invert, exception=exception, post_process=post_process, message=message, **kwargs)'  # noqa: E501
    ref2 = '(self, *args, invert=invert, exception=exception, post_process=post_process, message=message, **kwargs)'  # noqa: E501

    sgn1 = generate_signature(test)
    sgn2 = generate_signature(bool)
    sgn1_str = _signature_to_str(sgn1)
    sgn2_str = _signature_to_str(sgn2)

    assertion.eq(sgn1_str, ref1)
    assertion.eq(sgn2_str, ref2)
