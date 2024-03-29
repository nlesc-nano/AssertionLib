"""A module with various new assertion functions.

Index
-----
.. currentmodule:: assertionlib.assertion_functions
.. autosummary::
    len_eq
    str_eq
    shape_eq
    isdisjoint
    issuperset
    issubset
    function_eq

API
---
.. autofunction:: len_eq
.. autofunction:: str_eq
.. autofunction:: shape_eq
.. autofunction:: isdisjoint
.. autofunction:: issuperset
.. autofunction:: issubset
.. autofunction:: function_eq

"""

import warnings
import dis
from types import FunctionType
from itertools import zip_longest
from typing import (
    Any,
    Sized,
    Callable,
    TypeVar,
    Iterable,
    Union,
    Tuple,
    Hashable,
    TYPE_CHECKING
)

from .functions import to_positional

if TYPE_CHECKING:
    from numpy import ndarray
else:
    ndarray = 'numpy.ndarray'

__all__ = ['len_eq', 'str_eq', 'shape_eq', 'isdisjoint', 'issuperset', 'issubset', 'function_eq']

T = TypeVar('T')
IT = TypeVar('IT', bound=Union[None, dis.Instruction])


@to_positional
def len_eq(a: Sized, b: int) -> bool:
    """Check if the length of **a** is equivalent to **b**: :code:`len(a) == b`."""
    return len(a) == b


@to_positional
def str_eq(a: T, b: str, *, str_converter: Callable[[T], str] = repr) -> bool:
    """Check if the string-representation of **a** is equivalent to **b**: :code:`repr(a) == b`."""
    return str_converter(a) == b


@to_positional
def shape_eq(a: "ndarray[Any, Any]", b: Union["ndarray[Any, Any]", Tuple[int, ...]]) -> bool:
    """Check if the shapes of **a** and **b** are equivalent: :code:`a.shape == getattr(b, 'shape', b)`.

    **b** should be either an object with the ``shape`` attribute (*e.g.* a NumPy array)
    or a :class:`tuple` representing a valid array shape.

    """  # noqa: E501
    return a.shape == getattr(b, 'shape', b)


@to_positional
def isdisjoint(a: Iterable[Hashable], b: Iterable[Hashable]) -> bool:
    """Check if **a** has no elements in **b**."""
    try:
        return a.isdisjoint(b)  # type: ignore

    # **a** does not have the isdisjoint method
    except AttributeError:
        return set(a).isdisjoint(b)

    # **a.isdisjoint** is not a callable or
    # **a** and/or **b** do not consist of hashable elements
    except TypeError as ex:
        if callable(a.isdisjoint):  # type: ignore
            raise ex
        return set(a).isdisjoint(b)


@to_positional
def issuperset(a: Iterable[Hashable], b: Iterable[Hashable]) -> bool:
    """Check if **a** contains all elements from **b**."""
    try:
        return a.issuperset(b)  # type: ignore

    # **a** does not have the isdisjoint method
    except AttributeError:
        return set(a).issuperset(b)

    # **a.issuperset** is not a callable or
    # **a** and/or **b** do not consist of hashable elements
    except TypeError as ex:
        if callable(a.issuperset):  # type: ignore
            raise ex
        return set(a).issuperset(b)


@to_positional
def issubset(a: Iterable[Hashable], b: Iterable[Hashable]) -> bool:
    """Check if **b** contains all elements in **a**."""
    try:
        return a.issubset(b)  # type: ignore

    # **a** does not have the isdisjoint method
    except AttributeError:
        return set(a).issubset(b)

    # **a.issubset** is not a callable or
    # **a** and/or **b** do not consist of hashable elements
    except TypeError as ex:
        if callable(a.issubset):  # type: ignore
            raise ex
        return set(a).issubset(b)


@to_positional
def function_eq(func1: FunctionType, func2: FunctionType) -> bool:
    """Check if two functions are equivalent by checking if their :attr:`__code__` is identical.

    **func1** and **func2** should be instances of :data:`~types.FunctionType`
    or any other object with access to the :attr:`__code__` attribute.

    """
    warnings.warn(
        "`function_eq` is deprecated and will be removed in the future",
        DeprecationWarning, stacklevel=2,
    )

    code1 = None
    try:
        code1 = func1.__code__
        code2 = func2.__code__
    except AttributeError as ex:
        name, obj = ('func1', func1) if code1 is None else ('func2', func2)
        raise TypeError(f"{name!r} expected a function or object with the '__code__' attribute; "
                        f"observed type: {obj.__class__.__name__!r}") from ex

    iterator = zip_longest(dis.get_instructions(code1), dis.get_instructions(code2))
    tup_iter = ((_sanitize_instruction(i), _sanitize_instruction(j)) for i, j in iterator)
    return all([i == j for i, j in tup_iter])


def _sanitize_instruction(instruction: IT) -> IT:
    """Sanitize the supplied instruction by setting :attr:`~dis.Instruction.starts_line` to :data:`None`."""  # noqa
    if instruction is None:
        return None
    return instruction._replace(starts_line=None)  # type: ignore
