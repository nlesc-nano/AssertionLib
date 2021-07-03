"""A stub-only module containing a number of :class:`~typing.Protocol` subclasses."""

import sys
import types
from abc import abstractmethod
from typing import (
    Tuple,
    TypeVar,
    Any,
    type_check_only
)

if sys.version_info >= (3, 8):
    from typing import Protocol, SupportsIndex
else:
    from typing_extensions import Protocol, SupportsIndex

T_contra = TypeVar('T_contra', contravariant=True)
T_co = TypeVar('T_co', covariant=True)

_SupportsIndex = SupportsIndex

@type_check_only
class _SupportsShape(Protocol):
    @property
    def shape(self) -> Tuple[int, ...]: ...

@type_check_only
class _SupportsCode(Protocol):
    @property
    def __code__(self) -> types.CodeType: ...

@type_check_only
class _SupportsLengthHint(Protocol):
    def __length_hint__(self) -> int: ...

@type_check_only
class _SupportsNeg(Protocol[T_co]):
    def __neg__(self) -> T_co: ...

@type_check_only
class _SupportsPos(Protocol[T_co]):
    def __pos__(self) -> T_co: ...

@type_check_only
class _SupportsInvert(Protocol[T_co]):
    def __invert__(self) -> T_co: ...

@type_check_only
class _SupportsGetitem(Protocol[T_contra, T_co]):
    def __getitem__(self, __X: T_contra) -> T_co: ...

@type_check_only
class _SupportsAdd(Protocol[T_contra, T_co]):
    def __add__(self, __X: T_contra) -> T_co: ...

@type_check_only
class _SupportsSub(Protocol[T_contra, T_co]):
    def __sub__(self, __X: T_contra) -> T_co: ...

@type_check_only
class _SupportsMul(Protocol[T_contra, T_co]):
    def __mul__(self, __X: T_contra) -> T_co: ...

@type_check_only
class _SupportsFloordiv(Protocol[T_contra, T_co]):
    def __floordiv__(self, __X: T_contra) -> T_co: ...

@type_check_only
class _SupportsTruediv(Protocol[T_contra, T_co]):
    def __truediv__(self, __X: T_contra) -> T_co: ...

@type_check_only
class _SupportsPow(Protocol[T_contra, T_co]):
    def __pow__(self, __X: T_contra) -> T_co: ...

@type_check_only
class _SupportsMatmul(Protocol[T_contra, T_co]):
    def __matmul__(self, __X: T_contra) -> T_co: ...

@type_check_only
class _SupportsMod(Protocol[T_contra, T_co]):
    def __mod__(self, __X: T_contra) -> T_co: ...

@type_check_only
class _SupportsGt(Protocol[T_contra, T_co]):
    def __gt__(self, __X: T_contra) -> T_co: ...

@type_check_only
class _SupportsLt(Protocol[T_contra, T_co]):
    def __lt__(self, __X: T_contra) -> T_co: ...

@type_check_only
class _SupportsGe(Protocol[T_contra, T_co]):
    def __ge__(self, __X: T_contra) -> T_co: ...

@type_check_only
class _SupportsLe(Protocol[T_contra, T_co]):
    def __le__(self, __X: T_contra) -> T_co: ...

@type_check_only
class _SupportsLshift(Protocol[T_contra, T_co]):
    def __lshift__(self, __X: T_contra) -> T_co: ...

@type_check_only
class _SupportsRshift(Protocol[T_contra, T_co]):
    def __rshift__(self, __X: T_contra) -> T_co: ...

@type_check_only
class _SupportsXor(Protocol[T_contra, T_co]):
    def __xor__(self, __X: T_contra) -> T_co: ...

@type_check_only
class _SupportsOr(Protocol[T_contra, T_co]):
    def __or__(self, __X: T_contra) -> T_co: ...

@type_check_only
class _SupportsAnd(Protocol[T_contra, T_co]):
    def __and__(self, __X: T_contra) -> T_co: ...

@type_check_only
class _SupportsEq(Protocol[T_contra, T_co]):
    def __eq__(self, __X: T_contra) -> T_co: ...  # type: ignore

@type_check_only
class _SupportsNe(Protocol[T_contra, T_co]):
    def __ne__(self, __X: T_contra) -> T_co: ...  # type: ignore
